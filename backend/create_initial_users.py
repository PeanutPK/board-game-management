"""Create or update one admin user and one staff user.

Usage example:
python create_initial_users.py
"""

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine

# Import model modules so SQLAlchemy registers all relationship targets.
from app.models import booking as _booking_models  # noqa: F401
from app.models import game as _game_models  # noqa: F401
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


def main() -> None:
    """Create/update users with the requested roles."""
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

    print(admin_result)
    print(staff_result)


if __name__ == "__main__":
    main()
