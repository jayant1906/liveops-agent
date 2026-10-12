from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.database.models import EventRecord, Incident, LogRecord, MetricRecord


SERVICE_DEPENDENCIES = {
    "payment-service": ["database", "redis", "payment-provider"],
    "order-service": ["database", "payment-service"],
    "user-service": ["database", "redis"],
}


def get_logs(
    db: Session,
    service: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    query = db.query(LogRecord).order_by(LogRecord.timestamp.desc())
    if service:
        query = query.filter(LogRecord.service == service)

    logs = query.limit(limit).all()
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "service": log.service,
            "message": log.message,
            "request_id": log.request_id,
            "level": log.level,
        }
        for log in logs
    ]


def get_metrics(
    db: Session,
    service: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    query = db.query(MetricRecord).order_by(MetricRecord.timestamp.desc())
    if service:
        query = query.filter(MetricRecord.service == service)

    metrics = query.limit(limit).all()
    return [
        {
            "id": metric.id,
            "timestamp": metric.timestamp,
            "service": metric.service,
            "name": metric.name,
            "value": metric.value,
            "unit": metric.unit,
        }
        for metric in metrics
    ]


def get_deployments(
    db: Session,
    service: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    query = (
        db.query(EventRecord)
        .filter(EventRecord.event_type == "DEPLOYMENT")
        .order_by(EventRecord.timestamp.desc())
    )
    if service:
        query = query.filter(EventRecord.service == service)

    deployments = query.limit(limit).all()
    return [
        {
            "id": deployment.id,
            "timestamp": deployment.timestamp,
            "service": deployment.service,
            "message": deployment.message,
            "request_id": deployment.request_id,
        }
        for deployment in deployments
    ]


def search_knowledge_base(
    query: str,
    searcher: Any,
    k: int = 5,
) -> list[dict[str, Any]]:
    if searcher is None:
        return []

    results = searcher.search(query, k=k, use_reranker=True)
    knowledge_results = []
    for result in results:
        knowledge_results.append(
            {
                "text": result.text,
                "metadata": result.metadata,
                "score": result.reranker_score
                if result.reranker_score is not None
                else result.combined_score,
            }
        )

    return knowledge_results


def search_historical_incidents(
    db: Session,
    service: str | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    query = db.query(Incident).order_by(Incident.timestamp.desc())
    if service:
        query = query.filter(Incident.service == service)

    incidents = query.limit(limit).all()
    return [
        {
            "id": incident.id,
            "timestamp": incident.timestamp,
            "service": incident.service,
            "incident_type": incident.incident_type,
            "severity": incident.severity,
            "message": incident.message,
            "status": incident.status,
            "metric_value": incident.metric_value,
            "threshold": incident.threshold,
        }
        for incident in incidents
    ]


def get_service_dependencies(service: str) -> list[str]:
    return SERVICE_DEPENDENCIES.get(service, [])


AGENT_TOOLS = [
    get_logs,
    get_metrics,
    get_deployments,
    search_knowledge_base,
    search_historical_incidents,
    get_service_dependencies,
]
