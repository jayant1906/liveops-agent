# Incident 012: Dependency Circuit Breaker Too Sensitive

Date: 2026-06-15  
Service: order-service  
Severity: medium

## Summary
Order-service rejected valid checkout attempts because the payment circuit breaker opened during a brief provider blip and stayed open too long.

## Signals
- Payment gateway recovered within 3 minutes.
- Order-service continued returning fallback errors for 21 minutes.
- Circuit breaker logs showed an elevated cool-down interval.

## Cause
A config change increased circuit breaker cool-down to 30 minutes.

## Resolution
Restored cool-down to 2 minutes and manually half-opened the breaker.

## Retrieval Notes
Similar to provider outages, but failure continued after provider recovery.
