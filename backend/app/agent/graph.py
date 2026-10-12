from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph
from sqlalchemy.orm import Session

from app.agent.diagnostician import diagnose, evaluate_hypotheses
from app.agent.investigator import generate_hypotheses, investigate
from app.agent.state import AgentState


def create_investigation_graph(
    db: Session,
    knowledge_searcher: Any = None,
):
    workflow = StateGraph(AgentState)

    def investigate_node(state: AgentState) -> AgentState:
        return investigate(state, db, knowledge_searcher)

    workflow.add_node("investigate", investigate_node)
    workflow.add_node("generate_hypotheses", generate_hypotheses)
    workflow.add_node("evaluate_hypotheses", evaluate_hypotheses)
    workflow.add_node("diagnose", diagnose)

    workflow.add_edge(START, "investigate")
    workflow.add_edge("investigate", "generate_hypotheses")
    workflow.add_edge("generate_hypotheses", "evaluate_hypotheses")
    workflow.add_edge("evaluate_hypotheses", "diagnose")
    workflow.add_edge("diagnose", END)

    return workflow.compile()


def run_investigation(
    incident: dict[str, Any],
    db: Session,
    knowledge_searcher: Any = None,
) -> AgentState:
    graph = create_investigation_graph(db, knowledge_searcher)
    return graph.invoke({"incident": incident})
