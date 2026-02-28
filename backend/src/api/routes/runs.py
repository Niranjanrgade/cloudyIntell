from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.api.schemas.runs import CreateRunRequest, CreateRunResponse, ProviderRunDetail, RunDetail
from src.persistence.repositories import RunRepository
from src.persistence.session import get_db_session
from src.services.run_orchestrator import RunOrchestrator

router = APIRouter()


@router.post("/runs", response_model=CreateRunResponse, status_code=202)
def create_run(payload: CreateRunRequest) -> CreateRunResponse:
    with get_db_session() as session:
        repository = RunRepository(session)
        query = repository.create_query(
            raw_text=payload.query,
            provider_scope=payload.provider_scope,
            constraints=payload.constraints,
            optimization_preferences=payload.optimization_preferences,
        )
        orchestrator = RunOrchestrator(repository)
        orchestrator.execute_query(query.query_id)
        run_id = query.query_id
    return CreateRunResponse(run_id=run_id, status="running")


@router.get("/runs/{run_id}", response_model=RunDetail)
def get_run(run_id: str) -> RunDetail:
    with get_db_session() as session:
        repository = RunRepository(session)
        query = repository.get_query(run_id)
        if query is None:
            raise HTTPException(status_code=404, detail="Run not found")

        provider_runs = repository.list_provider_runs(query.query_id)
        return RunDetail(
            run_id=query.query_id,
            query=query.raw_text,
            provider_scope=query.provider_scope,
            provider_runs=[
                ProviderRunDetail(
                    provider=run.provider,
                    status=run.status,
                    iteration_count=run.iteration_count,
                    accepted=run.accepted,
                    terminal_reason=run.terminal_reason,
                    unresolved_findings=run.unresolved_findings,
                    latest_output=run.latest_output,
                    failure_reason=run.failure_reason,
                )
                for run in provider_runs
            ],
        )
