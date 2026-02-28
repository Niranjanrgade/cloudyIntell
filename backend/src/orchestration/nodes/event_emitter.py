from __future__ import annotations

import asyncio

from src.services.workflow_events import event_bus


async def emit_workflow_event(run_id: str, provider: str, event_type: str, node_type: str, node_state: str, payload: dict | None = None) -> None:
    await event_bus.publish(
        run_id=run_id,
        provider=provider,
        event_type=event_type,
        node={"id": f"{provider}-{node_type}", "type": node_type, "state": node_state},
        payload=payload or {},
    )


def emit_workflow_event_sync(run_id: str, provider: str, event_type: str, node_type: str, node_state: str, payload: dict | None = None) -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(emit_workflow_event(run_id, provider, event_type, node_type, node_state, payload))
    else:
        loop.create_task(emit_workflow_event(run_id, provider, event_type, node_type, node_state, payload))
