from __future__ import annotations

from src.agents.generator.domain_generators import DomainProposal


def reduce_architecture(provider: str, proposals: list[DomainProposal]) -> str:
    sections = [f"Provider: {provider.upper()}"]
    for proposal in proposals:
        sections.append(f"- {proposal.domain}: {proposal.content}")
    return "\n".join(sections)
