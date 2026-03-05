from fastapi import APIRouter, HTTPException
from typing import List
from models import BoardGame, BoardGameCreate

router = APIRouter(prefix="/games", tags=["games"])

# In-memory store for boilerplate purposes
games_db: List[BoardGame] = [
    BoardGame(
        id=1,
        title="Catan",
        genre="Strategy",
        min_players=3,
        max_players=4,
        available_copies=5,
        description="A classic resource management and trading game.",
    ),
    BoardGame(
        id=2,
        title="Pandemic",
        genre="Cooperative",
        min_players=2,
        max_players=4,
        available_copies=3,
        description="Work together to stop the spread of diseases worldwide.",
    ),
    BoardGame(
        id=3,
        title="Ticket to Ride",
        genre="Strategy",
        min_players=2,
        max_players=5,
        available_copies=4,
        description="Build railway routes across the country.",
    ),
]
_next_id = 4


@router.get("/", response_model=List[BoardGame])
def list_games():
    return games_db


@router.get("/{game_id}", response_model=BoardGame)
def get_game(game_id: int):
    for game in games_db:
        if game.id == game_id:
            return game
    raise HTTPException(status_code=404, detail="Game not found")


@router.post("/", response_model=BoardGame, status_code=201)
def create_game(game: BoardGameCreate):
    global _next_id
    new_game = BoardGame(id=_next_id, **game.model_dump())
    _next_id += 1
    games_db.append(new_game)
    return new_game


@router.put("/{game_id}", response_model=BoardGame)
def update_game(game_id: int, game: BoardGameCreate):
    for index, existing in enumerate(games_db):
        if existing.id == game_id:
            updated = BoardGame(id=game_id, **game.model_dump())
            games_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Game not found")


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: int):
    for index, game in enumerate(games_db):
        if game.id == game_id:
            games_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Game not found")
