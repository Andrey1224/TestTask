# app/repositories/post_repo.py

from threading import Lock
from datetime import datetime
from typing import Dict, List, Optional

# In-memory storage: user_id → list of posts
_posts: Dict[int, List[dict]] = {}
_lock = Lock()
_next_id = 1

class PostRepo:
    """
    In-memory repository for post storage and management.
    
    This repository provides thread-safe operations for storing posts in memory.
    Each post is represented as a dictionary with id, text, and created_at fields.
    Posts are organized by user_id for efficient user-specific operations.
    
    Note:
        This is an in-memory implementation suitable for development and testing.
        In production, this should be replaced with a proper database repository.
    """

    @staticmethod
    def add_post(user_id: int, text: str) -> dict:
        """
        Add a new post for a specific user.
        
        Args:
            user_id (int): ID of the user creating the post
            text (str): Content of the post
            
        Returns:
            dict: Created post with assigned ID and timestamp
            
        Note:
            This method is thread-safe and automatically assigns
            a unique incremental ID to each new post.
        """
        global _next_id

        with _lock:
            post_id = _next_id
            _next_id += 1
            post = {
                "id": post_id,
                "text": text,
                "created_at": datetime.utcnow()
            }
            _posts.setdefault(user_id, []).append(post)
            return post

    @staticmethod
    def get_posts(user_id: int) -> List[dict]:
        """
        Retrieve all posts for a specific user.
        
        Args:
            user_id (int): ID of the user whose posts to retrieve
            
        Returns:
            List[dict]: List of posts belonging to the user (copy of internal list)
        """
        return list(_posts.get(user_id, []))

    @staticmethod
    def delete_post(user_id: int, post_id: int) -> bool:
        """
        Delete a specific post for a user.
        
        Args:
            user_id (int): ID of the user who owns the post
            post_id (int): ID of the post to delete
            
        Returns:
            bool: True if post was found and deleted, False otherwise
        """
        user_posts = _posts.get(user_id, [])
        for idx, post in enumerate(user_posts):
            if post["id"] == post_id:
                user_posts.pop(idx)
                return True
        return False

    @staticmethod
    def clear_all() -> None:
        """
        Clear all posts from memory (useful for testing).
        
        This method removes all stored posts and resets the ID counter.
        Should only be used in testing scenarios.
        """
        global _posts, _next_id
        with _lock:
            _posts.clear()
            _next_id = 1