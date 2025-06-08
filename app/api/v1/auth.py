# app/api/v1/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.schemas.user import UserCreate, Token
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token, status_code=201)
async def signup(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    Creates a new user account with the provided email and password.
    Returns a JWT access token for immediate authentication.
    
    Args:
        user_in (UserCreate): User registration data containing email and password
        session (AsyncSession): Database session dependency
        
    Returns:
        Token: JWT access token for the newly registered user
        
    Raises:
        HTTPException: 400 if email is already registered
        HTTPException: 422 if validation fails (invalid email format, weak password)
    """
    service = UserService(session)
    return await service.register(user_in)

@router.post("/login", response_model=Token)
async def login(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and provide access token.
    
    Validates user credentials (email and password) and returns a JWT token
    if authentication is successful.
    
    Args:
        user_in (UserCreate): User login data containing email and password
        session (AsyncSession): Database session dependency
        
    Returns:
        Token: JWT access token for authenticated user
        
    Raises:
        HTTPException: 401 if credentials are invalid
        HTTPException: 422 if validation fails (invalid email format)
    """
    service = UserService(session)
    return await service.authenticate(user_in)