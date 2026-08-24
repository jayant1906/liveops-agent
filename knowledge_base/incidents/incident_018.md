# Incident 018: User Service Dependency Timeout

Date: 2026-07-26  
Service: user-service  
Severity: medium

## Summary
Profile lookups intermittently timed out, causing checkout preflight failures. Database metrics were normal for core tables.

## Signals
- Timeout logs named the preferences dependency.
- Login was mostly healthy; checkout preflight was affected.
- Error spikes matched calls that requested marketing preferences.

## Cause
The optional preferences service degraded and user-service treated it as required.

## Resolution
Enabled fallback preferences and lowered timeout from 2s to 300ms.

## Retrieval Notes
Similar to user-service database issues, but only optional preference lookups failed.
