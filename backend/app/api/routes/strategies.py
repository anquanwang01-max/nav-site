"""Strategy orchestration endpoints."""
from fastapi import APIRouter, Depends

from ...services.strategy_service import StrategyService
from ...models.schemas import StrategyRequest, StrategyResponse

router = APIRouter()


def get_strategy_service() -> StrategyService:
    return StrategyService()


@router.post("/generate", response_model=StrategyResponse)
async def generate_strategy(
    request: StrategyRequest,
    service: StrategyService = Depends(get_strategy_service),
):
    """Generate or optimize a strategy via the LLM-powered engine."""
    return await service.generate_strategy(request)


@router.get("/", response_model=list[StrategyResponse])
async def list_strategies(service: StrategyService = Depends(get_strategy_service)):
    """List available strategies and their metadata."""
    return await service.list_strategies()
