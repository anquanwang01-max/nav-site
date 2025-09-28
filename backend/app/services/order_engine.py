"""Order engine implementing authenticated OKX trading requests."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any

import httpx

from ..core.config import settings
from ..models.schemas import OrderCreateRequest, OrderResponse


class OrderEngine:
    """Simple OKX order routing client."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.okx_base_url)

    async def _signed_headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        timestamp = str(time.time())
        prehash = f"{timestamp}{method.upper()}{path}{body}"
        secret = settings.okx_api_secret.encode()
        signature = hmac.new(secret, prehash.encode(), hashlib.sha256).digest()
        sign_b64 = base64.b64encode(signature).decode()

        return {
            "OK-ACCESS-KEY": settings.okx_api_key,
            "OK-ACCESS-SIGN": sign_b64,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": settings.okx_passphrase,
            "Content-Type": "application/json",
        }

    async def place_order(self, order: OrderCreateRequest) -> OrderResponse:
        path = "/api/v5/trade/order"
        payload = json.dumps(order.dict(exclude_none=True))
        headers = await self._signed_headers("POST", path, payload)
        response = await self._client.post(path, content=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return OrderResponse(**data)

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        path = "/api/v5/trade/cancel-order"
        body = json.dumps({"ordId": order_id})
        headers = await self._signed_headers("POST", path, body)
        response = await self._client.post(path, content=body, headers=headers)
        response.raise_for_status()
        return response.json()

    async def list_orders(self) -> list[OrderResponse]:
        path = "/api/v5/trade/orders-pending"
        headers = await self._signed_headers("GET", path)
        response = await self._client.get(path, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [OrderResponse(**item) for item in data.get("data", [])]

    async def close(self) -> None:
        await self._client.aclose()
