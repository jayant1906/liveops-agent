# Runbook: Payment Service Degradation

## Symptoms
- Checkout failures or pending payments rise.
- Payment-service logs include gateway timeout, idempotency conflict, or provider 5xx.
- Order service may show downstream payment errors while user service remains healthy.

## Triage
1. Check payment error rate and gateway timeout rate.
2. Compare failures by provider, region, and payment method.
3. Inspect recent payment-service deployment or gateway config changes.
4. Confirm whether idempotency keys are being reused correctly.

## Decision Criteria
- Treat as provider degradation when gateway timeout or provider 5xx rises without a matching internal deployment.
- Treat as payment-service regression when failures begin immediately after release or config change.
- Prioritize idempotency protection when duplicate attempts or conflicts appear in logs.
- Use degraded mode when authorization is unreliable but orders can safely remain pending.

## Remediation
- Enable payment degraded mode if the gateway is timing out.
- Roll back the payment-service deployment if errors started after release.
- Reduce retry fanout if duplicate attempts are creating conflicts.
- Do not manually mark payments successful without provider confirmation.

## Verification
New checkout attempts should succeed, payment gateway timeout rate should fall below the incident threshold, pending payment backlog should shrink, and duplicate charge alerts should remain at zero.
