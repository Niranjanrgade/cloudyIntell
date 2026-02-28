"use client";

import { useEffect, useState } from "react";

import { getFindings, type RunDetail as RunDetailType, type ValidationFinding } from "../../services/runs";
import type { WorkflowEvent } from "../../services/workflow-stream";
import { subscribeWorkflowEvents } from "../../services/workflow-stream";
import { EvidenceSummary } from "../evidence/evidence-summary";
import { RemediationPanel } from "../evidence/remediation-panel";
import { ProviderResults } from "./provider-results";
import { HandoffTimeline } from "../workflow/handoff-timeline";
import { WorkflowGraph } from "../workflow/workflow-graph";

interface RunDetailProps {
  runId: string | null;
  run: RunDetailType | null;
}

export function RunDetail({ runId, run }: RunDetailProps) {
  const [events, setEvents] = useState<WorkflowEvent[]>([]);
  const [findings, setFindings] = useState<ValidationFinding[]>([]);

  useEffect(() => {
    if (!runId || !run) {
      return;
    }

    const unsubscribers = run.provider_runs
      .filter((providerRun) => providerRun.provider === "aws" || providerRun.provider === "azure")
      .map((providerRun) =>
        subscribeWorkflowEvents(runId, providerRun.provider, (event) => {
          setEvents((existing: WorkflowEvent[]) => [...existing, event]);
        }),
      );

    return () => {
      unsubscribers.forEach((unsubscribe) => unsubscribe());
    };
  }, [runId, run]);

  useEffect(() => {
    if (!runId || !run) {
      return;
    }

    const loadFindings = async () => {
      const responses = await Promise.all(
        run.provider_runs
          .filter((providerRun) => providerRun.provider === "aws" || providerRun.provider === "azure")
          .map((providerRun) => getFindings(runId, providerRun.provider)),
      );
      setFindings(responses.flatMap((response) => response.items));
    };

    void loadFindings();
  }, [runId, run]);

  return (
    <div className="space-y-4">
      <WorkflowGraph events={events} />
      <HandoffTimeline events={events} />
      <ProviderResults run={run} />
      <EvidenceSummary findings={findings} />
      <RemediationPanel findings={findings} />
    </div>
  );
}
