"""API for ordering management and simulate payment process."""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ordering_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.core.security import decode_access_token

router = APIRouter(prefix="/orders", tags=["orders"])


def get_current_user_id(authorization: str = Header(None)) -> int:
    """Extract user ID from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return int(sub)


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Create a new order."""
    return OrderService.create_order(db, user_id, order)


@router.get("/", response_model=list[OrderResponse])
def get_my_orders(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """Get all orders for the current user."""
    return OrderService.get_user_orders(db, user_id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get a specific order."""
    return OrderService.get_order(db, order_id)


@router.post("/{order_id}/complete", response_model=OrderResponse)
def complete_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Complete an order (simulate payment)."""
    return OrderService.complete_order(db, order_id)
