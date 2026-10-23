# Status

The claims pilot, built from `docs/PLAN.md`. Done so far: phases 1 to 3.

- `backend/`: FastAPI on SQLite. `backend/store.py` creates `backend/undercover.db` (or the file in
  `UNDERCOVER_DB`) and seeds it from `data/` on first start: the 25 claims, the policies and the
  customers. Read routes for claims, policies, claim history, the policy wording and the handlers,
  and the write routes: start a claim, record steps, record a decision, pay and sign off. A payout
  over $1,000 (`payout_approval_limit` in `data/company.json`) is refused until a handler signs off,
  and sign-off pays it.
- `backend/instructions.md`: the agent's instructions, served by `GET /api/instructions`.
- `agent/`: the UnderCover Agent. Six tools (`get_claim`, `get_policy`, `get_claim_history`,
  `get_policy_wording`, `record_decision`, `pay_claim`) that call the backend over HTTP. `run()`
  starts the claim and posts each step to the backend. It has no sign-off tool.
- `dashboard/`: still the backend health page.

## Run it

```bash
npm run dev      # backend on :8000, dashboard on :5173
```

With the backend running, work the queue (every waiting claim) or chosen claims:

```bash
npm run agent              # or: uv run -m agent CLM-1001 CLM-1002
```

The model is `openai/gpt-6-luna`, or `MODEL_NAME` from `.env` (such as `openrouter/free`).

To reset the data, stop the backend and delete `backend/undercover.db`.
