from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class ArchitectureQueryModel(Base):
    __tablename__ = "architecture_queries"

    query_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String(255), default="local-workspace")
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    provider_scope: Mapped[str] = mapped_column(String(16), nullable=False)
    constraints: Mapped[str | None] = mapped_column(Text)
    optimization_preferences: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)

    provider_runs: Mapped[list[ProviderRunModel]] = relationship(back_populates="query")


class ProviderRunModel(Base):
    __tablename__ = "provider_runs"

    provider_run_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    query_id: Mapped[str] = mapped_column(String(36), ForeignKey("architecture_queries.query_id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="generating")
    iteration_count: Mapped[int] = mapped_column(Integer, default=0)
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    terminal_reason: Mapped[str | None] = mapped_column(String(64))
    unresolved_findings: Mapped[int] = mapped_column(Integer, default=0)
    latest_output: Mapped[str | None] = mapped_column(Text)
    failure_reason: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    query: Mapped[ArchitectureQueryModel] = relationship(back_populates="provider_runs")
    findings: Mapped[list[ValidationFindingModel]] = relationship(back_populates="provider_run")
    events: Mapped[list[RunEventModel]] = relationship(back_populates="provider_run")
    feedback_items: Mapped[list[RefinementFeedbackModel]] = relationship(back_populates="provider_run")


class ValidationFindingModel(Base):
    __tablename__ = "validation_findings"

    finding_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("provider_runs.provider_run_id"), nullable=False)
    iteration: Mapped[int] = mapped_column(Integer, default=0)
    domain: Mapped[str] = mapped_column(String(32), nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    remediation: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)

    provider_run: Mapped[ProviderRunModel] = relationship(back_populates="findings")
    evidence: Mapped[list[EvidenceReferenceModel]] = relationship(back_populates="finding")


class EvidenceReferenceModel(Base):
    __tablename__ = "evidence_references"

    evidence_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    finding_id: Mapped[str] = mapped_column(String(36), ForeignKey("validation_findings.finding_id"), nullable=False)
    source_uri: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    availability_status: Mapped[str] = mapped_column(String(16), default="available")

    finding: Mapped[ValidationFindingModel] = relationship(back_populates="evidence")


class RunEventModel(Base):
    __tablename__ = "run_events"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("provider_runs.provider_run_id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    event_payload: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)

    provider_run: Mapped[ProviderRunModel] = relationship(back_populates="events")


class RefinementFeedbackModel(Base):
    __tablename__ = "refinement_feedback"

    feedback_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("provider_runs.provider_run_id"), nullable=False)
    iteration_from: Mapped[int] = mapped_column(Integer, nullable=False)
    target_domains: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    blocking_issues: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)

    provider_run: Mapped[ProviderRunModel] = relationship(back_populates="feedback_items")
