from uuid import uuid4

from src.database.sqlite import create_ticket, fetch_one


class ServiceNowMCP:
    def create_incident(self, customer_id: str, issue_type: str, description: str) -> dict:
        ticket_id = f"INC-{uuid4().hex[:8].upper()}"
        create_ticket(ticket_id=ticket_id, customer_id=customer_id, issue_type=issue_type, status="open")
        return {
            "ticket_id": ticket_id,
            "status": "open",
            "description": description,
            "provider": "local-servicenow-mock",
        }

    def get_incident(self, ticket_id: str) -> dict | None:
        return fetch_one("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))

    def update_incident(self, ticket_id: str, status: str) -> dict:
        return {"ticket_id": ticket_id, "status": status}

    def close_incident(self, ticket_id: str) -> dict:
        return {"ticket_id": ticket_id, "status": "closed"}
