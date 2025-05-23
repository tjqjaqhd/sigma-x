"""대시보드 API 모듈.

FastAPI 애플리케이션을 생성하여 실시간 포지션과 시스템 상태를 제공한다. 사양은
``docs/4_development/module_specs/interfaces/DashboardAPI_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import logging
from fastapi import APIRouter, FastAPI
from typing import Any, Dict


class DashboardAPI:
    def __init__(self, session_manager, system_status, ws_endpoint, logger=None) -> None:
        self.session_manager = session_manager
        self.system_status = system_status
        self.ws_endpoint = ws_endpoint
        self.logger = logger or logging.getLogger(__name__)

    def create_app(self) -> FastAPI:
        app = FastAPI()

        router = APIRouter()

        @router.get("/api/positions")
        async def get_positions() -> Dict[str, Any]:
            return self.session_manager.positions

        @router.get("/api/status")
        async def get_status() -> Dict[str, Any]:
            return await self.system_status.report_status()

        app.include_router(router)
        app.include_router(self.ws_endpoint.router)
        self.logger.debug("Dashboard API 초기화 완료")
        return app

