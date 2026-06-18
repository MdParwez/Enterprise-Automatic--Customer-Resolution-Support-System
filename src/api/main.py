from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.agents.workflow import AgentWorkflow
from src.database.sqlite import fetch_all
from src.models import CustomerIssue, ManualExecutionRequest, ResolutionResponse

app = FastAPI(title="Enterprise Resolution Agent", version="0.1.0")
workflow = AgentWorkflow()
WEB_DIR = Path(__file__).resolve().parents[2] / "web"
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (WEB_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-resolution-agent"}


@app.post("/resolve", response_model=ResolutionResponse)
def resolve_issue(issue: CustomerIssue) -> ResolutionResponse:
    return workflow.run(issue)


@app.post("/manual/execute")
def manual_execute(request: ManualExecutionRequest) -> dict:
    description = (
        f"Manual approval by {request.approver}. Action: {request.recommended_action}. "
        f"Approval note: {request.note or 'No note provided.'}"
    )
    ticket = workflow.servicenow.create_incident(
        customer_id=request.customer_id,
        issue_type=request.issue_type,
        description=description,
    )
    return {
        "status": "approved_and_executed",
        "ticket_id": ticket["ticket_id"],
        "ticket_status": ticket["status"],
        "approver": request.approver,
    }


@app.get("/customers")
def customers() -> list[dict]:
    return fetch_all("SELECT * FROM customers ORDER BY customer_id")


@app.get("/runs")
def runs() -> list[dict]:
    return fetch_all("SELECT * FROM agent_runs ORDER BY timestamp DESC LIMIT 25")


@app.get("/stats")
def stats() -> dict[str, int]:
    rows = fetch_all(
        """
        SELECT
            (SELECT COUNT(*) FROM agent_runs) AS total_queries,
            (SELECT COUNT(*) FROM agent_runs WHERE outcome = 'completed') AS auto_resolved,
            (SELECT COUNT(*) FROM agent_runs WHERE outcome = 'pending') AS pending_review,
            (SELECT COUNT(*) FROM tickets) AS tickets_created
        """
    )
    return rows[0] if rows else {"total_queries": 0, "auto_resolved": 0, "pending_review": 0, "tickets_created": 0}


@app.get("/capabilities")
def capabilities() -> dict:
    return {
        "issue_types": ["refund_delay", "flight_delay", "baggage", "billing", "subscription", "account"],
        "features": [
            "Multi-agent LangGraph orchestration",
            "Policy and historical-case RAG",
            "MCP-style tool execution",
            "Human approval gates",
            "Verification and reflection loop",
            "Audit logs and metrics",
            "Risk scoring and SLA recommendations",
        ],
    }
