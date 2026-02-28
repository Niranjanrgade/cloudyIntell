from __future__ import annotations

import json

from sqlalchemy import select

from src.persistence.models import ArchitectureQueryModel
from src.persistence.repositories import RunRepository


class HistoryService:
    def __init__(self, repository: RunRepository):
        self.repository = repository

    def get_history(self, provider: str | None = None) -> list[dict]:
        session = self.repository.session
        query_rows = session.scalars(select(ArchitectureQueryModel).order_by(ArchitectureQueryModel.created_at.desc())).all()
        history = []

        for query in query_rows:
            runs = self.repository.list_provider_runs(query.query_id)
            if provider:
                runs = [run for run in runs if run.provider == provider]
            if not runs:
                continue

            provider_runs = []
            for run in runs:
                feedback = [
                    {
                        "feedback_id": entry.feedback_id,
                        "iteration_from": entry.iteration_from,
                        "target_domains": json.loads(entry.target_domains),
                        "instructions": entry.instructions,
                        "blocking_issues": json.loads(entry.blocking_issues or "[]"),
                    }
                    for entry in self.repository.list_feedback(run.provider_run_id)
                ]
                provider_runs.append(
                    {
                        "provider": run.provider,
                        "status": run.status,
                        "iteration_count": run.iteration_count,
                        "accepted": run.accepted,
                        "terminal_reason": run.terminal_reason,
                        "unresolved_findings": run.unresolved_findings,
                        "latest_output": run.latest_output,
                        "failure_reason": run.failure_reason,
                        "refinement_feedback": feedback,
                    }
                )

            history.append(
                {
                    "run_id": query.query_id,
                    "query": query.raw_text,
                    "provider_scope": query.provider_scope,
                    "created_at": query.created_at,
                    "provider_runs": provider_runs,
                }
            )

        return history
