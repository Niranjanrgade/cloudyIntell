from __future__ import annotations

from dataclasses import dataclass

from src.agents.generator.domain_generators import DomainProposal


@dataclass(slots=True)
class ValidationResult:
    outcome: str
    reason: str
    remediation: str | None
    evidence: list[dict]


def validate_domain_proposal(provider: str, proposal: DomainProposal, query: str, iteration: int) -> ValidationResult:
    lowered = query.lower()
    if "no-evidence" in lowered:
        return ValidationResult(
            outcome="fail",
            reason="Required validation evidence is unavailable for this domain.",
            remediation="Refresh evidence corpus and rerun validation.",
            evidence=[
                {
                    "source_uri": "https://docs.example.invalid/unavailable",
                    "title": f"{provider.upper()} Evidence Retriever",
                    "excerpt": "Evidence retrieval failed.",
                    "availability_status": "unavailable",
                }
            ],
        )

    should_fail = "fail" in lowered or ("strict" in lowered and iteration == 0)
    if should_fail:
        return ValidationResult(
            outcome="fail",
            reason=f"{proposal.domain} decision violates {provider.upper()} constraints in current draft.",
            remediation=f"Adjust {proposal.domain} sizing and connectivity to satisfy provider constraints.",
            evidence=[
                {
                    "source_uri": f"https://docs.{provider}.example/{proposal.domain}",
                    "title": f"{provider.upper()} {proposal.domain} guidance",
                    "excerpt": "Service constraints and recommended patterns.",
                    "availability_status": "available",
                }
            ],
        )

    return ValidationResult(
        outcome="pass",
        reason=f"{proposal.domain} recommendation is valid for {provider.upper()}.",
        remediation=None,
        evidence=[
            {
                "source_uri": f"https://docs.{provider}.example/{proposal.domain}",
                "title": f"{provider.upper()} {proposal.domain} guidance",
                "excerpt": "Validated configuration baseline.",
                "availability_status": "available",
            }
        ],
    )
