const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const logger = require('../utils/logger');

const router = express.Router();

// Service proxy configurations
const services = {
  customer: {
    target: process.env.CUSTOMER_SERVICE_URL || 'http://customer-service:8080',
    pathRewrite: { '^/api/customer': '' }
  },
  risk: {
    target: process.env.RISK_SERVICE_URL || 'http://risk-service:8080',
    pathRewrite: { '^/api/risk': '' }
  },
  payment: {
    target: process.env.PAYMENT_SERVICE_URL || 'http://payment-service:8080',
    pathRewrite: { '^/api/payment': '' }
  },
  ml: {
    target: process.env.ML_SERVICE_URL || 'http://ml-service:8080',
    pathRewrite: { '^/api/ml': '' }
  },
  features: {
    target: process.env.FEATURE_STORE_URL || 'http://feature-store:8080',
    pathRewrite: { '^/api/features': '' }
  }
};

// Create proxy middleware for each service
Object.keys(services).forEach(serviceName => {
  const serviceConfig = services[serviceName];
  
  const proxy = createProxyMiddleware({
    target: serviceConfig.target,
    changeOrigin: true,
    pathRewrite: serviceConfig.pathRewrite,
    timeout: 30000,
    proxyTimeout: 30000,
    onProxyReq: (proxyReq, req, res) => {
      // Add correlation ID to downstream requests
      proxyReq.setHeader('X-Correlation-ID', req.correlationId);
      proxyReq.setHeader('X-Forwarded-For', req.ip);
      proxyReq.setHeader('X-Gateway-Service', 'fintech-api-gateway');
      
      logger.info(`Proxying request to ${serviceName}: ${req.method} ${req.originalUrl}`, {
        correlationId: req.correlationId,
        service: serviceName,
        target: serviceConfig.target
      });
    },
    onProxyRes: (proxyRes, req, res) => {
      logger.info(`Response from ${serviceName}: ${proxyRes.statusCode}`, {
        correlationId: req.correlationId,
        service: serviceName,
        statusCode: proxyRes.statusCode
      });
    },
    onError: (err, req, res) => {
      logger.error(`Proxy error for ${serviceName}:`, {
        error: err.message,
        correlationId: req.correlationId,
        service: serviceName
      });
      
      res.status(503).json({
        error: 'Service Unavailable',
        message: `The ${serviceName} service is currently unavailable`,
        correlationId: req.correlationId
      });
    }
  });

  router.use(`/${serviceName}/*`, proxy);
});

// BIAN service domain mappings
router.use('/customer-management/*', createProxyMiddleware({
  target: services.customer.target,
  changeOrigin: true,
  pathRewrite: { '^/api/customer-management': '' }
}));

router.use('/risk-compliance/*', createProxyMiddleware({
  target: services.risk.target,
  changeOrigin: true,
  pathRewrite: { '^/api/risk-compliance': '' }
}));

router.use('/payment-processing/*', createProxyMiddleware({
  target: services.payment.target,
  changeOrigin: true,
  pathRewrite: { '^/api/payment-processing': '' }
}));

module.exports = router;