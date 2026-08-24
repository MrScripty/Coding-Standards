from __future__ import annotations

from dataclasses import dataclass

from tools.graph_engine.graph_engine import Direction, EdgeRegistry, GraphError
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    FactSet,
    Truth,
)
from tools.standards_metadata.standards_metadata import PolicyUnitCorpus
from tools.standards_policy_impact.standards_policy_impact import (
    SOURCE_ID as POLICY_IMPACT_SOURCE_ID,
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
)

from .changes import ClassifiedChange, GraphSeedSelection, ReviewScope
from .errors import AnalysisError, AnalysisFailure
from .serialization import canonical_json_bytes, digest_bytes, identity


IMPACT_TRACE_DOMAIN = "coding-standards:impact-trace:v1"


@dataclass(frozen=True, slots=True)
class ImpactTrace:
    graph: str
    seed: str
    selected_group: str
    edge_id: str
    source: str
    target: str
    relation: str
    edge_groups: tuple[str, ...]
    path_nodes: tuple[str, ...]
    path_edges: tuple[str, ...]
    provenance_source: str
    provenance_kind: str
    provenance_locator: str
    metadata: tuple[tuple[str, str], ...]
    policy_semantics: PolicyImpactSemantics | None
    applicability: str
    unresolved_facts: tuple[str, ...]
    applicability_facts: tuple[tuple[str, str], ...]
    id: str


@dataclass(frozen=True, slots=True)
class ImpactCandidate:
    edge_id: str
    traces: tuple[ImpactTrace, ...]
    applicability: str
    unresolved_facts: tuple[str, ...]
    conservative_review_scope: ReviewScope | None


@dataclass(frozen=True, slots=True)
class ImpactSelection:
    change: ClassifiedChange
    candidates: tuple[ImpactCandidate, ...]


def select_impact(
    change: ClassifiedChange,
    accepted_graph: EdgeRegistry,
    proposed_graph: EdgeRegistry,
    accepted_policy_impact: CompiledPolicyImpactSet | None = None,
    proposed_policy_impact: CompiledPolicyImpactSet | None = None,
    facts: FactSet | None = None,
) -> ImpactSelection:
    selected_facts = _fact_context(
        accepted_policy_impact,
        proposed_policy_impact,
        facts,
    )
    traces = (
        *_traverse(
            "accepted",
            accepted_graph,
            change.graph,
            accepted_policy_impact,
            selected_facts,
        ),
        *_traverse(
            "proposed",
            proposed_graph,
            change.graph,
            proposed_policy_impact,
            selected_facts,
        ),
    )
    by_edge: dict[str, list[ImpactTrace]] = {}
    for trace in traces:
        by_edge.setdefault(trace.edge_id, []).append(trace)
    candidates: list[ImpactCandidate] = []
    for edge_id in sorted(by_edge):
        selected_traces = tuple(sorted(by_edge[edge_id], key=_trace_key))
        applicability = _aggregate_applicability(selected_traces)
        unresolved = tuple(
            sorted(
                {
                    fact
                    for trace in selected_traces
                    if trace.applicability == Truth.UNKNOWN.value
                    for fact in trace.unresolved_facts
                }
            )
        )
        candidates.append(
            ImpactCandidate(
                edge_id,
                selected_traces,
                applicability,
                unresolved,
                (
                    ReviewScope("whole-artifact") if unresolved else None
                ),
            )
        )
    return ImpactSelection(change, tuple(candidates))


def _fact_context(
    accepted: CompiledPolicyImpactSet | None,
    proposed: CompiledPolicyImpactSet | None,
    supplied: FactSet | None,
) -> FactSet | None:
    compiled = tuple(item for item in (accepted, proposed) if item is not None)
    if not compiled:
        return None
    digests = {item.fact_schema.digest for item in compiled}
    if len(digests) != 1:
        raise AnalysisError(
            AnalysisFailure(
                "IMPACT.FACT_SCHEMA_EVOLUTION_UNSUPPORTED",
                "unsupported",
                "accepted and proposed policy-impact fact schemas differ",
                field="fact_schema",
                observed="|".join(sorted(digests)),
            )
        )
    schema = compiled[0].fact_schema
    if supplied is None:
        return schema.bind({})
    if supplied.schema_digest != schema.digest:
        raise AnalysisError(
            AnalysisFailure(
                "IMPACT.FACT_SET_INVALID",
                "invalid",
                "analysis facts belong to a different policy-impact fact schema",
                field="schema_digest",
                observed=supplied.schema_digest,
            )
        )
    return supplied


