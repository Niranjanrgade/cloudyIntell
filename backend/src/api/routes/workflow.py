from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.services.workflow_events import event_bus, to_sse_message

router = APIRouter()


@router.get("/runs/{run_id}/providers/{provider}/events/stream")
async def stream_workflow_events(run_id: str, provider: str) -> StreamingResponse:
    queue = event_bus.subscribe(run_id, provider)

    async def generator() -> AsyncGenerator[str, None]:
        try:
            yield ": connected\n\n"
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15)
                    yield to_sse_message(event)
                except TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            event_bus.unsubscribe(run_id, provider, queue)

    return StreamingResponse(generator(), media_type="text/event-stream")
