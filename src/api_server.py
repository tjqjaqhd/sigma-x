from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class APIServer:
    """FastAPI 기반 REST/WS 서버."""

    def __init__(
        self, *, redis_client=None, channel: str = "ticks", order_key: str = "orders"
    ) -> None:
        self.app = FastAPI()
        self.redis = redis_client
        self.channel = channel
        self.order_key = order_key
        self._setup_routes()

    def _setup_routes(self) -> None:
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

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            if self.redis is None:
                import redis.asyncio as redis

                self.redis = redis.from_url("redis://localhost")
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(self.channel)

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
                await pubsub.close()
                await websocket.close()

    def run(self, *args, **kwargs) -> None:
        import uvicorn

        uvicorn.run(self.app, *args, **kwargs)
