from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class WorkflowEvent:
    event_id: str
    run_id: str
    provider: str
    event_type: str
    timestamp: str
    node: dict
    payload: dict


class WorkflowEventBus:
    def __init__(self) -> None:
        self._channels: dict[str, list[asyncio.Queue[WorkflowEvent]]] = defaultdict(list)

    @staticmethod
    def _key(run_id: str, provider: str) -> str:
        return f"{run_id}:{provider}"

    def subscribe(self, run_id: str, provider: str) -> asyncio.Queue[WorkflowEvent]:
        queue: asyncio.Queue[WorkflowEvent] = asyncio.Queue()
        self._channels[self._key(run_id, provider)].append(queue)
        return queue

    def unsubscribe(self, run_id: str, provider: str, queue: asyncio.Queue[WorkflowEvent]) -> None:
        key = self._key(run_id, provider)
        listeners = self._channels.get(key, [])
        if queue in listeners:
            listeners.remove(queue)

    async def publish(self, run_id: str, provider: str, event_type: str, node: dict, payload: dict | None = None) -> WorkflowEvent:
        event = WorkflowEvent(
            event_id=str(uuid4()),
            run_id=run_id,
            provider=provider,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            node=node,
            payload=payload or {},
        )
        for queue in self._channels.get(self._key(run_id, provider), []):
            await queue.put(event)
        return event


event_bus = WorkflowEventBus()


def to_sse_message(event: WorkflowEvent) -> str:
    return f"data: {json.dumps(asdict(event))}\n\n"
