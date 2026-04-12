"""Initialize admin/staff users and seed games from CSV.

Usage example:
python initial_database.py
"""

import csv
from pathlib import Path

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine

# Import model modules so SQLAlchemy registers all relationship targets.
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

        user.email = email
        user.username = username
        user.hashed_password = hashed_password
        user.is_admin = is_admin
        user.is_staff = is_staff
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


def seed_games_from_csv(csv_path: Path) -> tuple[int, int, int]:
    """Seed games using rows from CSV and set rent to one-third of price."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    db = SessionLocal()
    created = 0
    updated = 0
    skipped = 0

    try:
        existing_games = {game.title: game for game in db.query(Game).all()}

        with csv_path.open("r", encoding="utf-8", errors="replace", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                title = (row.get("Name") or "").strip()
                if not title:
                    skipped += 1
                    continue

                description = (row.get("Description") or "").strip() or "No description provided"

                # CSV has no explicit price field, so AvgRating is used as actual price.
                price = _parse_float(row.get("AvgRating"), 0.0)
                if price <= 0:
                    price = _parse_float(row.get("BayesAvgRating"), 0.0) * 100
                if price <= 0:
                    skipped += 1
                    continue

                rent = round(price / 3, 2)
                min_players = max(1, _parse_int(row.get("MinPlayers"), 1))
                max_players = max(min_players, _parse_int(row.get("MaxPlayers"), min_players))
                average_playtime = max(0, _parse_int(row.get("MfgPlaytime"), 0))

                recommended_age = _parse_int(row.get("MfgAgeRec"), 0)
                if recommended_age <= 0:
                    recommended_age = _parse_int(row.get("ComAgeRec"), 8)

                stock = _parse_int(row.get("NumOwned"), 0)
                stock = max(0, min(stock, 100))

                game = existing_games.get(title)
                if game is None:
                    game = Game(title=title)
                    db.add(game)
                    existing_games[title] = game
                    created += 1
                else:
                    updated += 1

                game.description = description
                game.price = price
                game.rent = rent
                game.min_players = min_players
                game.max_players = max_players
                game.average_playtime = average_playtime
                game.recommended_age = recommended_age
                game.stock = stock
                game.is_available = stock > 0

        db.commit()
        return created, updated, skipped
    finally:
        db.close()


def main() -> None:
    """Create/update users and seed games from CSV."""
    setup = input("Use default setup? (y/n): ").lower()
    if not setup or setup == "y":
        admin_email = "admin@example.com"
        admin_username = "admin"
        admin_password = "adminpassword"
        staff_email = "staff@example.com"
        staff_username = "staff"
        staff_password = "staffpassword"
    else:
        admin_email = input("Admin email: ")
        admin_username = input("Admin username: ")
        admin_password = input("Admin password: ")
        staff_email = input("Staff email: ")
        staff_username = input("Staff username: ")
        staff_password = input("Staff password: ")

    if admin_email == staff_email:
        raise ValueError("Admin and staff emails must be different")
    if admin_username == staff_username:
        raise ValueError("Admin and staff usernames must be different")

    # Ensure tables exist before attempting inserts/updates.
    Base.metadata.create_all(bind=engine)

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

    games_csv_path = Path(__file__).resolve().parent / "app" / "db" / "initial_data" / "games.csv"
    created_games, updated_games, skipped_games = seed_games_from_csv(games_csv_path)

    print(admin_result)
    print(staff_result)
    print(
        f"Games seeded from CSV. Created: {created_games}, Updated: {updated_games}, Skipped: {skipped_games}"
    )


if __name__ == "__main__":
    main()
