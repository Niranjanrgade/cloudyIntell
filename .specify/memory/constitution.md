<!--
Sync Impact Report
- Version change: template (unversioned) → 1.0.0
- Modified principles:
	- Principle 1 (template) → I. Recursive Evaluator-Optimizer Architecture
	- Principle 2 (template) → II. Domain-Scoped Multi-Agent Orchestration
	- Principle 3 (template) → III. Fact-Based Validation with RAG Evidence (NON-NEGOTIABLE)
	- Principle 4 (template) → IV. Provider-Specific Fidelity and Separation
	- Principle 5 (template) → V. Transparent State and Documentation by Default
- Added sections:
	- Operational Constraints
	- Development Workflow & Quality Gates
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ updated: .specify/templates/plan-template.md
	- ✅ updated: .specify/templates/spec-template.md
	- ✅ updated: .specify/templates/tasks-template.md
	- ⚠ pending: .specify/templates/commands/*.md (directory not present)
	- ✅ reviewed: README.md (no references present)
- Follow-up TODOs:
	- None
-->

# CloudyIntel Constitution

## Core Principles

### I. Recursive Evaluator-Optimizer Architecture
All solution generation MUST run through an explicit evaluator-optimizer loop.
Generated architecture outputs MUST be validated, and failed validations MUST return
actionable feedback to the generator before any output is marked accepted.
Rationale: Cloud architectures are high-impact systems where first-pass generation is
insufficiently reliable without structured refinement.

### II. Domain-Scoped Multi-Agent Orchestration
The Architect Supervisor MUST decompose requests into domain tasks and delegate them to
specialized agents for compute, storage, networking, and databases. A reducer/coordinator
MUST synthesize domain outputs into one coherent architecture decision set.
Rationale: Domain specialization improves precision while preserving a single, integrated
solution contract for users.

### III. Fact-Based Validation with RAG Evidence (NON-NEGOTIABLE)
Validation agents MUST ground findings in authoritative vendor documentation retrieved
through RAG. Every rejection or critical warning MUST include traceable evidence and
specific remediation guidance. Unverifiable claims MUST NOT be used as validation criteria.
Rationale: Evidence-backed validation is required to prevent hallucinated architecture advice.

### IV. Provider-Specific Fidelity and Separation
AWS and Azure processing loops MUST remain provider-specific for generation and validation.
Cross-provider abstractions MAY be presented to users only after provider-compliant outputs
have been independently verified.
Rationale: Provider services, limits, and best practices differ materially and require distinct
reasoning paths.

### V. Transparent State and Documentation by Default
The system UI MUST expose workflow state, active nodes, and hand-offs in a graph-aligned
view. All implemented features, orchestration rules, validation policies, and interfaces MUST
include descriptive, easy-to-read documentation at delivery time.
Rationale: Architect users need observability into system reasoning and maintainers need
clear, persistent operational knowledge.

## Operational Constraints

- LangGraph state transitions MUST be explicit, deterministic, and auditable.
- CoPilotKit interactions MUST reflect real graph state and MUST NOT present synthetic
	hand-off events as completed execution.
- Architecture acceptance MUST require both synthesis completeness and validation pass state.
- Any fallback behavior (timeouts, unavailable retrievers, degraded validation) MUST be
	surfaced to the user as a non-silent status.

## Development Workflow & Quality Gates

1. Specifications MUST define user stories, provider scope, validation expectations,
	 documentation deliverables, and measurable outcomes.
2. Plans MUST pass a Constitution Check that verifies evaluator-optimizer loops,
	 domain delegation, RAG evidence paths, provider separation, and UI transparency.
3. Tasks MUST include work for generation, validation, integration, and user-facing
	 documentation updates.
4. Pull requests MUST include compliance notes for each core principle and MUST identify
	 any intentional deviations with rationale.
5. Releases MUST include an updated quickstart or equivalent runbook when behavior,
	 graph flow, or validation policy changes.

## Governance

This constitution is the highest-priority engineering policy for CloudyIntel. Any conflicting
guidance in plans, tasks, or local conventions is superseded by this document.

Amendment process:
- Propose changes via pull request that includes: motivation, principle or section deltas,
	migration impact, and template synchronization updates.
- Approval requires at least one maintainer review and explicit confirmation that dependent
	templates and guidance files were checked.
- Ratification occurs on merge to the default branch.

Versioning policy:
- MAJOR: Removes or redefines a principle or governance rule in a backward-incompatible way.
- MINOR: Adds a new principle/section or materially expands required practices.
- PATCH: Clarifies wording, fixes ambiguity, or performs non-semantic refinements.

Compliance review expectations:
- Every implementation plan and pull request MUST include a constitution compliance check.
- Non-compliance MUST block merge unless a documented exception is approved by maintainers.
- Exception records MUST include scope, risk, owner, and expiry or review date.

**Version**: 1.0.0 | **Ratified**: 2026-02-28 | **Last Amended**: 2026-02-28
