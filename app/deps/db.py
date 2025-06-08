# app/deps/db.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for FastAPI.
    
    Provides an async SQLAlchemy session for database operations.
    The session is automatically closed when the request completes,
    ensuring proper resource cleanup.
    
    Yields:
        AsyncSession: Database session for executing queries
        
    Note:
        This is a FastAPI dependency that should be used with Depends().
        The session is managed automatically - no manual closing required.
    """
    async with async_session() as session:
        yield session