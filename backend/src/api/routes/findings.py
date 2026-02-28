from __future__ import annotations

from fastapi import APIRouter

from src.api.schemas.runs import FindingListResponse, ValidationFinding
from src.persistence.repositories import RunRepository
from src.persistence.session import get_db_session
from src.services.findings_service import FindingsService

router = APIRouter()


@router.get("/runs/{run_id}/providers/{provider}/findings", response_model=FindingListResponse)
def list_findings(run_id: str, provider: str) -> FindingListResponse:
    with get_db_session() as session:
        repository = RunRepository(session)
        service = FindingsService(repository)
        findings = service.list_findings_for_provider(query_id=run_id, provider=provider)
    return FindingListResponse(items=[ValidationFinding(**finding) for finding in findings])
