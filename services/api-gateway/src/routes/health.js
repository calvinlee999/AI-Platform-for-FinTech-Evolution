const express = require('express');
const router = express.Router();

// Health check endpoint
router.get('/', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'fintech-api-gateway',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '1.0.0',
    uptime: process.uptime(),
    correlationId: req.correlationId
  });
});

// Readiness check
router.get('/ready', (req, res) => {
  // Check if all downstream services are available
  const services = [
    { name: 'customer-service', url: process.env.CUSTOMER_SERVICE_URL },
    { name: 'risk-service', url: process.env.RISK_SERVICE_URL },
    { name: 'payment-service', url: process.env.PAYMENT_SERVICE_URL },
    { name: 'ml-service', url: process.env.ML_SERVICE_URL },
    { name: 'feature-store', url: process.env.FEATURE_STORE_URL }
  ];

  res.status(200).json({
    status: 'ready',
    services: services.map(service => ({
      name: service.name,
      configured: !!service.url
    })),
    correlationId: req.correlationId
  });
});

// Liveness check
router.get('/live', (req, res) => {
  res.status(200).json({
    status: 'alive',
    timestamp: new Date().toISOString(),
    correlationId: req.correlationId
  });
});

module.exports = router;