"""
app/routers/health.py
Health check and status endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.core.container import container

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "ok",
        "service": "ASTU Route AI",
        "version": "0.1.0"
    }


@router.get("/db")
async def check_database():
    """Check database connectivity"""
    try:
        db = container.get_database()
        is_healthy = db.test_connection()
        
        if is_healthy:
            return {"status": "ok", "database": "connected"}
        else:
            raise HTTPException(status_code=503, detail="Database connection failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database check failed: {str(e)}")


@router.get("/ai")
async def check_ai_service():
    """Check AI service configuration"""
    try:
        ai = container.get_ai_service()
        return {
            "status": "ok",
            "ai_model": ai.model,
            "embedding_model": ai.embedding_model
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service check failed: {str(e)}")


@router.get("/cache")
async def check_cache_service():
    """Check cache service status"""
    try:
        cache = container.get_cache_service()
        cache_type = type(cache).__name__
        return {
            "status": "ok",
            "cache_type": cache_type
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Cache check failed: {str(e)}")
