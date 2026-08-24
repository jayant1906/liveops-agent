# System Architecture

## Overview
LiveOps is an incident-response simulation platform. FastAPI exposes telemetry, incident, deployment, and remediation endpoints. Service modules simulate user, order, and payment behavior. Detection logic watches metrics and creates incidents. The agent investigates, diagnoses, remediates, and verifies recovery.

## Main Components
- Frontend dashboard: shows active incidents, diagnosis, remediation actions, and verification results.
- API layer: accepts telemetry and exposes incident workflows.
- Services: `user-service`, `order-service`, and `payment-service` model common production dependencies.
- Detection: threshold-based incident detection over recent telemetry.
- Agent: graph-based workflow for investigation, diagnosis, remediation, and verification.
- Knowledge base: runbooks, architecture notes, and historical incidents used for retrieval.

## Incident Flow
Telemetry arrives through API endpoints or traffic generation scripts. Detection compares recent metrics with configured thresholds. When an incident is opened, the agent gathers logs, metrics, events, and retrieved knowledge base chunks before recommending or executing actions.

## Deployment Events
Deployments are first-class events because many incidents are caused by config changes, schema drift, or new code paths. Rollback is allowed only when the suspected deployment is recent and verification can confirm user-facing recovery.

## Service Boundaries
Order service owns checkout orchestration. Payment service owns provider calls, retries, idempotency keys, and payment status. User service owns profile and session lookups. Cross-service calls should include request ids so related logs can be tied together during investigation.

## Reliability Priorities
The platform favors safe recovery over aggressive automation. The agent should gather enough evidence to distinguish similar failures, choose the lowest-risk remediation, and verify that error rate and latency return below threshold.
