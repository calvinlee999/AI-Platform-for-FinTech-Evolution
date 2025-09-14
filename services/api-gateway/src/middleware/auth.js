const jwt = require('jsonwebtoken');
const redis = require('redis');
const logger = require('../utils/logger');

let redisClient;

// Initialize Redis client for token validation
if (process.env.REDIS_URL) {
  redisClient = redis.createClient({
    url: process.env.REDIS_URL
  });
  
  redisClient.on('error', (err) => {
    logger.error('Redis Client Error:', err);
  });
  
  redisClient.connect().catch(console.error);
}

/**
 * JWT Authentication Middleware
 * Validates JWT tokens and checks against Redis for revoked tokens
 */
const authMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Missing or invalid authorization header',
        correlationId: req.correlationId
      });
    }

    const token = authHeader.substring(7); // Remove 'Bearer ' prefix
    
    // Check if token is blacklisted (if Redis is available)
    if (redisClient) {
      try {
        const isBlacklisted = await redisClient.get(`blacklist:${token}`);
        if (isBlacklisted) {
          return res.status(401).json({
            error: 'Unauthorized',
            message: 'Token has been revoked',
            correlationId: req.correlationId
          });
        }
      } catch (redisError) {
        logger.warn('Redis check failed, proceeding without blacklist validation:', redisError);
      }
    }

    // Verify JWT token
    const jwtSecret = process.env.JWT_SECRET || 'fintech-platform-secret-key';
    const decoded = jwt.verify(token, jwtSecret);
    
    // Add user info to request
    req.user = {
      id: decoded.sub,
      email: decoded.email,
      role: decoded.role,
      permissions: decoded.permissions || [],
      customerId: decoded.customerId
    };

    // Log authentication success
    logger.info('Authentication successful', {
      userId: req.user.id,
      correlationId: req.correlationId,
      role: req.user.role
    });

    next();
  } catch (error) {
    logger.error('Authentication failed:', {
      error: error.message,
      correlationId: req.correlationId
    });

    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Token has expired',
        correlationId: req.correlationId
      });
    }

    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Invalid token',
        correlationId: req.correlationId
      });
    }

    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'Authentication service error',
      correlationId: req.correlationId
    });
  }
};

/**
 * Role-based authorization middleware
 */
const authorize = (requiredRoles = []) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'User not authenticated',
        correlationId: req.correlationId
      });
    }

    if (requiredRoles.length === 0) {
      return next(); // No specific role required
    }

    if (!requiredRoles.includes(req.user.role)) {
      logger.warn('Authorization failed - insufficient role:', {
        userId: req.user.id,
        userRole: req.user.role,
        requiredRoles,
        correlationId: req.correlationId
      });

      return res.status(403).json({
        error: 'Forbidden',
        message: 'Insufficient permissions',
        correlationId: req.correlationId
      });
    }

    next();
  };
};

/**
 * Permission-based authorization middleware
 */
const requirePermission = (requiredPermission) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'User not authenticated',
        correlationId: req.correlationId
      });
    }

    if (!req.user.permissions.includes(requiredPermission)) {
      logger.warn('Authorization failed - missing permission:', {
        userId: req.user.id,
        requiredPermission,
        userPermissions: req.user.permissions,
        correlationId: req.correlationId
      });

      return res.status(403).json({
        error: 'Forbidden',
        message: `Permission '${requiredPermission}' required`,
        correlationId: req.correlationId
      });
    }

    next();
  };
};

module.exports = {
  authMiddleware,
  authorize,
  requirePermission
};