import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { App } from "./App";
import type { Claim, ClaimSummary } from "./api";

export const summary: ClaimSummary = {
  claim_id: "CLM-1001",
  summary: "Flight home canceled",
  claim_type: "trip_delay",
  amount_claimed: 420,
  customer_name: "Maya Patel",
  status: "waiting",
  decision: null,
  payout: null,
  paid_amount: null,
};

export const claim: Claim = {
  ...summary,
  policy_id: "POL-2001",
  customer_id: "CUS-3001",
  submitted_on: "2026-06-24",
  incident_date: "2026-06-18",
  incident_location: "Rome, Italy",
  story: "My flight home from Rome was canceled.",
  items: [
    { description: "Airport hotel", category: "accommodation", amount: 245 },
  ],
  documents: [
    { name: "Hotel receipt", type: "receipt", content: "Total $245.00." },
  ],
  reason: null,
  policy_section: null,
  signed_off_by: null,
};

const policy = {
  policy_id: "POL-2001",
  plan: "premium",
  add_ons: [],
  purchased_on: "2026-04-22",
  trip: {
    destination: "Rome, Italy",
    departs_on: "2026-06-10",
    returns_on: "2026-06-18",
    trip_cost: 3100,
  },
  travelers: ["Maya Patel"],
};

const history = [
  {
    claim_id: "CLM-0412",
    filed_on: "2024-08-19",
    claim_type: "baggage_delay",
    summary: "Bag arrived late",
    outcome: "approved",
    amount_paid: 140,
  },
];

export function fakeBackend(routes: Record<string, unknown>) {
  const fetchMock = vi.fn((path: string) => {
    if (!(path in routes))
      return Promise.resolve(new Response("", { status: 404 }));
    return Promise.resolve(new Response(JSON.stringify(routes[path])));
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

export const claimRoutes = (loaded: Claim, steps: unknown[] = []) => ({
  "/api/claims/CLM-1001": loaded,
  "/api/claims/CLM-1001/steps": steps,
  "/api/policies/POL-2001": policy,
  "/api/customers/CUS-3001/claims": history,
  "/api/handlers": [
    {
      handler_id: "HND-01",
      name: "Dana Whitfield",
      role: "Senior Claims Handler",
    },
  ],
});

beforeEach(() => {
  window.location.hash = "";
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

it("shows the queue with a count per state", async () => {
  fakeBackend({
    "/api/claims": [
      summary,
      {
        ...summary,
        claim_id: "CLM-1002",
        status: "decided",
        amount_claimed: 1250,
      },
    ],
  });
  render(<App />);
  expect(await screen.findByRole("link", { name: "CLM-1001" })).toBeDefined();
  expect(screen.getByText("$1,250.00")).toBeDefined();
  expect(screen.getAllByText("Trip delay")).toHaveLength(2);
  expect(screen.getAllByText("Waiting")).toHaveLength(2);
  expect(screen.getAllByText("Decided")).toHaveLength(2);
});

it("shows a claim in full before it is decided", async () => {
  fakeBackend(claimRoutes(claim));
  window.location.hash = "#/claims/CLM-1001";
  render(<App />);
  expect(
    await screen.findByText("My flight home from Rome was canceled."),
  ).toBeDefined();
  expect(
    screen.getByText("The agent has not decided this claim yet."),
  ).toBeDefined();
  expect(screen.getByText("Total $245.00.")).toBeDefined();
  expect(await screen.findByText("Premium")).toBeDefined();
  expect(await screen.findByText(/Bag arrived late/)).toBeDefined();
  expect(screen.getByText("No steps yet.")).toBeDefined();
});

it("shows the decision, its reasons and the steps", async () => {
  const decided: Claim = {
    ...claim,
    status: "decided",
    decision: "approve",
    payout: 420,
    paid_amount: 420,
    reason: "The delay is covered.",
    policy_section: "3. Trip Delay",
  };
  const steps = [
    { id: 1, kind: "tool_call", text: 'get_claim({"claim_id": "CLM-1001"})' },
    { id: 2, kind: "reply", text: "Approved, $420.00." },
  ];
  fakeBackend(claimRoutes(decided, steps));
  window.location.hash = "#/claims/CLM-1001";
  render(<App />);
  expect(await screen.findByText("The delay is covered.")).toBeDefined();
  expect(screen.getByText("Policy section: 3. Trip Delay")).toBeDefined();
  expect(screen.getByText("Paid $420.00")).toBeDefined();
  expect(await screen.findByText("Approved, $420.00.")).toBeDefined();
});

it("shows the instructions read only", async () => {
  fakeBackend({
    "/api/instructions": { text: "You are the UnderCover Agent." },
  });
  window.location.hash = "#/instructions";
  render(<App />);
  expect(
    await screen.findByText("You are the UnderCover Agent."),
  ).toBeDefined();
  expect(screen.queryByRole("textbox")).toBeNull();
});

it("follows the hash from the queue to a claim", async () => {
  fakeBackend({ "/api/claims": [summary], ...claimRoutes(claim) });
  render(<App />);
  await screen.findByRole("link", { name: "CLM-1001" });
  window.location.hash = "#/claims/CLM-1001";
  window.dispatchEvent(new HashChangeEvent("hashchange"));
  expect(
    await screen.findByText("My flight home from Rome was canceled."),
  ).toBeDefined();
});
