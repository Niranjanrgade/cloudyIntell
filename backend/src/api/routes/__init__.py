from fastapi import APIRouter

from src.api.routes.findings import router as findings_router
from src.api.routes.history import router as history_router
from src.api.routes.runs import router as runs_router
from src.api.routes.workflow import router as workflow_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(runs_router)
api_router.include_router(workflow_router)
api_router.include_router(findings_router)
api_router.include_router(history_router)
