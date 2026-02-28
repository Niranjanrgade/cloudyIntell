import React from "react";
import type { ValidationFinding } from "../../services/runs";

interface EvidenceSummaryProps {
  findings: ValidationFinding[];
}

export function EvidenceSummary({ findings }: EvidenceSummaryProps) {
  return (
    <section className="rounded border bg-white p-4">
      <h3 className="text-sm font-semibold">Evidence Summary</h3>
      <ul className="mt-2 space-y-2 text-xs">
        {findings.length === 0 ? <li className="text-slate-500">No findings loaded.</li> : null}
        {findings.map((finding) => (
          <li key={finding.finding_id} className="rounded border bg-slate-50 p-2">
            <div className="font-medium">{finding.domain} · {finding.outcome.toUpperCase()}</div>
            <div>{finding.reason}</div>
            {finding.evidence.map((evidence, index) => (
              <div key={`${finding.finding_id}-${index}`} className="mt-1 text-slate-600">
                {evidence.title} ({evidence.availability_status})
              </div>
            ))}
          </li>
        ))}
      </ul>
    </section>
  );
}
