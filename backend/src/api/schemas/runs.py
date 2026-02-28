from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


Provider = Literal["aws", "azure"]
ProviderScope = Literal["aws", "azure", "both"]


class CreateRunRequest(BaseModel):
    query: str = Field(min_length=1)
    provider_scope: ProviderScope
    constraints: dict[str, Any] = Field(default_factory=dict)
    optimization_preferences: dict[str, Any] = Field(default_factory=dict)


class CreateRunResponse(BaseModel):
    run_id: str
    status: Literal["queued", "running"] = "running"


class EvidenceReference(BaseModel):
    source_uri: str
    title: str
    excerpt: str | None = None
    availability_status: Literal["available", "unavailable"] = "available"


class ValidationFinding(BaseModel):
    finding_id: str
    iteration: int
    domain: Literal["compute", "storage", "network", "database", "cross_domain"]
    outcome: Literal["pass", "fail", "warn"]
    severity: Literal["critical", "high", "medium", "low"]
    reason: str
    remediation: str | None = None
    evidence: list[EvidenceReference] = Field(default_factory=list)


class ProviderRunDetail(BaseModel):
    provider: Provider
    status: Literal["generating", "validating", "optimizing", "accepted", "stopped", "failed"]
    iteration_count: int
    accepted: bool
    terminal_reason: str | None = None
    unresolved_findings: int = 0
    latest_output: str | None = None
    failure_reason: str | None = None
    refinement_feedback: list[dict[str, Any]] = Field(default_factory=list)


class RunDetail(BaseModel):
    run_id: str
    query: str
    provider_scope: ProviderScope
    provider_runs: list[ProviderRunDetail]


class HistoryItem(BaseModel):
    run_id: str
    query: str
    provider_scope: ProviderScope
    created_at: datetime
    provider_runs: list[ProviderRunDetail]


class HistoryResponse(BaseModel):
    items: list[HistoryItem]


class FindingListResponse(BaseModel):
    items: list[ValidationFinding]
