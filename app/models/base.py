# app/models/base.py

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create asynchronous database engine
engine = create_async_engine(
    settings.mysql_url,
    echo=True,                    # Enable SQL query logging for development
    future=True,                  # Use SQLAlchemy 2.0 style
)

# Configure session factory for database operations
# expire_on_commit=False prevents objects from being expired after commit
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all SQLAlchemy models
Base = declarative_base()