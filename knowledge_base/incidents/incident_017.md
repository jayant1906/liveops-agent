# Incident 017: Order Event Queue Backlog

Date: 2026-07-18  
Service: order-service  
Severity: high

## Summary
Orders were accepted but status updates lagged. Payment succeeded, yet dashboard showed orders pending for several minutes.

## Signals
- Queue depth increased from 300 to 19,000.
- Payment success rate remained normal.
- Worker logs showed deserialization errors on one event type.

## Cause
A producer deployment added a field that older queue consumers did not tolerate.

## Resolution
Rolled forward the consumer compatibility fix and replayed failed messages.

## Retrieval Notes
Similar to payment pending incidents, but provider success and queue backlog identify async processing failure.
