"""FastAPI WebSocket 엔드포인트."""

from __future__ import annotations

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .redis_pubsub import RedisPubSub


class WebSocketEndpoint:
    """Redis 메시지를 브라우저로 전달한다."""

    def __init__(self, redis: RedisPubSub, logger=None) -> None:
        self.redis = redis
        self.logger = logger or logging.getLogger(__name__)
        self.router = APIRouter()
        self.router.websocket("/ws")(self._handle_ws)

    async def _handle_ws(self, websocket: WebSocket) -> None:
        await websocket.accept()
        await self.redis.connect()
        try:
            async for msg in self.redis.subscribe("price_update"):
                await websocket.send_json(msg)
        except WebSocketDisconnect:
            self.logger.info("웹소켓 연결 종료")
        finally:
            await websocket.close()
