"""Market data service coordinating REST/WebSocket clients."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx

from ..core.config import settings
from .okx_ws import OKXWebSocketClient


class MarketDataService:
    """High-level market data abstraction used by API and workers."""

    def __init__(self) -> None:
        self._http_client = httpx.AsyncClient(base_url=settings.okx_base_url)
        self._ws_client = OKXWebSocketClient()

    async def fetch_tickers(self) -> list[dict[str, Any]]:
        """Fetch ticker snapshot via REST."""
        response = await self._http_client.get("/api/v5/market/tickers?instType=SWAP")
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    async def fetch_candles(self, symbol: str, granularity: str) -> list[list[str]]:
        """Fetch historical candles via REST."""
        params = {"instId": symbol, "bar": granularity}
        response = await self._http_client.get("/api/v5/market/candles", params=params)
        response.raise_for_status()
        payload = response.json()
        return payload.get("data", [])

    async def stream_live_candles(self, symbol: str, interval: str):
        """Yield live candles from the WebSocket channel."""
        async for message in self._ws_client.subscribe_candles(symbol=symbol, interval=interval):
            yield message

    async def close(self) -> None:
        await asyncio.gather(
            self._http_client.aclose(),
            self._ws_client.close(),
        )
