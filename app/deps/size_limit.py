# app/deps/size_limit.py

from fastapi import Request, HTTPException
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE

async def size_limit_1mb(request: Request):
    """
    Dependency to limit request body size to 1MB (1,048,576 bytes).
    
    This dependency reads the entire request body and validates that
    its size doesn't exceed the 1MB limit. This helps prevent abuse
    and ensures reasonable resource usage.
    
    Args:
        request (Request): FastAPI request object containing the body
        
    Raises:
        HTTPException: 413 (Request Entity Too Large) if body exceeds 1MB
        
    Note:
        This dependency should be added to endpoints that accept user content
        to prevent oversized requests from consuming excessive server resources.
    """
    body = await request.body()
    if len(body) > 1_048_576:  # 1MB = 1,048,576 bytes
        raise HTTPException(
            status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Request body too large"
        )