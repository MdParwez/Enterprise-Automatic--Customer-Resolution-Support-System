from __future__ import annotations

import json
<<<<<<< HEAD
import re
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539

from langgraph.graph import END, StateGraph

from src.agents.state import ERAState, add_event, initial_state
from src.database.sqlite import initialize_database, record_agent_run, seed_database
from src.evaluation.metrics import build_metrics
from src.knowledge.retriever import KnowledgeRetriever
<<<<<<< HEAD
from src.llm.groq_client import LLMResolutionAdvisor
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
from src.mcp_servers.database_mcp import DatabaseMCP
from src.mcp_servers.filesystem_mcp import FilesystemMCP
from src.mcp_servers.servicenow_mcp import ServiceNowMCP
from src.models import CustomerIssue, Decision, ResolutionResponse


class AgentWorkflow:
    def __init__(self) -> None:
        initialize_database()
        seed_database()
        self.database = DatabaseMCP()
        self.filesystem = FilesystemMCP()
        self.servicenow = ServiceNowMCP()
        self.knowledge = KnowledgeRetriever()
<<<<<<< HEAD
        self.llm = LLMResolutionAdvisor()
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        self.graph = self._build_graph()

    def run(self, issue: CustomerIssue) -> ResolutionResponse:
        state = self.graph.invoke(initial_state(issue))
        decision = state["decision"]
        metrics = build_metrics(
            started_at=state["started_at"],
            tool_calls=state.get("tool_calls", 0),
            reflection_attempts=state.get("reflection_attempts", 0),
            policy_refs=decision.policy_refs,
        )
        response = ResolutionResponse(
            run_id=issue.run_id,
            issue_type=decision.issue_type,
            decision=decision,
            approval_status=state["approval_status"],
            execution_status=self._execution_status(state),
            ticket_id=state.get("ticket", {}).get("ticket_id") if state.get("ticket") else None,
            final_response=state["final_response"],
            verification=state["verification"],
            metrics=metrics,
            events=state["events"],
            plan=state.get("plan", []),
            case_context=state.get("case_context", {}),
            evidence=state.get("knowledge", []),
            automation_trace=state.get("automation_trace", []),
            unique_features=state.get("unique_features", []),
<<<<<<< HEAD
            workflow_status=state.get("workflow_status", {}),
            internal_updates=state.get("internal_updates", []),
            tool_call_log=state.get("tool_call_log", []),
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        )
        record_agent_run(issue.run_id, decision.issue_type, decision.model_dump_json(), response.execution_status)
        self.filesystem.save_logs(issue.run_id, [event.model_dump() for event in state["events"]])
        self.filesystem.save_audit_trail(issue.run_id, response.model_dump())
        self.filesystem.save_report(issue.run_id, {"customer_response": response.final_response, "metrics": metrics})
        return response

    def _build_graph(self):
        graph = StateGraph(ERAState)
        graph.add_node("supervisor", self.supervisor_agent)
        graph.add_node("customer_agent", self.customer_agent)
<<<<<<< HEAD
        graph.add_node("ticket_agent", self.ticket_agent)
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        graph.add_node("booking_agent", self.booking_agent)
        graph.add_node("knowledge_agent", self.knowledge_agent)
        graph.add_node("resolution_agent", self.resolution_agent)
        graph.add_node("approval_agent", self.approval_agent)
        graph.add_node("execution_agent", self.execution_agent)
        graph.add_node("verification_agent", self.verification_agent)
        graph.add_node("reflection_agent", self.reflection_agent)

        graph.set_entry_point("supervisor")
        graph.add_edge("supervisor", "customer_agent")
<<<<<<< HEAD
        graph.add_edge("customer_agent", "ticket_agent")
        graph.add_edge("ticket_agent", "booking_agent")
