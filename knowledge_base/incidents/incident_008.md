# Incident 008: Slow Query On Incident Dashboard

Date: 2026-05-17  
Service: api  
Severity: medium

## Summary
The incident dashboard became slow while service APIs remained mostly healthy. Database connections were available, but a status filter query scanned the full incidents table.

## Signals
- `api.dashboard.p95` exceeded 3s.
- Slow query logs showed `SELECT ... FROM incidents WHERE status`.
- Pool usage peaked at 62%, not exhausted.

## Cause
Missing index on incident status and timestamp after incident volume increased.

## Resolution
Added an index and changed dashboard query ordering.

## Retrieval Notes
Looks similar to pool exhaustion, but active connections were not saturated.
