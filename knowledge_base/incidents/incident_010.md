# Incident 010: Rollback Blocked By Migration

Date: 2026-06-02  
Service: order-service  
Severity: high

## Summary
A new order-service version caused validation errors on coupon checkout. A direct rollback was unsafe because the release also included a forward-only migration.

## Signals
- Errors started 6 minutes after deployment.
- Logs showed `unknown coupon_scope`.
- Database schema had already added a non-null column.

## Cause
New validation logic rejected legacy coupon scopes.

## Resolution
Disabled the coupon validation feature flag instead of rolling back. A patch deploy followed later.

## Retrieval Notes
Similar to bad deployment rollback cases, but rollback was not the safe remediation.
