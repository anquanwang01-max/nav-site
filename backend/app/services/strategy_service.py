"""Strategy service handling DeepSeek prompt orchestration."""
from __future__ import annotations

import httpx

from ..core.config import settings
from ..models.schemas import StrategyRequest, StrategyResponse


class StrategyService:
    """Small facade around the LLM strategy generation workflow."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.deepseek_api_url)

    async def generate_strategy(self, request: StrategyRequest) -> StrategyResponse:
        payload = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
        }
        headers = {"Authorization": f"Bearer {settings.deepseek_api_key}"}
        response = await self._client.post("/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return StrategyResponse(
            strategy_name=request.strategy_name,
            description=request.description,
            llm_response=data,
        )

    async def list_strategies(self) -> list[StrategyResponse]:
        # Placeholder: would normally query persistence layer
        return []

    async def close(self) -> None:
        await self._client.aclose()
