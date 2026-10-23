# Status

The claims pilot, built from `docs/PLAN.md`. Done so far: phases 1 and 2.

- `backend/`: FastAPI on SQLite. `backend/store.py` creates `backend/undercover.db` (or the file in
  `UNDERCOVER_DB`) and seeds it from `data/` on first start: the 25 claims, the policies and the
  customers. Read routes for claims, policies, claim history, the policy wording and the handlers,
  and the write routes: start a claim, record steps, record a decision, pay and sign off. A payout
  over $1,000 (`payout_approval_limit` in `data/company.json`) is refused until a handler signs off,
  and sign-off pays it.
- `agent/`: still the hello-world agent.
- `dashboard/`: still the backend health page.

## Run it

```bash
npm run dev      # backend on :8000, dashboard on :5173
```

To reset the data, stop the backend and delete `backend/undercover.db`.
