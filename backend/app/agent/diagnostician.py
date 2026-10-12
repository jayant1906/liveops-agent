from __future__ import annotations

from app.agent.state import AgentState


def _evidence_text(state: AgentState) -> str:
    evidence = []
    evidence.extend(str(log.get("message", "")) for log in state.get("logs", []))
    evidence.extend(str(metric.get("name", "")) for metric in state.get("metrics", []))
    evidence.extend(str(metric.get("unit", "")) for metric in state.get("metrics", []))
    evidence.extend(
        str(deployment.get("message", ""))
        for deployment in state.get("deployments", [])
    )
    evidence.extend(
        str(result.get("text", ""))
        for result in state.get("knowledge_results", [])
    )
    evidence.extend(
        str(incident.get("message", ""))
        for incident in state.get("historical_incidents", [])
    )
    evidence.extend(state.get("dependencies", []))
    return " ".join(evidence).lower()


def evaluate_hypotheses(state: AgentState) -> AgentState:
    evidence_text = _evidence_text(state)
    hypotheses = []

    for hypothesis in state.get("hypotheses", []):
        name = hypothesis["name"]
        score = 0.2
        evidence = []

        if name == "DB failure":
            database_terms = [
                "database",
                "connection",
                "connection pool",
                "db_connections",
                "timeout",
            ]
            matches = [term for term in database_terms if term in evidence_text]
            score += len(matches) * 0.14
            evidence.extend(matches)

        if name == "Bad deployment":
            if state.get("deployments"):
                score += 0.45
                evidence.append("recent deployment event")
            if "deploy" in evidence_text or "release" in evidence_text:
                score += 0.2
                evidence.append("deployment or release reference")

        if name == "External dependency":
            dependency_terms = [
                "dependency",
                "provider",
                "redis",
                "external service",
                "unavailable",
            ]
            matches = [term for term in dependency_terms if term in evidence_text]
            score += len(matches) * 0.14
            evidence.extend(matches)

        hypothesis["score"] = min(score, 0.99)
        hypothesis["evidence"] = evidence
        hypotheses.append(hypothesis)

    return {"hypotheses": hypotheses}


def diagnose(state: AgentState) -> AgentState:
    hypotheses = sorted(
        state.get("hypotheses", []),
        key=lambda hypothesis: hypothesis["score"],
        reverse=True,
    )

    if not hypotheses:
        return {
            "diagnosis": {
                "summary": "No diagnosis could be generated.",
                "confidence": 0.0,
                "hypothesis": None,
                "hypotheses": [],
            }
        }

    best_hypothesis = hypotheses[0]
    database_hypothesis = next(
        (
            hypothesis
            for hypothesis in hypotheses
            if hypothesis["name"] == "DB failure"
        ),
        None,
    )
    deployment_hypothesis = next(
        (
            hypothesis
            for hypothesis in hypotheses
            if hypothesis["name"] == "Bad deployment"
        ),
        None,
    )

    if (
        database_hypothesis
        and deployment_hypothesis
        and database_hypothesis["score"] >= 0.5
        and deployment_hypothesis["score"] >= 0.5
    ):
        summary = (
            "A database connection leak associated with the recent payment-service "
            "deployment is the most likely cause."
        )
        recommendation = {
            "action": "rollback_deployment",
            "service": state.get("incident", {}).get("service"),
            "reason": "Rollback to the previous healthy payment-service version.",
            "execute": False,
        }
    else:
        summary = best_hypothesis["description"]
        recommendation = {
            "action": "investigate_further",
            "service": state.get("incident", {}).get("service"),
            "reason": "Collect more evidence before taking remediation action.",
            "execute": False,
        }

    return {
        "diagnosis": {
            "summary": summary,
            "confidence": best_hypothesis["score"],
            "hypothesis": best_hypothesis["name"],
            "evidence": best_hypothesis["evidence"],
            "knowledge_results": state.get("knowledge_results", []),
            "historical_incidents": state.get("historical_incidents", []),
            "recommendation": recommendation,
            "hypotheses": hypotheses,
        }
    }
