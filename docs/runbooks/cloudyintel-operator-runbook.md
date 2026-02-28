# CloudyIntel Operator Runbook

## Workflow state semantics
- `generating`: Domain agents are producing architecture candidates.
- `validating`: Validator agents evaluate generated decisions with evidence.
- `optimizing`: Failed findings are fed back for refinement.
- `accepted`: Provider output passed required validation.
- `stopped`: Iteration cap or evidence-unavailable gate reached.

## Workflow event troubleshooting
- If SSE stream is silent, verify backend event emission and stream endpoint availability.
- If graph transitions lag, inspect event backlog and API process health.
- If hand-off events are missing, confirm reducer/validator transition emits events.

## Failure handling
- For `evidence_unavailable`, refresh evidence corpus and rerun.
- For `iteration_limit`, inspect unresolved findings and tighten query constraints.

## Run monitoring
- Monitor `/health` and `/api/v1/history` for service state and run completion patterns.
- Track high unresolved-finding counts and repeated evidence-unavailable terminal reasons.

## Content-source refresh
- Refresh local AWS/Azure evidence corpus in `EVIDENCE_CORPUS_PATH`.
- Reindex retrieval data before running new validation-heavy workloads.
- After refresh, execute a smoke query for each provider to verify evidence availability.
