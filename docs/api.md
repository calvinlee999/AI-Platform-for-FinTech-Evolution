# API Documentation

## Overview

The FinTech AI Platform provides a comprehensive set of REST APIs for banking and financial services operations. All APIs follow RESTful principles and return JSON responses.

## Base URLs

- **Development**: `http://localhost:8080`
- **Production**: `https://api.fintech-platform.com`

## Authentication

All API endpoints (except health checks) require JWT authentication.

```bash
# Get token (implementation-specific)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use token in requests
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8080/api/customer/customers
```

## API Gateway Routes

All requests go through the API Gateway at port 8080:

| Route Pattern | Target Service | Purpose |
|---------------|----------------|---------|
| `/api/customer/*` | Customer Service | Customer management |
| `/api/risk/*` | Risk Service | Risk assessment |
| `/api/payment/*` | Payment Service | Payment processing |
| `/api/ml/*` | ML Service | AI/ML predictions |
| `/api/features/*` | Feature Store | Feature management |

## Customer Management API

### Create Customer

```http
POST /api/customer/customers
Authorization: Bearer {token}
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "middleName": "Michael",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "dateOfBirth": "1990-01-01",
  "gender": "M",
  "nationality": "US",
  "occupation": "Software Engineer",
  "annualIncome": 75000
}
```

**Response:**
```json
{
  "customer": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "customerNumber": "CUST-1640995200000-ABC123",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "status": "ACTIVE",
    "onboardingDate": "2024-01-15T10:30:00Z"
  },
  "correlationId": "customer-1640995200-xyz789"
}
```

### Get Customer

```http
GET /api/customer/customers/{customer-id}
Authorization: Bearer {token}
```

### Update Customer

```http
PUT /api/customer/customers/{customer-id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "phone": "+1234567891",
  "annualIncome": 80000
}
```

### List Customers

```http
GET /api/customer/customers?page=1&limit=10
Authorization: Bearer {token}
```

## KYC Management API

### Submit KYC Information

```http
POST /api/customer/kyc/customer/{customer-id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "identificationNumber": "123456789",
  "identificationType": "PASSPORT",
  "issuingCountry": "US",
  "expiryDate": "2030-12-31",
  "sourceOfFunds": "EMPLOYMENT",
  "purposeOfRelationship": "BANKING_SERVICES"
}
```

### Get KYC Status

```http
GET /api/customer/kyc/customer/{customer-id}
Authorization: Bearer {token}
```

### Update KYC Status

```http
PATCH /api/customer/kyc/{kyc-id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "APPROVED",
  "approvedBy": "compliance-officer-001"
}
```

## Risk Assessment API

### Assess Credit Risk

```http
POST /api/risk/risk/assess
Authorization: Bearer {token}
Content-Type: application/json

{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "assessment_type": "credit",
  "loan_amount": 25000,
  "annual_income": 75000,
  "credit_history_length": 8,
  "employment_status": "EMPLOYED",
  "debt_to_income_ratio": 0.3
}
```

**Response:**
```json
{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "assessment_type": "credit",
  "risk_score": 45.2,
  "risk_category": "MEDIUM",
  "recommendation": "APPROVE",
  "factors": {
    "income_adequacy": "GOOD",
    "debt_burden": "LOW",
    "credit_experience": "GOOD"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Risk Profile

```http
GET /api/risk/risk/customer/{customer-id}/profile
Authorization: Bearer {token}
```

## Compliance API

### Perform Compliance Check

```http
POST /api/risk/compliance/check?customer_id={customer-id}
Authorization: Bearer {token}
Content-Type: application/json

