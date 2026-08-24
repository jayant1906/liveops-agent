# Incident 013: Database Lock From Backfill

Date: 2026-06-22  
Service: api  
Severity: high

## Summary
Telemetry writes slowed and incident creation lagged. Database pool was not exhausted, but writes waited behind a backfill transaction.

## Signals
- Lock wait time increased.
- Active connections stayed moderate.
- A maintenance event started 12 minutes before the alert.

## Cause
A backfill updated incidents in one large transaction and blocked newer writes.

## Resolution
Canceled the backfill and reran it in small batches.

## Retrieval Notes
Similar to slow query and pool exhaustion symptoms, but lock waits and maintenance event point to transaction blocking.
