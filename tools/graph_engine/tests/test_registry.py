from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ENGINE_ROOT))

from graph_engine import (
    AliasConflictError,
    Direction,
    Edge,
    EdgeGroup,
    EdgeRegistry,
    ForbiddenTraversalError,
    GraphContribution,
    InvalidEdgeError,
    InvalidGroupError,
    InvalidSourceError,
    MissingArtifactError,
    Node,
    PathEscapeError,
    Provenance,
    TraversalPolicy,
    UnknownEdgeError,
    UnknownGroupError,
    UnknownNodeError,
)


@dataclass(frozen=True)
class Source:
    id: str
    contribution: GraphContribution

    def load(self) -> GraphContribution:
        return self.contribution


class EdgeRegistryTest(unittest.TestCase):
    def test_explicit_logical_artifacts_remove_filesystem_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            provenance = Provenance("logical", "provider", "fixture")
            source = Source(
                "logical",
                GraphContribution(
                    (Node("policy", ("standards/policy.md",), provenance),),
                    (),
                    (),
                ),
            )
            registry = EdgeRegistry(
                root,
                (source,),
                logical_artifacts=("standards/policy.md",),
            )
            self.assertFalse((root / "standards/policy.md").exists())
            self.assertEqual(registry.resolve("standards/policy.md"), "policy")
            with self.assertRaises(UnknownNodeError):
                registry.resolve("standards/missing.md")

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("workflows/planning.md")
        self.write("prompts/plan.md")
        self.write("templates/PLAN.md")
        self.write("unconnected.md")
        self.provenance = Provenance("test", "provider", "test_registry.py")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(path, encoding="utf-8")

    def group(
        self,
        group_id: str = "semantic",
        *,
        directions: frozenset[Direction] = frozenset(
            {Direction.INCOMING, Direction.OUTGOING}
        ),
        transitive: bool = False,
    ) -> EdgeGroup:
        return EdgeGroup(
            group_id,
            f"Purpose for {group_id}",
            TraversalPolicy(directions, transitive),
            self.provenance,
        )

    def node(self, node_id: str, *aliases: str) -> Node:
        return Node(node_id, aliases, self.provenance)

    def edge(
        self,
        edge_id: str,
        source: str,
        target: str,
        *,
        groups: tuple[str, ...] = ("semantic",),
        traversable: bool = True,
    ) -> Edge:
        return Edge(
            edge_id,
            source,
            target,
            "projects",
            groups,
            self.provenance,
            {"applicability": "when selected"},
            traversable,
        )

    def registry(
        self,
        *,
        nodes: tuple[Node, ...] | None = None,
        groups: tuple[EdgeGroup, ...] | None = None,
        edges: tuple[Edge, ...] | None = None,
    ) -> EdgeRegistry:
        return EdgeRegistry(
            self.root,
            (
                Source(
                    "test",
                    GraphContribution(
                        nodes
                        or (
                            self.node("workflow.planning", "workflows/planning.md"),
                            self.node("prompt.plan", "prompts/plan.md"),
                        ),
                        groups or (self.group(),),
                        edges
                        or (
                            self.edge(
                                "planning-to-prompt",
                                "workflow.planning",
                                "prompt.plan",
                            ),
                        ),
                    ),
                ),
            ),
        )

    def test_one_declaration_is_discoverable_from_both_endpoints(self) -> None:
        registry = self.registry()

        self.assertEqual([v.edge.id for v in registry.outgoing("workflow.planning")], ["planning-to-prompt"])
        self.assertEqual([v.edge.id for v in registry.incoming("prompt.plan")], ["planning-to-prompt"])
        self.assertEqual(registry.outgoing("workflow.planning")[0].opposite, "prompt.plan")
        self.assertEqual(registry.incoming("prompt.plan")[0].opposite, "workflow.planning")

    def test_logical_and_path_aliases_resolve_to_the_same_node_and_edges(self) -> None:
        registry = self.registry()

        self.assertEqual(registry.resolve("workflow.planning"), "workflow.planning")
        self.assertEqual(registry.resolve("workflows/planning.md"), "workflow.planning")
        self.assertEqual(registry.incident("workflow.planning"), registry.incident("workflows/planning.md"))

    def test_incoming_outgoing_and_incident_queries_are_directional(self) -> None:
        registry = self.registry()

        self.assertEqual(registry.incoming("workflow.planning"), ())
        self.assertEqual(len(registry.outgoing("workflow.planning")), 1)
        self.assertEqual(len(registry.incident("prompt.plan")), 1)
        self.assertEqual(registry.incident("prompt.plan")[0].direction, Direction.INCOMING)

    def test_edge_can_belong_to_multiple_groups_without_duplication(self) -> None:
        registry = self.registry(
            groups=(self.group(), self.group("policy-impact")),
            edges=(
                self.edge(
                    "planning-to-prompt",
                    "workflow.planning",
                    "prompt.plan",
                    groups=("semantic", "policy-impact"),
                ),
            ),
        )

        self.assertEqual(len(registry.edges), 1)
        self.assertEqual([g.id for g in registry.groups_for("workflow.planning")], ["policy-impact", "semantic"])
        self.assertEqual([e.id for e in registry.edges_for_group("semantic")], ["planning-to-prompt"])
        self.assertEqual([e.id for e in registry.edges_for_group("policy-impact")], ["planning-to-prompt"])

    def test_compatible_cross_source_node_declarations_merge_once(self) -> None:
        second_provenance = Provenance("second", "provider", "second")
        registry = EdgeRegistry(
            self.root,
            (
                Source(
                    "test",
                    GraphContribution(
                        (
                            self.node("workflow.planning", "workflows/planning.md"),
                            self.node("prompt.plan", "prompts/plan.md"),
                        ),
                        (self.group(),),
                        (self.edge("planning-to-prompt", "workflow.planning", "prompt.plan"),),
                    ),
                ),
                Source(
                    "second",
                    GraphContribution(
                        (
                            Node(
                                "workflow.planning",
                                ("workflows/planning.md",),
                                second_provenance,
                                {"repository_path": "workflows/planning.md"},
                            ),
                        ),
                        (),
                        (),
                    ),
                ),
            ),
        )

        self.assertEqual(len(registry.nodes), 2)
        self.assertEqual(registry.resolve("workflows/planning.md"), "workflow.planning")
        self.assertEqual(
            registry.nodes["workflow.planning"].metadata["repository_path"],
            "workflows/planning.md",
        )

    def test_group_filter_excludes_edges_outside_selected_group(self) -> None:
        registry = self.registry(
            nodes=(
                self.node("workflow.planning", "workflows/planning.md"),
                self.node("prompt.plan", "prompts/plan.md"),
                self.node("template.plan", "templates/PLAN.md"),
            ),
            groups=(self.group(), self.group("templates")),
            edges=(
                self.edge("prompt", "workflow.planning", "prompt.plan"),
                self.edge(
                    "template",
                    "workflow.planning",
                    "template.plan",
                    groups=("templates",),
                ),
            ),
        )

        self.assertEqual([v.edge.id for v in registry.outgoing("workflow.planning", ("semantic",))], ["prompt"])
        self.assertEqual([v.edge.id for v in registry.outgoing("workflow.planning", ("templates",))], ["template"])

    def test_exact_edge_traversal_follows_only_selected_edge(self) -> None:
        registry = self.registry()

        result = registry.traverse_edge("planning-to-prompt", Direction.OUTGOING)

        self.assertEqual(result.edges, ("planning-to-prompt",))
        self.assertEqual(result.steps[0].path_nodes, ("workflow.planning", "prompt.plan"))

    def test_group_traversal_follows_only_eligible_group_edges(self) -> None:
        registry = self.registry(
            nodes=(
                self.node("workflow.planning", "workflows/planning.md"),
                self.node("prompt.plan", "prompts/plan.md"),
                self.node("template.plan", "templates/PLAN.md"),
            ),
            groups=(self.group(), self.group("templates")),
            edges=(
                self.edge("prompt", "workflow.planning", "prompt.plan"),
                self.edge("blocked", "workflow.planning", "template.plan", traversable=False),
                self.edge(
                    "template",
                    "workflow.planning",
                    "template.plan",
                    groups=("templates",),
                ),
            ),
        )

        result = registry.traverse_group(
            "workflow.planning", "semantic", Direction.OUTGOING
        )

        self.assertEqual(result.edges, ("prompt",))

    def test_transitive_traversal_is_rejected_by_default(self) -> None:
        registry = self.registry()

        with self.assertRaises(ForbiddenTraversalError):
            registry.traverse_group(
                "workflow.planning",
                "semantic",
                Direction.OUTGOING,
                transitive=True,
            )

    def test_explicitly_permitted_transitive_traversal_terminates_cycle(self) -> None:
        registry = self.registry(
            nodes=(
                self.node("workflow.planning", "workflows/planning.md"),
                self.node("prompt.plan", "prompts/plan.md"),
                self.node("template.plan", "templates/PLAN.md"),
            ),
            groups=(self.group(transitive=True),),
            edges=(
                self.edge("a", "workflow.planning", "prompt.plan"),
                self.edge("b", "prompt.plan", "template.plan"),
                self.edge("c", "template.plan", "workflow.planning"),
            ),
        )

        result = registry.traverse_group(
            "workflow.planning", "semantic", Direction.OUTGOING, transitive=True
        )

        self.assertEqual(result.edges, ("a", "b", "c"))
        self.assertEqual(result.nodes, ("prompt.plan", "template.plan", "workflow.planning"))
        self.assertEqual(result.steps[1].path_edges, ("a", "b"))
        self.assertEqual(
            registry.find_cycle("semantic"),
            ("prompt.plan", "template.plan", "workflow.planning", "prompt.plan"),
        )

    def test_dependency_order_is_dependency_first_and_honors_preferred_ties(self) -> None:
        registry = self.registry(
            nodes=(
                self.node("a"),
                self.node("b"),
                self.node("c"),
                self.node("d"),
            ),
            groups=(self.group(transitive=True),),
            edges=(
                self.edge("a-b", "a", "b"),
                self.edge("a-c", "a", "c"),
                self.edge("c-d", "c", "d"),
            ),
        )

        self.assertEqual(
            registry.dependency_order(
                "semantic", ("a",), preferred_order=("a", "c", "d", "b")
            ),
            ("d", "c", "b", "a"),
        )

    def test_long_dependency_chain_and_cycle_do_not_use_python_recursion(self) -> None:
        node_count = 1_500
        node_ids = tuple(f"n{index:04d}" for index in range(node_count))
        nodes = tuple(self.node(node_id) for node_id in node_ids)
        chain = tuple(
            self.edge(f"e{index:04d}", node_ids[index], node_ids[index + 1])
            for index in range(node_count - 1)
        )
        registry = self.registry(
            nodes=nodes,
            groups=(self.group(transitive=True),),
            edges=chain,
        )

        self.assertIsNone(registry.find_cycle("semantic"))
        self.assertEqual(
            registry.dependency_order("semantic", (node_ids[0],)),
            tuple(reversed(node_ids)),
        )

        cyclic = self.registry(
            nodes=nodes,
            groups=(self.group(transitive=True),),
            edges=(*chain, self.edge("cycle", node_ids[-1], node_ids[0])),
        )
        cycle = cyclic.find_cycle("semantic")
        self.assertIsNotNone(cycle)
        assert cycle is not None
        self.assertEqual(len(cycle), node_count + 1)
        self.assertEqual(cycle[0], cycle[-1])
        with self.assertRaisesRegex(InvalidGroupError, "contains a cycle"):
            cyclic.dependency_order("semantic", (node_ids[0],))

    def test_provenance_is_retained_on_queries_and_traversal(self) -> None:
        registry = self.registry()

        self.assertEqual(registry.edge("planning-to-prompt").provenance, self.provenance)
        self.assertEqual(
            registry.traverse_edge("planning-to-prompt", Direction.OUTGOING).steps[0].edge.provenance,
            self.provenance,
        )

    def test_existing_unconnected_artifact_returns_empty_result(self) -> None:
        registry = self.registry()

        self.assertEqual(registry.incident("unconnected.md"), ())
        self.assertEqual(registry.groups_for("unconnected.md"), ())

    def test_unknown_group_is_rejected_for_unconnected_artifact(self) -> None:
        registry = self.registry()

        with self.assertRaises(UnknownGroupError):
            registry.incident("unconnected.md", ("unknown",))
        with self.assertRaises(UnknownGroupError):
            registry.traverse_group(
                "unconnected.md", "unknown", Direction.OUTGOING
            )

    def test_missing_artifact_and_unknown_logical_node_are_distinct(self) -> None:
        registry = self.registry()

        with self.assertRaises(MissingArtifactError):
            registry.incident("missing/file.md")
        with self.assertRaises(UnknownNodeError):
            registry.incident("workflow.unknown")

    def test_unknown_group_and_edge_return_typed_failures(self) -> None:
        registry = self.registry()

        with self.assertRaises(UnknownGroupError):
            registry.edges_for_group("unknown")
        with self.assertRaises(UnknownEdgeError):
            registry.edge("unknown")

    def test_duplicate_ids_dangling_endpoints_and_invalid_groups_are_rejected(self) -> None:
        with self.assertRaises(InvalidGroupError):
            self.registry(groups=(self.group(), self.group()))
        with self.assertRaises(InvalidEdgeError):
            self.registry(
                edges=(
                    self.edge("same", "workflow.planning", "prompt.plan"),
                    self.edge("same", "workflow.planning", "prompt.plan"),
                )
            )
        with self.assertRaises(InvalidEdgeError):
            self.registry(edges=(self.edge("dangling", "missing", "prompt.plan"),))
        with self.assertRaises(InvalidEdgeError):
            self.registry(
                edges=(
                    self.edge(
                        "bad-group",
                        "workflow.planning",
                        "prompt.plan",
                        groups=("unknown",),
                    ),
                )
            )

    def test_contradictory_aliases_and_duplicate_artifact_nodes_are_rejected(self) -> None:
        with self.assertRaises(AliasConflictError):
            self.registry(
                nodes=(
                    self.node("a", "workflows/planning.md"),
                    self.node("b", "workflows/planning.md"),
                ),
                edges=(),
            )

        with self.assertRaises(MissingArtifactError):
            self.registry(nodes=(self.node("a", "missing/path.md"),), edges=())

    def test_provider_cannot_misstate_authoritative_provenance(self) -> None:
        other = Provenance("other", "provider", "other.py")
        source = Source(
            "test",
            GraphContribution(
                (Node("a", (), other), Node("b", (), other)),
                (
                    EdgeGroup(
                        "semantic",
                        "Semantic edges.",
                        TraversalPolicy(
                            frozenset({Direction.INCOMING, Direction.OUTGOING})
                        ),
                        other,
                    ),
                ),
                (Edge("a-b", "a", "b", "projects", ("semantic",), other),),
            ),
        )

        with self.assertRaises(InvalidSourceError):
            EdgeRegistry(self.root, (source,))
        with self.assertRaises(AliasConflictError):
            self.registry(
                nodes=(
                    self.node("a", "b"),
                    self.node("b"),
                ),
                edges=(),
            )

    def test_repository_and_symlink_escape_are_rejected(self) -> None:
        with self.assertRaises(PathEscapeError):
            self.registry(nodes=(self.node("bad", "../outside.md"),), edges=())

        outside = Path(self.temp_dir.name).parent / "outside-graph-test.md"
        outside.write_text("outside", encoding="utf-8")
        symlink = self.root / "escape.md"
        try:
            symlink.symlink_to(outside)
            with self.assertRaises(PathEscapeError):
                self.registry(nodes=(self.node("bad", "escape.md"),), edges=())
        finally:
            symlink.unlink(missing_ok=True)
            outside.unlink(missing_ok=True)

    def test_unregistered_sources_contribute_no_edges(self) -> None:
        unregistered = Source(
            "unregistered",
            GraphContribution(
                (self.node("a"), self.node("b")),
                (self.group(),),
                (self.edge("hidden", "a", "b"),),
            ),
        )

        registry = EdgeRegistry(self.root, ())

        self.assertEqual(registry.edges, {})
        self.assertNotIn(unregistered.id, registry.edges)

    def test_result_order_is_independent_of_declaration_order(self) -> None:
        nodes = (
            self.node("workflow.planning", "workflows/planning.md"),
            self.node("prompt.plan", "prompts/plan.md"),
            self.node("template.plan", "templates/PLAN.md"),
        )
        edges = (
            self.edge("z", "workflow.planning", "template.plan"),
            self.edge("a", "workflow.planning", "prompt.plan"),
        )
        first = self.registry(nodes=nodes, edges=edges)
        second = self.registry(nodes=tuple(reversed(nodes)), edges=tuple(reversed(edges)))

        self.assertEqual(
            [view.edge.id for view in first.outgoing("workflow.planning")],
            [view.edge.id for view in second.outgoing("workflow.planning")],
        )
        self.assertEqual(list(first.edges), list(second.edges))
