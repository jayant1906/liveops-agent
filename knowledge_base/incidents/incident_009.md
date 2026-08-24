# Incident 009: User Service Session Cache Leak

Date: 2026-05-24  
Service: user-service  
Severity: high

## Summary
Login latency rose during a promotion. Memory climbed on all user-service pods and sessions started timing out.

## Signals
- Memory increased in proportion to login volume.
- No recent deployment in the first hour of the incident.
- Restarting one pod fixed that pod temporarily.

## Cause
An unbounded in-memory session cache retained expired sessions during high traffic.

## Resolution
Restarted affected pods in batches and lowered cache TTL through config.

## Retrieval Notes
Similar to payment-service memory leak, but no receipt code or payment path was involved.
