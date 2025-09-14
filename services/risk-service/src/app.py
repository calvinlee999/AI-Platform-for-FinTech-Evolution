import os
import httpx
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import structlog

from api.health import router as health_router
from api.risk_assessment import router as risk_router
from api.compliance import router as compliance_router
from services.ml_client import MLClient
from utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Global services
ml_client = MLClient()

app = FastAPI(
    title="FinTech Risk & Compliance Service",
    description="Risk assessment and regulatory compliance service for FinTech platform",
    version="1.0.0"
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

# Dependency for authentication
async def get_current_user(credentials = Depends(security)):
    return {"user_id": "system", "role": "service"}

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(
    risk_router, 
    prefix="/risk", 
    tags=["risk-assessment"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    compliance_router, 
    prefix="/compliance", 
    tags=["compliance"],
    dependencies=[Depends(get_current_user)]
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Risk Service...")
    await ml_client.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Risk Service...")
    await ml_client.cleanup()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )