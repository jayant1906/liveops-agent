# Incident 002: Database Pool Exhaustion In API

Date: 2026-04-08  
Service: api  
Severity: high

## Summary
The API returned intermittent 500s and slow dashboard responses. All services showed some latency because API workers waited for PostgreSQL connections.

## Signals
- `db.pool.in_use` stayed at 100%.
- Logs showed `connection acquisition timeout`.
- Slow query count was low.

## Cause
A code path opened a transaction before calling downstream services and held the connection while waiting.

## Resolution
Restarted affected API workers and deployed a patch that opened transactions only around database writes.

## Retrieval Notes
Similar to slow query incidents, but the pool was exhausted even though queries were not slow.
