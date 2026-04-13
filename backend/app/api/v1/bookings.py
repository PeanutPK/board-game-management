"""API for game booking logics."""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.booking_schema import BookingCreate, BookingResponse
from app.services.booking_service import BookingService
from app.core.security import decode_access_token

router = APIRouter(prefix="/bookings", tags=["bookings"])


def get_current_user_id(authorization: str = Header(None)) -> int:
    """Extract user ID from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return int(sub)


@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Create a new booking."""
    return BookingService.create_booking(db, user_id, booking)


@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """Get all active bookings for the current user."""
    return BookingService.get_user_bookings(db, user_id)


@router.post("/{booking_id}/return")
def return_booking(
    booking_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return a booking."""
    return BookingService.return_booking(db, user_id, booking_id)
