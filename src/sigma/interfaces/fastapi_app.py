"""FastAPI 애플리케이션 초기화 모듈."""

from __future__ import annotations

from sigma.common.logging_service import get_logger
from fastapi import FastAPI


def init_app(config: dict) -> FastAPI:
    """설정 객체를 받아 FastAPI 인스턴스를 생성한다."""

    if config is None:
        raise ValueError("config 필요")

    app = FastAPI()

    if config.get("enable_cors"):
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.get("cors_origins", ["*"]),
            allow_methods=["*"],
            allow_headers=["*"],
        )

    router = config.get("api_router")
    if router is not None:
        app.include_router(router)

    logger = get_logger(__name__)
    logger.debug("FastAPI 앱 초기화 완료")
    return app
