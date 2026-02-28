from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class Provider(StrEnum):
    AWS = "aws"
    AZURE = "azure"


class ProviderRunStatus(StrEnum):
    GENERATING = "generating"
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    ACCEPTED = "accepted"
    STOPPED = "stopped"
    FAILED = "failed"


class NodeType(StrEnum):
    SUPERVISOR = "supervisor"
    DOMAIN_GENERATOR = "domain_generator"
    REDUCER = "reducer"
    VALIDATOR = "validator"
    OPTIMIZER = "optimizer"


class NodeState(StrEnum):
    IDLE = "idle"
    ACTIVE = "active"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class WorkflowNodeSnapshot:
    node_id: str
    node_type: NodeType
    state: NodeState
    iteration: int = 0


@dataclass(slots=True)
class ProviderRunState:
    run_id: str
    provider: Provider
    status: ProviderRunStatus = ProviderRunStatus.GENERATING
    iteration_count: int = 0
    accepted: bool = False
    unresolved_findings: int = 0
    failure_reason: str | None = None
    nodes: dict[str, WorkflowNodeSnapshot] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
