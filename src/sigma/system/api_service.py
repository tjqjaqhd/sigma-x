"""API 서비스 초기화."""

import os
from threading import Thread
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Response, Depends, HTTPException, status, Query
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from sigma.utils.logger import logger
from sigma.data.models import SystemConfig

app = FastAPI()

# API_TOKEN = SystemConfig.get("API_TOKEN", "changeme")  # 모듈 레벨에서 제거

def get_api_token():
    return SystemConfig.get("API_TOKEN", "changeme")


def auth_header(token: Annotated[str, Depends(lambda: "")]):
    if token != get_api_token():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus 메트릭 엔드포인트."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/bot/start")
def bot_start(token: Annotated[str, Depends(auth_header)] = "", mode: str = Query("live")):
    is_simulation = (mode == "sim")
    # TradingSession.is_simulation = is_simulation (실제 세션 객체가 있다면)
    return {"status": "started", "mode": mode, "is_simulation": is_simulation}


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
        uvicorn.run(app, host="0.0.0.0", port=int(SystemConfig.get("PORT", 8000)))

    if SystemConfig.get("RUN_SERVER"):
        Thread(target=_run, daemon=True).start()
    logger.info("API 서비스 초기화")
