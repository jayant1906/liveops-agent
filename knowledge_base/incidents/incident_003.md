# Incident 003: Order Service Memory Growth After Release

Date: 2026-04-14  
Service: order-service  
Severity: medium

## Summary
Order-service latency increased gradually after a release that added checkout recommendation payloads. The service recovered after pod restarts, then memory began climbing again.

## Signals
- Memory grew from 500MB to 1.6GB over 90 minutes.
- p95 latency rose after memory exceeded 1.2GB.
- Error rate stayed below high severity threshold.

## Cause
Recommendation payloads were appended to an in-process list for debugging and never cleared.

## Resolution
Disabled recommendation debugging and rolled forward a patch that removed the retained list.

## Retrieval Notes
Similar to traffic saturation because latency rose under load, but memory slope was the leading indicator.
