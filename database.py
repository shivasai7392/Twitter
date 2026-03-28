"""SQLAlchemy database engine, session, and dependency setup."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Shiv%407392@localhost:3306/twitter"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for dependency injection."""
    with SessionLocal() as db:
        yield db
