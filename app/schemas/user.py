# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserCreate(BaseModel):
    """
    Schema for user registration input data.
    
    This schema validates user input during account creation,
    ensuring email format and password strength requirements.
    
    Attributes:
        email (EmailStr): Valid email address for user account
        password (str): Password with minimum 8 characters requirement
    """
    email: EmailStr = Field(..., description="Valid email address")
    password: Annotated[str, Field(
        min_length=8, 
        description="Password must be at least 8 characters long"
    )]

class UserRead(BaseModel):
    """
    Schema for user data output in API responses.
    
    This schema represents user information returned by the API,
    excluding sensitive data like passwords.
    
    Attributes:
        id (int): Unique user identifier
        email (EmailStr): User's email address
    """
    id: int = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User's email address")

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True  # Updated from orm_mode for Pydantic v2

class Token(BaseModel):
    """
    Schema for JWT token response.
    
    This schema represents the structure of authentication tokens
    returned after successful login or registration.
    
    Attributes:
        access_token (str): JWT access token string
        token_type (str): Type of token, defaults to "bearer"
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")