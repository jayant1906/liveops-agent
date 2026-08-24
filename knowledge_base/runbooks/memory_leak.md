# Runbook: Memory Leak

## Symptoms
- Memory usage rises steadily over time.
- Latency increases after sustained traffic.
- Restarts temporarily fix the problem, then memory rises again.

## Triage
1. Compare memory growth with traffic volume and deployment events.
2. Look for repeated large payload processing, cache growth, or unbounded lists.
3. Check whether one pod or all pods are affected.
4. Distinguish memory leak from temporary spike during batch work.

## Decision Criteria
- Treat as memory leak when memory rises steadily and does not return to baseline after traffic drops.
- Treat as traffic spike when memory and latency normalize after load returns to baseline.
- Restart only affected instances when recovery is urgent and enough diagnostic evidence has been captured.
- Roll back or disable a feature when the memory slope began after a release or feature flag change.

## Remediation
- Restart only the affected instances to restore service while preserving evidence.
- Roll back if the leak began after a deployment.
- Disable the feature path if a flag controls the allocation-heavy behavior.
- Capture heap or object statistics before broad restarts when possible.

## Verification
Memory usage should stabilize below the configured threshold, the memory growth slope should flatten, restarts should stop, and p95 latency should return toward its normal range.
