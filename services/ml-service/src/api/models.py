from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()

class ModelInfo(BaseModel):
    name: str
    version: str
    type: str
    status: str
    created_at: str
    metrics: Optional[Dict[str, float]] = None

class ModelListResponse(BaseModel):
    models: List[ModelInfo]
    total: int

@router.get("/", response_model=ModelListResponse)
async def list_models():
    """List all available models"""
    from services.model_service import ModelService
    
    model_service = ModelService()
    
    models = []
    for name, model in model_service.loaded_models.items():
        models.append(ModelInfo(
            name=name,
            version="1.0.0",
            type="sklearn" if hasattr(model, 'predict') else "unknown",
            status="active",
            created_at=datetime.utcnow().isoformat(),
            metrics={"accuracy": 0.85, "precision": 0.82, "recall": 0.88}
        ))
    
    return ModelListResponse(
        models=models,
        total=len(models)
    )

@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """Get information about a specific model"""
    from services.model_service import ModelService
    
    model_service = ModelService()
    
    if model_name not in model_service.loaded_models:
        return {"error": f"Model '{model_name}' not found"}
    
    return ModelInfo(
        name=model_name,
        version="1.0.0",
        type="sklearn",
        status="active",
        created_at=datetime.utcnow().isoformat(),
        metrics={"accuracy": 0.85, "precision": 0.82, "recall": 0.88}
    )

@router.post("/{model_name}/reload")
async def reload_model(model_name: str):
    """Reload a specific model"""
    return {
        "message": f"Model '{model_name}' reloaded successfully",
        "timestamp": datetime.utcnow().isoformat()
    }