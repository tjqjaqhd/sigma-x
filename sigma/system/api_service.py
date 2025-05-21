"""API 서비스 초기화."""

import os
from threading import Thread
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Response, Depends, HTTPException, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from sigma.utils.logger import logger

app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN", "changeme")


def auth_header(token: Annotated[str, Depends(lambda: "")]):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus 메트릭 엔드포인트."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/bot/start")
def bot_start(token: Annotated[str, Depends(auth_header)] = ""):
    return {"status": "started"}


@app.post("/bot/stop")
def bot_stop(token: Annotated[str, Depends(auth_header)] = ""):
    return {"status": "stopped"}


@app.get("/performance")
def performance(token: Annotated[str, Depends(auth_header)] = ""):
    return {"pnl": 0}


@app.get("/positions")
def positions(token: Annotated[str, Depends(auth_header)] = ""):
    return []


def init_api() -> None:
    """FastAPI 서버를 백그라운드 스레드로 실행합니다."""

    def _run() -> None:  # pragma: no cover - 서버 실행
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

    if os.getenv("RUN_SERVER"):
        Thread(target=_run, daemon=True).start()
    logger.info("API 서비스 초기화")
