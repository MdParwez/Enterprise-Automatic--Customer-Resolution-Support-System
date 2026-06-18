from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


<<<<<<< HEAD
IssueType = Literal[
    "refund_delay",
    "flight_delay",
    "baggage",
    "billing",
    "subscription",
    "account",
    "ticket_status",
    "complaint",
    "general",
]
=======
IssueType = Literal["refund_delay", "flight_delay", "baggage", "billing", "subscription", "account", "general"]
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
ApprovalStatus = Literal["auto_approved", "manual_required", "rejected"]
ExecutionStatus = Literal["pending", "completed", "failed"]


class CustomerIssue(BaseModel):
    customer_id: str
    message: str
    channel: str = "chat"
    run_id: str = Field(default_factory=lambda: f"RUN-{uuid4().hex[:10].upper()}")


class ManualExecutionRequest(BaseModel):
    customer_id: str
    issue_type: IssueType
    recommended_action: str
    approver: str
    note: str = ""


class AgentEvent(BaseModel):
    agent: str
    action: str
    detail: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Decision(BaseModel):
    issue_type: IssueType
    recommended_action: str
    rationale: str
    risk_level: Literal["low", "medium", "high"]
    compensation_amount: float = 0
    policy_refs: list[str] = Field(default_factory=list)
    confidence_score: float = 0.85
    sla_target: str = "24 hours"
    approval_reason: str = ""
    risk_flags: list[str] = Field(default_factory=list)
    next_best_actions: list[str] = Field(default_factory=list)
<<<<<<< HEAD
    ai_provider: str = "local_rules"
    ai_summary: str = ""
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539


class ResolutionResponse(BaseModel):
    run_id: str
    issue_type: IssueType
    decision: Decision
    approval_status: ApprovalStatus
    execution_status: ExecutionStatus
    ticket_id: str | None = None
    final_response: str
    verification: dict[str, Any]
    metrics: dict[str, Any]
    events: list[AgentEvent]
    plan: list[str] = Field(default_factory=list)
    case_context: dict[str, Any] = Field(default_factory=dict)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    automation_trace: list[dict[str, Any]] = Field(default_factory=list)
    unique_features: list[str] = Field(default_factory=list)
<<<<<<< HEAD
    workflow_status: dict[str, Any] = Field(default_factory=dict)
    internal_updates: list[dict[str, Any]] = Field(default_factory=list)
    tool_call_log: list[dict[str, Any]] = Field(default_factory=list)
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
