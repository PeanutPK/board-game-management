"""API for game reviews."""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import UserReview
from app.schemas.review_schema import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService

router = APIRouter(prefix="/games", tags=["reviews"])


def get_current_user_id(authorization: str = Header(None)) -> int:
    """Extract the user ID from the bearer token."""
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


def _serialize_review(review: UserReview) -> ReviewResponse:
    """Convert a review ORM object into the API response schema."""
    username = review.user.username if review.user else "Unknown"
    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        game_id=review.game_id,
        username=username,
        rating=review.rating,
        comment=review.comment,
    )


@router.get("/{game_id}/reviews", response_model=list[ReviewResponse])
def get_game_reviews(game_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a game."""
    reviews = ReviewService.get_game_reviews(db, game_id)
    return [_serialize_review(review) for review in reviews]


@router.post("/{game_id}/reviews", response_model=ReviewResponse)
def create_or_update_review(
    game_id: int,
    review: ReviewCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Create or update the current user's review for a game."""
    saved_review = ReviewService.save_review(db, user_id, game_id, review)
    return _serialize_review(saved_review)
