from __future__ import annotations

from pathlib import Path

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    DEFAULT_REGISTRY,
    PolicyImpactSource,
    compile_policy_impact,
)
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSourceInput,
)

from .metadata import metadata_dependency_source
from .policy_units import PolicyUnitGraphSource


POLICY_IMPACT_REGISTRY = DEFAULT_REGISTRY


def standards_navigation_registry(
    source: ContentSourceInput,
    corpus: CanonicalStandardsCorpus,
    policy_impact_registry: str = POLICY_IMPACT_REGISTRY,
    *,
    compiled_policy_impact: CompiledPolicyImpactSet | None = None,
) -> EdgeRegistry:
    """Build the explicit graph view used for canonical standards navigation."""

    compiled = (
        compiled_policy_impact
        or compile_policy_impact(
            source,
            corpus,
            policy_impact_registry,
        )
    )
    sources = (
        metadata_dependency_source(corpus.modules),
        PolicyUnitGraphSource(corpus.policy_unit_corpus),
        PolicyImpactSource(compiled),
    )
    return EdgeRegistry(
        Path("/"),
        sources,
        logical_artifacts=(module.path for module in corpus.modules),
    )
