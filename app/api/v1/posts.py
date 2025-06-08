# app/api/v1/posts.py

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from app.schemas.post import PostCreate, PostRead
from app.services.post_service import PostService
from app.deps.auth import get_current_user
from app.deps.size_limit import size_limit_1mb
from app.schemas.user import UserRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(size_limit_1mb)]
)
async def add_post(
    post_in: PostCreate,
    current_user: UserRead = Depends(get_current_user)
):
    """
    Create a new post for the authenticated user.
    
    Creates a new post with the provided text content and associates it
    with the currently authenticated user. The request body size is limited
    to 1MB to prevent abuse.
    
    Args:
        post_in (PostCreate): Post creation data containing text content
        current_user (UserRead): Currently authenticated user from JWT token
        
    Returns:
        PostRead: Created post with assigned ID and timestamp
        
    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 413 if request body exceeds 1MB limit
        HTTPException: 422 if validation fails (empty text)
    """
    service = PostService()
    return await service.add_post(current_user.id, post_in)

@router.get(
    "/",
    response_model=List[PostRead],
    dependencies=[Depends(size_limit_1mb)]
)
@cache(expire=300)  # Cache for 5 minutes
async def get_posts(
    current_user: UserRead = Depends(get_current_user)
):
    """
    Retrieve all posts for the authenticated user.
    
    Returns a list of all posts created by the currently authenticated user.
    Results are cached for 5 minutes to improve performance.
    
    Args:
        current_user (UserRead): Currently authenticated user from JWT token
        
    Returns:
        List[PostRead]: List of posts belonging to the authenticated user
        
    Raises:
        HTTPException: 401 if user is not authenticated
        
    Note:
        Results are cached for 5 minutes. New posts may not appear immediately
        in the list due to caching.
    """
    service = PostService()
    return await service.get_posts(current_user.id)

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: int,
    current_user: UserRead = Depends(get_current_user)
):
    """
    Delete a specific post owned by the authenticated user.
    
    Removes the specified post from the user's posts. Only the owner
    of the post can delete it.
    
    Args:
        post_id (int): ID of the post to delete
        current_user (UserRead): Currently authenticated user from JWT token
        
    Returns:
        None: Empty response with 204 status code on successful deletion
        
    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 404 if post is not found or doesn't belong to user
    """
    service = PostService()
    await service.delete_post(current_user.id, post_id)