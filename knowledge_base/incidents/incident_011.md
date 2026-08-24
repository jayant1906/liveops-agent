# Incident 011: Duplicate Payment Attempts

Date: 2026-06-09  
Service: payment-service  
Severity: critical

## Summary
Payment retry fanout produced duplicate authorization attempts for a subset of checkouts. Customer charges were not captured twice, but duplicate auth alerts fired.

## Signals
- Idempotency conflict logs increased sharply.
- Gateway timeout rate was moderate, not severe.
- Retry count rose after a client library deploy.

## Cause
The retry wrapper regenerated idempotency keys after timeout.

## Resolution
Rolled back the client library and paused automatic retries for affected requests.

## Retrieval Notes
Similar to gateway timeout incidents, but idempotency conflict messages are the deciding clue.
