from __future__ import annotations

from dataclasses import dataclass

from tools.graph_engine.graph_engine import Direction, EdgeRegistry, GraphError
from tools.standards_metadata.standards_metadata import PolicyUnitCorpus
from tools.standards_policy_impact.standards_policy_impact import (
    SOURCE_ID as POLICY_IMPACT_SOURCE_ID,
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
)

from .changes import ClassifiedChange, GraphSeedSelection
from .errors import AnalysisError, AnalysisFailure
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


@dataclass(frozen=True, slots=True)
class ImpactCandidate:
    edge_id: str
    traces: tuple[ImpactTrace, ...]


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
) -> ImpactSelection:
    traces = (
        *_traverse("accepted", accepted_graph, change.graph, accepted_policy_impact),
        *_traverse("proposed", proposed_graph, change.graph, proposed_policy_impact),
    )
    by_edge: dict[str, list[ImpactTrace]] = {}
    for trace in traces:
        by_edge.setdefault(trace.edge_id, []).append(trace)
    candidates = tuple(
        ImpactCandidate(
            edge_id,
            tuple(sorted(by_edge[edge_id], key=_trace_key)),
        )
        for edge_id in sorted(by_edge)
    )
    return ImpactSelection(change, candidates)


def _traverse(
    side: str,
    graph: EdgeRegistry,
    selection: GraphSeedSelection,
    policy_impact: CompiledPolicyImpactSet | None,
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
        (
            ""
            if trace.policy_semantics is None
            else trace.policy_semantics.dependency_fingerprint
        ),
    )
