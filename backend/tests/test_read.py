import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import store
from backend.main import app

client = TestClient(app)


def test_queue_is_seeded_from_claims_json():
    queue_ids = [
        c["claim_id"] for c in json.loads(Path("data/claims.json").read_text())
    ]
    claims = client.get("/api/claims").json()
    assert [c["claim_id"] for c in claims] == queue_ids
    assert len(claims) == 25
    assert {c["status"] for c in claims} == {"waiting"}
    assert "CLM-1901" not in queue_ids


def test_list_claims_fields():
    first = client.get("/api/claims").json()[0]
    assert first == {
        "claim_id": "CLM-1001",
        "summary": "Flight home canceled by the airline, rebooked the next morning",
        "claim_type": "trip_delay",
        "amount_claimed": 420.0,
        "customer_name": "Maya Patel",
        "status": "waiting",
        "decision": None,
        "payout": None,
        "paid_amount": None,
    }


def test_get_claim():
    claim = client.get("/api/claims/CLM-1001").json()
    assert claim["story"].startswith("My flight home from Rome")
    assert len(claim["items"]) == 3
    assert len(claim["documents"]) == 4
    assert claim["status"] == "waiting"


def test_get_policy():
    policy = client.get("/api/policies/POL-2001").json()
    assert policy["plan"] == "premium"
    assert policy["trip"]["destination"] == "Rome, Italy"


def test_claim_history_has_no_personal_details():
    response = client.get("/api/customers/CUS-3001/claims")
    assert [c["claim_id"] for c in response.json()] == ["CLM-0412"]
    for field in ["email", "phone", "address", "date_of_birth", "Jersey City"]:
        assert field not in response.text


def test_policy_wording():
    text = client.get("/api/policy-wording").json()["text"]
    assert text == Path("data/policy_wording.md").read_text(encoding="utf-8")


def test_handlers():
    handlers = client.get("/api/handlers").json()
    assert [h["handler_id"] for h in handlers] == ["HND-01", "HND-02", "HND-03"]


@pytest.mark.parametrize(
    "path",
    [
        "/api/claims/CLM-0000",
        "/api/policies/POL-0000",
        "/api/customers/CUS-0000/claims",
    ],
)
def test_unknown_is_404(path):
    assert client.get(path).status_code == 404


def test_opening_twice_does_not_reseed():
    store.connect().close()
    conn = store.connect()
    assert conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0] == 25
    assert conn.execute("SELECT COUNT(*) FROM policies").fetchone()[0] == 50
    conn.close()


def test_instructions():
    text = client.get("/api/instructions").json()["text"]
    assert text == Path("backend/instructions.md").read_text(encoding="utf-8")
    assert "section 10" in text
