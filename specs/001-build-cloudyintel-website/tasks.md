# Tasks: CloudyIntel Architecture Website

**Input**: Design documents from `/specs/001-build-cloudyintel-website/`
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Include test tasks because the specification defines mandatory testing scenarios and independent story verification.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize backend/frontend workspaces and baseline tooling for local/dev execution.

- [X] T001 Create backend project scaffold in backend/pyproject.toml and backend/src/__init__.py
- [X] T002 Create frontend Next.js + TypeScript scaffold in frontend/package.json and frontend/src/app/page.tsx
- [X] T003 [P] Add backend environment template for local mode in backend/.env.example
- [X] T004 [P] Add frontend environment template for API base URL and mode in frontend/.env.example
- [X] T005 [P] Configure backend test tooling in backend/pytest.ini and backend/tests/conftest.py
- [X] T006 [P] Configure frontend test tooling in frontend/vitest.config.ts and frontend/playwright.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement core orchestration, persistence, API shell, and shared UI infrastructure required by all user stories.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T007 Implement SQLite models and session management for core entities in backend/src/persistence/models.py and backend/src/persistence/session.py
- [X] T008 [P] Implement repository layer for queries/runs/events/findings in backend/src/persistence/repositories.py
- [X] T009 [P] Define shared Pydantic API schemas from contract types in backend/src/api/schemas/runs.py
- [X] T010 Implement FastAPI app factory, middleware, and router registration in backend/src/api/app.py and backend/src/api/routes/__init__.py
- [X] T011 [P] Implement LangGraph shared state models and transition enums in backend/src/orchestration/state/models.py
- [X] T012 [P] Implement provider-isolated run context builder in backend/src/orchestration/state/provider_context.py
- [X] T013 Implement workflow event bus and SSE publisher abstraction in backend/src/services/workflow_events.py
- [X] T014 [P] Implement frontend API client and query hooks foundation in frontend/src/services/api-client.ts and frontend/src/services/runs.ts
- [X] T015 [P] Implement global app shell with local/dev banner and provider theme tokens in frontend/src/app/layout.tsx and frontend/src/components/app/dev-banner.tsx

**Checkpoint**: Foundation ready; user stories can be delivered independently.

---

## Phase 3: User Story 1 - Generate Validated Architecture by Provider (Priority: P1) 🎯 MVP

**Goal**: Accept a query and deliver provider-separated AWS/Azure architecture outputs through recursive generation-validation loops with iteration cap and best-result fallback.

**Independent Test**: Submit one AWS-only and one Azure-only query and verify provider-specific outputs with no cross-provider contamination, plus iterative retry behavior up to 3 rounds.

### Tests for User Story 1

- [X] T016 [P] [US1] Add contract tests for create/get run endpoints in backend/tests/contract/test_runs_api.py
- [X] T017 [P] [US1] Add integration tests for provider separation and max-iteration stopping in backend/tests/integration/test_provider_loops.py
- [X] T018 [P] [US1] Add integration test for evidence-unavailable not-validated outcome in backend/tests/integration/test_evidence_unavailable.py

### Implementation for User Story 1

- [X] T019 [P] [US1] Implement domain generator agent interfaces (compute/storage/network/database) in backend/src/agents/generator/domain_generators.py
- [X] T020 [P] [US1] Implement domain validator agent interfaces with remediation output in backend/src/agents/validator/domain_validators.py
- [X] T021 [US1] Implement architecture reducer/coordinator for provider proposals in backend/src/orchestration/nodes/reducer.py
- [X] T022 [US1] Implement recursive evaluator-optimizer loop node chain in backend/src/orchestration/graph/provider_loop.py
- [X] T023 [US1] Implement evidence-gated acceptance logic and terminal reason assignment in backend/src/services/acceptance_policy.py
- [X] T024 [US1] Implement POST /api/v1/runs and GET /api/v1/runs/{runId} routes in backend/src/api/routes/runs.py
- [X] T025 [US1] Implement backend orchestration service that executes per-provider runs in backend/src/services/run_orchestrator.py
- [X] T026 [US1] Implement query submission UI with provider-scope selector in frontend/src/components/runs/query-form.tsx
- [X] T027 [US1] Implement separated provider results view with unresolved findings indicator in frontend/src/components/runs/provider-results.tsx
- [X] T028 [US1] Wire run submission and polling lifecycle in frontend/src/app/page.tsx
- [X] T029 [US1] Document US1 run behavior and stopping semantics in docs/runbooks/cloudyintel-user-guide.md

