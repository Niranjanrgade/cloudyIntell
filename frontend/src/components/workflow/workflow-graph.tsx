import React from "react";
import type { WorkflowEvent } from "../../services/workflow-stream";

interface WorkflowGraphProps {
  events: WorkflowEvent[];
}

const labels: Record<string, string> = {
  generating: "Generating",
  validating: "Validating",
  optimizing: "Optimizing",
  accepted: "Accepted",
  stopped: "Stopped",
};

export function WorkflowGraph({ events }: WorkflowGraphProps) {
  const latest = events.at(-1);
  const status = String((latest?.payload?.status as string | undefined) ?? "generating");

  return (
    <section className="rounded border bg-white p-4">
      <h3 className="text-sm font-semibold">Workflow Graph State</h3>
      <div className="mt-2 grid grid-cols-5 gap-2 text-xs">
        {Object.entries(labels).map(([key, label]) => {
          const active = key === status;
          return (
            <div
              key={key}
              className={`rounded border px-2 py-1 text-center ${active ? "bg-slate-900 text-white" : "bg-slate-50"}`}
            >
              {label}
            </div>
          );
        })}
      </div>
      <p className="mt-3 text-xs text-slate-600">Active node: {latest?.node.id ?? "pending"}</p>
    </section>
  );
}
