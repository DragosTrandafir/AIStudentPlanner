from backend.config.database import Base, engine

# Import all models so that they are registered on the Base before create_all
from backend.domain.user import User  # noqa: F401
from backend.domain.subject import Subject  # noqa: F401
from backend.domain.plan import Plan
from backend.domain.ai_task import AITask  # noqa: F401
from backend.domain.feedback import Feedback  # noqa: F401


def create_all() -> None:
    """Create all database tables based on the SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all()
    print("Database tables created (or already exist).")
