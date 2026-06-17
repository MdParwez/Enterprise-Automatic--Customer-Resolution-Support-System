# Enterprise Resolution Agent

Enterprise Resolution Agent (ERA) is a production-style agentic AI support platform. It investigates customer issues, retrieves operational context, applies policies, executes actions through MCP-style tools, verifies outcomes, and records learnings for evaluation.

The project is designed to run locally without external credentials, while preserving clear integration points for OpenAI or Azure OpenAI, Qdrant, ServiceNow MCP, Filesystem MCP, Database MCP, and LangSmith.

## Architecture

```text
HTML UI -> FastAPI -> LangGraph workflow
                    -> SQLite
                    -> Qdrant-ready knowledge layer
                    -> MCP tool adapters
                    -> Audit and evaluation logs
```

Agents:

- Supervisor Agent
- Customer Agent
- Booking/Order Agent
- Knowledge Agent
- Resolution Agent
- Approval Agent
- Execution Agent
- Verification Agent
- Reflection Agent

## Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\seed_data.py
uvicorn src.api.main:app --reload --port 8000
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Resolution cockpit: http://127.0.0.1:8000

## Example Request

```json
{
  "customer_id": "CUST-1001",
  "message": "My refund is delayed.",
  "channel": "chat"
}
```

## Environment

Optional variables:

```text
OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
QDRANT_URL=
QDRANT_API_KEY=
SERVICENOW_INSTANCE_URL=
SERVICENOW_TOKEN=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=enterprise-resolution-agent
```

Without these values, ERA uses local deterministic resolution logic, SQLite, in-memory knowledge retrieval, and mock ServiceNow MCP behavior.

## UI Capabilities

- Case intake with reusable sample issues
- Resolution summary with confidence, risk, SLA, compensation, and approval status
- Agent automation trace
- Policy and historical-case evidence
- Verification results
- Recent run history
- Coverage across refunds, flight delays, baggage, billing, subscriptions, and account recovery
