import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from prometheus_client import make_asgi_app
import structlog

from api.health import router as health_router
from api.models import router as models_router
from api.predictions import router as predictions_router
from services.model_service import ModelService
from services.kafka_service import KafkaService
from utils.logger import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger()

# Global services
model_service = ModelService()
kafka_service = KafkaService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting ML Service...")
    
    try:
        # Initialize services
        await model_service.initialize()
        await kafka_service.initialize()
        
        logger.info("ML Service startup completed successfully")
        yield
        
    except Exception as e:
        logger.error("Failed to start ML Service", error=str(e))
        raise
    finally:
        # Shutdown
        logger.info("Shutting down ML Service...")
        await kafka_service.shutdown()
        await model_service.cleanup()
        logger.info("ML Service shutdown completed")

# Create FastAPI app
app = FastAPI(
    title="FinTech AI/ML Service",
    description="AI/ML service for FinTech platform providing credit scoring, fraud detection, and customer analytics",
    version="1.0.0",
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,ml-service").split(",")
)

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token and extract user information"""
    # In production, validate JWT token here
    # For now, return a mock user
    return {"user_id": "system", "role": "service"}

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(
    models_router, 
    prefix="/models", 
    tags=["models"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    predictions_router, 
    prefix="/predict", 
    tags=["predictions"],
    dependencies=[Depends(get_current_user)]
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        reload=os.getenv("ENVIRONMENT") == "development"
    )