# Runbook: Database Connection Exhaustion

## Symptoms
- p95 latency rises across multiple services.
- Logs include `connection acquisition timeout`, `pool exhausted`, or `too many clients`.
- Database CPU may be normal while app request queues grow.

## Triage
1. Check whether the issue affects one service or all services.
2. Compare database pool usage, active connections, and slow query count.
3. Look for a recent deployment that changed connection pool size or transaction handling.
4. Confirm whether long-running transactions are holding connections.

## Decision Criteria
- Treat as app pool exhaustion when app pool usage is saturated but PostgreSQL still has available connections.
- Treat as too many connections when PostgreSQL rejects new sessions before queries run.
- Treat as slow query or lock contention when connections are available but query or lock wait time is elevated.
- Choose rollback only when the timing matches a deployment that changed pool size, worker count, or transaction scope.

## Remediation
- Restart the affected service only if leaked connections are suspected and requests are failing.
- Roll back the latest deployment if pool configuration or transaction scope changed.
- Temporarily reduce worker concurrency if the database is saturated.
- Do not increase pool size until database max connections and downstream capacity are confirmed.

## Verification
Latency should fall below threshold, connection acquisition errors should stop, and active connection count should return to normal.
