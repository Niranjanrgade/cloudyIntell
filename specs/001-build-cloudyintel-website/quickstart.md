# Quickstart: CloudyIntel Architecture Website

## Purpose
Run CloudyIntel locally to submit architecture queries, observe provider-separated workflow graphs, review validation evidence/remediation, and inspect persisted run history.

## Prerequisites
- Python 3.14+ available locally
- Node.js 20+ and npm/pnpm
- Local access to curated AWS and Azure documentation corpus for retrieval
- Local/dev environment only (no authentication by design)

## 1) Backend setup (FastAPI + LangGraph/LangChain)
1. Create and activate a Python environment.
2. Install backend dependencies (FastAPI, Uvicorn, LangChain, LangGraph, SQLite driver, test tools).
3. Configure environment values:
   - `CLOUDYINTEL_ENV=local`
   - `EVIDENCE_CORPUS_PATH=<workspace-local-path>`
   - `RUN_DB_PATH=<workspace-local-path>/cloudyintel_runs.db`
4. Start API server on `http://localhost:8000`.

Example:

```bash
cd backend
uv run uvicorn src.api.app:app --reload --port 8000
```

## 2) Frontend setup (Next.js + CopilotKit)
1. Install frontend dependencies (Next.js, React, CopilotKit, graph visualization dependencies).
2. Configure frontend environment:
   - `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
   - `NEXT_PUBLIC_CLOUDYINTEL_MODE=local`
3. Start frontend on `http://localhost:3000`.

Example:

```bash
cd frontend
npm install
npm run dev
```

## 3) Verify core behavior
1. Open UI and confirm local/dev banner is visible (auth disabled).
2. Submit AWS-only query:
   - Verify graph shows generating -> validating -> accepted or stopped.
   - Verify findings include evidence references.
3. Submit Azure-only query with stricter constraints to force refinement:
   - Verify optimize cycle appears.
   - Verify max 3 iterations.
4. Submit both-provider query:
   - Verify two separated provider outputs and timelines.
5. Simulate evidence-unavailable scenario for one provider:
   - Verify provider output marked not validated.
   - Verify remediation actions are present.

## 4) History and restart validation
1. Complete at least one run.
2. Refresh browser and restart local services.
3. Verify run history persists and remains traceable by run ID and provider.

## 5) Testing checklist
- Backend: run unit and integration tests for orchestration, provider separation, and evidence gating.
- Frontend: run component tests for graph state rendering and evidence panel.
- E2E: run flow tests for AWS-only, Azure iterative refinement, both-provider separation, and evidence-unavailable path.

Example:

```bash
cd backend && uv run pytest
cd ../frontend && npm run test && npm run test:e2e
```

## Troubleshooting
- If runs never reach accepted: inspect validation findings and evidence availability flags.
- If graph stalls: inspect SSE stream endpoint and backend run event emission.
- If history missing after restart: validate `RUN_DB_PATH` points to persistent workspace-local location.