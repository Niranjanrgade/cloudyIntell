from __future__ import annotations

from fastapi import APIRouter

from src.api.schemas.runs import HistoryResponse, ProviderRunDetail
from src.persistence.repositories import RunRepository
from src.persistence.session import get_db_session
from src.services.history_service import HistoryService

router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
def get_history(provider: str | None = None) -> HistoryResponse:
    with get_db_session() as session:
        service = HistoryService(RunRepository(session))
        rows = service.get_history(provider=provider)
    for row in rows:
        row["provider_runs"] = [ProviderRunDetail(**provider_run) for provider_run in row["provider_runs"]]
    return HistoryResponse(items=rows)
