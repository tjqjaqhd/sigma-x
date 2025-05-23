"""단순 캐시 모듈.

사양은 ``docs/4_development/module_specs/common/Cache_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional


class Cache:
    def __init__(
        self,
        redis=None,
        default_ttl: int = 60,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.redis = redis
        self.default_ttl = default_ttl
        self.logger = logger or logging.getLogger(__name__)
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}

    async def initialize(self) -> None:
        """외부 캐시 초기화 훅."""
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.default_ttl
        self._store[key] = value
        self._expiry[key] = time.time() + ttl

    def get(self, key: str) -> Any:
        exp = self._expiry.get(key)
        if exp and exp < time.time():
            self._store.pop(key, None)
            self._expiry.pop(key, None)
            return None
        return self._store.get(key)

    async def expire(self) -> None:
        now = time.time()
        for k in list(self._expiry):
            if self._expiry[k] < now:
                self._expiry.pop(k, None)
                self._store.pop(k, None)

