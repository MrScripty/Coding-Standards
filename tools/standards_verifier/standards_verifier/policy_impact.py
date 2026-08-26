from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from tools.graph_engine.graph_engine import EdgeRegistry, GraphError
from tools.standards_applicability.standards_applicability import ApplicabilityProgram
from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    CoverageIndex,
    compile_coverage,
)
from tools.standards_graph.standards_graph import metadata_dependency_source
from tools.standards_metadata.standards_metadata import (
    MetadataError,
    PolicyUnitCorpus,
    load_canonical_standards_corpus,
)
from tools.standards_graph.standards_graph import PolicyUnitGraphSource
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    PolicyImpactError,
    PolicyImpactSource,
    compile_policy_impact,
)

from .diagnostics import Diagnostic, EngineError
from .paths import contained_file


POLICY_GROUP = "policy-impact"
DEFAULT_SOURCE_REGISTRY = "evaluation/standards-effectiveness/edge-source-registry.toml"
DEFAULT_POLICY_REGISTRY = "evaluation/standards-effectiveness/policy-impact-registry.toml"


@dataclass(frozen=True, slots=True)
class ImpactEdge:
    edge_id: str
    owner: str
    consumer: str
    relation: str
    applicability_program: ApplicabilityProgram
    evidence_owner: str


@dataclass(frozen=True, slots=True)
class PolicyImpactAdapter:
    registry: EdgeRegistry
    compiled: CompiledPolicyImpactSet
    policy_units: PolicyUnitCorpus
    coverage: CoverageIndex

    @property
    def covered_owners(self) -> frozenset[str]:
        owners = {unit.module for unit in self.policy_units.units}
        return frozenset(
            owner
            for owner in owners
            if not self.coverage.uncovered_for_module_corpus(self.policy_units, owner)
        )

    def consumers_for(self, owner: str) -> tuple[ImpactEdge, ...]:
        uncovered = self.coverage.uncovered_for_module_corpus(
            self.policy_units,
            owner,
        )
        if uncovered or not self.policy_units.for_module(owner):
            raise EngineError(
                Diagnostic(
                    "POLICY_IMPACT.OWNER_NOT_AUDITED",
                    "unavailable",
                    "policy owner lacks current consumer-coverage certificates",
                    observed="|".join(uncovered) if uncovered else owner,
                )
            )
        return self.declared_consumers_for(owner)

    def declared_consumers_for(self, owner: str) -> tuple[ImpactEdge, ...]:
        return _declared_consumers(
            self.registry,
            self.compiled,
            self.policy_units,
            owner,
        )


def _declared_consumers(
    registry: EdgeRegistry,
    compiled: CompiledPolicyImpactSet,
    policy_units: PolicyUnitCorpus,
    owner: str,
) -> tuple[ImpactEdge, ...]:
    edges = (
        _impact_edge(registry, compiled, owner, view.edge.id)
        for unit in policy_units.for_module(owner)
        for view in registry.outgoing(unit.id, (POLICY_GROUP,))
    )
    return tuple(
        sorted(edges, key=lambda edge: (edge.consumer, edge.relation, edge.edge_id))
    )


