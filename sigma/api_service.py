from fastapi import FastAPI
from sigma.utils.logger import logger


def init_api() -> FastAPI:
    """FastAPI 앱을 초기화합니다."""
    logger.info("API 서비스 초기화")
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Sigma API"}

    return app