=======
        graph.add_edge("customer_agent", "booking_agent")
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        graph.add_edge("booking_agent", "knowledge_agent")
        graph.add_edge("knowledge_agent", "resolution_agent")
        graph.add_edge("resolution_agent", "approval_agent")
        graph.add_edge("approval_agent", "execution_agent")
        graph.add_edge("execution_agent", "verification_agent")
        graph.add_conditional_edges("verification_agent", self.needs_reflection, {"reflect": "reflection_agent", "done": END})
        graph.add_edge("reflection_agent", "execution_agent")
        return graph.compile()

    def supervisor_agent(self, state: ERAState) -> ERAState:
        message = state["issue"].message.lower()
        issue_type = "refund_delay"
        if "bag" in message:
            issue_type = "baggage"
        elif "bill" in message or "charge" in message:
            issue_type = "billing"
<<<<<<< HEAD
        elif "ticket" in message and any(term in message for term in ["status", "where", "update", "progress"]):
            issue_type = "ticket_status"
        elif "complaint" in message or "complain" in message:
            issue_type = "complaint"
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        elif "subscription" in message:
            issue_type = "subscription"
        elif "account" in message or "login" in message:
            issue_type = "account"
        elif "flight" in message or "delay" in message:
            issue_type = "flight_delay"
        if "refund" in message:
            issue_type = "refund_delay"
<<<<<<< HEAD
        if "ticket" in message and any(term in message for term in ["status", "where", "update", "progress"]):
            issue_type = "ticket_status"

        state["issue_type"] = issue_type
        state["plan"] = [
            "Understand request and identify customer",
            "Check active tickets before creating anything new",
            "Retrieve order, booking, payment, and refund state",
            "Search policies and historical cases",
            "Decide whether to update, auto-resolve, escalate, or ask for human help",
            "Track progress and keep the customer updated",
=======

        state["issue_type"] = issue_type
        state["plan"] = [
            "Retrieve customer context",
            "Retrieve booking/order and payment state",
            "Search policies and historical cases",
            "Recommend compliant resolution",
            "Approve, execute, verify, and record audit trail",
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        ]
        state["automation_trace"] = [
            {"stage": "intake", "status": "complete", "summary": "Issue classified and routed by supervisor."}
        ]
        state["unique_features"] = [
<<<<<<< HEAD
            "Investigates before creating tickets",
            "Routes work across AI agents and human teams",
            "Uses policy evidence and historical resolutions",
            "Tracks workflow progress after escalation",
            "Keeps customer updates separate from internal notes",
            "Supports SaaS-style expansion across industries",
        ]
        state["workflow_status"] = {"phase": "investigating", "owner": "Supervisor", "progress": 10}
        state["internal_updates"] = []
        state["tool_call_log"] = []
=======
            "Policy-grounded autonomous resolution",
            "Human-in-the-loop approval gates",
            "Verification before customer response",
            "Reflection loop for failed execution",
            "Audit-ready evidence and tool trace",
            "Multi-domain support: refunds, flights, baggage, billing, subscriptions, accounts",
        ]
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        return add_event(state, "Supervisor Agent", "plan", f"Classified issue as {issue_type} and created execution plan.")

    def customer_agent(self, state: ERAState) -> ERAState:
        issue = state["issue"]
        state["customer"] = self.database.get_customer(issue.customer_id)
        state["customer_history"] = self.database.get_customer_history(issue.customer_id)
        state["tool_calls"] = state.get("tool_calls", 0) + 2
<<<<<<< HEAD
        state.setdefault("tool_call_log", []).extend(
            [
                {"tool": "Database MCP", "operation": "get_customer", "status": "success" if state["customer"] else "not_found"},
                {"tool": "Database MCP", "operation": "get_customer_history", "status": "success"},
            ]
        )
        state["workflow_status"] = {"phase": "customer_identified", "owner": "Customer Agent", "progress": 25}
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        state.setdefault("automation_trace", []).append(
            {"stage": "customer_context", "status": "complete", "summary": "Loaded profile, tier, and previous ticket history."}
        )
        detail = "Customer found." if state["customer"] else "Customer not found."
        return add_event(state, "Customer Agent", "retrieve_customer", detail)

