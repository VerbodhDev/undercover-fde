"""Work the claims queue: uv run -m agent [CLAIM_ID ...]."""

import sys
import uuid

from agent.main import backend, run


def main(claim_ids: list[str]) -> None:
    """Run the agent on the claims given, or on every waiting claim in queue order."""
    if not claim_ids:
        with backend() as client:
            claims = client.get("/api/claims").json()
        claim_ids = [c["claim_id"] for c in claims if c["status"] == "waiting"]
    for claim_id in claim_ids:
        print(f"{claim_id}: {run(claim_id, f'{claim_id}-{uuid.uuid4().hex[:8]}')}")


if __name__ == "__main__":
    main(sys.argv[1:])
