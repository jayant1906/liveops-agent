# Incident 007: Memory Leak In Receipt Rendering

Date: 2026-05-11  
Service: payment-service  
Severity: medium

## Summary
Payment-service memory climbed for two hours after receipt traffic increased. Latency rose, then two pods restarted.

## Signals
- `process.memory.rss` grew from 420MB to 1.8GB.
- Error rate stayed low until restarts.
- Heap samples pointed to cached receipt templates.

## Cause
Receipt rendering cached per-user templates without eviction.

## Resolution
Disabled rich receipt rendering with a feature flag and restarted the two largest pods.

## Retrieval Notes
Similar to general latency incidents, but gradual memory slope and restart recovery indicate leak.
