from datetime import datetime, timezone
from typing import Any, TypedDict

from src.models import AgentEvent, CustomerIssue, Decision


class ERAState(TypedDict, total=False):
    issue: CustomerIssue
    issue_type: str
    plan: list[str]
    customer: dict[str, Any] | None
    booking: dict[str, Any] | None
    refund: dict[str, Any] | None
    customer_history: list[dict[str, Any]]
    active_tickets: list[dict[str, Any]]
    existing_ticket: dict[str, Any] | None
    requested_ticket_id: str | None
    knowledge: list[dict[str, Any]]
    decision: Decision
    case_context: dict[str, Any]
    automation_trace: list[dict[str, Any]]
    unique_features: list[str]
    workflow_status: dict[str, Any]
    internal_updates: list[dict[str, Any]]
    tool_call_log: list[dict[str, Any]]
    approval_status: str
    ticket: dict[str, Any] | None
    verification: dict[str, Any]
    final_response: str
    events: list[AgentEvent]
    tool_calls: int
    reflection_attempts: int
    started_at: datetime


def initial_state(issue: CustomerIssue) -> ERAState:
    return {
        "issue": issue,
        "events": [],
        "tool_calls": 0,
        "reflection_attempts": 0,
        "started_at": datetime.now(timezone.utc),
    }


def add_event(state: ERAState, agent: str, action: str, detail: str) -> ERAState:
    state.setdefault("events", []).append(AgentEvent(agent=agent, action=action, detail=detail))
    return state
