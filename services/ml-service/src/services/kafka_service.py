import os
import asyncio
from kafka import KafkaProducer, KafkaConsumer
import json
import structlog

logger = structlog.get_logger()

class KafkaService:
    """Service for handling Kafka messaging"""
    
    def __init__(self):
        self.producer = None
        self.consumer = None
        self.brokers = os.getenv("KAFKA_BROKERS", "localhost:9092").split(",")
        
    async def initialize(self):
        """Initialize Kafka connections"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.brokers,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                retry_backoff_ms=1000,
                retries=3
            )
            
            logger.info("Kafka service initialized", brokers=self.brokers)
            
        except Exception as e:
            logger.warning("Kafka initialization failed, continuing without messaging", error=str(e))
            self.producer = None
    
    async def publish_prediction(self, model_name: str, prediction: dict, customer_id: str = None):
        """Publish prediction result to Kafka"""
        if not self.producer:
            logger.warning("Kafka producer not available, skipping event publication")
            return
            
        try:
            event = {
                "event_type": "prediction_made",
                "model_name": model_name,
                "prediction": prediction,
                "customer_id": customer_id,
                "timestamp": prediction.get("timestamp"),
                "service": "ml-service"
            }
            
            self.producer.send("ml.predictions", value=event)
            self.producer.flush()
            
            logger.info("Prediction event published", model_name=model_name, customer_id=customer_id)
            
        except Exception as e:
            logger.error("Failed to publish prediction event", error=str(e))
    
    async def shutdown(self):
        """Shutdown Kafka connections"""
        try:
            if self.producer:
                self.producer.close()
            if self.consumer:
                self.consumer.close()
            logger.info("Kafka service shutdown completed")
        except Exception as e:
            logger.error("Error during Kafka shutdown", error=str(e))