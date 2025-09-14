import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from typing import Dict, Any, List
import structlog

# Setup basic logging
import logging
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

app = FastAPI(
    title="FinTech Feature Store",
    description="Feature management and serving for ML models",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# In-memory feature store (for demo purposes)
feature_store = {
    "customer_features": {},
    "transaction_features": {},
    "risk_features": {}
}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "fintech-feature-store",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "features_count": sum(len(v) for v in feature_store.values())
    }

@app.get("/health/ready")
async def readiness_check():
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health/live")
async def liveness_check():
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}

@app.post("/features/{feature_group}/{entity_id}")
async def store_features(feature_group: str, entity_id: str, features: Dict[str, Any]):
    """Store features for an entity"""
    if feature_group not in feature_store:
        feature_store[feature_group] = {}
    
    feature_store[feature_group][entity_id] = {
        "features": features,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info("Features stored", feature_group=feature_group, entity_id=entity_id)
    
    return {
        "message": "Features stored successfully",
        "feature_group": feature_group,
        "entity_id": entity_id,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/features/{feature_group}/{entity_id}")
async def get_features(feature_group: str, entity_id: str):
    """Retrieve features for an entity"""
    if feature_group not in feature_store:
        raise HTTPException(status_code=404, detail="Feature group not found")
    
    if entity_id not in feature_store[feature_group]:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return feature_store[feature_group][entity_id]

@app.get("/features/{feature_group}")
async def list_entities(feature_group: str):
    """List all entities in a feature group"""
    if feature_group not in feature_store:
        raise HTTPException(status_code=404, detail="Feature group not found")
    
    return {
        "feature_group": feature_group,
        "entities": list(feature_store[feature_group].keys()),
        "count": len(feature_store[feature_group])
    }

@app.get("/feature-groups")
async def list_feature_groups():
    """List all feature groups"""
    return {
        "feature_groups": list(feature_store.keys()),
        "count": len(feature_store)
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level="info"
    )