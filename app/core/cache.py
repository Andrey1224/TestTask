# app/core/cache.py

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

async def init_cache():
    """
    Initialize in-memory cache for the application.
    
    Sets up FastAPI cache with in-memory backend for caching API responses.
    This function should be called during application startup.
    
    Note:
        In-memory cache is suitable for development and single-instance deployments.
        For production with multiple instances, consider using Redis backend.
    """
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")