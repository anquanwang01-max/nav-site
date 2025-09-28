"""Background worker ingesting market data and persisting to storage."""
from __future__ import annotations

import asyncio
import logging

from backend.app.services.market_data import MarketDataService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run_worker(symbol: str = "BTC-USDT-SWAP") -> None:
    service = MarketDataService()
    try:
        async for message in service.stream_live_candles(symbol=symbol, interval="1s"):
            logger.info("received candle update: %s", message)
    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(run_worker())
