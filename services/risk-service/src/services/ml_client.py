import os
import httpx
import structlog

logger = structlog.get_logger()

class MLClient:
    """Client for communicating with ML Service"""
    
    def __init__(self):
        self.base_url = os.getenv("ML_MODEL_ENDPOINT", "http://ml-service:8080")
        self.client = None
        
    async def initialize(self):
        """Initialize HTTP client"""
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info("ML Client initialized", base_url=self.base_url)
        
    async def cleanup(self):
        """Cleanup HTTP client"""
        if self.client:
            await self.client.aclose()
            
    async def predict_credit_risk(self, customer_id: str, features: dict):
        """Get credit risk prediction from ML service"""
        try:
            if not self.client:
                await self.initialize()
                
            payload = {
                "customer_id": customer_id,
                "annual_income": features.get("annual_income"),
                "credit_history_length": features.get("credit_history_length"),
                "current_debt": features.get("current_debt"),
                "employment_status": features.get("employment_status"),
                "age": features.get("age"),
                "loan_amount": features.get("loan_amount"),
                "loan_purpose": features.get("loan_purpose")
            }
            
            response = await self.client.post(
                f"{self.base_url}/predict/credit-risk",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("Credit risk prediction received", customer_id=customer_id)
                return result
            else:
                logger.error("ML service request failed", 
                           status_code=response.status_code,
                           response=response.text)
                # Return default values if ML service is unavailable
                return {
                    "prediction": {
                        "risk_score": 50.0,
                        "risk_category": "MEDIUM",
                        "approval_recommendation": False
                    },
                    "confidence": 0.5
                }
                
        except Exception as e:
            logger.error("Error calling ML service", error=str(e))
            # Return safe defaults
            return {
                "prediction": {
                    "risk_score": 75.0,  # Conservative default
                    "risk_category": "HIGH",
                    "approval_recommendation": False
                },
                "confidence": 0.0
            }
            
    async def predict_fraud(self, transaction_data: dict):
        """Get fraud prediction from ML service"""
        try:
            if not self.client:
                await self.initialize()
                
            response = await self.client.post(
                f"{self.base_url}/predict/fraud-detection",
                json=transaction_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error("Fraud prediction failed", status_code=response.status_code)
                return {
                    "prediction": {
                        "is_fraud": False,
                        "fraud_probability": 0.1,
                        "risk_level": "LOW"
                    },
                    "confidence": 0.5
                }
                
        except Exception as e:
            logger.error("Error in fraud prediction", error=str(e))
            return {
                "prediction": {
                    "is_fraud": True,  # Conservative default
                    "fraud_probability": 0.8,
                    "risk_level": "HIGH"
                },
                "confidence": 0.0
            }