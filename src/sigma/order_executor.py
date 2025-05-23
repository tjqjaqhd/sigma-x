"""OrderExecutor 모듈.

실계좌 주문 전송을 담당한다. 여기서는 모의 주문을 즉시 체결하여 Redis 채널에
퍼블리시하는 간단한 형태로 구현한다.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, Dict


class DummyRedis:
    async def publish(self, channel: str, message: str) -> None:  # pragma: no cover - 외부 의존성 대체
        pass


class OrderExecutor:
    def __init__(self, redis=None, logger=None) -> None:
        self.redis = redis or DummyRedis()
        self.logger = logger or logging.getLogger(__name__)

    async def execute(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """주문을 전송하고 즉시 체결 이벤트를 반환한다."""
        fill = {
            "order_id": str(uuid.uuid4()),
            "filled_size": order.get("size"),
            "price": order.get("price"),
            "ts": time.time(),
        }
        await self.redis.publish("order.fill", json.dumps(fill))
        self.logger.debug("주문 체결: %s", fill)
        return fill

    async def listen_fills(self) -> None:
        """체결 데이터 수신용 더미 메서드."""
        pass
