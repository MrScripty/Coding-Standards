from __future__ import annotations

from dataclasses import dataclass

from tools.graph_engine.graph_engine import GraphContribution, Node, Provenance
from tools.standards_metadata.standards_metadata import PolicyUnitCorpus


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
                    "repository_path": unit.document,
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
