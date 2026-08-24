# Runbook: Deployment Rollback

## Use When
- Errors begin shortly after a deployment event.
- Failures map to changed code paths or configuration.
- No wider dependency or database outage explains the symptoms.

## Triage
1. Find the latest deployment for the affected service.
2. Compare error onset with deployment timestamp.
3. Check whether a feature flag can disable the risky behavior.
4. Review whether migrations are backward compatible before rolling back.

## Decision Criteria
- Roll back when the release timing, changed code path, and error signature all point to the new version.
- Prefer feature flag disablement when it fully avoids the failing behavior and has lower blast radius.
- Avoid rollback when schema changes are forward-only or the old version cannot read current data.
- Roll forward with a patch when rollback risk is higher than the current incident risk.

## Remediation
- Prefer feature flag disablement when it fully avoids the failing path.
- Roll back the service when the new version is strongly correlated with the incident.
- Avoid rollback if it would run old code against an incompatible schema.

## Verification
Error rate should fall below the configured incident threshold within one or two traffic windows. Confirm latency also returns toward its normal range and that no new schema, queue, or compatibility errors appear after the rollback.