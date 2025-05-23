"""비동기 이벤트 루프 관리 모듈.

``EventLoop`` 은 여러 코루틴 태스크를 등록하여 순차적으로 실행하고, 완료되면
자동으로 정리한다. 사양은
``docs/4_development/module_specs/common/EventLoop_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
from sigma.common.logging_service import get_logger
from typing import Any, Coroutine, Iterable, Set
import logging


class EventLoop:
    """asyncio 기반 간단한 태스크 스케줄러."""

    def __init__(self, max_tasks: int = 100, logger: logging.Logger | None = None) -> None:
        self.max_tasks = max_tasks
        self.logger = logger or get_logger(__name__)
        self._tasks: Set[asyncio.Task[Any]] = set()
        self._running = False

    def spawn(self, coro: Coroutine[Any, Any, Any]) -> asyncio.Task[Any]:
        """코루틴을 태스크로 등록한다."""
        if len(self._tasks) >= self.max_tasks:
            raise RuntimeError("too many tasks")
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def start(self) -> None:
        """등록된 태스크가 모두 끝날 때까지 실행한다."""
        self._running = True
        while self._running and self._tasks:
            done, _ = await asyncio.wait(self._tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if exc := task.exception():
                    self.logger.exception("태스크 예외: %s", exc)

    async def stop(self) -> None:
        """모든 태스크를 취소하고 종료한다."""
        self._running = False
        for task in list(self._tasks):
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def run(self, mode: str, config: dict) -> None:
        """설정에 등록된 태스크를 실행한다. (시세 수신→전략 호출→주문 실행 체인 구체화)"""
        # 기존 tasks 등록 방식도 지원
        tasks = config.get("tasks", [])
        for coro in tasks:
            self.spawn(coro)

        # 시세 수신→전략 호출→주문 실행 체인
        market_ws = config.get("market_ws")
        trading_bot = config.get("trading_bot")
        if market_ws and trading_bot:

            async def tick_chain():
                await market_ws.connect()
                await market_ws.subscribe()
                assert market_ws.ws
                async for msg in market_ws.ws:
                    try:
                        import json

                        tick = market_ws._standardize(json.loads(msg))
                        await trading_bot.process_tick(tick)
                    except Exception as exc:
                        self.logger.exception("틱 체인 처리 오류: %s", exc)

            self.spawn(tick_chain())

        self.logger.info("EventLoop 시작: %s", mode)
        try:
            await self.start()
        finally:
            await self.stop()


def create_tasks(loop: EventLoop, coros: Iterable[Coroutine[Any, Any, Any]]) -> None:
    """여러 코루틴을 일괄 등록한다."""

    for coro in coros:
        loop.spawn(coro)
