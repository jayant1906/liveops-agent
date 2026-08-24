# Incident 016: API Worker Saturation From Traffic Spike

Date: 2026-07-12  
Service: api  
Severity: medium

## Summary
API latency rose during a traffic spike. Database, payment provider, and service error rates stayed healthy.

## Signals
- Request rate doubled in 9 minutes.
- CPU rose above 88% on all API workers.
- Queue depth increased without dependency errors.

## Cause
Autoscaling lagged behind legitimate traffic.

## Resolution
Increased API worker replicas and tuned the autoscaling threshold.

## Retrieval Notes
Can resemble database slowness, but dependency metrics were clean and CPU saturation led the incident.
