"""Descriptive provenance associations derived from their sole source record."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from tools.graph_engine.graph_engine import (
    Direction, Edge, EdgeGroup, GraphContribution, Node, Provenance, TraversalPolicy,
)
from tools.standards_metadata.standards_metadata import DECISION_PROVENANCE, SupportingContent

PROVENANCE_GROUP = "decision-provenance"


@dataclass(frozen=True, slots=True)
class DecisionProvenanceSource:
    supporting: SupportingContent
    id: str = "standards.decision-provenance"

    def load(self) -> GraphContribution:
        source = Provenance(self.id, "provider", DECISION_PROVENANCE)
        nodes = tuple(Node(record.id, (), source, {"artifact_kind": "decision-provenance"})
                      for record in self.supporting.provenance.values())
        group = EdgeGroup(PROVENANCE_GROUP, "Reasoning available to standards authors.",
                          TraversalPolicy(frozenset({Direction.INCOMING, Direction.OUTGOING}), False), source)
        edges = tuple(Edge(f"provenance:{quote(record.subject, safe='')}:{quote(record.id, safe='')}",
                           record.subject, record.id, "justified-by", (PROVENANCE_GROUP,), source)
                      for record in self.supporting.provenance.values() if not record.retired)
        supersession = tuple(
            Edge(f"provenance-supersedes:{quote(record.id, safe='')}:{quote(predecessor, safe='')}",
                 record.id, predecessor, "supersedes", (PROVENANCE_GROUP,), source)
            for record in self.supporting.provenance.values() for predecessor in record.supersedes)
        return GraphContribution(nodes, (group,), (*edges, *supersession))
