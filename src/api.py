from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class TradeRequest(BaseModel):
    symbol: str
    side: str
    price: float
    quantity: float


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """서비스 헬스 체크."""
    return {"status": "ok"}


@router.post("/trade")
async def trade(req: TradeRequest) -> dict[str, TradeRequest]:
    """단순 에코 트레이드 엔드포인트."""
    return {"received": req}


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(data)
    except WebSocketDisconnect:
        pass


app = FastAPI()
app.include_router(router)
