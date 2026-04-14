"""Booking business logic and interactions with the database focus on booking management and time slot validation."""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any, cast

from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate
from app.services.game_service import GameService


class BookingService:
    """Service for booking operations."""

    @staticmethod
    def create_booking(db: Session, user_id: int, booking: BookingCreate) -> Booking:
        """Create a new booking (rental)."""
        # Check if game exists and is available
        game = GameService.get_game(db, booking.game_id)
        if not game.is_available or cast(int, cast(Any, game).stock) <= 0:
            raise HTTPException(status_code=400, detail="Game is not available")

        # Renting consumes one unit from stock immediately.
        current_stock = cast(int, cast(Any, game).stock)
        setattr(game, "stock", current_stock - 1)
        setattr(game, "is_available", current_stock - 1 > 0)

        # Create booking
        db_booking = Booking(
            user_id=user_id, game_id=booking.game_id, return_date=booking.return_date
        )
        db.add(db_booking)
        db.add(game)
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
        if not booking.is_active:
            raise HTTPException(status_code=400, detail="Booking already returned")

        setattr(booking, "is_active", False)

        game = GameService.get_game(db, cast(int, cast(Any, booking).game_id))
        setattr(game, "stock", cast(int, cast(Any, game).stock) + 1)
        setattr(game, "is_available", True)

        db.add(booking)
        db.add(game)
        db.commit()
        db.refresh(booking)
        return booking
