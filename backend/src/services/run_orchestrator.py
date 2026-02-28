from __future__ import annotations

from src.orchestration.nodes.event_emitter import emit_workflow_event_sync
from src.orchestration.graph.provider_loop import execute_provider_loop
from src.persistence.repositories import RunRepository


class RunOrchestrator:
    def __init__(self, repository: RunRepository):
        self.repository = repository

    def execute_query(self, query_id: str) -> None:
        query = self.repository.get_query(query_id)
        if query is None:
            raise ValueError("Query not found")

        provider_runs = self.repository.list_provider_runs(query.query_id)
        for provider_run in provider_runs:
            emit_workflow_event_sync(
                run_id=query.query_id,
                provider=provider_run.provider,
                event_type="state_transition",
                node_type="domain_generator",
                node_state="active",
                payload={"status": "generating"},
            )
            result = execute_provider_loop(provider=provider_run.provider, query=query.raw_text)
            self.repository.add_event(
                provider_run.provider_run_id,
                "state_transition",
                {"status": result["status"], "iteration_count": result["iteration_count"]},
            )
            emit_workflow_event_sync(
                run_id=query.query_id,
                provider=provider_run.provider,
                event_type="handoff",
                node_type="reducer",
                node_state="completed",
                payload={"from": "domain_generator", "to": "validator"},
            )
            emit_workflow_event_sync(
                run_id=query.query_id,
                provider=provider_run.provider,
                event_type="completion" if result["accepted"] else "validation_result",
                node_type="validator",
                node_state="completed" if result["accepted"] else "failed",
                payload={"terminal_reason": result["terminal_reason"], "unresolved_findings": result["unresolved_findings"]},
            )
            self.repository.update_provider_run(
                provider_run.provider_run_id,
                status=result["status"],
                iteration_count=result["iteration_count"],
                accepted=result["accepted"],
                terminal_reason=result["terminal_reason"],
                unresolved_findings=result["unresolved_findings"],
                latest_output=result["output"],
                failure_reason=result.get("failure_reason") if result["status"] == "failed" else None,
            )
            self.repository.save_findings(provider_run.provider_run_id, result["findings"])
            for feedback in result.get("feedback_history", []):
                self.repository.add_feedback(
                    provider_run.provider_run_id,
                    iteration_from=feedback["iteration_from"],
                    target_domains=feedback["target_domains"],
                    instructions=feedback["instructions"],
                    blocking_issues=feedback.get("blocking_issues", []),
                )
