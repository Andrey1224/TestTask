# app/repositories/user_repo.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepo:
    """
    Repository class for user database operations.
    
    This class provides static methods for common user database operations
    including creation, retrieval by email and ID. All methods are asynchronous
    and work with SQLAlchemy's async session.
    """

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            session (AsyncSession): Database session for executing queries
            email (str): Email address to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their unique identifier.
        
        Args:
            session (AsyncSession): Database session for executing queries
            user_id (int): User ID to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        session: AsyncSession, user_in: UserCreate, password_hash: str
    ) -> User:
        """
        Create a new user in the database.
        
        Args:
            session (AsyncSession): Database session for executing queries
            user_in (UserCreate): User creation data containing email and password
            password_hash (str): Pre-hashed password for secure storage
            
        Returns:
            User: Newly created user object with assigned ID
            
        Note:
            This method commits the transaction and refreshes the object
            to ensure the auto-generated ID is available.
        """
        user = User(email=user_in.email, password_hash=password_hash)
        session.add(user)
        await session.commit()
        await session.refresh(user)  # Retrieve the auto-generated ID
        return user