# CloudyIntel User Guide

## Query usage
- Enter a workload description with constraints.
- Select provider scope: AWS, Azure, or Both.
- Submit and wait for provider-separated results.

## Stopping behavior
- CloudyIntel runs a recursive generate-validate loop.
- Each provider can refine up to 3 iterations.
- If unresolved findings remain at iteration limit, best draft is returned and flagged.

## Evidence interpretation
- Passed findings include evidence references supporting decisions.
- Failed findings include reason and remediation guidance.
- If evidence is unavailable, provider result is marked not validated.

## Using remediation feedback
- Open the remediation panel to review domain-specific fixes.
- Apply remediation to query constraints (capacity, networking, storage class, or topology) and rerun.
- Prioritize high-severity failed findings first.

## Troubleshooting
- If a run shows `stopped` and `evidence_unavailable`, refresh local evidence corpus and rerun.
- If a run shows unresolved findings, adjust constraints and retry.
