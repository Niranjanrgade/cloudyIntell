from __future__ import annotations

from dataclasses import dataclass


DOMAINS = ["compute", "storage", "network", "database"]


@dataclass(slots=True)
class DomainProposal:
    domain: str
    content: str
    rationale: str


def generate_domain_proposals(provider: str, query: str, iteration: int, feedback: str | None = None) -> list[DomainProposal]:
    suffix = f" (iteration {iteration})"
    feedback_suffix = f" | feedback: {feedback}" if feedback else ""
    return [
        DomainProposal(
            domain=domain,
            content=f"{provider.upper()} {domain} architecture for: {query}{suffix}{feedback_suffix}",
            rationale=f"{provider.upper()} best-practice baseline for {domain}",
        )
        for domain in DOMAINS
    ]
