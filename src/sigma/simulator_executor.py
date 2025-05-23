"""SimulatorExecutor 모듈.

백테스트와 시뮬레이션 환경에서 가상 체결을 수행한다. 자세한 사양은
``docs/4_development/module_specs`` 참고.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, Dict


class DummyRedis:
    async def publish(self, channel: str, message: str) -> None:  # pragma: no cover
        pass


class SimulatorExecutor:
    def __init__(self, redis=None, logger=None) -> None:
        self.redis = redis or DummyRedis()
        self.logger = logger or logging.getLogger(__name__)

    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """주문을 가상으로 즉시 체결한다."""
        fill = {
            "order_id": f"sim-{uuid.uuid4()}",
            "filled_size": order.get("size"),
            "price": order.get("price"),
            "ts": time.time(),
        }
        await self.redis.publish("order.fill", json.dumps(fill))
        self.logger.debug("시뮬레이터 체결: %s", fill)
        return fill

    async def publish_fill(self, fill: Dict[str, Any]) -> None:
        await self.redis.publish("order.fill", json.dumps(fill))
