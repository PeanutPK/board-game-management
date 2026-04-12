"""Game business logic and interactions with the database focus on stock checking."""

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
        db: Session, skip: int = 0, limit: int = 10, available_only: bool = False
    ) -> list[Game]:
        """Get all games with pagination."""
        query = db.query(Game).offset(skip).limit(limit)
        if available_only:
            query = query.filter(Game.stock > 0)
        return query.all()

    @staticmethod
    def create_game(db: Session, game: GameCreate) -> Game:
        """Create a new game."""
        db_game = Game(
            title=game.title,
            description=game.description,
            price=game.price,
            rent=game.rent,
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
            db_game.is_available = db_game.stock > 0

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
        return game.stock >= quantity
