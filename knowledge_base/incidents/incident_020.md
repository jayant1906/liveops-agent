# Incident 020: Payment Service Slow Database Writes

Date: 2026-08-10  
Service: payment-service  
Severity: high

## Summary
Payment authorization succeeded at the provider, but internal payment status writes were slow. Orders remained pending until writes completed.

## Signals
- Gateway success rate was normal.
- `payment.status_write.p95` exceeded 2s.
- Slow query logs showed missing index on idempotency lookup.

## Cause
The idempotency table grew and a lookup query lacked the expected composite index.

## Resolution
Added the missing index and replayed delayed status updates.

## Retrieval Notes
Similar to payment provider failures because orders stayed pending, but provider calls were healthy.
