"""동적 플러그인 로더.

설계 세부 사항은
``docs/4_development/module_specs/common/PluginLoader_Spec.md``를 참고한다.
"""

from __future__ import annotations

import importlib
import logging
from typing import Any, Dict, Optional


class PluginLoader:
    """모듈을 문자열 경로로 로드하여 캐싱한다."""

    def __init__(self, logger=None) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.cache: Dict[str, Any] = {}

    def load_module(self, path: str) -> Optional[Any]:
        if path in self.cache:
            return self.cache[path]
        try:
            module = importlib.import_module(path)
            self.cache[path] = module
            self.logger.debug("모듈 로드 성공: %s", path)
            return module
        except ModuleNotFoundError as exc:
            self.logger.error("모듈 로드 실패: %s", exc)
            return None

    def load_strategy(self, path: str) -> Optional[Any]:
        module = self.load_module(path)
        return getattr(module, "Strategy", None) if module else None

    def load_executor(self, path: str) -> Optional[Any]:
        module = self.load_module(path)
        return getattr(module, "Executor", None) if module else None

