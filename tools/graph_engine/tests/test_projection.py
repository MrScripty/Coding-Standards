from __future__ import annotations

import unittest

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeGroup,
    GraphContribution,
    InvalidSourceError,
    Node,
    Provenance,
    TraversalPolicy,
    load_graph_contribution,
    project_graph_contribution,
)


class GraphProjectionTest(unittest.TestCase):
    def test_closed_projection_round_trips_every_graph_record(self) -> None:
        provenance = Provenance("source", "provider", "fixture")
        contribution = GraphContribution(
            (Node("left", ("left.md",), provenance, {"authority": "normative"}), Node("right")),
            (
                EdgeGroup(
                    "group",
                    "Fixture traversal.",
                    TraversalPolicy(
                        frozenset({Direction.INCOMING, Direction.OUTGOING}), True
                    ),
                    provenance,
                    "validator",
                    {"contract": "1"},
                ),
            ),
            (
                Edge(
                    "edge",
                    "left",
                    "right",
                    "requires",
                    ("group",),
                    provenance,
                    {"evidence": "fixture"},
                    False,
                ),
            ),
        )
        projected = project_graph_contribution(contribution)
        self.assertEqual(load_graph_contribution(projected), contribution)

        projected["extra"] = None
        with self.assertRaises(InvalidSourceError):
            load_graph_contribution(projected)


if __name__ == "__main__":
    unittest.main()
