import asyncio

from sigma.core.execution import OrderWorker, OrderEvent


def test_order_worker(tmp_path):
    async def _run():
        queue = asyncio.Queue()
        worker = OrderWorker(queue)
        worker.start()
        await queue.put(OrderEvent(signal="BUY"))
        await asyncio.sleep(0.1)
        worker.stop()

    asyncio.run(_run())
