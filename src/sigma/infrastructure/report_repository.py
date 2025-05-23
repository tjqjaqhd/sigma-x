"""리포트 저장소 모듈.

`docs/4_development/module_specs/infrastructure/ReportRepository_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

import pandas as pd


class ReportRepository:
    def __init__(self, db, logger=None) -> None:
        self.db = db
        self.logger = logger or logging.getLogger(__name__)

    async def save_report(self, report: Dict[str, Any]) -> None:
        # 실제 DB 저장 로직 필요
        self.logger.info(
            "리포트 저장: %s, PnL: %s",
            report.get("strategy_id"),
            report.get("pnl"),
        )

    def _path(self, name: str) -> str:
        return os.path.join(self.base_dir, name)

    def save_report_sync(self, data: Any, name: str) -> str:
        path = self._path(name)
        if hasattr(data, "to_csv"):
            data.to_csv(path, index=False)
        else:
            with open(path, "w") as fp:
                json.dump(data, fp)
        self.logger.debug("리포트 저장: %s", path)
        return path

    def load_report(self, name: str) -> Any:
        path = self._path(name)
        if name.endswith(".csv"):
            return pd.read_csv(path)
        with open(path) as fp:
            return json.load(fp)

    def archive(self, name: str) -> str:
        path = self._path(name)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        archived = f"{path}.bak"
        os.rename(path, archived)
        self.logger.debug("리포트 아카이브: %s", archived)
        return archived
