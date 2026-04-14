"""Game business logic and interactions with the database focus on stock checking."""

from typing import Any, cast

from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.game import Game
from app.schemas.game_schema import GameCreate, GameUpdate


class GameService:
    """Service for game operations."""

    @staticmethod
    def count_games(db: Session) -> int:
        """Count total number of games."""
        return db.query(Game).count()

    @staticmethod
    def count_available_games(db: Session) -> int:
        """Count number of games with stock > 0."""
        return db.query(Game).filter(Game.stock > 0).count()

    @staticmethod
    def get_game_by_title(db: Session, title: str) -> Game:
        """Get game by title."""
        game = db.query(Game).filter(Game.title == title).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    @staticmethod
    def get_game(db: Session, game_id: int) -> Game:
        """Get game by ID."""
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    @staticmethod
    def get_all_games(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        available_only: bool = False,
        search: str = "",
        min_stock: int = -1,
        max_stock: int = -1,
        sort_by: str = "title",
    ) -> tuple[list[Game], int]:
        """Get all games with pagination, filtering, and sorting.

        Returns: (games_list, total_count)
        """
        query = db.query(Game)

        # Apply filters
        if available_only:
            query = query.filter(Game.stock > 0)

        if search.strip():
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Game.title.ilike(search_term),
                    Game.description.ilike(search_term),
                )
            )

        if min_stock >= 0:
            query = query.filter(Game.stock >= min_stock)

        if max_stock >= 0:
            query = query.filter(Game.stock <= max_stock)

        # Get total count before pagination
        total_count = query.count()

        # Apply sorting
        if sort_by == "price_asc":
            query = query.order_by(Game.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Game.price.desc())
        elif sort_by == "rating":
            query = query.order_by(func.coalesce(Game.average_rating, 0).desc())
        elif sort_by == "stock":
            query = query.order_by(Game.stock.desc())
        else:  # Default to title
            query = query.order_by(Game.title.asc())

        # Apply pagination
        games = query.offset(skip).limit(limit).all()

        return games, total_count

    @staticmethod
    def get_trending_games(db: Session, limit: int = 4) -> list[Game]:
        """Get the highest rated games."""
        return (
            db.query(Game)
            .order_by(func.coalesce(Game.average_rating, 0).desc(), Game.price.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_game(db: Session, game: GameCreate) -> Game:
        """Create a new game."""
        average_rating = (
            game.average_rating if game.average_rating is not None else game.price
        )
        db_game = Game(
            title=game.title,
            description=game.description,
            price=game.price,
            rent=game.rent,
            average_rating=average_rating,
            min_players=game.min_players,
            max_players=game.max_players,
            average_playtime=game.average_playtime,
            recommended_age=game.recommended_age,
            stock=game.stock,
            is_available=game.stock > 0,
        )
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game

    @staticmethod
    def update_game(db: Session, game_id: int, game_update: GameUpdate) -> Game:
        """Update an existing game."""
        db_game = GameService.get_game(db, game_id)

        update_data = game_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_game, field, value)

        if "stock" in update_data and "is_available" not in update_data:
            stock_value = cast(int, update_data["stock"])
            setattr(db_game, "is_available", stock_value > 0)

        if (
            "average_rating" not in update_data
            and cast(Any, db_game).average_rating is None
        ):
            setattr(db_game, "average_rating", cast(Any, db_game).price)

        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game

    @staticmethod
    def delete_game(db: Session, game_id: int) -> dict:
        """Delete a game."""
        db_game = GameService.get_game(db, game_id)
        db.delete(db_game)
        db.commit()
        return {"message": "Game deleted"}

    @staticmethod
    def check_stock(db: Session, game_id: int, quantity: int) -> bool:
        """Check if game has enough stock."""
        game = GameService.get_game(db, game_id)
        return bool(cast(Any, game).stock >= quantity)

    @staticmethod
    def get_available_stock_for_rental(db: Session, game_id: int) -> int:
        """Get available stock for rental."""
        game = GameService.get_game(db, game_id)
        return max(0, cast(int, cast(Any, game).stock))
