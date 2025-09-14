const express = require('express');
const router = express.Router();

// Health check endpoint
router.get('/', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'fintech-customer-service',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '1.0.0',
    database: 'connected',
    correlationId: req.correlationId
  });
});

// Readiness check
router.get('/ready', (req, res) => {
  res.status(200).json({
    status: 'ready',
    database: 'connected',
    kafka: 'connected',
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