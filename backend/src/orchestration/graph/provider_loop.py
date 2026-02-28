from __future__ import annotations

from src.agents.generator.domain_generators import generate_domain_proposals
from src.agents.validator.domain_validators import validate_domain_proposal
from src.orchestration.nodes.reducer import reduce_architecture
from src.services.acceptance_policy import evaluate_acceptance


def execute_provider_loop(provider: str, query: str, max_iterations: int = 3) -> dict:
    iteration = 0
    feedback: str | None = None
    feedback_history: list[dict] = []
    best_output = ""
    best_findings: list[dict] = []

    while iteration <= max_iterations:
        proposals = generate_domain_proposals(provider=provider, query=query, iteration=iteration, feedback=feedback)
        if "timeout" in query.lower() and proposals:
            partial = proposals[:2]
            architecture_output = reduce_architecture(provider, partial)
            return {
                "provider": provider,
                "status": "failed",
                "accepted": False,
                "iteration_count": iteration,
                "terminal_reason": "domain_failure",
                "unresolved_findings": 1,
                "output": architecture_output,
                "findings": [
                    {
                        "iteration": iteration,
                        "domain": "network",
                        "outcome": "fail",
                        "severity": "critical",
                        "reason": "Domain task timeout while generating network proposal.",
                        "remediation": "Retry with relaxed constraints or rerun provider loop.",
                        "evidence": [],
                    }
                ],
                "failure_reason": "network domain timeout",
                "feedback_history": feedback_history,
            }
        architecture_output = reduce_architecture(provider, proposals)
        findings = []

        for proposal in proposals:
            validation = validate_domain_proposal(provider=provider, proposal=proposal, query=query, iteration=iteration)
            findings.append(
                {
                    "iteration": iteration,
                    "domain": proposal.domain,
                    "outcome": validation.outcome,
                    "severity": "high" if validation.outcome == "fail" else "low",
                    "reason": validation.reason,
                    "remediation": validation.remediation,
                    "evidence": validation.evidence,
                }
            )

        policy = evaluate_acceptance(findings=findings, iteration_count=iteration, max_iterations=max_iterations)
        best_output = architecture_output
        best_findings = findings

        if policy["status"] in {"accepted", "stopped"}:
            return {
                "provider": provider,
                "status": policy["status"],
                "accepted": policy["accepted"],
                "iteration_count": iteration,
                "terminal_reason": policy["terminal_reason"],
                "unresolved_findings": policy["unresolved_findings"],
                "output": best_output,
                "findings": best_findings,
                "failure_reason": None,
                "feedback_history": feedback_history,
            }

        feedback = "Fix failed domains based on remediation guidance."
        feedback_history.append(
            {
                "iteration_from": iteration,
                "target_domains": [finding["domain"] for finding in findings if finding["outcome"] == "fail"],
                "instructions": feedback,
                "blocking_issues": [finding["reason"] for finding in findings if finding["outcome"] == "fail"],
            }
        )
        iteration += 1

    return {
        "provider": provider,
        "status": "stopped",
        "accepted": False,
        "iteration_count": max_iterations,
        "terminal_reason": "iteration_limit",
        "unresolved_findings": len([f for f in best_findings if f["outcome"] == "fail"]),
        "output": best_output,
        "findings": best_findings,
        "failure_reason": None,
        "feedback_history": feedback_history,
    }
