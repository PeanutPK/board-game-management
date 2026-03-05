from pydantic import BaseModel
from typing import Optional


class BoardGame(BaseModel):
    id: int
    title: str
    genre: str
    min_players: int
    max_players: int
    available_copies: int
    description: Optional[str] = None


class BoardGameCreate(BaseModel):
    title: str
    genre: str
    min_players: int
    max_players: int
    available_copies: int
    description: Optional[str] = None


class Store(BaseModel):
    id: int
    name: str
    location: str
    contact: Optional[str] = None


class StoreCreate(BaseModel):
    name: str
    location: str
    contact: Optional[str] = None
