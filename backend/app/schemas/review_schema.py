"""Review schema definitions for request validation and response formatting."""

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Review creation request schema."""

    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=500)


class ReviewResponse(BaseModel):
    """Review response schema."""

    id: int
    user_id: int
    game_id: int
    username: str
    rating: int
    comment: str

    class Config:
        from_attributes = True
