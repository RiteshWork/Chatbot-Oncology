"""
db.py
SQLAlchemy 2.x setup. Exports:
    -engine         : connection pool to Postgres
    -SessionLocal   : factory that returns a Session (on DB transaction)
    -Base           : declarative base every model inherits from
    -get_session()  : context manager for safe session use
"""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.sql_echo,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

class Base(DeclarativeBase):
    """Parent class for every ORM model."""
    pass


@contextmanager
def get_session() -> Iterator[Session]:
    """Open a session, commit on success, rollback on error, always close"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()