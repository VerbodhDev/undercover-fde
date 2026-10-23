import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from agent import __main__ as runner
from agent import main
from backend.main import app


class StubModel(GenericFakeChatModel):
    """A chat model that gives scripted replies in place of a real model."""

    def bind_tools(self, tools, **kwargs):
        return self


@pytest.fixture(autouse=True)
def in_process_backend(monkeypatch):
    monkeypatch.setattr(main, "backend", lambda: TestClient(app))
    monkeypatch.setattr(runner, "backend", lambda: TestClient(app))


def calls(*tool_calls):
    """An AI message that calls the given tools, as (name, args) pairs."""
    return AIMessage(
        content="",
        tool_calls=[
            {"name": name, "args": args, "id": str(i)}
            for i, (name, args) in enumerate(tool_calls)
        ],
    )


def decision(payout):
    return {
        "claim_id": "CLM-1001",
        "decision": "approve",
        "payout": payout,
        "reason": "The flight was canceled for a crew problem. The costs are covered.",
        "policy_section": "3. Trip Delay",
    }


def test_get_claim():
    assert json.loads(main.get_claim.invoke({"claim_id": "CLM-1001"}))["policy_id"] == (
        "POL-2001"
    )


def test_get_policy():
    policy = json.loads(main.get_policy.invoke({"policy_id": "POL-2001"}))
    assert policy["plan"] == "premium"


def test_get_claim_history():
    history = json.loads(main.get_claim_history.invoke({"customer_id": "CUS-3001"}))
    assert history[0]["claim_id"] == "CLM-0412"


def test_get_policy_wording():
    assert "Trip Delay" in json.loads(main.get_policy_wording.invoke({}))["text"]


def test_record_decision_and_pay():
    claim = json.loads(main.record_decision.invoke(decision(420.0)))
    assert claim["status"] == "decided"
    args = {"claim_id": "CLM-1001", "amount": 420.0}
    assert json.loads(main.pay_claim.invoke(args))["paid_amount"] == 420.0


def test_refusal_comes_back_as_text():
    reply = main.pay_claim.invoke({"claim_id": "CLM-1001", "amount": 420.0})
    assert reply.startswith("Refused (409)")


def test_run_approves_and_pays():
    replies = [
        calls(
            ("get_claim", {"claim_id": "CLM-1001"}),
            ("get_policy", {"policy_id": "POL-2001"}),
        ),
        calls(
            ("get_claim_history", {"customer_id": "CUS-3001"}),
            ("get_policy_wording", {}),
        ),
        calls(("record_decision", decision(420.0))),
        calls(("pay_claim", {"claim_id": "CLM-1001", "amount": 420.0})),
        AIMessage(content="Approved, $420.00."),
    ]
    reply = main.run("CLM-1001", "thread-1", StubModel(messages=iter(replies)))
    assert reply == "Approved, $420.00."
    client = TestClient(app)
    claim = client.get("/api/claims/CLM-1001").json()
    assert claim["status"] == "decided"
    assert claim["paid_amount"] == 420.0
    steps = client.get("/api/claims/CLM-1001/steps").json()
    assert len(steps) >= 6
    assert steps[0] == {
        "id": steps[0]["id"],
        "kind": "tool_call",
        "text": ('get_claim({"claim_id": "CLM-1001"})'),
    }
    assert steps[-1]["text"] == "Approved, $420.00."


def test_run_cannot_pay_over_the_limit():
    replies = [
        calls(("record_decision", decision(1250.0))),
        calls(("pay_claim", {"claim_id": "CLM-1001", "amount": 1250.0})),
        AIMessage(content="Approved, $1,250.00, waiting for sign-off."),
    ]
    main.run("CLM-1001", "thread-1", StubModel(messages=iter(replies)))
    client = TestClient(app)
    claim = client.get("/api/claims/CLM-1001").json()
    assert claim["status"] == "waiting_for_sign_off"
    assert claim["paid_amount"] is None
    results = [s["text"] for s in client.get("/api/claims/CLM-1001/steps").json()]
    assert any(r.startswith("pay_claim: Refused (403)") for r in results)


def test_runner_works_waiting_claims_in_order(monkeypatch):
    TestClient(app).post(
        "/api/claims/CLM-1002/decision",
        json={**decision(0), "decision": "decline"},
    )
    worked = []
    monkeypatch.setattr(
        runner, "run", lambda claim_id, thread_id: worked.append(claim_id)
    )
    runner.main([])
    queue = [c["claim_id"] for c in json.loads(Path("data/claims.json").read_text())]
    assert worked == [c for c in queue if c != "CLM-1002"]


def test_runner_works_claims_given(monkeypatch):
    worked = []
    monkeypatch.setattr(
        runner, "run", lambda claim_id, thread_id: worked.append(claim_id)
    )
    runner.main(["CLM-1003", "CLM-1001"])
    assert worked == ["CLM-1003", "CLM-1001"]


def test_agent_never_reads_data():
    for source in Path("agent").glob("*.py"):
        assert "data/" not in source.read_text(encoding="utf-8")


def test_model_name(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.delenv("MODEL_NAME", raising=False)
    assert main.model().model_name == "openai/gpt-6-luna"
    monkeypatch.setenv("MODEL_NAME", "openrouter/free")
    assert main.model().model_name == "openrouter/free"
