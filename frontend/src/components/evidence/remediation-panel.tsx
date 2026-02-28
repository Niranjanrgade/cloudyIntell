import type { ValidationFinding } from "../../services/runs";

interface RemediationPanelProps {
  findings: ValidationFinding[];
}

export function RemediationPanel({ findings }: RemediationPanelProps) {
  const failed = findings.filter((finding) => finding.outcome === "fail");

  return (
    <section className="rounded border bg-white p-4">
      <h3 className="text-sm font-semibold">Remediation Guidance</h3>
      <ul className="mt-2 space-y-2 text-xs">
        {failed.length === 0 ? <li className="text-slate-500">No remediation needed.</li> : null}
        {failed.map((finding) => (
          <li key={finding.finding_id} className="rounded border bg-rose-50 p-2">
            <div className="font-medium">{finding.domain}</div>
            <div>{finding.remediation ?? "No remediation provided."}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
