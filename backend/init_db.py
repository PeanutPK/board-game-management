"""Initialize admin/staff users and seed games from CSV.

Usage example:
python initial_database.py
"""

import csv
from pathlib import Path
from typing import Any

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine

from app.models import booking as _booking_models  # noqa: F401
from app.models import game as _game_models  # noqa: F401
from app.models.game import Game
from app.models.user import User


def upsert_user(
    *,
    email: str,
    username: str,
    password: str,
    is_admin: bool,
    is_staff: bool,
) -> str:
    """Create a user if missing, otherwise update role/password fields."""
    db = SessionLocal()
    try:
        user = (
            db.query(User)
            .filter((User.email == email) | (User.username == username))
            .first()
        )

        hashed_password = get_password_hash(password)

        if user is None:
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
                is_admin=is_admin,
                is_staff=is_staff,
            )
            db.add(user)
            db.commit()
            return f"Created user '{username}' ({email})"

        setattr(user, "email", email)
        setattr(user, "username", username)
        setattr(user, "hashed_password", hashed_password)
        setattr(user, "is_admin", is_admin)
        setattr(user, "is_staff", is_staff)
        db.commit()
        return f"Updated user '{username}' ({email})"
    finally:
        db.close()


def _parse_float(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_int(value: str | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _ensure_avg_rating_column() -> None:
    """Add the avg_rating column when upgrading an existing SQLite database."""
    with engine.begin() as conn:
        cols = conn.exec_driver_sql("PRAGMA table_info(games)").fetchall()
        col_names = {column[1] for column in cols}

        if "avg_rating" not in col_names:
            conn.exec_driver_sql("ALTER TABLE games ADD COLUMN avg_rating FLOAT")


def _resolve_price(avg_rating: float, bayes_avg_rating: float) -> float:
    if avg_rating > 0:
        return avg_rating
    return bayes_avg_rating


def _resolve_average_playtime(row: dict[str, str | None]) -> int:
    avg_playtime = max(0, _parse_int(row.get("MfgPlaytime"), 0))
    if avg_playtime:
        return avg_playtime
    return _parse_int(row.get("ComMaxPlaytime"), 0)


def _resolve_recommended_age(row: dict[str, str | None]) -> int:
    recommended_age = _parse_int(row.get("MfgAgeRec"), 0)
    if recommended_age > 0:
        return recommended_age
    return _parse_int(row.get("ComAgeRec"), 8)


def _resolve_stock(row: dict[str, str | None]) -> int:
    stock = _parse_int(row.get("NumOwned"), 0)
    return max(0, min(stock, 100))


def _parse_game_row(row: dict[str, str | None]) -> dict[str, Any] | None:
    title = (row.get("Name") or "").strip()
    if not title:
        return None

    desc = (
        row.get("Description") or ""
    ).strip().capitalize() or "No description provided"

    avg_rating = _parse_float(row.get("AvgRating"), 0.0)
    bayes_avg_rating = _parse_float(row.get("BayesAvgRating"), 0.0)
    price = _resolve_price(avg_rating, bayes_avg_rating)
    if price <= 0:
        return None

    min_players = max(1, _parse_int(row.get("MinPlayers"), 1))
    max_players = max(min_players, _parse_int(row.get("MaxPlayers"), min_players))
    stock = _resolve_stock(row)

    return {
        "title": title,
        "description": desc,
        "price": price,
        "rent": round(price / 3, 2),
        "average_rating": avg_rating,
        "min_players": min_players,
        "max_players": max_players,
        "average_playtime": _resolve_average_playtime(row),
        "recommended_age": _resolve_recommended_age(row),
        "stock": stock,
        "is_available": stock > 0,
    }


def _apply_game_fields(game: Game, fields: dict[str, Any]) -> None:
    for key, value in fields.items():
        if key == "title":
            continue
        setattr(game, key, value)


def _read_setup_values() -> tuple[tuple[str, str, str], tuple[str, str, str]]:
    setup = input("Use default setup? (y/n): ").strip().lower()
    if not setup or setup == "y":
        return (
            ("admin@example.com", "admin", "adminpassword"),
            ("staff@example.com", "staff", "staffpassword"),
        )

    return (
        (
            input("Admin email: "),
            input("Admin username: "),
            input("Admin password: "),
        ),
        (
            input("Staff email: "),
            input("Staff username: "),
            input("Staff password: "),
        ),
    )


def _validate_distinct_users(
    admin_values: tuple[str, str, str],
    staff_values: tuple[str, str, str],
) -> None:
    admin_email, admin_username, _ = admin_values
    staff_email, staff_username, _ = staff_values

    if admin_email == staff_email:
        raise ValueError("Admin and staff emails must be different")
    if admin_username == staff_username:
        raise ValueError("Admin and staff usernames must be different")


def seed_games_from_csv(path: Path) -> tuple[int, int, int]:
    """Seed games using rows from CSV and set rent to one-third of price."""
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    db = SessionLocal()
    created = 0
    updated = 0
    skipped = 0

    try:
        existing_games: dict[str, Game] = {
            str(game.title): game for game in db.query(Game).all()
        }

        with path.open(encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                parsed = _parse_game_row(row)
                if parsed is None:
                    skipped += 1
                    continue
                title = str(parsed["title"])
                game = existing_games.get(title)
                if game is None:
                    game = Game(title=title)
                    db.add(game)
                    existing_games[title] = game
                    created += 1
                else:
                    updated += 1

                _apply_game_fields(game, parsed)

        db.commit()
        return created, updated, skipped
    finally:
        db.close()


def main() -> None:
    """Create/update users and seed games from CSV."""
    admin_values, staff_values = _read_setup_values()
    _validate_distinct_users(admin_values, staff_values)
    admin_email, admin_username, admin_password = admin_values
    staff_email, staff_username, staff_password = staff_values

    # Ensure tables exist before attempting inserts/updates.
    Base.metadata.create_all(bind=engine)
    _ensure_avg_rating_column()

    admin_result = upsert_user(
        email=admin_email,
        username=admin_username,
        password=admin_password,
        is_admin=True,
        is_staff=True,
    )
    staff_result = upsert_user(
        email=staff_email,
        username=staff_username,
        password=staff_password,
        is_admin=False,
        is_staff=True,
    )

    base = Path(__file__).resolve().parent
    path = base / "app/db/data/games.csv"

    created, updated, skipped = seed_games_from_csv(path)

    print(admin_result)
    print(staff_result)
    print(f"""
Games seeded from CSV.\n\
Created: {created},\n\
Updated: {updated},\n\
Skipped: {skipped}
""")


if __name__ == "__main__":
    main()
