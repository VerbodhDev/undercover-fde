import { useEffect, useState } from "react";
import { listClaims, type ClaimSummary, type Status } from "./api";
import { label, money, statusLabels } from "./format";

const QUEUE_POLL_MS = 5000;

export function StatusChip({ status }: Readonly<{ status: Status }>) {
  return <span className={`chip ${status}`}>{statusLabels[status]}</span>;
}

export function Queue() {
  const [claims, setClaims] = useState<ClaimSummary[] | null>(null);

  useEffect(() => {
    void listClaims().then(setClaims);
    const timer = setInterval(() => {
      void listClaims().then(setClaims);
    }, QUEUE_POLL_MS);
    return () => {
      clearInterval(timer);
    };
  }, []);

  if (!claims) return <p className="muted">Loading the queue</p>;

  const statuses = Object.keys(statusLabels) as Status[];
  return (
    <section className="stack">
      <h1>Claims queue</h1>
      <ul className="counts">
        {statuses.map((status) => (
          <li key={status} className="panel">
            <span className="count">
              {claims.filter((c) => c.status === status).length}
            </span>
            <StatusChip status={status} />
          </li>
        ))}
      </ul>
      <div className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>Claim</th>
              <th>Customer</th>
              <th>Type</th>
              <th className="num">Claimed</th>
              <th>State</th>
            </tr>
          </thead>
          <tbody>
            {claims.map((claim) => (
              <tr key={claim.claim_id}>
                <td>
                  <a className="mono" href={`#/claims/${claim.claim_id}`}>
                    {claim.claim_id}
                  </a>
                  <div className="muted small">{claim.summary}</div>
                </td>
                <td>{claim.customer_name}</td>
                <td>{label(claim.claim_type)}</td>
                <td className="num mono">{money(claim.amount_claimed)}</td>
                <td>
                  <StatusChip status={claim.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
