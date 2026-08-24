# Incident 006: Payment Client Config Regression

Date: 2026-05-03  
Service: payment-service  
Severity: high

## Summary
Checkout failures rose immediately after a payment-service deploy. Logs showed gateway timeout messages, but provider status was clean.

## Signals
- Errors began 4 minutes after deploy `payment-service:2026.05.03.2`.
- Timeout budget changed from 2500ms to 700ms.
- Retries increased queue depth.

## Cause
The new payment client config used a timeout lower than normal gateway p95.

## Resolution
Rolled back payment-service and drained the retry queue.

## Retrieval Notes
Similar to provider timeout incidents, but the deployment timestamp and changed timeout setting identify this as internal.