<<<<<<< HEAD
    def ticket_agent(self, state: ERAState) -> ERAState:
        customer = state.get("customer")
        requested_ticket_id = self._extract_ticket_id(state["issue"].message)
        requested_ticket = self.database.get_ticket(requested_ticket_id) if requested_ticket_id else None
        active_tickets = self.database.get_active_tickets(customer["customer_id"], state["issue_type"]) if customer else []
        if state["issue_type"] == "ticket_status" and customer and not active_tickets:
            active_tickets = self.database.get_active_tickets(customer["customer_id"])
        state["active_tickets"] = active_tickets
        state["requested_ticket_id"] = requested_ticket_id
        state["existing_ticket"] = requested_ticket or (active_tickets[0] if active_tickets else None)
        state["tool_calls"] = state.get("tool_calls", 0) + 1
        state.setdefault("tool_call_log", []).append(
            {"tool": "Database MCP", "operation": "get_ticket_and_active_tickets", "status": "found" if state["existing_ticket"] else "none"}
        )
        if state["existing_ticket"]:
            summary = f"Found active ticket {state['existing_ticket']['ticket_id']}; new ticket creation is not needed yet."
            state.setdefault("internal_updates", []).append(
                {"team": "Support Operations", "message": summary, "status": "monitoring"}
            )
        else:
            summary = "No active ticket found; workflow can create one only after order, policy, and risk checks."
        state["workflow_status"] = {"phase": "ticket_checked", "owner": "Ticket Agent", "progress": 35}
        state.setdefault("automation_trace", []).append(
            {"stage": "ticket_check", "status": "complete", "summary": summary}
        )
        return add_event(state, "Ticket Agent", "check_existing_tickets", summary)

=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
    def booking_agent(self, state: ERAState) -> ERAState:
        customer = state.get("customer")
        if customer:
            booking = self.database.get_booking(customer["customer_id"])
            refund = self.database.get_refund(booking["booking_id"]) if booking else None
        else:
            booking = None
            refund = None
        state["booking"] = booking
        state["refund"] = refund
        state["tool_calls"] = state.get("tool_calls", 0) + 2
        state["case_context"] = {
            "customer": state.get("customer"),
            "booking": booking,
            "refund": refund,
<<<<<<< HEAD
            "active_tickets": state.get("active_tickets", []),
            "existing_ticket": state.get("existing_ticket"),
            "requested_ticket_id": state.get("requested_ticket_id"),
            "history_count": len(state.get("customer_history", [])),
            "detected_entities": self._extract_entities(state["issue"].message),
        }
        state.setdefault("tool_call_log", []).extend(
            [
                {"tool": "Database MCP", "operation": "get_booking", "status": "success" if booking else "not_found"},
                {"tool": "Database MCP", "operation": "get_refund", "status": "success" if refund else "not_found"},
            ]
        )
        state["workflow_status"] = {"phase": "operations_checked", "owner": "Order Agent", "progress": 50}
=======
            "history_count": len(state.get("customer_history", [])),
            "detected_entities": self._extract_entities(state["issue"].message),
        }
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        state.setdefault("automation_trace", []).append(
            {"stage": "operational_lookup", "status": "complete", "summary": "Resolved customer, booking, refund, and history records from SQLite."}
        )
        return add_event(state, "Booking/Order Agent", "retrieve_order_state", f"Booking={bool(booking)}, refund={bool(refund)}.")

    def knowledge_agent(self, state: ERAState) -> ERAState:
        query = f"{state['issue'].message} {state.get('issue_type')} {state.get('refund')}"
        results = self.knowledge.search(query)
        state["knowledge"] = [result.__dict__ for result in results]
        state["tool_calls"] = state.get("tool_calls", 0) + 1
<<<<<<< HEAD
        state.setdefault("tool_call_log", []).append(
            {"tool": "Knowledge Base MCP", "operation": "search_policy_and_cases", "status": "success"}
        )
        state["workflow_status"] = {"phase": "policy_checked", "owner": "Policy and Knowledge Agents", "progress": 65}
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        state.setdefault("automation_trace", []).append(
            {"stage": "rag", "status": "complete", "summary": f"Retrieved {len(results)} policies and similar cases from the knowledge layer."}
        )
        return add_event(state, "Knowledge Agent", "retrieve_context", f"Retrieved {len(results)} policy and case documents.")

    def resolution_agent(self, state: ERAState) -> ERAState:
        customer = state.get("customer") or {}
        refund = state.get("refund") or {}
        days_pending = int(refund.get("days_pending") or 0)
        tier = customer.get("tier", "standard")
        issue_type = state["issue_type"]
        playbook = self._playbook(issue_type, days_pending, tier)
