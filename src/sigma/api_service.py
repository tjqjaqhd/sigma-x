"""외부 REST API 호출 유틸리티.

사양은 ``docs/4_development/module_specs/common/APIService_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp


class ApiService:
    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: int = 5,
        max_retry: int = 3,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.timeout = timeout
        self.max_retry = max_retry
        self.session = session or aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout)
        )
        self.logger = logger or logging.getLogger(__name__)

    async def request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        for attempt in range(1, self.max_retry + 1):
            try:
                async with self.session.request(method, url, **kwargs) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except Exception as exc:  # pragma: no cover - 네트워크 오류
                self.logger.warning(
                    "API 요청 실패 %s (%d/%d): %s", url, attempt, self.max_retry, exc
                )
                if attempt >= self.max_retry:
                    raise
                await asyncio.sleep(1)

    async def get(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        return await self.request("POST", url, **kwargs)

    async def close(self) -> None:
        await self.session.close()

