"""이벤트 루프."""

import asyncio

from src.sigma.utils.logger import logger


async def start_event_loop(bot, price_queue, order_queue) -> None:
    """비동기 이벤트 루프를 시작합니다."""

    async def run_bot() -> None:
        while True:  # pragma: no cover - 무한 루프
            data = await price_queue.get()
            for signal in bot.strategy.generate_signals(data):
                await order_queue.put(signal)

    logger.info("이벤트 루프 시작")
    await asyncio.gather(run_bot())
