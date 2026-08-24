# Runbook: External Dependency Failure

## Symptoms
- One service reports timeouts or 5xx responses from a downstream provider.
- Internal database and CPU metrics remain healthy.
- Retries increase request latency and may amplify load.

## Triage
1. Identify the failing dependency and affected endpoint.
2. Check timeout rate, retry count, and circuit breaker state.
3. Compare provider errors with internal deployment events.
4. Confirm whether fallback or degraded mode is available.

## Decision Criteria
- Treat as external provider failure when internal CPU, database, and deployment signals are clean.
- Treat as internal client/config failure when errors begin immediately after a deployment or timeout change.
- Prefer degraded mode when user impact can be reduced without corrupting state.
- Reduce retries when retry volume is increasing queues or making downstream saturation worse.

## Remediation
- Enable circuit breaker or degraded mode when supported.
- Reduce retry attempts if retries are causing queue buildup.
- Roll back only when the dependency failure starts immediately after a client/config deployment.
- Escalate to the provider when internal metrics are clean.

## Verification
Timeout rate should decrease, queues should drain, and successful degraded responses should replace hard failures. If normal operation is restored, confirm dependency calls succeed without excessive retries before disabling the circuit breaker or degraded mode.
