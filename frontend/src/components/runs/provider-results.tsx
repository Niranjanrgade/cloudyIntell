import type { RunDetail } from "../../services/runs";

interface ProviderResultsProps {
  run: RunDetail | null;
}

export function ProviderResults({ run }: ProviderResultsProps) {
  if (!run) {
    return (
      <section className="rounded border bg-white p-4">
        <h2 className="text-lg font-semibold">Provider Results</h2>
        <p className="mt-2 text-sm text-slate-600">Submit a query to view AWS and Azure outputs.</p>
      </section>
    );
  }

  return (
    <section className="rounded border bg-white p-4">
      <h2 className="text-lg font-semibold">Provider Results</h2>
      <div className="mt-3 space-y-3">
        {run.provider_runs.map((providerRun) => (
          <article key={providerRun.provider} className="rounded border p-3">
            <h3 className="text-sm font-semibold uppercase">{providerRun.provider}</h3>
            <p className="mt-1 text-sm">Status: {providerRun.status}</p>
            <p className="text-sm">Iterations: {providerRun.iteration_count}</p>
            <p className="text-sm">Accepted: {providerRun.accepted ? "Yes" : "No"}</p>
            {providerRun.unresolved_findings > 0 ? (
              <p className="mt-1 text-sm text-amber-700">
                Unresolved findings: {providerRun.unresolved_findings}
              </p>
            ) : null}
            {providerRun.failure_reason ? (
              <p className="mt-1 text-sm text-rose-700">Failure reason: {providerRun.failure_reason}</p>
            ) : null}
            {providerRun.latest_output ? (
              <pre className="mt-2 overflow-auto rounded bg-slate-50 p-2 text-xs">{providerRun.latest_output}</pre>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
