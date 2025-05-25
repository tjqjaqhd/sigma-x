from __future__ import annotations

import hmac
import hashlib
import time
from typing import Any, Dict, Optional

import aiohttp
from urllib.parse import urlencode


class BaseExchangeClient:
    """공통 기능을 제공하는 거래소 API 클라이언트."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.session = session or aiohttp.ClientSession()

    async def close(self) -> None:
        await self.session.close()


class UpbitClient(BaseExchangeClient):
    """업비트 현물 거래 API 연동."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        *,
        base_url: str = "https://api.upbit.com",
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        super().__init__(session)
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url

    async def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json",
        }

    async def place_order(self, side: str, symbol: str, volume: float) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/orders"
        payload = {
            "market": symbol,
            "side": side.lower(),
            "volume": str(volume),
            "ord_type": "market",
        }
        headers = await self._headers()
        async with self.session.post(url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_balance(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/accounts"
        headers = await self._headers()
        async with self.session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()


class BinanceFuturesClient(BaseExchangeClient):
    """바이낸스 선물 API 연동."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        *,
        base_url: str = "https://fapi.binance.com",
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        super().__init__(session)
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _sign(self, params: Dict[str, Any]) -> str:
        query = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        return f"{query}&signature={signature}"

    async def place_order(self, side: str, symbol: str, quantity: float, *, leverage: int = 1) -> Dict[str, Any]:
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
            "leverage": leverage,
        }
        query = self._sign(params)
        url = f"{self.base_url}{endpoint}?{query}"
        headers = {"X-MBX-APIKEY": self.api_key}
        async with self.session.post(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_balance(self) -> Dict[str, Any]:
        endpoint = "/fapi/v2/balance"
        params = {"timestamp": int(time.time() * 1000)}
        query = self._sign(params)
        url = f"{self.base_url}{endpoint}?{query}"
        headers = {"X-MBX-APIKEY": self.api_key}
        async with self.session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()
