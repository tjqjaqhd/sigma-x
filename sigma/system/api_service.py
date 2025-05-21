"""API 서비스 초기화."""

import os
from threading import Thread

import uvicorn
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from sigma.utils.logger import logger
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy
from sigma.core.adaptive import ParamAdjuster

app = FastAPI()
_bot: TradingBot | None = None


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus 메트릭 엔드포인트."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/bot/start")
def start_bot() -> dict:
    global _bot
    if _bot is None:
        _bot = TradingBot(strategy=DummyStrategy())
    _bot.run(iterations=1)
    return {"status": "started"}


@app.post("/bot/stop")
def stop_bot() -> dict:
    global _bot
    _bot = None
    return {"status": "stopped"}


@app.post("/strategy/update")
def update_strategy(name: str, value: str) -> dict:
    ParamAdjuster().update_param(name, value)
    return {"name": name, "value": value}


def init_api() -> None:
    """FastAPI 서버를 백그라운드 스레드로 실행합니다."""

    def _run() -> None:  # pragma: no cover - 서버 실행
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

    if os.getenv("RUN_SERVER"):
        Thread(target=_run, daemon=True).start()
    logger.info("API 서비스 초기화")
