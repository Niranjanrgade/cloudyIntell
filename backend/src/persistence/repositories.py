from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.persistence.models import (
    ArchitectureQueryModel,
    EvidenceReferenceModel,
    ProviderRunModel,
    RefinementFeedbackModel,
    RunEventModel,
    ValidationFindingModel,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RunRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_query(self, raw_text: str, provider_scope: str, constraints: dict | None = None, optimization_preferences: dict | None = None) -> ArchitectureQueryModel:
        query = ArchitectureQueryModel(
            raw_text=raw_text,
            provider_scope=provider_scope,
            constraints=json.dumps(constraints or {}),
            optimization_preferences=json.dumps(optimization_preferences or {}),
        )
        self.session.add(query)
        self.session.flush()
        providers = [provider_scope] if provider_scope in {"aws", "azure"} else ["aws", "azure"]
        for provider in providers:
            run = ProviderRunModel(query_id=query.query_id, provider=provider)
            self.session.add(run)
        self.session.commit()
        self.session.refresh(query)
        return query

    def get_query(self, query_id: str) -> ArchitectureQueryModel | None:
        return self.session.get(ArchitectureQueryModel, query_id)

    def list_provider_runs(self, query_id: str) -> list[ProviderRunModel]:
        stmt = select(ProviderRunModel).where(ProviderRunModel.query_id == query_id)
        return list(self.session.scalars(stmt))

    def get_provider_run(self, provider_run_id: str) -> ProviderRunModel | None:
        return self.session.get(ProviderRunModel, provider_run_id)

    def update_provider_run(
        self,
        provider_run_id: str,
        *,
        status: str,
        iteration_count: int | None = None,
        accepted: bool | None = None,
        terminal_reason: str | None = None,
        unresolved_findings: int | None = None,
        latest_output: str | None = None,
        failure_reason: str | None = None,
    ) -> ProviderRunModel:
        run = self.session.get(ProviderRunModel, provider_run_id)
        if run is None:
            raise ValueError("Provider run not found")
        run.status = status
        if iteration_count is not None:
            run.iteration_count = iteration_count
        if accepted is not None:
            run.accepted = accepted
        if terminal_reason is not None:
            run.terminal_reason = terminal_reason
        if unresolved_findings is not None:
            run.unresolved_findings = unresolved_findings
        if latest_output is not None:
            run.latest_output = latest_output
        if failure_reason is not None:
            run.failure_reason = failure_reason
        if status in {"accepted", "stopped", "failed"}:
            run.completed_at = _utc_now()
        self.session.commit()
        self.session.refresh(run)
        return run

    def save_findings(self, provider_run_id: str, findings: Iterable[dict]) -> list[ValidationFindingModel]:
        persisted: list[ValidationFindingModel] = []
        for finding in findings:
            model = ValidationFindingModel(
                provider_run_id=provider_run_id,
                iteration=finding.get("iteration", 0),
                domain=finding["domain"],
                outcome=finding["outcome"],
                severity=finding.get("severity", "medium"),
                reason=finding["reason"],
                remediation=finding.get("remediation"),
            )
            self.session.add(model)
            self.session.flush()
            for evidence in finding.get("evidence", []):
                self.session.add(
                    EvidenceReferenceModel(
                        finding_id=model.finding_id,
                        source_uri=evidence.get("source_uri", ""),
                        title=evidence.get("title", "Unknown source"),
                        excerpt=evidence.get("excerpt", ""),
                        availability_status=evidence.get("availability_status", "available"),
                    )
                )
            persisted.append(model)
        self.session.commit()
        return persisted

    def list_findings(self, provider_run_id: str) -> list[ValidationFindingModel]:
        stmt = select(ValidationFindingModel).where(ValidationFindingModel.provider_run_id == provider_run_id)
        return list(self.session.scalars(stmt))

    def add_feedback(self, provider_run_id: str, iteration_from: int, target_domains: list[str], instructions: str, blocking_issues: list[str] | None = None) -> RefinementFeedbackModel:
        feedback = RefinementFeedbackModel(
            provider_run_id=provider_run_id,
            iteration_from=iteration_from,
            target_domains=json.dumps(target_domains),
            instructions=instructions,
            blocking_issues=json.dumps(blocking_issues or []),
        )
        self.session.add(feedback)
        self.session.commit()
        self.session.refresh(feedback)
        return feedback

    def list_feedback(self, provider_run_id: str) -> list[RefinementFeedbackModel]:
        stmt = select(RefinementFeedbackModel).where(RefinementFeedbackModel.provider_run_id == provider_run_id)
        return list(self.session.scalars(stmt))

    def add_event(self, provider_run_id: str, event_type: str, payload: dict) -> RunEventModel:
        event = RunEventModel(provider_run_id=provider_run_id, event_type=event_type, event_payload=json.dumps(payload))
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def list_events(self, provider_run_id: str) -> list[RunEventModel]:
        stmt = select(RunEventModel).where(RunEventModel.provider_run_id == provider_run_id)
        return list(self.session.scalars(stmt))
