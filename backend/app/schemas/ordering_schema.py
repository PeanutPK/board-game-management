"""Ordering schema definitions for request validation and response formatting."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    """Order creation request schema."""
    game_id: int
    quantity: int = 1


class OrderResponse(BaseModel):
    """Order response schema."""
    id: int
    user_id: int
    game_id: int
    order_date: datetime
    quantity: int
    total_price: int
    status: str
