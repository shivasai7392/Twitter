"""Pydantic schemas for post validation and serialization."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base schema with common user fields."""

    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user API responses, includes id and created_at."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime | None = None


class PostBase(BaseModel):
    """Base schema with common post fields."""

    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    """Schema for creating a new post."""

    author_id: int  # TEMPORARY


class PostResponse(PostBase):
    """Schema for post API responses, includes id and date_posted."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    date_posted: datetime
    author: UserResponse