["kyc", "aml", "sanctions"]
```

**Response:**
```json
{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "overall_status": "PASSED",
  "checks": [
    {
      "customer_id": "123e4567-e89b-12d3-a456-426614174000",
      "check_type": "kyc",
      "status": "PASSED",
      "details": {
        "identity_verified": true,
        "address_verified": true,
        "documents_complete": true
      }
    }
  ],
  "risk_level": "LOW",
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### Get Compliance Report

```http
GET /api/risk/compliance/report/{customer-id}
Authorization: Bearer {token}
```

## ML Service API

### Credit Risk Prediction

```http
POST /api/ml/predict/credit-risk
Authorization: Bearer {token}
Content-Type: application/json

{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "annual_income": 75000,
  "credit_history_length": 8,
  "current_debt": 22500,
  "employment_status": "EMPLOYED",
  "age": 32,
  "loan_amount": 25000,
  "loan_purpose": "HOME_IMPROVEMENT"
}
```

**Response:**
```json
{
  "model_name": "credit_risk",
  "prediction": {
    "risk_score": 42.5,
    "risk_category": "MEDIUM",
    "approval_recommendation": true
  },
  "confidence": 0.87,
  "timestamp": "2024-01-15T10:30:00Z",
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "correlation_id": "credit-1640995200.123"
}
```

### Fraud Detection

```http
POST /api/ml/predict/fraud-detection
Authorization: Bearer {token}
Content-Type: application/json

{
  "transaction_id": "txn_123456789",
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "amount": 1500.00,
  "merchant_category": "GROCERY",
  "location": "NEW_YORK",
  "time_of_day": 14,
  "day_of_week": 3,
  "card_present": true,
  "previous_transactions_count": 25
}
```

### List Models

```http
GET /api/ml/models
Authorization: Bearer {token}
```

### Get Model Info

```http
GET /api/ml/models/{model-name}
Authorization: Bearer {token}
```

## Payment Service API

### Process Payment

```http
POST /api/payment/payments
Authorization: Bearer {token}
Content-Type: application/json

{
  "customer_id": "123e4567-e89b-12d3-a456-426614174000",
  "amount": 100.50,
  "currency": "USD",
  "method": "CARD",
  "reference": "INV-001"
}
```

**Response:**
```json
{
  "payment_id": "pay_1640995200",
  "status": "completed",
  "amount": 100.50,
  "currency": "USD",
  "processed_at": "2024-01-15T10:30:00Z"
}
```

## Feature Store API

### Store Features

```http
POST /api/features/{feature-group}/{entity-id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "annual_income": 75000,
  "credit_score": 720,
  "account_age_days": 1825,
  "transaction_count_30d": 45
}
```

### Get Features

```http
GET /api/features/{feature-group}/{entity-id}
Authorization: Bearer {token}
```

### List Feature Groups

```http
GET /api/features/feature-groups
Authorization: Bearer {token}
```

## Health Check Endpoints

All services provide health check endpoints:

```http
GET /health
GET /health/ready  
GET /health/live
```

## Error Responses

All APIs return consistent error responses:

```json
{
  "error": "Bad Request",
  "message": "Validation failed for field 'email'",
  "details": {
    "field": "email",
    "code": "INVALID_FORMAT"
  },
  "correlationId": "req-1640995200-abc123",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

API requests are rate limited:

- **Development**: 100 requests per 15 minutes per IP
- **Production**: 1000 requests per 15 minutes per authenticated user

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995800
```

## Pagination

List endpoints support pagination:

```http
GET /api/customer/customers?page=2&limit=20&sort=createdAt&order=desc
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "hasNext": true,
    "hasPrev": true
  }
}
```

## Correlation IDs

All requests include correlation IDs for tracing:

- Automatically generated if not provided
- Include in requests: `X-Correlation-ID: your-id`
- Returned in all responses for debugging

## Webhooks

Configure webhooks for real-time notifications:

```http
POST /api/webhooks
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/fintech",
  "events": ["customer.created", "payment.completed", "kyc.approved"],
  "secret": "webhook-secret-key"
}
```

## SDK Examples

### JavaScript/Node.js

```javascript
const fintechApi = new FintechApiClient({
  baseUrl: 'http://localhost:8080',
  token: 'your-jwt-token'
});

// Create customer
const customer = await fintechApi.customers.create({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com'
});

// Assess risk
const riskAssessment = await fintechApi.risk.assess({
  customerId: customer.id,
  assessmentType: 'credit',
  loanAmount: 25000
});
```

### Python

```python
from fintech_api import FintechApiClient

client = FintechApiClient(
    base_url='http://localhost:8080',
    token='your-jwt-token'
)

# ML prediction
prediction = client.ml.predict_credit_risk(
    customer_id='123e4567-e89b-12d3-a456-426614174000',
    annual_income=75000,
    loan_amount=25000
)
```

## OpenAPI Specification

Full OpenAPI/Swagger specifications available at:
- `/api/customer/docs` - Customer Service
- `/api/risk/docs` - Risk Service  
- `/api/ml/docs` - ML Service