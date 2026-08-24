# Database Architecture

## Purpose
LiveOps uses PostgreSQL as the system of record for incident history, telemetry samples, and remediation audit events. The database supports operator dashboards and gives the agent durable context about what happened, what was attempted, and whether recovery succeeded.

## Core Tables
- `logs`: structured application logs from `payment-service`, `order-service`, `user-service`, and edge workers. Logs carry timestamp, service, level, message, and optional request id.
- `metrics`: sampled service metrics such as latency, error rate, memory usage, queue depth, database pool usage, and dependency timeout rate.
- `events`: deployment, feature flag, autoscaling, dependency, and remediation events. These are lower-volume facts used to explain metric changes.
- `incidents`: detected incidents with service, incident type, severity, message, status, metric value, and threshold.

## Relationships
The core telemetry tables are correlated by `service`, timestamp window, and optional `request_id` rather than strict foreign keys. A single incident is usually explained by a cluster of related rows:
- `incidents` is the starting point for agent investigation and stores the detected symptom.
- `metrics` provides the numeric evidence that crossed a threshold or shows recovery.
- `logs` provides request-level or worker-level detail for the same service and time window.
- `events` explains changes around the incident, such as deployments, feature flag updates, dependency changes, restarts, and remediation attempts.

For example, a database failure incident may have an `incidents` row for `api` latency, `metrics` rows for pool usage or failed connection attempts, `logs` rows with connection errors, and `events` rows showing a database restart or injected failure.

## Access Pattern
The API writes telemetry through repository methods instead of direct model access. Detection jobs read recent windows of metrics and logs, then create an `incidents` row when thresholds are crossed. The agent reads incidents first, then follows related logs, metrics, and events by timestamp and service.

## Query Shape
Most investigation queries filter by:
- `service`
- recent timestamp window
- incident type or metric name
- request id when a single user flow is affected

Indexes should be added first on `timestamp`, `service`, and combined `service, timestamp` when data volume grows. Incident status views should prefer indexed status and timestamp predicates.

## Retention
High-cardinality logs and metrics can be retained for a shorter window in production, usually 14-30 days. Incidents and remediation events should be retained longer because they train retrieval and post-incident analysis. Historical Markdown incidents in the knowledge base are curated summaries, not replacements for database records.

## Failure Modes
- Database unavailable: services fail to open new connections and logs show connection refused, host unreachable, DNS failure, or database timeout errors. This should trigger broad blast-radius investigation because API, detection, telemetry writes, and incident persistence may all degrade at once.
- Too many connections: PostgreSQL rejects new sessions with too many clients or remaining connection slots reserved errors. App logs may show authentication succeeded but connection creation failed before queries ran. This is different from slow queries because the database may be responsive for existing sessions.
- Connection pool exhaustion: app workers wait for a pool slot and logs show connection acquisition timeouts. This can happen even when PostgreSQL still has capacity, usually because the service is holding connections too long.
- Slow queries: p95 latency rises while connections are available. Slow query logs or lock waits identify the affected table or transaction.
- Migration errors: failures correlate with a recent deployment event and schema-related exceptions such as missing columns, invalid enum values, or incompatible rollback behavior.

## Operational Notes
Keep remediation writes idempotent. If the agent retries an action after a timeout, the audit event should include the same action key or request id so duplicate attempts can be recognized later.
