"""
main.py
ASTU Route AI FastAPI application entry point.

Clean architecture with:
- Dependency injection container
- Service layer abstraction
- Exception handling
- CORS and middleware setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from config import settings
from app.core.logging_config import logger, setup_logging
from app.core.exceptions import AstuRouteException
from app.core.container import container
from app.routers import health, query, route, nearby
import logging

# Setup logging
setup_logging("astu", logging.INFO if settings.is_production() else logging.DEBUG)

# Create FastAPI app
app = FastAPI(
    title="ASTU Route AI",
    description="AI-powered campus navigation and knowledge system for Adama Science and Technology University",
    version="0.1.0",
    docs_url="/api/docs" if settings.is_development() else None,
    redoc_url="/api/redoc" if settings.is_development() else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.is_development() else ["https://astu-route-ai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(AstuRouteException)
async def astu_exception_handler(request, exc: AstuRouteException):
    """Handle custom application exceptions"""
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.message,
            "code": exc.code,
            "path": str(request.url)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "code": "VALIDATION_ERROR",
            "details": str(exc)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR"
        }
    )


# Lifespan events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("=== ASTU Route AI Starting ===")
    logger.info(f"Environment: {settings.node_env}")
    logger.info(f"Server: {settings.host}:{settings.port}")
    
    # Initialize database
    try:
        db = container.get_database()
        if db.test_connection():
            logger.info("✓ Database connected")
        else:
            logger.warning("⚠ Database connection warning")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    # Initialize AI service
    try:
        ai = container.get_ai_service()
        logger.info(f"✓ AI service ready: {ai.model}")
    except Exception as e:
        logger.error(f"✗ AI service initialization failed: {e}")
    
    # Initialize cache
    try:
        cache = container.get_cache_service()
        logger.info(f"✓ Cache service ready: {type(cache).__name__}")
    except Exception as e:
        logger.error(f"✗ Cache service initialization failed: {e}")
    
    logger.info("=== Startup Complete ===\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down services...")
    await container.shutdown()
    logger.info("Shutdown complete")


# Include routers
from app.routers import health, query, route, nearby

app.include_router(health.router)
app.include_router(query.router)
app.include_router(route.router)
app.include_router(nearby.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info"""
    return {
        "name": "ASTU Route AI",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.is_development())