**Checkpoint**: US1 is fully functional and independently testable as MVP.

---

## Phase 4: User Story 2 - Observe Agent Workflow and Hand-offs (Priority: P2)

**Goal**: Provide live graph visibility of node states, transitions, hand-offs, and optimization cycles during execution.

**Independent Test**: Run a query that triggers at least one failed validation and confirm the UI graph shows active node transitions and optimize/retry state changes in sequence.

### Tests for User Story 2

- [X] T030 [P] [US2] Add contract test for SSE workflow stream endpoint in backend/tests/contract/test_workflow_stream_api.py
- [X] T031 [P] [US2] Add frontend unit test for graph node state rendering and transitions in frontend/tests/unit/workflow-graph.test.tsx
- [X] T032 [P] [US2] Add e2e test for hand-off and optimization cycle visibility in frontend/tests/e2e/workflow-visibility.spec.ts

### Implementation for User Story 2

- [X] T033 [US2] Implement GET /api/v1/runs/{runId}/providers/{provider}/events/stream endpoint in backend/src/api/routes/workflow.py
- [X] T034 [US2] Emit typed workflow events from LangGraph node transitions in backend/src/orchestration/nodes/event_emitter.py
- [X] T035 [US2] Implement frontend SSE subscription and reconnection handling in frontend/src/services/workflow-stream.ts
- [X] T036 [US2] Implement workflow graph component with generating/validating/optimizing/accepted/stopped states in frontend/src/components/workflow/workflow-graph.tsx
- [X] T037 [US2] Implement hand-off timeline panel bound to streamed events in frontend/src/components/workflow/handoff-timeline.tsx
- [X] T038 [US2] Integrate workflow graph and timeline into run detail screen in frontend/src/components/runs/run-detail.tsx
- [X] T039 [US2] Document workflow state semantics and troubleshooting in docs/runbooks/cloudyintel-operator-runbook.md

**Checkpoint**: US2 is independently testable with transparent graph-state visibility.

---

## Phase 5: User Story 3 - Review Validation Evidence and Feedback (Priority: P3)

**Goal**: Expose domain-level evidence summaries and actionable remediation feedback for accepted/rejected validation outcomes.

**Independent Test**: Force a validation failure and verify every rejected decision shows reason, evidence reference, and improvement guidance.

### Tests for User Story 3

- [X] T040 [P] [US3] Add contract test for findings endpoint payload shape in backend/tests/contract/test_findings_api.py
- [X] T041 [P] [US3] Add backend integration test for evidence mapping and remediation population in backend/tests/integration/test_findings_evidence.py
- [X] T042 [P] [US3] Add frontend unit test for evidence and remediation panels in frontend/tests/unit/evidence-panel.test.tsx

### Implementation for User Story 3

- [X] T043 [US3] Implement findings query service with evidence joins in backend/src/services/findings_service.py
- [X] T044 [US3] Implement GET /api/v1/runs/{runId}/providers/{provider}/findings route in backend/src/api/routes/findings.py
- [X] T045 [US3] Implement evidence reference normalization for provider-authoritative sources in backend/src/retrieval/evidence_mapper.py
- [X] T046 [US3] Implement validation evidence summary UI component in frontend/src/components/evidence/evidence-summary.tsx
- [X] T047 [US3] Implement remediation guidance panel for failed findings in frontend/src/components/evidence/remediation-panel.tsx
- [X] T048 [US3] Integrate findings/evidence panels into run detail page in frontend/src/components/runs/run-detail.tsx
- [X] T049 [US3] Document evidence interpretation and remediation usage in docs/runbooks/cloudyintel-user-guide.md