<<<<<<< HEAD
        refined = self.llm.refine_resolution(
            issue_message=state["issue"].message,
            issue_type=issue_type,
            case_context=state.get("case_context", {}),
            evidence=state.get("knowledge", []),
            playbook=playbook,
        )
        playbook = {**playbook, **{key: value for key, value in refined.items() if value not in (None, "", [])}}
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        compensation = playbook["compensation_amount"]
        decision = Decision(
            issue_type=issue_type,
            recommended_action=playbook["recommended_action"],
            rationale=playbook["rationale"],
            risk_level=playbook["risk_level"],
            compensation_amount=compensation,
            policy_refs=[doc["title"] for doc in state.get("knowledge", []) if doc["collection"] == "policies"],
            confidence_score=playbook["confidence_score"],
            sla_target=playbook["sla_target"],
            approval_reason=playbook["approval_reason"],
            risk_flags=playbook["risk_flags"],
            next_best_actions=playbook["next_best_actions"],
<<<<<<< HEAD
            ai_provider=playbook.get("ai_provider", "local_rules"),
            ai_summary=playbook.get("ai_summary", ""),
        )
        state["decision"] = decision
        if state.get("existing_ticket"):
            if issue_type == "ticket_status":
                decision.recommended_action = f"Return status for ticket {state['existing_ticket']['ticket_id']} and continue monitoring"
                decision.rationale = "The customer asked for ticket progress, so OmniSupport checked the existing case and will update the customer instead of creating a new ticket."
                decision.next_best_actions = ["Share ticket status", "Check next owner update", "Schedule follow-up if status remains open"]
            else:
                decision.recommended_action = f"Update existing ticket {state['existing_ticket']['ticket_id']} and notify customer with current status"
                decision.rationale = "An active ticket already exists, so OmniSupport will avoid duplicate ticket creation and continue tracking progress."
                decision.next_best_actions = ["Check latest internal owner update", "Notify customer with ticket status", "Schedule next status check"]
            decision.risk_level = "low"
            decision.approval_reason = "Updating an existing support case is low risk."
        state["workflow_status"] = {"phase": "decision_ready", "owner": "Resolution Agent", "progress": 78}
        state.setdefault("automation_trace", []).append(
            {
                "stage": "reasoning",
                "status": "complete",
                "summary": f"Selected {issue_type} playbook with {decision.confidence_score:.0%} confidence using {decision.ai_provider}.",
            }
=======
        )
        state["decision"] = decision
        state.setdefault("automation_trace", []).append(
            {"stage": "reasoning", "status": "complete", "summary": f"Selected {issue_type} playbook with {decision.confidence_score:.0%} confidence."}
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        )
        return add_event(state, "Resolution Agent", "decide", decision.rationale)

    def approval_agent(self, state: ERAState) -> ERAState:
        decision = state["decision"]
        state["approval_status"] = "auto_approved" if decision.risk_level == "low" else "manual_required"
<<<<<<< HEAD
        state["workflow_status"] = {
            "phase": "approved" if state["approval_status"] == "auto_approved" else "awaiting_human_review",
            "owner": "Approval Agent" if state["approval_status"] == "auto_approved" else "Human Collaboration Agent",
            "progress": 86,
        }
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        state.setdefault("automation_trace", []).append(
            {"stage": "approval", "status": state["approval_status"], "summary": decision.approval_reason}
        )
        return add_event(state, "Approval Agent", "approve", f"Approval status: {state['approval_status']}.")

    def execution_agent(self, state: ERAState) -> ERAState:
        if state["approval_status"] != "auto_approved":
            state["ticket"] = None
