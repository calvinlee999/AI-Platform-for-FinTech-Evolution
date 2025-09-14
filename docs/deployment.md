# Deployment Guide

## Quick Start (Development)

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum
- 10GB free disk space

### 1. Clone and Start

```bash
git clone https://github.com/calvinlee999/AI-Platform-for-FinTech-Evolution.git
cd AI-Platform-for-FinTech-Evolution

# Start all services
docker compose up -d

# Check service health
docker compose ps
```

### 2. Verify Services

Wait for all services to be healthy (2-3 minutes), then test:

```bash
# API Gateway
curl http://localhost:8080/health

# Customer Service  
curl http://localhost:8081/health

# Risk Service
curl http://localhost:8082/health

# Payment Service
curl http://localhost:8083/health

# ML Service
curl http://localhost:8084/health

# Feature Store
curl http://localhost:8085/health
```

### 3. Access Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## Service Architecture

### Core Services

| Service | Port | Technology | Purpose |
|---------|------|------------|---------|
| API Gateway | 8080 | Node.js | Request routing, authentication |
| Customer Service | 8081 | Node.js | Customer management, KYC |
| Risk Service | 8082 | Python/FastAPI | Risk assessment, compliance |
| Payment Service | 8083 | Go | Payment processing |
| ML Service | 8084 | Python/FastAPI | AI/ML model serving |
| Feature Store | 8085 | Python/FastAPI | Feature management |

### Infrastructure Services

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Caching, sessions |
| Kafka | 9092 | Event streaming |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboards |

## API Examples

### 1. Customer Management

```bash
# Create customer
curl -X POST http://localhost:8080/api/customer/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "firstName": "John",
    "lastName": "Doe", 
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "dateOfBirth": "1990-01-01",
    "nationality": "US"
  }'

# Get customer
curl http://localhost:8080/api/customer/customers/{customer-id} \
  -H "Authorization: Bearer your-jwt-token"
```

### 2. Risk Assessment

```bash
# Assess credit risk
curl -X POST http://localhost:8080/api/risk/risk/assess \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "assessment_type": "credit",
    "annual_income": 75000,
    "loan_amount": 25000,
    "credit_history_length": 8,
    "employment_status": "EMPLOYED"
  }'
```

### 3. ML Predictions

```bash
# Credit risk prediction
curl -X POST http://localhost:8080/api/ml/predict/credit-risk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "annual_income": 75000,
    "credit_history_length": 8,
    "current_debt": 15000,
    "employment_status": "EMPLOYED",
    "age": 32,
    "loan_amount": 25000,
    "loan_purpose": "HOME_IMPROVEMENT"
  }'

# Fraud detection
curl -X POST http://localhost:8080/api/ml/predict/fraud-detection \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "transaction_id": "txn_123456789",
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "amount": 1500.00,
    "merchant_category": "GROCERY",
    "location": "NEW_YORK",
    "time_of_day": 14,
    "day_of_week": 3,
    "card_present": true,
    "previous_transactions_count": 25
  }'
```

### 4. Payment Processing

```bash
# Process payment
curl -X POST http://localhost:8080/api/payment/payments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "amount": 100.50,
    "currency": "USD",
    "method": "CARD",
    "reference": "INV-001"
  }'
```

## Production Deployment

### Kubernetes

```bash
# Create namespace
kubectl create namespace fintech-ai

# Deploy infrastructure
kubectl apply -f infrastructure/kubernetes/

# Deploy services
for service in services/*/k8s/; do
  kubectl apply -f $service
done

# Check deployment
kubectl get pods -n fintech-ai
```

### Environment Variables

Create `.env` files for each service:

```bash
# API Gateway
NODE_ENV=production
JWT_SECRET=your-strong-secret-key
REDIS_URL=redis://redis:6379

# Customer Service  
DATABASE_URL=postgresql://user:pass@postgres:5432/customer_db
KAFKA_BROKERS=kafka1:9092,kafka2:9092

# ML Service
MODEL_STORE_PATH=/app/models
FEATURE_STORE_URL=http://feature-store:8080
```

## Scaling Guidelines

### Horizontal Scaling

```yaml
# kubernetes/api-gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3  # Scale based on load
  template:
    spec:
      containers:
      - name: api-gateway
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi" 
            cpu: "500m"
```

### Database Scaling

```yaml
# PostgreSQL with read replicas
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster
spec:
  instances: 3
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
```

## Monitoring Setup

### Custom Dashboards

Import Grafana dashboards:

1. Go to http://localhost:3000
2. Login with admin/admin
3. Import dashboard JSON from `monitoring/dashboards/`

### Alerts

Configure Prometheus alerts in `monitoring/alerts.yml`:

```yaml
groups:
- name: fintech-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    annotations:
      summary: "High error rate detected"
```

## Security Hardening

### Production Security Checklist

- [ ] Use strong JWT secrets
- [ ] Enable TLS/SSL certificates
- [ ] Configure network policies
- [ ] Set up secrets management
- [ ] Enable audit logging
- [ ] Configure backup strategies
- [ ] Set up monitoring alerts
- [ ] Implement access controls

### Network Policies

```yaml
# Allow only necessary traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
```

## Troubleshooting

### Common Issues

1. **Services not starting**: Check Docker logs
   ```bash
   docker compose logs service-name
   ```

2. **Database connection errors**: Verify PostgreSQL is ready
   ```bash
   docker compose exec postgres pg_isready
   ```

3. **Memory issues**: Increase Docker memory limit to 8GB+

4. **Port conflicts**: Stop other services using ports 8080-8085

### Health Checks

All services provide health endpoints:

```bash
# Check all service health
for port in 8080 8081 8082 8083 8084 8085; do
  echo "Port $port: $(curl -s http://localhost:$port/health | jq -r .status)"
done
```

### Performance Tuning

1. **Database**: Tune PostgreSQL settings in `postgresql.conf`
2. **Redis**: Configure memory policies
3. **Kafka**: Adjust partition and replication settings
4. **Node.js**: Set appropriate heap sizes

## Backup and Recovery

### Database Backup

```bash
# Automated backup script
docker compose exec postgres pg_dump -U postgres customer_db > backup_$(date +%Y%m%d).sql
```

### Service Data

```bash
# Backup service configurations
tar -czf config_backup_$(date +%Y%m%d).tar.gz services/*/config/
```

## Maintenance

### Regular Tasks

1. **Daily**: Check service health and logs
2. **Weekly**: Review monitoring metrics and alerts  
3. **Monthly**: Update dependencies and security patches
4. **Quarterly**: Performance review and capacity planning

### Updates

```bash
# Update services
docker compose pull
docker compose up -d --force-recreate

# Rolling update in Kubernetes
kubectl rollout restart deployment/api-gateway -n fintech-ai
```