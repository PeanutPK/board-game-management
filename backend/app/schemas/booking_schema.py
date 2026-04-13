"""Booking schema definitions for request validation and response formatting."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingCreate(BaseModel):
    """Booking creation request schema."""

    game_id: int
    return_date: Optional[datetime] = None


class BookingResponse(BaseModel):
    """Booking response schema."""

    id: int
    user_id: int
    game_id: int
    booking_date: datetime
    return_date: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True
