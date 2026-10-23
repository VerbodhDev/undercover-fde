"""The UnderCover backend."""

import json
import sqlite3
from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException

from backend import store

app = FastAPI(title="UnderCover")


def get_db() -> Iterator[sqlite3.Connection]:
    """Give each request its own connection to the store."""
    conn = store.connect()
    try:
        yield conn
    finally:
        conn.close()


Db = Annotated[sqlite3.Connection, Depends(get_db)]


def claim_row(db: sqlite3.Connection, claim_id: str) -> sqlite3.Row:
    """Return the claim's row, or raise 404."""
    row = db.execute("SELECT * FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"Claim {claim_id} not found")
    return row


def record(db: sqlite3.Connection, table: str, key: str, value: str) -> dict[str, Any]:
    """Return one policy or customer record, or raise 404."""
    row = db.execute(f"SELECT data FROM {table} WHERE {key} = ?", (value,)).fetchone()  # noqa: S608
    if row is None:
        raise HTTPException(404, f"{value} not found")
    return json.loads(row["data"])


def customer_name(db: sqlite3.Connection, customer_id: str) -> str:
    """Return the customer's name."""
    return record(db, "customers", "customer_id", customer_id)["name"]


def claim_view(db: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    """Combine the claim as filed with where it stands now."""
    claim = json.loads(row["data"])
    claim.pop("status")
    return {
        **claim,
        "customer_name": customer_name(db, claim["customer_id"]),
        "status": row["status"],
        "decision": row["decision"],
        "payout": row["payout"],
        "reason": row["reason"],
        "policy_section": row["policy_section"],
        "paid_amount": row["paid_amount"],
        "signed_off_by": row["signed_off_by"],
    }


@app.get("/api/health", operation_id="health")
def health() -> dict[str, str]:
    """Check that the backend is running."""
    return {"status": "ok"}


@app.get("/api/claims", operation_id="list_claims")
def list_claims(db: Db) -> list[dict[str, Any]]:
    """List the claims queue in order, with where each claim stands."""
    rows = db.execute("SELECT * FROM claims ORDER BY position").fetchall()
    fields = ["claim_id", "summary", "claim_type", "amount_claimed", "customer_name"]
    fields += ["status", "decision", "payout", "paid_amount"]
    return [{f: v for f, v in claim_view(db, r).items() if f in fields} for r in rows]


@app.get("/api/claims/{claim_id}", operation_id="get_claim")
def get_claim(claim_id: str, db: Db) -> dict[str, Any]:
    """Get one claim in full: the story, the items, the documents and its decision."""
    return claim_view(db, claim_row(db, claim_id))


@app.get("/api/policies/{policy_id}", operation_id="get_policy")
def get_policy(policy_id: str, db: Db) -> dict[str, Any]:
    """Get a policy: the plan, the add-ons, the trip and the travelers."""
    return record(db, "policies", "policy_id", policy_id)


@app.get("/api/customers/{customer_id}/claims", operation_id="get_claim_history")
def get_claim_history(customer_id: str, db: Db) -> list[dict[str, Any]]:
    """Get the customer's earlier claims, with the outcome and amount paid."""
    return record(db, "customers", "customer_id", customer_id)["previous_claims"]


@app.get("/api/policy-wording", operation_id="get_policy_wording")
def get_policy_wording() -> dict[str, str]:
    """Get the policy wording, the contract that decisions follow."""
    return {"text": (store.DATA / "policy_wording.md").read_text(encoding="utf-8")}


@app.get("/api/handlers", operation_id="list_handlers")
def list_handlers() -> list[dict[str, Any]]:
    """List the claims handlers."""
    return store.load("handlers.json")
