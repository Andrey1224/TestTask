# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_repo import UserRepo
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import (
    hash_password, verify_password,
    create_access_token
)

class UserService:
    """
    Service layer for user-related business logic.
    
    This service handles user registration, authentication, and related
    operations. It coordinates between the repository layer and API endpoints,
    implementing business rules and security measures.
    
    Attributes:
        session (AsyncSession): Database session for repository operations
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the user service with a database session.
        
        Args:
            session (AsyncSession): Database session for repository operations
        """
        self.session = session

    async def register(self, user_in: UserCreate) -> Token:
        """
        Register a new user account.
        
        This method creates a new user account if the email is not already
        registered, hashes the password securely, and returns a JWT token
        for immediate authentication.
        
        Args:
            user_in (UserCreate): User registration data containing email and password
            
        Returns:
            Token: JWT access token for the newly registered user
            
        Raises:
            HTTPException: 400 if email is already registered
        """
        existing = await UserRepo.get_by_email(self.session, user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        pwd_hash = hash_password(user_in.password)
        user = await UserRepo.create_user(
            self.session, user_in, pwd_hash
        )
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token)

    async def authenticate(self, user_in: UserCreate) -> Token:
        """
        Authenticate a user and provide access token.
        
        This method verifies user credentials (email and password) and
        returns a JWT token if authentication is successful.
        
        Args:
            user_in (UserCreate): User login data containing email and password
            
        Returns:
            Token: JWT access token for authenticated user
            
        Raises:
            HTTPException: 401 if credentials are invalid
        """
        user = await UserRepo.get_by_email(self.session, user_in.email)
        if not user or not verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        token = create_access_token(subject=user.id)
        return Token(access_token=token)