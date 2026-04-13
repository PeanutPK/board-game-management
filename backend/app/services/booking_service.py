"""Booking business logic and interactions with the database focus on booking management and time slot validation."""

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate
from app.services.game_service import GameService


class BookingService:
    """Service for booking operations."""

    @staticmethod
    def create_booking(db: Session, user_id: int, booking: BookingCreate) -> Booking:
        """Create a new booking."""
        # Check if game exists and is available
        game = GameService.get_game(db, booking.game_id)
        if not game.is_available:
            raise HTTPException(status_code=400, detail="Game is not available")

        # Create booking
        db_booking = Booking(
            user_id=user_id, game_id=booking.game_id, return_date=booking.return_date
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: int) -> list[Booking]:
        """Get all active bookings for a user."""
        return (
            db.query(Booking)
            .filter(Booking.user_id == user_id, Booking.is_active)
            .all()
        )

    @staticmethod
    def return_booking(db: Session, user_id: int, booking_id: int) -> Booking:
        """Mark a booking as returned."""
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        setattr(booking, "is_active", False)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
