import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from src.config import get_settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    tier TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS refunds (
    refund_id TEXT PRIMARY KEY,
    booking_id TEXT NOT NULL,
    status TEXT NOT NULL,
    days_pending INTEGER NOT NULL,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS agent_runs (
    run_id TEXT PRIMARY KEY,
    issue_type TEXT NOT NULL,
    decision TEXT NOT NULL,
    outcome TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
"""


@contextmanager
def db_connection() -> Iterator[sqlite3.Connection]:
    path = get_settings().database_path
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database(path: Path | None = None) -> None:
    if path is not None:
        get_settings().database_path = path
    with db_connection() as connection:
        connection.executescript(SCHEMA)


def seed_database() -> None:
    initialize_database()
    with db_connection() as connection:
        connection.executemany(
            "INSERT OR IGNORE INTO customers(customer_id, name, email, tier) VALUES (?, ?, ?, ?)",
            [
                ("CUST-1001", "Aarav Mehta", "aarav.mehta@example.com", "platinum"),
                ("CUST-1002", "Maya Singh", "maya.singh@example.com", "gold"),
                ("CUST-1003", "Noah Carter", "noah.carter@example.com", "standard"),
            ],
        )
        connection.executemany(
            "INSERT OR IGNORE INTO bookings(booking_id, customer_id, status) VALUES (?, ?, ?)",
            [
                ("BOOK-7001", "CUST-1001", "cancelled"),
                ("BOOK-7002", "CUST-1002", "completed"),
                ("BOOK-7003", "CUST-1003", "delayed"),
            ],
        )
        connection.executemany(
            "INSERT OR IGNORE INTO refunds(refund_id, booking_id, status, days_pending) VALUES (?, ?, ?, ?)",
            [
                ("REF-9001", "BOOK-7001", "processing", 12),
                ("REF-9002", "BOOK-7002", "completed", 1),
            ],
        )


def fetch_one(query: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    with db_connection() as connection:
        row = connection.execute(query, params).fetchone()
        return dict(row) if row else None


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with db_connection() as connection:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def create_ticket(ticket_id: str, customer_id: str, issue_type: str, status: str) -> None:
    with db_connection() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO tickets(ticket_id, customer_id, issue_type, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (ticket_id, customer_id, issue_type, status, datetime.now(timezone.utc).isoformat()),
        )


def record_agent_run(run_id: str, issue_type: str, decision: str, outcome: str) -> None:
    with db_connection() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO agent_runs(run_id, issue_type, decision, outcome, timestamp) VALUES (?, ?, ?, ?, ?)",
            (run_id, issue_type, decision, outcome, datetime.now(timezone.utc).isoformat()),
        )
