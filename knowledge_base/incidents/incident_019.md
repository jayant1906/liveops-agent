# Incident 019: Database Credential Rotation Failure

Date: 2026-08-03  
Service: api  
Severity: high

## Summary
After credential rotation, some API pods failed database authentication while older pods stayed healthy.

## Signals
- Logs showed `password authentication failed`.
- Errors affected only newly restarted pods.
- Database connection count dropped instead of rising.

## Cause
Secret rollout updated the database password but not every deployment environment variable.

## Resolution
Redeployed API pods with the corrected secret reference.

## Retrieval Notes
Different from pool exhaustion: connections failed at authentication rather than waiting for available pool slots.
