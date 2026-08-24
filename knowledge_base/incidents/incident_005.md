# Incident 005: Payment Gateway Timeout Spike

Date: 2026-04-28  
Service: payment-service  
Severity: high

## Summary
Payment attempts failed with gateway timeout errors. Order-service reported downstream payment failures, but user-service and database metrics were healthy.

## Signals
- `payment.gateway.timeout_rate` reached 18%.
- `payment.error_rate` crossed the high severity threshold.
- Database pool usage stayed below 50%.

## Cause
The external payment gateway had elevated latency in one region.

## Resolution
Enabled payment degraded mode and reduced retry attempts from 3 to 1 until provider latency recovered.

## Retrieval Notes
Looks like payment deployment failure from the outside, but no deployment preceded the alert.
