from __future__ import annotations

from src.persistence.repositories import RunRepository
from src.retrieval.evidence_mapper import normalize_evidence_reference


class FindingsService:
    def __init__(self, repository: RunRepository):
        self.repository = repository

    def list_findings_for_provider(self, query_id: str, provider: str) -> list[dict]:
        provider_runs = self.repository.list_provider_runs(query_id)
        provider_run = next((run for run in provider_runs if run.provider == provider), None)
        if provider_run is None:
            return []

        findings = self.repository.list_findings(provider_run.provider_run_id)
        return [
            {
                "finding_id": finding.finding_id,
                "iteration": finding.iteration,
                "domain": finding.domain,
                "outcome": finding.outcome,
                "severity": finding.severity,
                "reason": finding.reason,
                "remediation": finding.remediation,
                "evidence": [
                    normalize_evidence_reference(
                        source_uri=evidence.source_uri,
                        title=evidence.title,
                        excerpt=evidence.excerpt,
                        availability_status=evidence.availability_status,
                    )
                    for evidence in finding.evidence
                ],
            }
            for finding in findings
        ]
