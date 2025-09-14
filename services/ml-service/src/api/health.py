from fastapi import APIRouter
from pydantic import BaseModel
import platform
import os
from datetime import datetime

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    python_version: str
    environment: str
    models_loaded: int

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from services.model_service import ModelService
    
    model_service = ModelService()
    
    return HealthResponse(
        status="healthy",
        service="fintech-ml-service",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        python_version=platform.python_version(),
        environment=os.getenv("ENVIRONMENT", "development"),
        models_loaded=len(model_service.loaded_models)
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    from services.model_service import ModelService
    
    model_service = ModelService()
    
    # Check if critical models are loaded
    required_models = ["credit_risk", "fraud_detection"]
    loaded_models = list(model_service.loaded_models.keys())
    
    ready = all(model in loaded_models for model in required_models)
    
    return {
        "status": "ready" if ready else "not_ready",
        "required_models": required_models,
        "loaded_models": loaded_models,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/live")
async def liveness_check():
    """Liveness check endpoint"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }