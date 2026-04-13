"""API for game browsing and management."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.game_schema import GameCreate, GameResponse, GameUpdate
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[GameResponse])
def get_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    """Get all games with pagination."""
    return GameService.get_all_games(
        db, skip=skip, limit=limit, available_only=available_only
    )


@router.get("/trending", response_model=list[GameResponse])
def get_trending_games(
    limit: int = Query(4, ge=1, le=12),
    db: Session = Depends(get_db),
):
    """Get the highest rated games for the trending section."""
    return GameService.get_trending_games(db, limit=limit)


@router.get("/stats", response_model=dict[str, int])
def get_game_stats(db: Session = Depends(get_db)):
    """Get game statistics."""
    return {
        "total": GameService.count_games(db),
        "available": GameService.count_available_games(db),
    }


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game by ID."""
    return GameService.get_game(db, game_id)


@router.post("/", response_model=GameResponse)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    """Create a new game."""
    return GameService.create_game(db, game)


@router.put("/{game_id}", response_model=GameResponse)
def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)):
    """Update an existing game."""
    return GameService.update_game(db, game_id, game_update)


@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    """Delete a game."""
    return GameService.delete_game(db, game_id)