<<<<<<< HEAD
            state.setdefault("internal_updates", []).append(
                {"team": self._team_for_issue(state["decision"].issue_type), "message": "Waiting for manager review before execution.", "status": "waiting"}
            )
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
            state.setdefault("automation_trace", []).append(
                {"stage": "execution", "status": "held", "summary": "Execution paused for manual approver review."}
            )
            return add_event(state, "Execution Agent", "hold", "Manual approval required before execution.")
        description = f"{state['decision'].recommended_action}. Customer message: {state['issue'].message}"
<<<<<<< HEAD
        if state.get("existing_ticket") and state["decision"].issue_type == "ticket_status":
            state["ticket"] = state["existing_ticket"]
            operation = "get_ticket_status"
            summary = f"Read ticket {state['ticket']['ticket_id']} status and prepared customer update."
        elif state.get("existing_ticket"):
            state["ticket"] = state["existing_ticket"]
            operation = "update_existing_ticket"
            summary = f"Updated existing ticket {state['ticket']['ticket_id']} and queued customer notification."
        else:
            state["ticket"] = self.servicenow.create_incident(state["issue"].customer_id, state["decision"].issue_type, description)
            operation = "create_incident"
            summary = f"Created ticket {state['ticket']['ticket_id']}, assigned {self._team_for_issue(state['decision'].issue_type)}, and queued customer update."
        state["tool_calls"] = state.get("tool_calls", 0) + 1
        state.setdefault("tool_call_log", []).append(
            {"tool": "ServiceNow MCP", "operation": operation, "status": "success"}
        )
        state.setdefault("internal_updates", []).append(
            {"team": self._team_for_issue(state["decision"].issue_type), "message": summary, "status": "assigned"}
        )
        state["workflow_status"] = {"phase": "tracking_progress", "owner": self._team_for_issue(state["decision"].issue_type), "progress": 94}
        state.setdefault("automation_trace", []).append(
            {"stage": "execution", "status": "complete", "summary": summary}
        )
        return add_event(state, "Execution Agent", operation, summary)
=======
        state["ticket"] = self.servicenow.create_incident(state["issue"].customer_id, state["decision"].issue_type, description)
        state["tool_calls"] = state.get("tool_calls", 0) + 1
        state.setdefault("automation_trace", []).append(
            {"stage": "execution", "status": "complete", "summary": f"Created ServiceNow-style incident {state['ticket']['ticket_id']}."}
        )
        return add_event(state, "Execution Agent", "create_incident", f"Created incident {state['ticket']['ticket_id']}.")
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539

    def verification_agent(self, state: ERAState) -> ERAState:
        ticket = state.get("ticket")
        verified_ticket = self.servicenow.get_incident(ticket["ticket_id"]) if ticket else None
        state["verification"] = {
            "ticket_created": bool(verified_ticket),
            "ticket_status": verified_ticket.get("status") if verified_ticket else None,
            "policy_refs_checked": len(state["decision"].policy_refs),
            "customer_record_verified": bool(state.get("customer")),
            "audit_trail_ready": True,
            "sla_target": state["decision"].sla_target,
        }
        state["tool_calls"] = state.get("tool_calls", 0) + 1
        if verified_ticket:
            name = (state.get("customer") or {}).get("name", "there")
<<<<<<< HEAD
            if state["decision"].issue_type == "ticket_status":
                state["final_response"] = (
                    f"Hi {name}, I checked ticket {ticket['ticket_id']}. Current status: "
                    f"{verified_ticket.get('status', 'open')}. Owner: "
                    f"{self._team_for_issue(verified_ticket.get('issue_type', state['decision'].issue_type))}. "
                    f"I will keep tracking it and update you when the next team update arrives."
                )
            else:
                state["final_response"] = (
                    f"Hi {name}, I investigated your case and found ticket {ticket['ticket_id']} is now being tracked. "
                    f"Recommended resolution: {state['decision'].recommended_action}. "
                    f"Target SLA: {state['decision'].sla_target}."
                )
=======
            state["final_response"] = (
                f"Hi {name}, I investigated your case and created escalation {ticket['ticket_id']}. "
                f"Recommended resolution: {state['decision'].recommended_action}. "
                f"Target SLA: {state['decision'].sla_target}."
            )
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        else:
            state["final_response"] = "I could not complete the autonomous execution, so this case needs manual review."
        state.setdefault("automation_trace", []).append(
            {"stage": "verification", "status": "complete" if verified_ticket else "failed", "summary": "Checked ticket state, policy evidence, and audit readiness."}
        )
