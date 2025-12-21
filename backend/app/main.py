"""
FastAPI Application Entry Point
Job Search API with security best practices
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.database import engine, Base
from app.routers import jobs
from app.schemas import HealthResponse

settings = get_settings()

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup: Create tables if they don't exist (for development)
    # In production, use migrations (Alembic)
    # Base.metadata.create_all(bind=engine)
    print("🚀 Job Search API starting up...")
    yield
    # Shutdown
    print("👋 Job Search API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Job Search API",
    description="API for searching job recruitment information from multiple sources",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET"],  # Read-only API
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors without exposing internal details."""
    import traceback
    # Log the actual error for debugging
    print(f"=" * 50)
    print(f"ERROR on {request.method} {request.url}")
    print(f"Exception: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    print(f"=" * 50)
    
    # In DEBUG mode, return detailed error
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), "type": type(exc).__name__}
        )
    
    # Return generic error to client in production
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and database connectivity."""
    from sqlalchemy import text
    from app.database import SessionLocal
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        version="1.0.0"
    )


# Include routers
app.include_router(jobs.router, prefix=settings.API_PREFIX)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Job Search API",
        "version": "1.0.0",
        "docs": "/api/docs" if settings.DEBUG else "Disabled in production",
        "health": "/health"
    }
