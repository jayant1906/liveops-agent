# Incident 014: Bad Deployment In Metrics Parser

Date: 2026-06-29  
Service: api  
Severity: medium

## Summary
Detection stopped creating incidents for payment errors because the metrics parser dropped percentage units after a deployment.

## Signals
- Raw logs showed payment failures.
- `metrics` rows for `payment.error_rate` were missing.
- Deployment `api:2026.06.29.1` changed parser normalization.

## Cause
The parser treated `%` as invalid and discarded the metric.

## Resolution
Rolled back the API parser release and replayed telemetry from logs.

## Retrieval Notes
Similar to payment outage, but the customer path was failing before detection noticed.
