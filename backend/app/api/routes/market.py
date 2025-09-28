"""Market data endpoints."""
from fastapi import APIRouter, Depends

from ...services.market_data import MarketDataService

router = APIRouter()


def get_market_service() -> MarketDataService:
    return MarketDataService()


@router.get("/tickers")
async def list_tickers(service: MarketDataService = Depends(get_market_service)):
    """Return the cached ticker list from the market data service."""
    return await service.fetch_tickers()


@router.get("/candles/{symbol}")
async def get_candles(
    symbol: str,
    granularity: str = "1m",
    service: MarketDataService = Depends(get_market_service),
):
    """Return OHLCV candles for the requested symbol and granularity."""
    return await service.fetch_candles(symbol=symbol, granularity=granularity)
