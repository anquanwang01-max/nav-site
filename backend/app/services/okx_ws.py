"""Async WebSocket client for streaming OKX market data."""
from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator

import websockets

OKX_PUBLIC_WS = "wss://ws.okx.com:8443/ws/v5/public"


class OKXWebSocketClient:
    """Lightweight WebSocket client tailored for OKX public market data."""

    def __init__(self, url: str = OKX_PUBLIC_WS) -> None:
        self._url = url
        self._connection: websockets.WebSocketClientProtocol | None = None
        self._lock = asyncio.Lock()

    async def _ensure_connection(self) -> websockets.WebSocketClientProtocol:
        if self._connection and self._connection.open:
            return self._connection

        async with self._lock:
            if self._connection and self._connection.open:
                return self._connection
            self._connection = await websockets.connect(self._url, ping_interval=20)
            return self._connection

    async def subscribe_candles(
        self, symbol: str, interval: str
    ) -> AsyncGenerator[dict, None]:
        """Subscribe to candle data for the specified symbol/interval."""

        payload = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "candle" + interval,
                    "instId": symbol,
                }
            ],
        }

        connection = await self._ensure_connection()
        await connection.send(json.dumps(payload))

        try:
            async for message in connection:
                data = json.loads(message)
                if data.get("event") == "subscribe" and data.get("arg", {}).get("channel", ""):
                    continue
                yield data
        finally:
            await self.unsubscribe(payload)

    async def unsubscribe(self, payload: dict) -> None:
        if not self._connection or not self._connection.open:
            return
        payload = {"op": "unsubscribe", "args": payload.get("args", [])}
        await self._connection.send(json.dumps(payload))

    async def close(self) -> None:
        if self._connection and self._connection.open:
            await self._connection.close()
        self._connection = None
