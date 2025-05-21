"""API 서비스 초기화."""

import os
from threading import Thread

import uvicorn
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from sigma.utils.logger import logger

app = FastAPI()


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus 메트릭 엔드포인트."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def init_api() -> None:
    """FastAPI 서버를 백그라운드 스레드로 실행합니다."""

    def _run() -> None:  # pragma: no cover - 서버 실행
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

    if os.getenv("RUN_SERVER"):
        Thread(target=_run, daemon=True).start()
    logger.info("API 서비스 초기화")
