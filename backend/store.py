"""The UnderCover store: SQLite, seeded from data/ on first use."""

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DATA = Path(__file__).parent.parent / "data"
DEFAULT_DB = Path(__file__).parent / "undercover.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    position INTEGER NOT NULL,
    data TEXT NOT NULL,
    status TEXT NOT NULL,
    decision TEXT,
    payout REAL,
    reason TEXT,
    policy_section TEXT,
    paid_amount REAL,
    signed_off_by TEXT
);
CREATE TABLE IF NOT EXISTS policies (policy_id TEXT PRIMARY KEY, data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS customers (customer_id TEXT PRIMARY KEY, data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    text TEXT NOT NULL
);
"""


def load(name: str) -> Any:
    """Read one JSON file from data/."""
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def seed(conn: sqlite3.Connection) -> None:
    """Copy the queue, the policies and the customers from data/."""
    claims = load("claims.json")
    conn.executemany(
        "INSERT INTO claims (claim_id, position, data, status) VALUES (?, ?, ?, ?)",
        [(c["claim_id"], i, json.dumps(c), "waiting") for i, c in enumerate(claims)],
    )
    conn.executemany(
        "INSERT INTO policies VALUES (?, ?)",
        [(p["policy_id"], json.dumps(p)) for p in load("policies.json")],
    )
    conn.executemany(
        "INSERT INTO customers VALUES (?, ?)",
        [(c["customer_id"], json.dumps(c)) for c in load("customers.json")],
    )


def connect() -> sqlite3.Connection:
    """Open the database named in UNDERCOVER_DB, creating and seeding it if new."""
    conn = sqlite3.connect(os.getenv("UNDERCOVER_DB", str(DEFAULT_DB)))
    conn.row_factory = sqlite3.Row
    with conn:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0] == 0:
            seed(conn)
    return conn
