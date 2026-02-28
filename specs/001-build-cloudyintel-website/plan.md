# Implementation Plan: CloudyIntel Architecture Website

**Branch**: `001-build-cloudyintel-website` | **Date**: 2026-02-28 | **Spec**: `/specs/001-build-cloudyintel-website/spec.md`
**Input**: Feature specification from `/specs/001-build-cloudyintel-website/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a local/dev-only web application that accepts architecture queries and runs provider-separated AWS/Azure recursive generator-validator loops with a max of 3 refinements, evidence-grounded validation, and transparent workflow visualization. The implementation uses a FastAPI backend with LangGraph orchestration and LangChain-powered generation/validation, plus a CopilotKit-compatible React frontend to show live graph states, validation evidence, remediation feedback, and persisted run history.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.14+ (from `pyproject.toml`) for backend, TypeScript 5.x for frontend  
**Primary Dependencies**: FastAPI, Pydantic, Uvicorn, LangChain, LangGraph, CopilotKit, React (Next.js), TanStack Query, Tailwind CSS  
**Storage**: Local SQLite (run metadata/history) + local filesystem artifact cache for evidence snapshots  
**Testing**: `pytest` (backend unit/integration), `vitest` + React Testing Library (frontend unit), Playwright (critical flow e2e)  
**Target Platform**: Local/dev deployment on macOS/Linux with modern Chromium-based browser
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: Align with SC-001 and SC-005: provider result within 5 minutes for valid queries; workflow state visibility within 2 seconds of backend transition  
**Constraints**: Max 3 refinement iterations per provider; strict AWS/Azure state separation; no authentication; acceptance blocked if required evidence unavailable  
**Scale/Scope**: Single-workspace local usage, one active query per session, run history persisted per workspace

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Evaluator-optimizer loop is explicit, with accept/reject transitions and feedback paths.
- Domain orchestration is defined (supervisor delegation + reducer/coordinator synthesis).
- Validation design is RAG-grounded with authoritative vendor evidence and remediation output.
- AWS and Azure flows are separated with provider-specific constraints and checks.
- UI/interaction plan includes graph-state transparency and agent hand-off visibility.
- Documentation deliverables are enumerated (feature docs, runbook/quickstart impact).

Gate result (pre-Phase 0): **PASS**
- Recursive loop: Explicit generate → validate → feedback → refine transitions with stop at 3 iterations.
- Domain orchestration: Supervisor delegates compute/storage/network/database tasks and reducer synthesizes provider proposals.
- RAG validation: Validator requires retriever-backed evidence references and remediation guidance for failures.
- Provider separation: Independent provider run state, evidence, and outcomes for AWS vs Azure.
- Transparency: UI contract includes graph node transitions, active state, and hand-offs.
- Documentation: User and operator quickstart/runbook artifacts included in plan outputs.

Gate result (post-Phase 1 design): **PASS**
- `research.md` defines evaluator-optimizer policy, provider separation, and evidence-gated acceptance.
- `data-model.md` includes explicit run and node states, transition guards, and iteration caps.
- `contracts/openapi.yaml` and `contracts/workflow-event.schema.json` specify external interfaces for status, evidence, and workflow visibility.
- `quickstart.md` enumerates local/dev operation constraints and verification for required UX/documentation outcomes.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── orchestration/
│   │   ├── graph/
│   │   ├── nodes/
│   │   └── state/
│   ├── agents/
│   │   ├── generator/
│   │   └── validator/
│   ├── retrieval/
│   ├── persistence/
│   └── services/
└── tests/
  ├── unit/
  ├── integration/
  └── contract/

frontend/
├── src/
│   ├── app/
│   ├── components/
│   │   ├── workflow/
│   │   ├── evidence/
│   │   └── runs/
│   ├── lib/
│   └── services/
└── tests/
  ├── unit/
  └── e2e/

docs/
└── runbooks/
```

**Structure Decision**: Use a web application split with `backend/` (FastAPI + LangGraph/LangChain orchestration) and `frontend/` (Next.js React + CopilotKit UI). This structure directly supports independent API/orchestration concerns, real-time workflow visibility, and provider-separated run persistence while keeping test suites aligned by boundary.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
