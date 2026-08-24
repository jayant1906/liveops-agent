# Incident 015: Payment Provider 5xx With Healthy Latency

Date: 2026-07-04  
Service: payment-service  
Severity: high

## Summary
Payments failed quickly with provider 5xx responses. Latency stayed near baseline because failures returned immediately.

## Signals
- `payment.provider_5xx_rate` hit 12%.
- `payment.gateway.timeout_rate` stayed below 1%.
- No new payment-service deployment.

## Cause
Provider-side validation outage for card authorization.

## Resolution
Enabled alternate provider routing for eligible traffic and notified support.

## Retrieval Notes
Similar to gateway timeouts, but latency did not rise and 5xx rate was the primary signal.