def _traverse(
    side: str,
    graph: EdgeRegistry,
    selection: GraphSeedSelection,
    policy_impact: CompiledPolicyImpactSet | None,
    facts: FactSet | None,
) -> tuple[ImpactTrace, ...]:
    if side == "accepted":
        seeds = selection.accepted_seeds
        groups = selection.accepted_groups
    else:
        seeds = selection.proposed_seeds
        groups = selection.proposed_groups
    traces: list[ImpactTrace] = []
    seen: set[tuple[object, ...]] = set()
    try:
        for seed in sorted(seeds):
            for group_id in groups:
                graph.edges_for_group(group_id)
                group = graph.groups[group_id]
                result = graph.traverse_group(
                    seed,
                    group_id,
                    Direction.OUTGOING,
                    transitive=group.traversal.transitive,
                )
                for step in result.steps:
                    edge = step.edge
                    semantics = (
                        None
                        if policy_impact is None
                        else policy_impact.semantics.get(edge.id)
                    )
                    if (
                        edge.provenance.source_id == POLICY_IMPACT_SOURCE_ID
                        and semantics is None
                    ):
                        raise AnalysisError(
                            AnalysisFailure(
                                "IMPACT.POLICY_SEMANTICS_MISSING",
                                "invalid",
                                "compiled policy-impact edge has no matching semantic authority",
                                field="edge_id",
                                observed=edge.id,
                            )
                        )
                    applicability = "not-declared"
                    unresolved_facts: tuple[str, ...] = ()
                    applicability_facts: tuple[tuple[str, str], ...] = ()
                    if semantics is not None:
                        if facts is None:
                            raise AnalysisError(
                                AnalysisFailure(
                                    "IMPACT.FACT_SET_MISSING",
                                    "invalid",
                                    "compiled policy-impact semantics require a fact set",
                                    field="edge_id",
                                    observed=edge.id,
                                )
                            )
                        try:
                            evaluation = semantics.applicability_program.evaluate(facts)
                        except ApplicabilityError as error:
                            failure = error.failure
                            raise AnalysisError(
                                AnalysisFailure(
                                    "IMPACT.APPLICABILITY_INVALID",
                                    failure.outcome,
                                    failure.message,
                                    field=failure.field,
                                    observed=failure.observed,
                                )
                            ) from error
                        applicability = evaluation.truth.value
                        unresolved_facts = evaluation.unresolved_facts
                        applicability_facts = tuple(
                            (
                                fact,
                                _fact_value_digest(facts, fact),
                            )
                            for fact in semantics.applicability_program.referenced_facts
                        )
                    trace_projection = {
                        "graph": side,
                        "seed": seed,
                        "selected_group": group_id,
                        "edge_id": edge.id,
                        "source": edge.source,
                        "target": edge.target,
                        "relation": edge.relation,
                        "edge_groups": sorted(edge.groups),
                        "path_nodes": list(step.path_nodes),
                        "path_edges": list(step.path_edges),
                        "provenance": {
                            "source": edge.provenance.source_id,
                            "kind": edge.provenance.kind,
                            "locator": edge.provenance.locator,
                        },
                        "metadata": dict(sorted(edge.metadata.items())),
                        "policy_semantics": (
                            None
                            if semantics is None
                            else semantics.dependency_fingerprint
                        ),
                        "applicability": applicability,
                        "unresolved_facts": list(unresolved_facts),
                        "applicability_facts": [
                            {"fact": fact, "digest": digest}
                            for fact, digest in applicability_facts
                        ],
                    }
                    trace = ImpactTrace(
                        side,
                        seed,
                        group_id,
                        edge.id,
                        edge.source,
                        edge.target,
                        edge.relation,
                        tuple(sorted(edge.groups)),
                        step.path_nodes,
                        step.path_edges,
                        edge.provenance.source_id,
                        edge.provenance.kind,
                        edge.provenance.locator,
                        tuple(sorted(edge.metadata.items())),
                        semantics,
                        applicability,
                        unresolved_facts,
                        applicability_facts,
                        identity(
                            IMPACT_TRACE_DOMAIN,
                            "impact-trace",
                            trace_projection,
                        ),
                    )
                    key = _trace_key(trace)
                    if key not in seen:
                        seen.add(key)
                        traces.append(trace)
    except GraphError as error:
        details = error.failure.details
        raise AnalysisError(
            AnalysisFailure(
                "IMPACT.GRAPH_INVALID",
                "invalid",
                error.failure.message,
                field=next(iter(details), None),
                observed=str(next(iter(details.values()), "")) or None,
            )
        ) from error
    return tuple(sorted(traces, key=_trace_key))


def _aggregate_applicability(traces: tuple[ImpactTrace, ...]) -> str:
    states = {trace.applicability for trace in traces}
    if Truth.TRUE.value in states:
        return Truth.TRUE.value
    if Truth.UNKNOWN.value in states:
        return Truth.UNKNOWN.value
    if Truth.FALSE.value in states:
        return Truth.FALSE.value
    return "not-declared"


def _trace_key(trace: ImpactTrace) -> tuple[object, ...]:
    return (
        trace.graph,
        trace.seed,
        trace.selected_group,
        trace.edge_id,
        trace.source,
        trace.target,
        trace.relation,
        trace.path_nodes,
        trace.path_edges,
        trace.provenance_source,
        trace.provenance_kind,
        trace.provenance_locator,
        trace.metadata,
        trace.applicability,
        trace.unresolved_facts,
        trace.applicability_facts,
        (
            ""
            if trace.policy_semantics is None
            else trace.policy_semantics.dependency_fingerprint
        ),
    )


def _fact_value_digest(facts: FactSet, fact: str) -> str:
    value = facts.canonical_values.get(fact)
    projection: dict[str, object]
    if value is None:
        projection = {"state": "missing"}
    else:
        projection = {"type": value.type, "state": value.state}
        if value.state == "known":
            projection["value"] = value.value
    return digest_bytes(canonical_json_bytes(projection))
