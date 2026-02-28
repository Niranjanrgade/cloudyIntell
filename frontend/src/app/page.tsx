"use client";

import { useEffect, useMemo, useState } from "react";

import { QueryForm } from "../components/runs/query-form";
import { RunDetail } from "../components/runs/run-detail";
import { HistoryList } from "../components/runs/history-list";
import { createRun, getRun, type RunDetail } from "../services/runs";

export default function HomePage() {
  const [runId, setRunId] = useState<string | null>(null);
  const [run, setRun] = useState<RunDetail | null>(null);
  const [loading, setLoading] = useState(false);

  const shouldPoll = useMemo(
    () => run?.provider_runs.some((providerRun) => !["accepted", "stopped", "failed"].includes(providerRun.status)) ?? false,
    [run],
  );

  useEffect(() => {
    if (!runId || !shouldPoll) {
      return;
    }
    const timer = setInterval(async () => {
      const updated = await getRun(runId);
      setRun(updated);
    }, 1500);
    return () => clearInterval(timer);
  }, [runId, shouldPoll]);

  return (
    <main className="min-h-screen p-6">
      <h1 className="text-2xl font-semibold">CloudyIntel</h1>
      <p className="mt-2 text-sm">Architecture generation and validation workspace.</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <QueryForm
          loading={loading}
          onSubmit={async (payload) => {
            setLoading(true);
            try {
              const created = await createRun(payload);
              setRunId(created.run_id);
              const detail = await getRun(created.run_id);
              setRun(detail);
            } finally {
              setLoading(false);
            }
          }}
        />
        <RunDetail run={run} runId={runId} />
      </div>

      <div className="mt-4">
        <HistoryList />
      </div>
    </main>
  );
}
