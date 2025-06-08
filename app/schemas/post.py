# app/schemas/post.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated

class PostCreate(BaseModel):
    """
    Schema for creating a new post.
    
    This schema validates input data when users create new posts,
    ensuring text content meets minimum requirements.
    
    Attributes:
        text (str): Post content with minimum 1 character requirement
    """
    text: Annotated[str, Field(
        min_length=1, 
        description="Post text content (minimum 1 character)"
    )]

class PostRead(BaseModel):
    """
    Schema for post data output in API responses.
    
    This schema represents post information returned by the API,
    including metadata like creation timestamp and unique identifier.
    
    Attributes:
        id (int): Unique post identifier assigned by the system
        text (str): Post content text
        created_at (datetime): Timestamp when the post was created
    """
    id: int = Field(..., description="Unique post identifier")
    text: str = Field(..., description="Post content text")
    created_at: datetime = Field(..., description="Post creation timestamp")

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True  # Updated from orm_mode for Pydantic v2