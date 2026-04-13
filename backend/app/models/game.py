"""Game model and related database operations."""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Game(Base):
    """Game database model."""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    rent = Column(Float)
    average_rating = Column(Float)
    min_players = Column(Integer)
    max_players = Column(Integer)
    average_playtime = Column(Integer)
    recommended_age = Column(Integer)
    stock = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)

    # Relationships
    bookings = relationship("Booking", back_populates="game")
    orders = relationship("Order", back_populates="game")
    reviews = relationship("UserReview", back_populates="game")
