"""거래 성과 리포트 생성 모듈.

``docs/4_development/module_specs/core/PerformanceReporter_Spec.md``의 사양을
구현한다.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, Iterable, List


class PerformanceReporter:
    """성과 데이터를 모아 간단한 텍스트 보고서를 작성한다."""

    def __init__(self, report_dir: str = "reports", logger=None) -> None:
        self.report_dir = report_dir
        self.logger = logger or logging.getLogger(__name__)
        os.makedirs(self.report_dir, exist_ok=True)

    def generate_report(self, trades: Iterable[Dict[str, float]]) -> str:
        total_pnl = sum(t.get("pnl", 0.0) for t in trades)
        count = sum(1 for _ in trades)
        content = f"총 거래 건수: {count}\n총 손익: {total_pnl:.2f}\n"
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.report_dir, f"report_{ts}.txt")
        with open(path, "w") as fp:
            fp.write(content)
        self.logger.info("리포트 저장: %s", path)
        return path

    def run_weekly(self, trades: List[Dict[str, float]]) -> str:
        return self.generate_report(trades)

    def run_monthly(self, trades: List[Dict[str, float]]) -> str:
        return self.generate_report(trades)

