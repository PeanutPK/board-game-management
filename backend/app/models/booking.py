"""Booking model and related database operations."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class Booking(Base):
    """Booking database model."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    booking_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="bookings")
    game = relationship("Game", back_populates="bookings")


class Order(Base):
    """Order database model."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Integer, default=1)
    total_price = Column(Integer)
    status = Column(String, default="pending")

    # Relationships
    user = relationship("User", back_populates="orders")
    game = relationship("Game", back_populates="orders")
