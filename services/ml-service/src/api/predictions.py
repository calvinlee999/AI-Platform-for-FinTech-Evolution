from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import structlog

from services.model_service import ModelService

logger = structlog.get_logger()
router = APIRouter()

class PredictionRequest(BaseModel):
    model_name: str
    features: Dict[str, Any]
    customer_id: Optional[str] = None

class PredictionResponse(BaseModel):
    model_name: str
    prediction: Any
    confidence: Optional[float] = None
    timestamp: str
    customer_id: Optional[str] = None
    correlation_id: str

class CreditRiskRequest(BaseModel):
    customer_id: str
    annual_income: float
    credit_history_length: int
    current_debt: float
    employment_status: str
    age: int
    loan_amount: float
    loan_purpose: str

class FraudDetectionRequest(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    merchant_category: str
    location: str
    time_of_day: int
    day_of_week: int
    card_present: bool
    previous_transactions_count: int

@router.post("/", response_model=PredictionResponse)
async def make_prediction(request: PredictionRequest):
    """Generic prediction endpoint"""
    try:
        model_service = ModelService()
        
        if request.model_name not in model_service.loaded_models:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model '{request.model_name}' not found"
            )
        
        result = await model_service.predict(
            model_name=request.model_name,
            features=request.features
        )
        
        logger.info(
            "Prediction made",
            model_name=request.model_name,
            customer_id=request.customer_id,
            prediction=result.get("prediction")
        )
        
        return PredictionResponse(
            model_name=request.model_name,
            prediction=result["prediction"],
            confidence=result.get("confidence"),
            timestamp=datetime.utcnow().isoformat(),
            customer_id=request.customer_id,
            correlation_id=f"pred-{datetime.now().timestamp()}"
        )
        
    except Exception as e:
        logger.error("Prediction failed", error=str(e), model_name=request.model_name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/credit-risk", response_model=PredictionResponse)
async def predict_credit_risk(request: CreditRiskRequest):
    """Credit risk assessment prediction"""
    try:
        features = {
            "annual_income": request.annual_income,
            "credit_history_length": request.credit_history_length,
            "current_debt": request.current_debt,
            "employment_status": request.employment_status,
            "age": request.age,
            "loan_amount": request.loan_amount,
            "loan_purpose": request.loan_purpose,
            "debt_to_income_ratio": request.current_debt / request.annual_income if request.annual_income > 0 else 0
        }
        
        model_service = ModelService()
        result = await model_service.predict("credit_risk", features)
        
        logger.info(
            "Credit risk prediction",
            customer_id=request.customer_id,
            risk_score=result.get("prediction"),
            loan_amount=request.loan_amount
        )
        
        return PredictionResponse(
            model_name="credit_risk",
            prediction=result["prediction"],
            confidence=result.get("confidence"),
            timestamp=datetime.utcnow().isoformat(),
            customer_id=request.customer_id,
            correlation_id=f"credit-{datetime.now().timestamp()}"
        )
        
    except Exception as e:
        logger.error("Credit risk prediction failed", error=str(e), customer_id=request.customer_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Credit risk prediction failed: {str(e)}"
        )

@router.post("/fraud-detection", response_model=PredictionResponse)
async def predict_fraud(request: FraudDetectionRequest):
    """Fraud detection prediction"""
    try:
        features = {
            "amount": request.amount,
            "merchant_category": request.merchant_category,
            "location": request.location,
            "time_of_day": request.time_of_day,
            "day_of_week": request.day_of_week,
            "card_present": request.card_present,
            "previous_transactions_count": request.previous_transactions_count
        }
        
        model_service = ModelService()
        result = await model_service.predict("fraud_detection", features)
        
        logger.info(
            "Fraud detection prediction",
            transaction_id=request.transaction_id,
            customer_id=request.customer_id,
            fraud_probability=result.get("prediction"),
            amount=request.amount
        )
        
        return PredictionResponse(
            model_name="fraud_detection",
            prediction=result["prediction"],
            confidence=result.get("confidence"),
            timestamp=datetime.utcnow().isoformat(),
            customer_id=request.customer_id,
            correlation_id=f"fraud-{datetime.now().timestamp()}"
        )
        
    except Exception as e:
        logger.error("Fraud detection failed", error=str(e), transaction_id=request.transaction_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fraud detection failed: {str(e)}"
        )