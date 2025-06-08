# app/core/security.py

from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings

# Password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration from settings
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_alg
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt algorithm.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password suitable for database storage
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token with user identifier as subject.
    
    Args:
        subject (str | int): User identifier to embed in token (usually user_id)
        expires_delta (Optional[timedelta]): Custom expiration time, defaults to settings value
        
    Returns:
        str: Encoded JWT token string
    """
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    
    Args:
        token (str): JWT token string to decode
        
    Returns:
        dict: Decoded token payload containing user information
        
    Raises:
        JWTError: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e