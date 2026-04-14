"""Review business logic and database interactions."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.game import Game
from app.models.user import UserReview
from app.schemas.review_schema import ReviewCreate
from app.services.game_service import GameService


class ReviewService:
    """Service for game review operations."""

    @staticmethod
    def get_game_reviews(db: Session, game_id: int) -> list[UserReview]:
        """Get all reviews for a game sorted by newest first."""
        GameService.get_game(db, game_id)
        return (
            db.query(UserReview)
            .filter(UserReview.game_id == game_id)
            .order_by(UserReview.id.desc())
            .all()
        )

    @staticmethod
    def save_review(
        db: Session,
        user_id: int,
        game_id: int,
        review: ReviewCreate,
    ) -> UserReview:
        """Create or update a user's review for a game."""
        GameService.get_game(db, game_id)

        db_review = (
            db.query(UserReview)
            .filter(UserReview.user_id == user_id, UserReview.game_id == game_id)
            .first()
        )

        if db_review is None:
            db_review = UserReview(
                user_id=user_id,
                game_id=game_id,
                rating=review.rating,
                comment=review.comment,
            )
            db.add(db_review)
        else:
            setattr(db_review, "rating", review.rating)
            setattr(db_review, "comment", review.comment)

        db.commit()
        db.refresh(db_review)
        return db_review
