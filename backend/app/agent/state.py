from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    incident: dict[str, Any]
    logs: list[dict[str, Any]]
    metrics: list[dict[str, Any]]
    deployments: list[dict[str, Any]]
    knowledge_results: list[dict[str, Any]]
    historical_incidents: list[dict[str, Any]]
    dependencies: list[str]
    hypotheses: list[dict[str, Any]]
    diagnosis: dict[str, Any]
