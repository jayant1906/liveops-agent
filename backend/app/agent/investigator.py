from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.agent.state import AgentState
from app.agent.tools import (
    get_deployments,
    get_logs,
    get_metrics,
    get_service_dependencies,
    search_historical_incidents,
    search_knowledge_base,
)


def investigate(
    state: AgentState,
    db: Session,
    knowledge_searcher: Any = None,
) -> AgentState:
    incident = state.get("incident", {})
    service = incident.get("service")
    query = " ".join(
        [
            str(service or ""),
            str(incident.get("incident_type", "")),
            str(incident.get("message", "")),
        ]
    ).strip()

    return {
        "logs": get_logs(db, service=service),
        "metrics": get_metrics(db, service=service),
        "deployments": get_deployments(db, service=service),
        "knowledge_results": search_knowledge_base(
            query,
            searcher=knowledge_searcher,
        ),
        "historical_incidents": search_historical_incidents(
            db,
            service=service,
        ),
        "dependencies": get_service_dependencies(service or ""),
    }


def generate_hypotheses(state: AgentState) -> AgentState:
    return {
        "hypotheses": [
            {
                "name": "DB failure",
                "description": "A database failure or connection issue caused the incident.",
                "score": 0.0,
                "evidence": [],
            },
            {
                "name": "Bad deployment",
                "description": "A recent deployment introduced the incident.",
                "score": 0.0,
                "evidence": [],
            },
            {
                "name": "External dependency",
                "description": "An external service or dependency caused the incident.",
                "score": 0.0,
                "evidence": [],
            },
        ]
    }
