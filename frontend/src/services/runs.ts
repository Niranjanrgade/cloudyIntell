import { apiRequest } from "./api-client";

export type Provider = "aws" | "azure";
export type ProviderScope = Provider | "both";

export interface CreateRunRequest {
  query: string;
  provider_scope: ProviderScope;
  constraints?: Record<string, unknown>;
  optimization_preferences?: Record<string, unknown>;
}

export interface CreateRunResponse {
  run_id: string;
  status: "queued" | "running";
}

export interface ProviderRunDetail {
  provider: Provider;
  status: "generating" | "validating" | "optimizing" | "accepted" | "stopped" | "failed";
  iteration_count: number;
  accepted: boolean;
  terminal_reason?: string;
  unresolved_findings: number;
  latest_output?: string;
  failure_reason?: string;
}

export interface RunDetail {
  run_id: string;
  query: string;
  provider_scope: ProviderScope;
  provider_runs: ProviderRunDetail[];
}

export interface EvidenceReference {
  source_uri: string;
  title: string;
  excerpt?: string;
  availability_status: "available" | "unavailable";
}

export interface ValidationFinding {
  finding_id: string;
  iteration: number;
  domain: "compute" | "storage" | "network" | "database" | "cross_domain";
  outcome: "pass" | "fail" | "warn";
  severity: "critical" | "high" | "medium" | "low";
  reason: string;
  remediation?: string;
  evidence: EvidenceReference[];
}

export async function createRun(payload: CreateRunRequest): Promise<CreateRunResponse> {
  return apiRequest<CreateRunResponse>("/api/v1/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getRun(runId: string): Promise<RunDetail> {
  return apiRequest<RunDetail>(`/api/v1/runs/${runId}`);
}

export async function getHistory(provider?: Provider): Promise<{ items: RunDetail[] }> {
  const suffix = provider ? `?provider=${provider}` : "";
  return apiRequest<{ items: RunDetail[] }>(`/api/v1/history${suffix}`);
}

export async function getFindings(runId: string, provider: Provider): Promise<{ items: ValidationFinding[] }> {
  return apiRequest<{ items: ValidationFinding[] }>(`/api/v1/runs/${runId}/providers/${provider}/findings`);
}
