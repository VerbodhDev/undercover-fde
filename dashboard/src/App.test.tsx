import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { App } from "./App";
import type { Claim } from "./api";
import { claim, claimRoutes, fakeBackend, summary } from "./fixtures";

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
