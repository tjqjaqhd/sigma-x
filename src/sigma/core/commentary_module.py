"""전략 결과 요약 코멘터리 생성 모듈."""

from __future__ import annotations

import logging
from typing import Dict


class CommentaryModule:
    """리포트용 텍스트 코멘터리를 생성한다."""

    def __init__(self, repository=None, logger=None) -> None:
        self.repository = repository
        self.logger = logger or logging.getLogger(__name__)

    def generate(self, summary: Dict[str, float]) -> str:
        trades = summary.get("trades", 0)
        pnl = summary.get("pnl", 0.0)
        text = f"이번 기간 거래 {trades}건, 수익 {pnl:.2f}"
        if self.repository and hasattr(self.repository, "save_commentary"):
            self.repository.save_commentary(text)
        self.logger.debug("코멘터리 생성: %s", text)
        return text