def _diagnostic(
    code: str,
    message: str,
    *,
    path: str | None = None,
    field: str | None = None,
    observed: str | None = None,
    suite: str | None = None,
    check: str | None = None,
    unavailable: bool = False,
) -> EngineError:
    return EngineError(
        Diagnostic(
            code,
            "unavailable" if unavailable else "invalid",
            message,
            suite=suite,
            check=check,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _translate_policy_error(
    error: PolicyImpactError,
    *,
    suite: str,
    check: str,
) -> EngineError:
    failure = error.failure
    return _diagnostic(
        failure.code,
        failure.message,
        path=failure.path,
        field=failure.field,
        observed=failure.observed,
        suite=suite,
        check=check,
        unavailable=failure.outcome == "unavailable",
    )


def _translate_analysis_error(
    error: AnalysisError,
    *,
    suite: str,
    check: str,
) -> EngineError:
    failure = error.failure
    return _diagnostic(
        failure.code,
        failure.message,
        path=failure.path,
        field=failure.field,
        observed=failure.observed,
        suite=suite,
        check=check,
        unavailable=failure.outcome == "unavailable",
    )


def _translate_metadata_error(
    error: MetadataError,
    *,
    suite: str,
    check: str,
) -> EngineError:
    failure = error.failure
    return _diagnostic(
        failure.code,
        failure.message,
        path=failure.path,
        field=failure.field,
        observed=failure.observed,
        suite=suite,
        check=check,
        unavailable=failure.outcome == "unavailable",
    )


def _repository_path(registry: EdgeRegistry, node_id: str, source_path: str) -> str:
    node = registry.nodes[node_id]
    value = node.metadata.get("repository_path")
    if not value:
        raise _diagnostic(
            "POLICY_IMPACT.UNKNOWN_CONSUMER",
            "policy-impact nodes require one repository_path",
            path=source_path,
            field="repository_path",
            observed=node_id,
        )
    return value


def _impact_edge(
    registry: EdgeRegistry,
    compiled: CompiledPolicyImpactSet,
    owner: str,
    edge_id: str,
) -> ImpactEdge:
    edge = registry.edge(edge_id)
    semantics = compiled.semantics_for(edge_id)
    return ImpactEdge(
        edge.id,
        owner,
        _repository_path(registry, edge.target, semantics.declaration_source),
        edge.relation,
        semantics.applicability_program,
        semantics.evidence_owner,
    )


def _validate_adapter(
    root: Path,
    registry: EdgeRegistry,
    compiled: CompiledPolicyImpactSet,
    policy_units: PolicyUnitCorpus,
    suite_paths: Mapping[str, str],
    *,
    suite: str,
    check: str,
) -> None:
    relationship_sources = {
        semantics.source for semantics in compiled.semantics.values()
    }
    relationship_owners = {
        unit.module
        for unit in policy_units.units
        if unit.id in relationship_sources
    }
    for owner in sorted(relationship_owners):
        for edge in _declared_consumers(registry, compiled, policy_units, owner):
            contained_file(root, edge.consumer, suite=suite, check=check)


def load_policy_impact(
    root: Path,
    registry_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "registry",
) -> PolicyImpactAdapter:
    repo_root = root.resolve()
    try:
        corpus = load_canonical_standards_corpus(repo_root)
        compiled = compile_policy_impact(repo_root, corpus, registry_path)
        registry = EdgeRegistry(
            repo_root,
            (
                metadata_dependency_source(corpus.modules),
                PolicyUnitGraphSource(corpus.policy_unit_corpus),
                PolicyImpactSource(compiled),
            ),
        )
    except PolicyImpactError as error:
        raise _translate_policy_error(error, suite=suite, check=check) from error
    except MetadataError as error:
        raise _translate_metadata_error(error, suite=suite, check=check) from error
    except GraphError as error:
        raise _diagnostic(
            error.failure.code,
            error.failure.message,
            observed=str(error.failure.details),
            suite=suite,
            check=check,
        ) from error
    _validate_adapter(
        repo_root,
        registry,
        compiled,
        corpus.policy_unit_corpus,
        suite_paths,
        suite=suite,
        check=check,
    )
    try:
        coverage = compile_coverage(repo_root, corpus, compiled)
    except AnalysisError as error:
        raise _translate_analysis_error(error, suite=suite, check=check) from error
    return PolicyImpactAdapter(registry, compiled, corpus.policy_unit_corpus, coverage)


def load_registered_policy_impact(
    root: Path,
    source_registry_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "registry",
) -> PolicyImpactAdapter:
    from .repository_graph import load_repository_registry

    try:
        corpus = load_canonical_standards_corpus(root.resolve())
        compiled = compile_policy_impact(root.resolve(), corpus, DEFAULT_POLICY_REGISTRY)
        registry = load_repository_registry(
            root,
            source_registry_path,
            corpus=corpus,
            compiled_policy_impact=compiled,
        )
    except PolicyImpactError as error:
        raise _translate_policy_error(error, suite=suite, check=check) from error
    except MetadataError as error:
        raise _translate_metadata_error(error, suite=suite, check=check) from error
    except GraphError as error:
        raise _diagnostic(
            error.failure.code,
            error.failure.message,
            observed=str(error.failure.details),
            suite=suite,
            check=check,
        ) from error
    _validate_adapter(
        root.resolve(),
        registry,
        compiled,
        corpus.policy_unit_corpus,
        suite_paths,
        suite=suite,
        check=check,
    )
    try:
        coverage = compile_coverage(root.resolve(), corpus, compiled)
    except AnalysisError as error:
        raise _translate_analysis_error(error, suite=suite, check=check) from error
    return PolicyImpactAdapter(registry, compiled, corpus.policy_unit_corpus, coverage)
