"""Game schema definitions for request validation and response formatting."""

from pydantic import BaseModel
from typing import Optional


class GameCreate(BaseModel):
    """Game creation request schema."""

    title: str
    description: str
    price: float
    rent: float
    min_players: int
    max_players: int
    average_playtime: int
    recommended_age: int
    stock: int


class GameUpdate(BaseModel):
    """Game update request schema."""

    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_available: Optional[bool] = None


class GameResponse(BaseModel):
    """Game response schema."""

    id: int
    title: str
    description: str
    price: float
    stock: int
    is_available: bool
