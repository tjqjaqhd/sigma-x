"""StrategyManager 모듈.

플러그인 방식의 전략을 로딩하고 실행한다. 자세한 사양은
``docs/4_development/module_specs`` 참조.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict, Iterable, Optional


StrategyFunc = Callable[[Dict[str, Any]], Awaitable[Optional[Dict[str, Any]]]]


from .plugin_loader import PluginLoader


class StrategyManager:
    """전략 플러그인 로딩 및 실행 담당."""

    def __init__(self, plugin_paths: Iterable[str] | None = None, logger=None) -> None:
        self.strategies: Dict[str, StrategyFunc] = {}
        self.logger = logger or logging.getLogger(__name__)
        self.plugin_paths = list(plugin_paths or [])
        self.loader = PluginLoader(logger=self.logger)

    def register_strategy(self, name: str, func: StrategyFunc) -> None:
        self.logger.debug("전략 등록: %s", name)
        self.strategies[name] = func

    async def initialize(self) -> None:
        """플러그인 경로에서 전략을 로딩한다."""
        for path in self.plugin_paths:
            strat = self.loader.load_strategy(path)
            if callable(strat):
                self.register_strategy(path, strat)
            else:
                self.logger.warning("전략 로드 실패: %s", path)

    async def execute(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """등록된 전략을 순차 실행해 첫 주문 초안을 반환한다."""
        for name, func in self.strategies.items():
            try:
                order = await func(tick)
                if order:
                    self.logger.debug("%s 전략 주문 생성: %s", name, order)
                    return order
            except Exception as exc:  # pragma: no cover - 전략 오류는 로깅
                self.logger.exception("전략 %s 실행 오류: %s", name, exc)
        return None

    async def shutdown(self) -> None:
        """정리 작업 수행."""
        self.strategies.clear()
