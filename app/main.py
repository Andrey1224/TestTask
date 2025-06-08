from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.deps.db import get_db
from app.api.v1.auth import router as auth_router
from app.api.v1.posts import router as posts_router
from app.core.cache import init_cache

app = FastAPI(
    title="FastAPI Blog API",
    version="1.0.0",
    description="A blog API with JWT authentication and post management",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Connect routers
app.include_router(auth_router)
app.include_router(posts_router)

@app.on_event("startup")
async def startup():
    """
    Application startup event handler.
    
    Initializes cache and performs any necessary startup operations.
    This function is called when the application starts up.
    """
    await init_cache()

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic API information.
    
    Returns:
        dict: API name and version information
    """
    return {"message": "FastAPI Blog API", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check(session: AsyncSession = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.
    
    Args:
        session (AsyncSession): Database session dependency
        
    Returns:
        dict: Health status and database connection status
        
    Raises:
        HTTPException: 500 if database connection fails
    """
    try:
        result = await session.execute(text("SELECT 1"))
        scalar = result.scalar_one()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")