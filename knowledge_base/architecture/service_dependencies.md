# Service Dependencies

## Dependency Map
- Frontend depends on FastAPI API endpoints.
- API depends on PostgreSQL for telemetry and incident state.
- Order service depends on user service for account state and payment service for checkout.
- Payment service depends on the external payment gateway and database idempotency records.
- Agent depends on telemetry repositories, remediation actions, verification checks, and retrieved knowledge base chunks.

## Critical Paths
Checkout is the most sensitive path. A normal request touches order service, user service, payment service, PostgreSQL, and the payment gateway. A failure in any part can appear as checkout latency or payment errors, so investigation must look at dependency health before selecting remediation.

## Common Correlations
- Payment gateway timeout: payment-service timeout logs, elevated dependency timeout rate, normal database pool usage.
- Database pool exhaustion: API and service latency rise together, connection acquisition errors, normal external gateway health.
- Bad deployment: errors begin within minutes of a deployment event and often affect one service or endpoint first.
- Memory leak: gradual memory climb followed by latency and restarts, often without a deployment exactly at onset.

## Blast Radius
User service degradation can cause login and checkout failures. Payment service degradation can leave orders pending or rejected. Database degradation affects all services and should be treated as broad blast radius even if the first alert names one service.