**Checkpoint**: US3 is independently testable with complete evidence and feedback visibility.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Complete history, quality hardening, and end-to-end validation across stories.

- [X] T050 Implement GET /api/v1/history endpoint with provider filter in backend/src/api/routes/history.py
- [X] T051 [P] Implement persisted history list UI and run replay entry points in frontend/src/components/runs/history-list.tsx
- [X] T052 [P] Add e2e regression for AWS-only, Azure iterative loop, dual-provider split, and evidence-unavailable path in frontend/tests/e2e/core-flows.spec.ts
- [X] T053 [P] Add backend performance/integration test for workflow transition latency budget in backend/tests/integration/test_workflow_latency.py
- [X] T054 Validate and update local setup and verification instructions in specs/001-build-cloudyintel-website/quickstart.md
- [X] T055 Final documentation pass for user and operator deliverables in docs/runbooks/cloudyintel-user-guide.md and docs/runbooks/cloudyintel-operator-runbook.md
- [X] T056 [US1] Implement partial-result payloads and domain failure reason propagation in backend/src/services/run_orchestrator.py and backend/src/api/schemas/runs.py
- [X] T057 [P] [US1] Add integration test for domain-timeout/domain-failure partial results in backend/tests/integration/test_partial_results.py
- [X] T058 [US1] Render partial results and failure reasons in frontend/src/components/runs/provider-results.tsx
- [X] T059 Implement refinement-feedback linkage persistence/query in backend/src/persistence/repositories.py and backend/src/services/history_service.py
- [X] T060 [P] Add integration test for iteration-to-feedback traceability in backend/tests/integration/test_history_feedback_linkage.py
- [X] T061 Update history API response to include refinement feedback linkage metadata in backend/src/api/routes/history.py and backend/src/api/schemas/runs.py

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): no dependencies.
- Foundational (Phase 2): depends on Setup; blocks all user stories.
- User Stories (Phases 3-5): depend on Foundational completion.
- Polish (Phase 6): depends on completion of desired user stories.

### User Story Dependencies

- US1 (P1): starts after Foundational; no dependency on US2/US3.
- US2 (P2): starts after Foundational; consumes run/workflow primitives built in Foundational.
- US3 (P3): starts after Foundational; independent from US2 except shared run detail surface.

### Within Each User Story

- Tests first, then implementation.
- Backend services/routes before frontend integration.
- Story documentation update before marking story complete.

### Dependency Graph (Story Completion Order)

- Foundational -> US1 -> Polish
- Foundational -> US2 -> Polish
- Foundational -> US3 -> Polish

---

## Parallel Execution Examples

### User Story 1

```bash
T016 + T017 + T018
T019 + T020
```

### User Story 2

```bash
T030 + T031 + T032
T035 + T036 + T037
```

### User Story 3

```bash
T040 + T041 + T042
T046 + T047
```

---

## Implementation Strategy

### MVP First (US1)

1. Complete Phase 1 and Phase 2.
2. Deliver Phase 3 (US1) and validate independent test criteria.
3. Demo/deploy local MVP.

### Incremental Delivery

1. Add US2 for workflow transparency.
2. Add US3 for evidence/remediation drill-down.
3. Finish with Phase 6 cross-cutting hardening and docs.

### Parallel Team Strategy

1. Team converges on Setup + Foundational.
2. After Foundational, assign US1/US2/US3 streams to separate developers.
3. Integrate at Phase 6 with e2e and documentation validation.

---

## Notes

- All tasks follow required checklist format: `- [ ] T### [P?] [US?] Description with file path`.
- `[P]` tasks target separate files and can run concurrently.
- Story labels are used only in user-story phases.
- Each story remains independently testable against its own acceptance criteria.