from __future__ import annotations

import asyncio
import os
import logging
from typing import Optional, Dict, Any

import base64
import hashlib
import hmac
import json
import time
from pydantic import BaseModel
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    HTTPException,
    status,
    Body,
)
from fastapi.security import OAuth2PasswordBearer
import aio_pika


class LoginInput(BaseModel):
    username: str
    password: str


class UpdateStrategyInput(BaseModel):
    """전략 업데이트 요청 모델."""

    name: str


class BacktestRequest(BaseModel):
    type: str
    params: Dict[str, Any]


class APIServer:
    """FastAPI 기반 REST/WS 서버.

    `token_expire_seconds` 값은 발급된 액세스 토큰의 유효 기간을 초 단위로
    정의합니다. 값이 작을수록 토큰이 빨리 만료되며, 0 이하로 설정하면 토큰이
    즉시 만료됩니다.
    """

    def __init__(
        self,
        *,
        redis_client=None,
        rabbitmq_url: str = "amqp://guest:guest@localhost/",
        channel: str = "ticks",
        order_key: str = "orders",
        users: Optional[Dict[str, Dict[str, str]]] = None,
        secret_key: str = "secret",
        algorithm: str = "HS256",
        alert_channel: str = "alerts",
        token_expire_seconds: int = 900,
        strategy_manager=None,
        db_session=None,
        scheduler=None,
        system_status=None,
    ) -> None:
        self.app = FastAPI()
        self.redis = redis_client
        self.rabbitmq_url = rabbitmq_url
        self.channel = channel
        self.order_key = order_key
        self.alert_channel = alert_channel
        self.users = users or {
            "admin": {"password": "admin", "role": "admin"},
            "trader": {"password": "trader", "role": "trader"},
        }
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_seconds = token_expire_seconds
        from .strategy_manager import StrategyManager

        self.strategy_manager = strategy_manager or StrategyManager()
        self.db = db_session
        self.scheduler = scheduler
        self.system_status = system_status
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self._setup_routes()
        self._setup_events()

    def _create_access_token(self, data: dict) -> str:
        data = data.copy()
        data["exp"] = int(time.time()) + self.token_expire_seconds
        payload = json.dumps(data, separators=(",", ":"), sort_keys=True).encode()
        payload_b64 = base64.urlsafe_b64encode(payload).decode().rstrip("=")
        signature = hmac.new(self.secret_key.encode(), payload_b64.encode(), hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        return f"{payload_b64}.{sig_b64}"

    async def _get_rabbitmq_channel(self):
        if not self.rabbitmq_connection:
            self.rabbitmq_connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.rabbitmq_channel = await self.rabbitmq_connection.channel()
        return self.rabbitmq_channel

    def _setup_routes(self) -> None:
        oauth2_scheme = self.oauth2_scheme

        async def get_current_user(token: str = Depends(oauth2_scheme)):
            try:
                payload_b64, sig_b64 = token.split(".")
                expected_sig = hmac.new(self.secret_key.encode(), payload_b64.encode(), hashlib.sha256).digest()
                if not hmac.compare_digest(
                    base64.urlsafe_b64encode(expected_sig).decode().rstrip("="),
                    sig_b64,
                ):
                    raise ValueError
                payload_json = base64.urlsafe_b64decode(payload_b64 + "=").decode()
                data = json.loads(payload_json)
                exp = data.get("exp")
                if exp is None or time.time() > exp:
                    raise ValueError
                username = data.get("sub")
                role = data.get("role")
                if username is None or role is None:
                    raise ValueError
                return {"username": username, "role": role}
            except Exception:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        def require_admin(user: dict = Depends(get_current_user)):
            if user["role"] != "admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            return user

        @self.app.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok"}

        @self.app.get("/metrics")
        async def metrics() -> str:
            from .metrics import metrics_text

            return metrics_text()

        @self.app.get("/orders")
        async def orders() -> dict[str, list[str]]:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            data = await self.redis.lrange(self.order_key, 0, -1)
            decoded = [d.decode() if isinstance(d, bytes) else d for d in data]
            return {"orders": decoded}

        @self.app.get("/pnl", dependencies=[Depends(require_admin)])
        async def pnl() -> dict[str, float]:
            from sqlalchemy import func
            from .database import BacktestResult

            with self.session_scope() as session:
                profit = session.query(func.sum(BacktestResult.profit)).scalar() or 0.0
                return {"pnl": float(profit)}

        from fastapi import Body
        from contextlib import contextmanager
        from .database import SessionLocal, init_db

        @contextmanager
        def session_scope(self):
            """Provide a transactional scope around a series of operations."""
            if self.db is None:
                init_db()
                session = SessionLocal()
                close = True
            else:
                session = self.db
                close = False
            try:
                yield session
            finally:
                if close:
                    session.close()

        self.session_scope = session_scope.__get__(self, APIServer)

        @self.app.post("/token")
        async def login(data: LoginInput = Body(...)) -> dict[str, str]:
            user = self.users.get(data.username)
            if not user or user["password"] != data.password:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            token = self._create_access_token({"sub": data.username, "role": user["role"]})
            return {"access_token": token, "token_type": "bearer"}

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(self.channel)
            await pubsub.subscribe(self.alert_channel)

            async def sender() -> None:
                async for message in pubsub.listen():
                    if message.get("type") == "message":
                        data = message["data"]
                        if isinstance(data, bytes):
                            data = data.decode()
                        await websocket.send_text(str(data))

            sender_task = asyncio.create_task(sender())
            try:
                while True:
                    try:
                        text = await websocket.receive_text()
                    except WebSocketDisconnect:
                        break
                    await self.redis.publish(self.channel, text)
            finally:
                sender_task.cancel()
                try:
                    await sender_task
                except asyncio.CancelledError:
                    pass
                await pubsub.unsubscribe(self.channel)
                await pubsub.unsubscribe(self.alert_channel)
                await pubsub.close()
                await websocket.close()

        @self.app.get("/strategies", dependencies=[Depends(require_admin)])
        async def strategies() -> dict[str, list[str]]:
            return {"strategies": self.strategy_manager.available()}

        @self.app.post("/strategies", dependencies=[Depends(require_admin)])
        async def update_strategy(
            data: UpdateStrategyInput = Body(...),
        ) -> dict[str, str]:
            from .strategy_manager import StrategyLoadError

            try:
                self.strategy_manager.change_strategy(data.name)
            except StrategyLoadError as exc:
                logging.exception("Invalid strategy %s: %s", data.name, exc)
                raise HTTPException(status_code=400, detail=f"invalid strategy: {data.name}")
            except Exception as exc:
                logging.exception("Unexpected error changing strategy: %s", exc)
                raise HTTPException(status_code=400, detail="strategy update failed")
            current = self.strategy_manager.current().__class__.__name__
            return {"status": "updated", "name": current}

        @self.app.get("/system/tasks", dependencies=[Depends(require_admin)])
        async def system_tasks() -> dict[str, list[str]]:
            tasks: list[str] = []
            if self.scheduler is not None:
                tasks.extend([j.id for j in self.scheduler.get_jobs()])
            return {"tasks": tasks}

        @self.app.get("/backtests", dependencies=[Depends(require_admin)])
        async def backtests(limit: int = 10, offset: int = 0) -> dict[str, list[dict]]:
            from .database import BacktestResult, SessionLocal, init_db

            if self.db is None:
                init_db()
                session = SessionLocal()
                close = True
            else:
                session = self.db
                close = False
            try:
                q = session.query(BacktestResult).order_by(BacktestResult.id.desc()).offset(offset).limit(limit)
                results = [
                    {
                        "id": r.id,
                        "profit": r.profit,
                        "created_at": r.created_at.isoformat(),
                    }
                    for r in q
                ]
                return {"results": results}
            finally:
                if close:
                    session.close()

        @self.app.post("/notify", dependencies=[Depends(require_admin)])
        async def notify(message: str) -> dict[str, str]:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            await self.redis.publish(self.alert_channel, message)
            return {"sent": message}

        @self.app.post("/api/backtest")
        async def create_backtest(request: BacktestRequest) -> Dict[str, str]:
            """백테스트 작업을 생성하고 RabbitMQ에 발행합니다."""
            try:
                channel = await self._get_rabbitmq_channel()
                queue = await channel.declare_queue("backtest", durable=True)
                
                message = aio_pika.Message(
                    body=request.json().encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                )
                
                await channel.default_exchange.publish(
                    message,
                    routing_key="backtest"
                )
                
                return {"status": "accepted", "message": "Backtest task queued successfully"}
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to queue backtest task: {str(e)}"
                )

        @self.app.get("/api/backtests/{report_id}")
        async def get_backtest_result(report_id: str) -> Dict[str, Any]:
            """백테스트 결과를 조회합니다."""
            try:
                from .report_repository import ReportRepository
                repo = ReportRepository()
                result = repo.get_report(report_id)
                if not result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Report not found"
                    )
                return result
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to retrieve backtest result: {str(e)}"
                )

    def _setup_events(self) -> None:
        @self.app.on_event("startup")
        async def startup() -> None:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url(os.getenv("SIGMA_REDIS_URL", "redis://localhost"))
            if getattr(self, "system_status", None) is not None:
                await self.system_status.report("api_server", "running")

        @self.app.on_event("shutdown")
        async def shutdown() -> None:
            if getattr(self, "system_status", None) is not None:
                await self.system_status.report("api_server", "stopped")
            if self.redis is not None:
                await self.redis.close()
                self.redis = None

    def run(self, *args, **kwargs) -> None:
        import uvicorn

        uvicorn.run(self.app, *args, **kwargs)
