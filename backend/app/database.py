"""
Database Connection Configuration
Secure connection to PostgreSQL with connection pooling
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Create engine with connection pooling for better performance
engine = create_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Ensures proper cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
