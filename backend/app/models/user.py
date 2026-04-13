"""User model and related database operations."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    bookings = relationship("Booking", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("UserReview", back_populates="user")


class UserReview(Base):
    """User review database model."""

    __tablename__ = "user_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    rating = Column(Integer)
    comment = Column(String)

    # Relationships
    user = relationship("User", back_populates="reviews")
    game = relationship("Game", back_populates="reviews")
