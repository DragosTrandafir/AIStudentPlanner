import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Read connection components from env, provide sensible defaults.
# Example Postgres URL: postgresql+psycopg://user:password@localhost:5432/ai_student_planner
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Fallback to a local SQLite file for development if Postgres is not set yet
    f"sqlite+pysqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai_student_planner.db'))}"
)

# echo can be toggled via env to print SQL for debugging
SQL_ECHO = os.getenv("SQL_ECHO", "0") in ("1", "true", "True")

engine = create_engine(DATABASE_URL, echo=SQL_ECHO, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True, expire_on_commit=False)

Base = declarative_base()


@contextmanager
def get_session() -> Iterator[Session]:
    """Context-managed session factory.
    Usage:
        with get_session() as session:
            ...
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
