import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import get_settings


class FilesystemMCP:
    def save_report(self, run_id: str, payload: dict[str, Any]) -> Path:
        path = get_settings().reports_dir / f"{run_id}.json"
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return path

    def save_logs(self, run_id: str, events: list[dict[str, Any]]) -> Path:
        path = get_settings().audit_dir / f"{run_id}-events.json"
        path.write_text(json.dumps(events, indent=2, default=str), encoding="utf-8")
        return path

    def save_audit_trail(self, run_id: str, payload: dict[str, Any]) -> Path:
        payload = {**payload, "saved_at": datetime.now(timezone.utc).isoformat()}
        path = get_settings().audit_dir / f"{run_id}-audit.json"
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return path
