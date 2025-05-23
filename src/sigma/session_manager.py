"""세션 상태 관리 모듈.

사양은 ``docs/4_development/module_specs/common/SessionManager_Spec.md`` 를 참조한다.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional


class SessionManager:
    def __init__(self, state_path: str = "session_state.json", logger=None) -> None:
        self.state_path = state_path
        self.logger = logger or logging.getLogger(__name__)
        self.balance: float = 0.0
        self.positions: Dict[str, float] = {}

    async def load_state(self) -> None:
        try:
            with open(self.state_path) as fp:
                data = json.load(fp)
            self.balance = float(data.get("balance", 0))
            self.positions = {k: float(v) for k, v in data.get("positions", {}).items()}
            self.logger.debug("세션 상태 로드: %s", data)
        except FileNotFoundError:
            self.logger.info("이전 세션 파일 없음")

    async def save_state(self) -> None:
        data = {"balance": self.balance, "positions": self.positions}
        with open(self.state_path, "w") as fp:
            json.dump(data, fp)
        self.logger.debug("세션 상태 저장: %s", data)

    def get_balance(self) -> float:
        return self.balance

    def update_position(self, symbol: str, size: float) -> None:
        self.positions[symbol] = self.positions.get(symbol, 0.0) + size

    async def handle_event(self, event: Dict[str, Any]) -> None:
        etype = event.get("type")
        data = event.get("data", {})
        if etype == "fill":
            symbol = data.get("symbol")
            size = float(data.get("size", 0))
            self.update_position(symbol, size)
        await self.save_state()

