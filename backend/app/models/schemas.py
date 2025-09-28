"""Shared Pydantic schemas."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    instId: str = Field(..., description="Instrument identifier, e.g. BTC-USDT-SWAP")
    tdMode: str = Field(..., description="Margin mode: cross or isolated")
    side: str = Field(..., description="buy or sell")
    ordType: str = Field(..., description="market, limit, post_only, fok, ioc")
    sz: str = Field(..., description="Order size")
    px: str | None = Field(None, description="Price for limit orders")
    reduceOnly: bool | None = Field(None, description="Reduce-only flag")
    takeProfitTriggerPx: str | None = None
    stopLossTriggerPx: str | None = None


class OrderResponse(BaseModel):
    code: str | None = None
    msg: str | None = None
    data: Any | None = None


class StrategyRequest(BaseModel):
    strategy_name: str
    description: str
    model: str = Field("deepseek-trader", description="LLM model to call")
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    messages: list[dict[str, str]] = Field(
        default_factory=list,
        description="Pre-seeded chat history for the DeepSeek API",
    )


class StrategyResponse(BaseModel):
    strategy_name: str
    description: str
    llm_response: Any