<<<<<<< HEAD
        state["workflow_status"] = {
            "phase": "customer_updated" if verified_ticket else "needs_review",
            "owner": "Notification Agent" if verified_ticket else "Human Collaboration Agent",
            "progress": 100 if verified_ticket else 88,
        }
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
        return add_event(state, "Verification Agent", "verify", json.dumps(state["verification"]))

    def reflection_agent(self, state: ERAState) -> ERAState:
        state["reflection_attempts"] = state.get("reflection_attempts", 0) + 1
        state["approval_status"] = "auto_approved"
        return add_event(state, "Reflection Agent", "retry_plan", "Adjusted workflow for one retry after verification failure.")

    def needs_reflection(self, state: ERAState) -> str:
        if state.get("verification", {}).get("ticket_created"):
            return "done"
        if state.get("reflection_attempts", 0) < 1 and state.get("approval_status") == "auto_approved":
            return "reflect"
        return "done"

    def _execution_status(self, state: ERAState) -> str:
        if state.get("ticket"):
            return "completed"
        if state.get("approval_status") == "manual_required":
            return "pending"
        return "failed"

    def _extract_entities(self, message: str) -> dict[str, str | None]:
        lowered = message.lower()
        return {
            "mentions_refund": "yes" if "refund" in lowered else "no",
            "mentions_delay": "yes" if "delay" in lowered or "late" in lowered else "no",
            "mentions_charge": "yes" if "charge" in lowered or "bill" in lowered else "no",
            "urgency": "high" if any(term in lowered for term in ["urgent", "immediately", "asap"]) else "normal",
        }

<<<<<<< HEAD
    def _extract_ticket_id(self, message: str) -> str | None:
        match = re.search(r"\b(?:INC|TKT|CASE)-[A-Z0-9]{6,12}\b", message.upper())
        return match.group(0) if match else None

    def _team_for_issue(self, issue_type: str) -> str:
        return {
            "refund_delay": "Refund Team",
            "flight_delay": "Travel Operations",
            "baggage": "Baggage Recovery Team",
            "billing": "Payments Team",
            "subscription": "Retention Team",
            "account": "Account Security Team",
            "ticket_status": "Support Operations",
            "complaint": "Customer Care Team",
        }.get(issue_type, "Support Triage")

