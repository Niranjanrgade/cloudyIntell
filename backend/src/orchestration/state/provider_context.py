from __future__ import annotations

from src.orchestration.state.models import Provider, ProviderRunState


def build_provider_states(run_id: str, provider_scope: str) -> dict[Provider, ProviderRunState]:
    providers = [Provider(provider_scope)] if provider_scope in {"aws", "azure"} else [Provider.AWS, Provider.AZURE]
    return {
        provider: ProviderRunState(run_id=run_id, provider=provider)
        for provider in providers
    }
