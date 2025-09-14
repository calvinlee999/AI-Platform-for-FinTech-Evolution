from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import structlog

logger = structlog.get_logger()
router = APIRouter()

class RiskAssessmentRequest(BaseModel):
    customer_id: str
    assessment_type: str  # 'credit', 'operational', 'market', 'liquidity'
    loan_amount: Optional[float] = None
    annual_income: Optional[float] = None
    credit_history_length: Optional[int] = None
    employment_status: Optional[str] = None
    debt_to_income_ratio: Optional[float] = None

class RiskAssessmentResponse(BaseModel):
    customer_id: str
    assessment_type: str
    risk_score: float
    risk_category: str
    recommendation: str
    factors: dict
    timestamp: str

@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest):
    """Perform comprehensive risk assessment"""
    try:
        from services.ml_client import MLClient
        from datetime import datetime
        
        ml_client = MLClient()
        
        if request.assessment_type == "credit":
            # Prepare features for credit risk model
            features = {
                "annual_income": request.annual_income or 50000,
                "credit_history_length": request.credit_history_length or 5,
                "current_debt": (request.debt_to_income_ratio or 0.3) * (request.annual_income or 50000),
                "employment_status": request.employment_status or "EMPLOYED",
                "age": 35,  # Default age
                "loan_amount": request.loan_amount or 25000,
                "loan_purpose": "PERSONAL"
            }
            
            # Call ML service for prediction
            prediction = await ml_client.predict_credit_risk(request.customer_id, features)
            
            risk_score = prediction.get("prediction", {}).get("risk_score", 50)
            risk_category = prediction.get("prediction", {}).get("risk_category", "MEDIUM")
            approval_recommendation = prediction.get("prediction", {}).get("approval_recommendation", False)
            
            recommendation = "APPROVE" if approval_recommendation else "DECLINE"
            
            factors = {
                "income_adequacy": "GOOD" if request.annual_income and request.annual_income > 40000 else "POOR",
                "debt_burden": "LOW" if request.debt_to_income_ratio and request.debt_to_income_ratio < 0.4 else "HIGH",
                "credit_experience": "GOOD" if request.credit_history_length and request.credit_history_length > 3 else "LIMITED"
            }
            
        else:
            # Default risk assessment for other types
            risk_score = 45.0
            risk_category = "MEDIUM"
            recommendation = "MONITOR"
            factors = {"assessment": "DEFAULT"}
        
        logger.info("Risk assessment completed", 
                   customer_id=request.customer_id, 
                   risk_score=risk_score,
                   risk_category=risk_category)
        
        return RiskAssessmentResponse(
            customer_id=request.customer_id,
            assessment_type=request.assessment_type,
            risk_score=risk_score,
            risk_category=risk_category,
            recommendation=recommendation,
            factors=factors,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error("Risk assessment failed", error=str(e), customer_id=request.customer_id)
        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(e)}"
        )

@router.get("/customer/{customer_id}/profile")
async def get_risk_profile(customer_id: str):
    """Get risk profile for a customer"""
    # In a real implementation, this would fetch from database
    return {
        "customer_id": customer_id,
        "risk_profile": "MEDIUM",
        "last_assessment": "2024-01-15T10:30:00Z",
        "factors": {
            "credit_score": 720,
            "payment_history": "GOOD",
            "account_stability": "HIGH"
        }
    }