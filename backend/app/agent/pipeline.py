from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.agent.graph import run_investigation
from app.database.models import Incident
from app.retrieval.knowledge_base import get_knowledge_searcher


def incident_to_dict(incident: Incident) -> dict[str, Any]:
    return {
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


def investigate_incident(
    incident: Incident,
    db: Session,
) -> dict[str, Any]:
    searcher = get_knowledge_searcher()
    state = run_investigation(
        incident_to_dict(incident),
        db,
        knowledge_searcher=searcher,
    )
    return {
        "incident": incident_to_dict(incident),
        "investigation": state,
    }
