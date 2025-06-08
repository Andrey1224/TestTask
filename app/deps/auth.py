# app/deps/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.deps.db import get_db
from app.repositories.user_repo import UserRepo
from app.schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> UserRead:
    """
    Extract and validate current user from JWT token.
    
    This dependency function decodes the JWT token, extracts the user ID
    from the 'sub' claim, and retrieves the corresponding user from the database.
    
    Args:
        token (str): JWT token from Authorization header
        session (AsyncSession): Database session dependency
        
    Returns:
        UserRead: Current authenticated user information
        
    Raises:
        HTTPException: 401 if token is invalid, expired, or user not found
    """
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserRepo.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserRead(id=user.id, email=user.email)