=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
    def _playbook(self, issue_type: str, days_pending: int, tier: str) -> dict:
        tier_bonus = tier in {"platinum", "gold"}
        playbooks = {
            "refund_delay": {
                "recommended_action": "Create finance escalation incident and offer $25 goodwill credit" if tier_bonus and days_pending > 7 else "Create finance escalation incident and send proactive refund status update",
                "rationale": f"Refund has been pending for {days_pending} days; policy threshold is 7 days for proactive escalation.",
                "risk_level": "low",
                "compensation_amount": 25.0 if tier_bonus and days_pending > 7 else 0.0,
                "confidence_score": 0.94,
                "sla_target": "24 business hours",
                "approval_reason": "Low-risk compensation is within auto-approval threshold.",
                "risk_flags": ["payment_gateway_delay", "customer_experience_risk"],
                "next_best_actions": ["Notify customer when finance accepts ticket", "Recheck refund status in 24 hours", "Close ticket after payment confirmation"],
            },
            "flight_delay": {
                "recommended_action": "Create operations incident, offer rebooking options, and issue meal voucher eligibility review",
                "rationale": "Flight delay issue requires passenger care workflow, operational routing, and compensation review.",
                "risk_level": "medium",
                "compensation_amount": 0.0,
                "confidence_score": 0.88,
                "sla_target": "2 hours",
                "approval_reason": "Operational ticket can be created, but compensation depends on jurisdiction and delay duration.",
                "risk_flags": ["time_sensitive", "regulatory_compensation_possible"],
                "next_best_actions": ["Check live flight status", "Offer alternate itinerary", "Send delay notification"],
            },
            "baggage": {
                "recommended_action": "Open baggage trace case, route to airport operations, and schedule 12-hour customer updates",
                "rationale": "Baggage issues require trace creation, airport ops ownership, and recurring customer communication.",
                "risk_level": "medium",
                "compensation_amount": 0.0,
                "confidence_score": 0.86,
                "sla_target": "12 hours",
                "approval_reason": "Trace creation is safe; reimbursements require receipt validation.",
                "risk_flags": ["asset_recovery", "reimbursement_possible"],
                "next_best_actions": ["Collect bag tag number", "Request delivery address", "Review essentials reimbursement"],
            },
            "billing": {
                "recommended_action": "Create payments reconciliation ticket and hold reversal until duplicate-charge verification completes",
                "rationale": "Billing issues require transaction matching and fraud-risk checks before financial reversal.",
                "risk_level": "high",
                "compensation_amount": 0.0,
                "confidence_score": 0.82,
                "sla_target": "48 hours",
                "approval_reason": "Financial reversals are high-risk and require manual approval.",
                "risk_flags": ["financial_control", "fraud_screening_required"],
                "next_best_actions": ["Match transaction IDs", "Check duplicate authorization", "Request manual approver review"],
            },
            "subscription": {
                "recommended_action": "Validate entitlement, apply eligible prorated credit, and update subscription status",
                "rationale": "Subscription issues require entitlement validation and policy-based credit calculation.",
                "risk_level": "low",
                "compensation_amount": 10.0 if tier_bonus else 0.0,
                "confidence_score": 0.84,
                "sla_target": "24 hours",
                "approval_reason": "Low-value account credit is within automation threshold.",
                "risk_flags": ["retention_opportunity"],
                "next_best_actions": ["Confirm desired plan", "Apply retention offer if eligible", "Send updated invoice summary"],
            },
            "account": {
                "recommended_action": "Create secure account recovery ticket and require identity verification before changes",
                "rationale": "Account issues may involve identity-sensitive actions and must be protected by verification.",
                "risk_level": "high",
                "compensation_amount": 0.0,
                "confidence_score": 0.8,
                "sla_target": "4 hours",
                "approval_reason": "Identity-sensitive requests require manual approval.",
                "risk_flags": ["identity_verification_required", "account_takeover_risk"],
                "next_best_actions": ["Run identity checks", "Review login history", "Escalate to security queue"],
            },
<<<<<<< HEAD
            "ticket_status": {
                "recommended_action": "Check existing ticket status and update the customer",
                "rationale": "The customer is asking for progress on an existing support case.",
                "risk_level": "low",
                "compensation_amount": 0.0,
                "confidence_score": 0.9,
                "sla_target": "real-time update",
                "approval_reason": "Reading and sharing ticket status is low risk.",
                "risk_flags": ["customer_waiting"],
                "next_best_actions": ["Find active ticket", "Read latest status", "Share progress update"],
            },
            "complaint": {
                "recommended_action": "Create complaint case, assign customer care owner, and notify the customer",
                "rationale": "A complaint requires a tracked case, internal ownership, and customer-visible follow-up.",
                "risk_level": "low",
                "compensation_amount": 0.0,
                "confidence_score": 0.86,
                "sla_target": "24 hours",
                "approval_reason": "Opening a complaint case is low risk; compensation or exceptions still require review.",
                "risk_flags": ["customer_escalation", "reputation_risk"],
                "next_best_actions": ["Create complaint case", "Assign customer care", "Notify customer with case ID"],
            },
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
            "general": {
                "recommended_action": "Create support triage incident and request missing details",
                "rationale": "Issue is not specific enough for autonomous execution.",
                "risk_level": "medium",
                "compensation_amount": 0.0,
                "confidence_score": 0.62,
                "sla_target": "24 hours",
                "approval_reason": "Manual review recommended due to incomplete classification.",
                "risk_flags": ["low_context"],
                "next_best_actions": ["Ask clarifying question", "Collect order or booking ID", "Route to support triage"],
            },
        }
        return playbooks.get(issue_type, playbooks["general"])
