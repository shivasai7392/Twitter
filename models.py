from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    """SQLAlchemy model for user accounts."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    profile_picture: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )

    @property
    def image_path(self) -> str:
        """Return the path to the user's profile picture."""
        if self.profile_picture:
            return f"/media/profile_pics/{self.profile_picture}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    """SQLAlchemy model for blog posts."""

    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    author: Mapped[User] = relationship("User", back_populates="posts")
