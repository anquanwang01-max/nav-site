"""Order management endpoints."""
from fastapi import APIRouter, Depends

from ...services.order_engine import OrderEngine
from ...models.schemas import OrderCreateRequest, OrderResponse

router = APIRouter()


def get_order_engine() -> OrderEngine:
    return OrderEngine()


@router.post("/", response_model=OrderResponse)
async def place_order(
    order: OrderCreateRequest,
    engine: OrderEngine = Depends(get_order_engine),
):
    """Submit an order to the trading venue."""
    return await engine.place_order(order)


@router.delete("/{order_id}")
async def cancel_order(order_id: str, engine: OrderEngine = Depends(get_order_engine)):
    """Cancel an existing order."""
    return await engine.cancel_order(order_id)


@router.get("/", response_model=list[OrderResponse])
async def list_orders(engine: OrderEngine = Depends(get_order_engine)):
    """Return a list of active and historical orders."""
    return await engine.list_orders()
