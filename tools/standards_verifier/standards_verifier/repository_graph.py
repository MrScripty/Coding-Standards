from __future__ import annotations

from pathlib import Path

from tools.graph_engine.graph_engine import EdgeRegistry, InvalidSourceError
from tools.graph_engine.graph_engine.manifest import load_registry as load_graph_registry
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    MetadataError,
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    DEFAULT_REGISTRY as POLICY_IMPACT_REGISTRY,
    PolicyImpactError,
    PolicyImpactSource,
    compile_policy_impact,
)
from tools.standards_graph.standards_graph import (
    PolicyUnitGraphSource,
    metadata_dependency_source,
)

from .config import load_registry as load_suite_registry
from .diagnostics import EngineError
from .graph_adapters import suite_dependency_source


SUITE_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"


def load_repository_registry(
    root: Path,
    source_registry: str,
    *,
    corpus: CanonicalStandardsCorpus | None = None,
    compiled_policy_impact: CompiledPolicyImpactSet | None = None,
) -> EdgeRegistry:
    repo_root = root.resolve()
    try:
        entries = load_suite_registry(repo_root, SUITE_REGISTRY)
    except EngineError as error:
        diagnostic = error.diagnostic
        raise InvalidSourceError(
            "suite dependency provider could not load the suite registry",
            code=diagnostic.code,
            path=diagnostic.path or SUITE_REGISTRY,
        ) from error
    try:
        corpus = corpus or load_canonical_standards_corpus(repo_root)
    except MetadataError as error:
        failure = error.failure
        raise InvalidSourceError(
            "metadata provider could not load the canonical standards corpus",
            code=failure.code,
            path=failure.path or "",
        ) from error
    try:
        policy_impact = compiled_policy_impact or compile_policy_impact(
            repo_root, corpus, POLICY_IMPACT_REGISTRY
        )
    except PolicyImpactError as error:
        failure = error.failure
        raise InvalidSourceError(
            "policy-impact provider could not compile registered declarations",
            code=failure.code,
            path=failure.path or POLICY_IMPACT_REGISTRY,
        ) from error
    providers = {
        "standards.policy-impact": PolicyImpactSource(policy_impact),
        "standards-verifier.suite-dependencies": suite_dependency_source(
            entries,
            SUITE_REGISTRY,
            include_path_aliases=True,
        ),
        "standards-verifier.metadata-dependencies": metadata_dependency_source(
            corpus.modules
        ),
        "standards.policy-units": PolicyUnitGraphSource(corpus.policy_unit_corpus),
    }
    return load_graph_registry(
        repo_root,
        source_registry,
        providers=providers,
    )
