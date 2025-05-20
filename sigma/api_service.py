from fastapi import FastAPI
from sigma.utils.logger import logger


def init_api() -> FastAPI:
    """FastAPI 인스턴스를 초기화합니다."""
    app = FastAPI()
    logger.info("api initialized")
    return app
