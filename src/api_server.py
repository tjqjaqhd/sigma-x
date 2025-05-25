from __future__ import annotations

import asyncio
import os
import logging
from typing import Optional, Dict

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
)
from fastapi.security import OAuth2PasswordBearer


class LoginInput(BaseModel):
    username: str
    password: str


class UpdateStrategyInput(BaseModel):
    """전략 업데이트 요청 모델."""

    name: str


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
        channel: str = "ticks",
        order_key: str = "orders",
        users: Optional[Dict[str, Dict[str, str]]] = None,
        secret_key: str = "secret",
        algorithm: str = "HS256",
        alert_channel: str = "alerts",
        token_expire_seconds: int = 900,
        strategy_manager=None,
    ) -> None:
        self.app = FastAPI()
        self.redis = redis_client
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
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
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

        @self.app.get("/orders")
        async def orders() -> dict[str, list[str]]:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            data = await self.redis.lrange(self.order_key, 0, -1)
            decoded = [d.decode() if isinstance(d, bytes) else d for d in data]
            return {"orders": decoded}

        from fastapi import Body

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
        async def update_strategy(data: UpdateStrategyInput = Body(...)) -> dict[str, str]:
            from .strategy_manager import StrategyLoadError

            try:
                self.strategy_manager.change_strategy(data.name)
            except StrategyLoadError as exc:
                logging.exception("Invalid strategy %s: %s", data.name, exc)
                raise HTTPException(status_code=400, detail=f"invalid strategy: {data.name}")
            except Exception as exc:
                logging.exception("Unexpected error changing strategy: %s", exc)
                raise HTTPException(status_code=400, detail="strategy update failed")
            return {"status": "updated", "name": data.name}

        @self.app.get("/system/tasks", dependencies=[Depends(require_admin)])
        async def system_tasks() -> dict[str, list[str]]:
            return {"tasks": []}

        @self.app.get("/backtests", dependencies=[Depends(require_admin)])
        async def backtests() -> dict[str, list[str]]:
            return {"results": []}

        @self.app.post("/notify", dependencies=[Depends(require_admin)])
        async def notify(message: str) -> dict[str, str]:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            await self.redis.publish(self.alert_channel, message)
            return {"sent": message}

    def _setup_events(self) -> None:
        @self.app.on_event("startup")
        async def startup() -> None:
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url(os.getenv("SIGMA_REDIS_URL", "redis://localhost"))

        @self.app.on_event("shutdown")
        async def shutdown() -> None:
            if self.redis is not None:
                await self.redis.close()
                self.redis = None

    def run(self, *args, **kwargs) -> None:
        import uvicorn

        uvicorn.run(self.app, *args, **kwargs)
