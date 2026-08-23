from __future__ import annotations

from dataclasses import dataclass

from tools.graph_engine.graph_engine import (
    Direction,
    EdgeRegistry,
    GraphContribution,
    GraphError,
    Node,
    Provenance,
)

from .changes import ClassifiedChange, GraphSeedSelection
from .errors import AnalysisError, AnalysisFailure
from .policy_units import PolicyUnitCorpus


POLICY_UNIT_SOURCE_ID = "standards.policy-units"


@dataclass(frozen=True, slots=True)
class PolicyUnitGraphSource:
    corpus: PolicyUnitCorpus
    id: str = POLICY_UNIT_SOURCE_ID

    def load(self) -> GraphContribution:
        nodes = [
            Node(
                unit.id,
                unit.aliases,
                Provenance(self.id, "provider", unit.source),
                {
                    "lifecycle": "active",
                    "module": unit.module,
                    "policy_unit_source": unit.source,
                },
            )
            for unit in self.corpus.units
        ]
        nodes.extend(
            Node(
                tombstone.id,
                (),
                Provenance(self.id, "provider", tombstone.source),
                {
                    "lifecycle": "retired",
                    "policy_unit_source": tombstone.source,
                },
            )
            for tombstone in self.corpus.tombstones
        )
        return GraphContribution(tuple(sorted(nodes, key=lambda item: item.id)), (), ())


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
) -> ImpactSelection:
    traces = (
        *_traverse("accepted", accepted_graph, change.graph),
        *_traverse("proposed", proposed_graph, change.graph),
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
    )
