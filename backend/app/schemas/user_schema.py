"""User schema definitions for request validation and response formatting."""

from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """User creation request schema."""

    email: EmailStr
    username: str
    password: str = Field(..., min_length=8, max_length=72)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    username: str
    is_staff: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserAdminCreate(BaseModel):
    """User creation schema for admin management."""

    email: EmailStr
    username: str
    password: str = Field(..., min_length=8, max_length=72)
    is_staff: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update schema for admin management."""

    email: EmailStr | None = None
    username: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=72)
    is_staff: bool | None = None
    is_admin: bool | None = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login request schema."""

    username: str
    password: str


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    username: str
    user_role: Literal["admin", "staff", "user"]
