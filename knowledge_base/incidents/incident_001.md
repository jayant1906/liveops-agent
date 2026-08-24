# Incident 001: Payment Service Deployment Error

Date: 2026-04-02  
Service: payment-service  
Severity: high

## Summary
Checkout failures increased after a payment-service release. The error affected card authorization requests but did not affect saved payment method reads.

## Signals
- `payment.error_rate` rose from 1% to 9%.
- Logs showed `missing provider_token`.
- The first error appeared 3 minutes after deployment.

## Cause
The deployment renamed an environment variable used by the gateway client.

## Resolution
Rolled back payment-service to the previous version and verified checkout success.

## Retrieval Notes
Similar to provider outage incidents, but rollback was correct because the provider was healthy and the failure matched deployment timing.
