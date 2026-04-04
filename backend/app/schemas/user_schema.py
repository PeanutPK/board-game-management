"""User schema definitions for request validation and response formatting."""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User creation request schema."""

    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    username: str
    is_active: bool
    is_admin: bool


class UserLogin(BaseModel):
    """User login request schema."""

    username: str
    password: str


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
