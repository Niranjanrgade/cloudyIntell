# Data Model: CloudyIntel Architecture Website

## Entity: ArchitectureQuery
- Purpose: Captures user input and execution intent.
- Fields:
  - `query_id` (UUID, required)
  - `workspace_id` (string, required)
  - `raw_text` (text, required)
  - `provider_scope` (enum: `aws` | `azure` | `both`, required)
  - `constraints` (JSON, optional)
  - `optimization_preferences` (JSON, optional)
  - `created_at` (datetime, required)
- Validation rules:
  - `raw_text` must be non-empty.
  - `provider_scope` must map to allowed values.

## Entity: ProviderRun
- Purpose: Tracks one provider-specific execution instance.
- Fields:
  - `provider_run_id` (UUID, required)
  - `query_id` (UUID FK -> ArchitectureQuery, required)
  - `provider` (enum: `aws` | `azure`, required)
  - `status` (enum: `generating` | `validating` | `optimizing` | `accepted` | `stopped` | `failed`, required)
  - `iteration_count` (integer, required, default 0)
  - `accepted` (boolean, required)
  - `terminal_reason` (enum: `accepted` | `iteration_limit` | `evidence_unavailable` | `domain_failure` | `timeout`, optional)
  - `started_at` (datetime, required)
  - `completed_at` (datetime, optional)
- Validation rules:
  - `iteration_count` in range 0..3.
  - `accepted=true` requires all required domains validated with evidence.
  - `provider` cannot change after creation.

## Entity: DomainTask
- Purpose: Represents domain-scoped work unit for a provider run.
- Fields:
  - `domain_task_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `domain` (enum: `compute` | `storage` | `network` | `database`, required)
  - `task_status` (enum: `pending` | `running` | `completed` | `failed`, required)
  - `started_at` (datetime, optional)
  - `completed_at` (datetime, optional)
  - `failure_reason` (text, optional)
- Validation rules:
  - One active task per `(provider_run_id, domain, iteration)`.

## Entity: DomainProposal
- Purpose: Stores generated domain recommendation and rationale.
- Fields:
  - `domain_proposal_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `domain` (enum, required)
  - `iteration` (integer, required)
  - `proposal_content` (JSON/text, required)
  - `rationale` (text, required)
  - `dependencies` (JSON array, optional)
  - `created_at` (datetime, required)
- Validation rules:
  - `iteration` must be <= `ProviderRun.iteration_count`.

## Entity: ArchitectureProposal
- Purpose: Provider-level synthesized architecture for an iteration.
- Fields:
  - `architecture_proposal_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `iteration` (integer, required)
  - `combined_design` (JSON/text, required)
  - `cross_domain_assumptions` (JSON, optional)
  - `synthesis_status` (enum: `draft` | `coherent` | `conflict_detected`, required)
  - `created_at` (datetime, required)
- Validation rules:
  - Must include all required domains unless partial result is explicitly flagged.

## Entity: ValidationFinding
- Purpose: Tracks validator outcomes per domain/cross-domain check.
- Fields:
  - `finding_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `iteration` (integer, required)
  - `domain` (enum + `cross_domain`, required)
  - `outcome` (enum: `pass` | `fail` | `warn`, required)
  - `severity` (enum: `critical` | `high` | `medium` | `low`, required)
  - `reason` (text, required)
  - `remediation` (text, optional but required when `outcome=fail`)
  - `evidence_required` (boolean, required, default true)
  - `created_at` (datetime, required)
- Validation rules:
  - Failing findings must include remediation.

## Entity: EvidenceReference
- Purpose: Preserves traceable evidence used by validation.
- Fields:
  - `evidence_id` (UUID, required)
  - `finding_id` (UUID FK -> ValidationFinding, required)
  - `provider` (enum: `aws` | `azure`, required)
  - `source_type` (enum: `official_doc`, required)
  - `source_uri` (string, required)
  - `title` (string, required)
  - `excerpt` (text, required)
  - `retrieved_at` (datetime, required)
  - `availability_status` (enum: `available` | `unavailable`, required)
- Validation rules:
  - `provider` must match associated `ProviderRun.provider`.

## Entity: RefinementFeedback
- Purpose: Feedback payload from validation to generation loop.
- Fields:
  - `feedback_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `iteration_from` (integer, required)
  - `target_domains` (JSON array of enums, required)
  - `instructions` (text, required)
  - `blocking_issues` (JSON array, optional)
  - `created_at` (datetime, required)
- Validation rules:
  - Must be present when run transitions from `validating` to `optimizing`.

## Entity: WorkflowNodeState
- Purpose: Current UI-visible state for each graph node.
- Fields:
  - `node_state_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `node_id` (string, required)
  - `node_type` (enum: `supervisor` | `domain_generator` | `reducer` | `validator` | `optimizer`, required)
  - `state` (enum: `idle` | `active` | `waiting` | `completed` | `failed`, required)
  - `active_iteration` (integer, optional)
  - `updated_at` (datetime, required)

## Entity: RunEvent
- Purpose: Immutable timeline for transitions, hand-offs, retries, and failures.
- Fields:
  - `event_id` (UUID, required)
  - `provider_run_id` (UUID FK -> ProviderRun, required)
  - `query_id` (UUID FK -> ArchitectureQuery, required)
  - `event_type` (enum: `state_transition` | `handoff` | `validation_result` | `retry` | `failure` | `completion`, required)
  - `event_payload` (JSON, required)
  - `occurred_at` (datetime, required)

## Relationships
- `ArchitectureQuery` 1 -> N `ProviderRun`
- `ProviderRun` 1 -> N `DomainTask`
- `ProviderRun` 1 -> N `DomainProposal`
- `ProviderRun` 1 -> N `ArchitectureProposal`
- `ProviderRun` 1 -> N `ValidationFinding`
- `ValidationFinding` 1 -> N `EvidenceReference`
- `ProviderRun` 1 -> N `RefinementFeedback`
- `ProviderRun` 1 -> N `WorkflowNodeState`
- `ProviderRun` 1 -> N `RunEvent`

## State Transitions
- Provider run lifecycle:
  - `generating` -> `validating` -> `accepted`
  - `generating` -> `validating` -> `optimizing` -> `generating` (next iteration)
  - `validating` -> `stopped` (iteration limit reached)
  - `validating` -> `stopped` (evidence unavailable)
  - any -> `failed` (unrecoverable domain/runtime error)
- Guard conditions:
  - Transition to `accepted` requires all required findings pass and evidence availability = `available`.
  - Transition to `optimizing` allowed only when `iteration_count < 3`.