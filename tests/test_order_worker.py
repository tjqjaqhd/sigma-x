import asyncio
from sigma.core.execution import OrderWorker, OrderEvent

import pytest

@pytest.mark.asyncio
async def test_order_worker():
    worker = OrderWorker()
    # 실제 RabbitMQ 연결이 필요하므로, 여기서는 start/stop만 호출(실제 큐 연결은 목업 필요)
    # 아래는 구조적 smoke test 수준
    await worker.start()
    await worker.stop()
