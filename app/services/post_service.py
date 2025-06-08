# app/services/post_service.py

from fastapi import HTTPException, status
from typing import List

from app.repositories.post_repo import PostRepo
from app.schemas.post import PostCreate, PostRead

class PostService:
    """
    Service layer for post-related business logic.
    
    This service handles post creation, retrieval, and deletion operations.
    It coordinates between the in-memory repository and API endpoints,
    implementing business rules and error handling.
    
    Note:
        This service uses an in-memory repository implementation.
        No database session is required for the current implementation.
    """

    def __init__(self):
        """
        Initialize the post service.
        
        Note:
            No session parameter needed for in-memory repository,
            but the constructor is kept for consistency with other services.
        """
        pass

    async def add_post(self, user_id: int, post_in: PostCreate) -> PostRead:
        """
        Create a new post for a specific user.
        
        Args:
            user_id (int): ID of the user creating the post
            post_in (PostCreate): Post creation data containing text content
            
        Returns:
            PostRead: Created post with assigned ID and timestamp
        """
        # Repository assigns ID and timestamp automatically
        post_dict = PostRepo.add_post(user_id, post_in.text)
        return PostRead(**post_dict)

    async def get_posts(self, user_id: int) -> List[PostRead]:
        """
        Retrieve all posts for a specific user.
        
        Args:
            user_id (int): ID of the user whose posts to retrieve
            
        Returns:
            List[PostRead]: List of posts belonging to the user
        """
        posts = PostRepo.get_posts(user_id)
        return [PostRead(**p) for p in posts]

    async def delete_post(self, user_id: int, post_id: int) -> None:
        """
        Delete a specific post for a user.
        
        Args:
            user_id (int): ID of the user who owns the post
            post_id (int): ID of the post to delete
            
        Raises:
            HTTPException: 404 if post is not found
        """
        deleted = PostRepo.delete_post(user_id, post_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post {post_id} not found"
            )