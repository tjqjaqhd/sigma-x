"""사용자 설정 관리 모듈.

``docs/4_development/module_specs/common/UserPrefs_Spec.md`` 의 사양을 구현한다.
"""

from __future__ import annotations

import json
from sigma.common.logging_service import get_logger
from typing import Any, Dict, Optional
import logging


class UserPrefs:
    def __init__(
        self,
        path: str = "user_prefs.json",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.path = path
        self.logger = logger or get_logger(__name__)
        self.prefs: Dict[str, Any] = {}

    async def load_prefs(self) -> None:
        try:
            with open(self.path) as fp:
                self.prefs = json.load(fp)
        except FileNotFoundError:
            self.logger.info("프리퍼런스 파일 없음: %s", self.path)
            self.prefs = {}

    async def save_prefs(self) -> None:
        with open(self.path, "w") as fp:
            json.dump(self.prefs, fp)

    def get(self, key: str, default: Any | None = None) -> Any:
        return self.prefs.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.prefs[key] = value
