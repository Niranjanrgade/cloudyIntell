# Research: CloudyIntel Architecture Website

## Decision 1: Use LangGraph as the orchestration runtime for provider loops
- Decision: Model each provider run (AWS/Azure) as an independent LangGraph execution path with explicit state transitions for generate, validate, optimize, accepted, and stopped.
- Rationale: LangGraph provides deterministic, inspectable graph transitions that map directly to constitution requirements for auditable recursive loops and UI-visible workflow state.
- Alternatives considered: Custom async workflow engine (higher implementation risk and lower observability consistency); Celery-style task chains (weaker graph-native transition semantics).

## Decision 2: Use LangChain for domain generation and validator prompts/tools
- Decision: Implement compute/storage/network/database domain agents and validation agents using LangChain abstractions with shared prompt templates and tool interfaces.
- Rationale: LangChain gives reusable abstractions for LLM calls, retrieval, prompt composition, and tool execution that reduce custom glue code and simplify provider-specific specialization.
- Alternatives considered: Raw model SDK orchestration (more boilerplate and harder provider/domain consistency); fully custom agent framework (slower delivery).

## Decision 3: RAG validation must use provider-authoritative sources only
- Decision: Restrict validation evidence to curated AWS and Azure documentation corpora, returning evidence references per finding and blocking acceptance when required evidence is unavailable.
- Rationale: Directly enforces constitution principle III and FR-023/FR-024 for factual validation and explicit non-validation handling.
- Alternatives considered: Open-web retrieval (higher risk of non-authoritative or stale sources); no evidence requirement (violates constitution and feature requirements).

## Decision 4: Separate AWS and Azure execution state end-to-end
- Decision: Keep provider runs isolated in graph state, persistence records, validation evidence, and UI presentation; never merge provider reasoning artifacts before final display composition.
- Rationale: Satisfies FR-008/FR-009 and constitution principle IV, preventing cross-provider contamination.
- Alternatives considered: Shared intermediate state with provider labels (higher contamination risk); unified optimization loop (violates provider fidelity requirement).

## Decision 5: Backend API with FastAPI + SSE for workflow updates
- Decision: Expose REST endpoints for run lifecycle/history and stream workflow transitions through Server-Sent Events.
- Rationale: FastAPI aligns with Python stack and typed schemas; SSE is simple for one-way real-time status and works well in local/dev environments without websocket complexity.
- Alternatives considered: WebSockets (more bidirectional complexity than required for current UX); polling-only updates (fails responsiveness target for visible transitions).

## Decision 6: Frontend framework is Next.js (React) with CopilotKit
- Decision: Build the UI in Next.js App Router using CopilotKit for assistant interaction surfaces and custom graph/evidence views.
- Rationale: Next.js + React is natively compatible with CopilotKit patterns and supports rapid implementation of stateful workflow views.
- Alternatives considered: Plain Vite React (valid, but weaker convention support for integrated app routing/runtime features); Vue/Angular (extra integration effort with CopilotKit ecosystem).

## Decision 7: Persist run history in workspace-local SQLite
- Decision: Store provider runs, iteration rounds, findings, evidence references, and event timeline in SQLite under workspace-local storage.
- Rationale: Meets FR-021/FR-022 persistence requirements with zero external infrastructure and reliable restart durability.
- Alternatives considered: JSON files only (harder querying and linkage across runs/iterations); Postgres (unnecessary operational overhead for local/dev scope).

## Decision 8: Testing strategy by boundary (backend, frontend, end-to-end)
- Decision: Use pytest for backend graph/service tests, vitest for frontend component/state tests, and Playwright for core user flows (single-provider, dual-provider, evidence-unavailable).
- Rationale: Validates critical behavior where failures are likely while keeping toolchain standard and maintainable.
- Alternatives considered: Backend-only tests (insufficient for workflow transparency UX); heavy e2e-only coverage (slower feedback and weaker fault isolation).

## Decision 9: Iteration stopping and best-result semantics
- Decision: Enforce maximum 3 refinement iterations per provider; if acceptance is not reached, return best draft with unresolved findings and remediation actions.
- Rationale: Implements clarified requirement and prevents infinite optimization loops while preserving user value from partial progress.
- Alternatives considered: Unlimited retries (non-deterministic runtime and poor UX); immediate failure on first validation miss (drops optimizer value).

## Decision 10: Documentation artifacts are first-class delivery items
- Decision: Deliver user-facing quickstart/usage guidance plus operator runbook notes for monitoring, failure handling, and evidence corpus maintenance.
- Rationale: Required by FR-016/FR-017 and constitution principle V.
- Alternatives considered: Inline code comments only (insufficient for users/operators); deferred docs after implementation (violates quality gate).