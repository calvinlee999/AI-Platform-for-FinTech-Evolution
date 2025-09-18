# Real-Time Fraud Detection Sequence

This file contains the Mermaid sequence diagram for the Real-Time Fraud Detection flow. The diagram was moved here from the main README to isolate rendering and troubleshooting.

```mermaid
sequenceDiagram
    participant Customer as Customer
    participant POS as Point of Sale
    participant Gateway as Payment Gateway
    participant AuthSvc as Authorization Service
    participant AIRouter as AI Model Router
    participant Cache as Redis Cache
    participant FraudModel as Fraud Detection Model
    participant RiskEngine as Risk Engine
    participant CoreBanking as Core Banking
    participant Monitor as Monitoring

    Note over Customer,Monitor: Real-Time Fraud Detection (Target: < 100ms)
    
    Customer->>+POS: Swipe/Insert Card
    Note right of Customer: t=0ms - Transaction initiated
    
    POS->>+Gateway: Transaction Request
    Note right of POS: t=5ms - POS processing
    
    Gateway->>+AuthSvc: Authorization Request + Customer ID
    Note right of Gateway: t=10ms - Gateway routing
    
    alt Cache Hit (Fraud Pattern Exists)
        AuthSvc->>+Cache: Check fraud pattern cache
        Note right of AuthSvc: t=15ms - Cache lookup
        Cache-->>AuthSvc: Known fraud pattern
        Note right of Cache: t=20ms - Immediate response
        deactivate Cache
        AuthSvc->>+Monitor: Log fraud attempt
        Monitor-->>AuthSvc: Logged
        deactivate Monitor
        AuthSvc-->>Gateway: DECLINE (High Risk)
        deactivate AuthSvc
        Gateway-->>POS: Transaction Declined
        deactivate Gateway
        POS-->>Customer: Card Declined
        deactivate POS
        Note right of Customer: t=30ms TOTAL - Fast decline
    else Cache Miss (New Pattern)
        AuthSvc->>+Cache: Check fraud pattern cache
        Note right of AuthSvc: t=15ms - Cache lookup
        Cache-->>AuthSvc: No cached result
        Note right of Cache: t=20ms - Cache miss
        deactivate Cache
        
        AuthSvc->>+AIRouter: Real-time fraud analysis request
        Note right of AuthSvc: t=25ms - AI routing
        
        AIRouter->>+FraudModel: Analyze transaction pattern
        Note right of AIRouter: t=30ms - Model selection
        
        par Parallel Analysis
            FraudModel->>FraudModel: Pattern matching
            Note right of FraudModel: t=30-60ms - AI processing
        and
            AuthSvc->>+RiskEngine: Customer risk profile
            RiskEngine->>+CoreBanking: Account history
            CoreBanking-->>RiskEngine: Transaction history
            deactivate CoreBanking
            RiskEngine-->>AuthSvc: Risk score
            deactivate RiskEngine
        end
        
        FraudModel-->>AIRouter: Fraud probability score
        deactivate FraudModel
        Note right of FraudModel: t=65ms - AI result
        
        AIRouter-->>AuthSvc: Consolidated fraud assessment
        deactivate AIRouter
        Note right of AIRouter: t=70ms - Result consolidation
        
        alt Low Risk Score (< 0.3)
            AuthSvc->>+Cache: Cache approval pattern
            Cache-->>AuthSvc: Pattern cached
            deactivate Cache
            AuthSvc-->>Gateway: APPROVE
            deactivate AuthSvc
            Gateway-->>POS: Transaction Approved
            deactivate Gateway
            POS-->>Customer: Payment Successful
            deactivate POS
            Note right of Customer: t=85ms TOTAL - Fast approval
        else Medium Risk Score (0.3-0.7)
            AuthSvc->>+Monitor: Log suspicious activity
            Monitor-->>AuthSvc: Activity logged
            deactivate Monitor
            AuthSvc-->>Gateway: APPROVE with monitoring
            deactivate AuthSvc
            Gateway-->>POS: Transaction Approved
            deactivate Gateway
            POS-->>Customer: Payment Successful
            deactivate POS
            Note right of Customer: t=95ms TOTAL - Monitored approval
        else High Risk Score (> 0.7)
            AuthSvc->>+Cache: Cache decline pattern
            Cache-->>AuthSvc: Pattern cached
            deactivate Cache
            AuthSvc->>+Monitor: Log fraud attempt
            Monitor-->>AuthSvc: Fraud logged
            deactivate Monitor
            AuthSvc-->>Gateway: DECLINE (AI Detected Risk)
            deactivate AuthSvc
            Gateway-->>POS: Transaction Declined
            deactivate Gateway
            POS-->>Customer: Transaction Declined
            deactivate POS
            Note right of Customer: t=100ms TOTAL - AI-based decline
        end
    end
```
