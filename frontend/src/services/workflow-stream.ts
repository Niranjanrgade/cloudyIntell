export interface WorkflowEvent {
  event_id: string;
  run_id: string;
  provider: "aws" | "azure";
  iteration?: number;
  event_type: "state_transition" | "handoff" | "validation_result" | "retry" | "failure" | "completion";
  timestamp: string;
  node: {
    id: string;
    type: "supervisor" | "domain_generator" | "reducer" | "validator" | "optimizer";
    state: "idle" | "active" | "waiting" | "completed" | "failed";
  };
  payload: Record<string, unknown>;
}

export function subscribeWorkflowEvents(runId: string, provider: "aws" | "azure", onEvent: (event: WorkflowEvent) => void): () => void {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const source = new EventSource(`${base}/api/v1/runs/${runId}/providers/${provider}/events/stream`);

  source.onmessage = (event) => {
    try {
      const parsed = JSON.parse(event.data) as WorkflowEvent;
      onEvent(parsed);
    } catch {
      // ignore malformed event payloads
    }
  };

  source.onerror = () => {
    source.close();
  };

  return () => source.close();
}
