"""FastAPI application entry point for the crypto quant trading platform."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import market, orders, strategies
from .core.config import settings


app = FastAPI(
    title="Quant Crypto Trading Platform",
    description="REST API gateway providing market data, strategy orchestration, and order routing",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Health check endpoint used by monitoring and orchestrators."""
    return {"status": "ok"}
