from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeGroup,
    EdgeRegistry,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_analysis.standards_analysis import (
    POLICY_IMPACT,
    STANDARDS_REQUIRES,
    STANDARDS_SPECIALIZES,
    AnalysisError,
    ChangeDescriptor,
    ChangeKind,
    ReviewScope,
    SemanticProposal,
    classify_changes,
    generate_applicability_resolution_work,
    select_impact,
)
from tools.standards_engine.contracts.validate_contracts import validate
from tools.standards_graph.standards_graph import PolicyUnitGraphSource
from tools.standards_metadata.standards_metadata import (
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
)
from tools.standards_policy_impact.standards_policy_impact import (
    SOURCE_ID as POLICY_IMPACT_SOURCE_ID,
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
    PolicyImpactSource,
)


POLICY = "workflow.test.policy"
MODULE = "workflow.test"
SOURCE_ID = "fixture.relationships"
PROVENANCE = Provenance(SOURCE_ID, "provider", "fixture")
SCOPE = ReviewScope("structured", ("Policy",))
REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


def policy_unit(
    policy_id: str = POLICY,
    *,
    module: str = MODULE,
    revision: int = 3,
    representation: str = "sha256:" + "a" * 64,
    structural: str = "sha256:" + "b" * 64,
    heading: tuple[str, ...] = ("Policy",),
    predecessors: tuple[str, ...] = (),
) -> PolicyUnit:
    return PolicyUnit(
        policy_id,
        module,
        heading,
        revision,
        (f"{policy_id}.alias",),
        predecessors,
        (),
        "module.md",
        "## Policy\n\nText.\n",
        representation,
        structural,
        "units.toml",
    )


def corpus(
    *units: PolicyUnit,
    tombstones: tuple[PolicyUnitTombstone, ...] = (),
) -> PolicyUnitCorpus:
    return PolicyUnitCorpus("registry.toml", ("units.toml",), units, tombstones)


def groups() -> tuple[EdgeGroup, ...]:
    both = frozenset((Direction.INCOMING, Direction.OUTGOING))
    return (
        EdgeGroup(
            POLICY_IMPACT,
            "Policy consumers.",
            TraversalPolicy(both, False),
            PROVENANCE,
        ),
        EdgeGroup(
            STANDARDS_REQUIRES,
            "Required standards.",
            TraversalPolicy(both, True),
            PROVENANCE,
        ),
        EdgeGroup(
            STANDARDS_SPECIALIZES,
            "Specialized standards.",
            TraversalPolicy(both, True),
            PROVENANCE,
        ),
    )


@dataclass(frozen=True, slots=True)
class RelationshipSource:
    selected_edges: tuple[Edge, ...]
    selected_nodes: tuple[str, ...]
    id: str = SOURCE_ID

    def load(self) -> GraphContribution:
        return GraphContribution(
            tuple(Node(node, provenance=PROVENANCE) for node in sorted(self.selected_nodes)),
            groups(),
            self.selected_edges,
        )


def edge(
    edge_id: str,
    source: str,
    target: str,
    relation: str,
    group: str,
) -> Edge:
    return Edge(
        edge_id,
        source,
        target,
        relation,
        (group,),
        PROVENANCE,
        {"applicability": "true", "evidence_owner": "fixture"},
    )


class ImpactSelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def registry(
        self,
        policy_corpus: PolicyUnitCorpus,
        selected_edges: tuple[Edge, ...] = (),
        extra_nodes: tuple[str, ...] = (),
    ) -> EdgeRegistry:
        endpoints = {
            endpoint
            for selected in selected_edges
            for endpoint in (selected.source, selected.target)
        }
        policy_nodes = {
            item.id
            for item in (*policy_corpus.units, *policy_corpus.tombstones)
        }
        nodes = tuple(sorted(endpoints.union(extra_nodes) - policy_nodes))
        return EdgeRegistry(
            self.root,
            (
                PolicyUnitGraphSource(policy_corpus),
                RelationshipSource(selected_edges, nodes),
            ),
        )

    def compiled_policy_graph(
        self,
        policy_corpus: PolicyUnitCorpus,
        *,
        expression: dict[str, object],
        fact_schema_id: str = "fixture.policy-impact.facts",
        fact_declarations: list[dict[str, object]] | None = None,
        edge_id: str = "policy-impact:v1/workflow.test.policy/normative-consumer/consumer",
    ) -> tuple[EdgeRegistry, CompiledPolicyImpactSet]:
        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": fact_schema_id,
                "version": 1,
                "facts": fact_declarations or [],
            }
        )
        policy_edge = Edge(
            edge_id,
            POLICY,
            "consumer",
            "normative-consumer",
            (POLICY_IMPACT,),
            Provenance(POLICY_IMPACT_SOURCE_ID, "generator", "declarations.toml"),
        )
        semantics = PolicyImpactSemantics(
            edge_id,
            POLICY,
            "consumer",
            "normative-consumer",
            fact_schema.compile(expression),
            None,
            None,
            "source-to-consumer",
            "suite:evidence",
            "Fixture semantics.",
            "declarations.toml",
            "sha256:" + "d" * 64,
        )
        compiled = CompiledPolicyImpactSet(
            GraphContribution((), (), (policy_edge,)),
            {edge_id: semantics},
            fact_schema,
            "catalog.toml",
            ("declarations.toml",),
            ("registry.toml", "catalog.toml", "declarations.toml"),
            "sha256:" + "e" * 64,
            "sha256:" + "f" * 64,
        )
        graph = EdgeRegistry(
            self.root,
            (
                PolicyUnitGraphSource(policy_corpus),
                RelationshipSource((), ("consumer",)),
                PolicyImpactSource(compiled),
            ),
        )
        return graph, compiled

    def modification(self) -> object:
        selected = policy_unit()
        return classify_changes(
            corpus(selected),
            corpus(selected),
            (ChangeDescriptor(ChangeKind.MODIFICATION, (POLICY,), (POLICY,), SCOPE),),
        )[0]

    def test_policy_unit_source_registers_active_alias_and_retired_identity(self) -> None:
        active = policy_unit()
        retired = PolicyUnitTombstone(
            "workflow.test.retired",
            2,
            (),
            "review.retirement",
            "units.toml",
        )
        graph = self.registry(corpus(active, tombstones=(retired,)))

        self.assertEqual(graph.resolve(active.aliases[0]), active.id)
        self.assertEqual(graph.nodes[active.id].metadata["module"], MODULE)
        self.assertEqual(graph.nodes[retired.id].metadata["lifecycle"], "retired")
        self.assertEqual(graph.outgoing(active.id, (POLICY_IMPACT,)), ())

    def test_modification_unions_accepted_and_proposed_edges_with_both_traces(self) -> None:
        before = policy_unit()
        after = policy_unit(
            representation="sha256:" + "c" * 64,
            structural="sha256:" + "d" * 64,
        )
        change = classify_changes(
            corpus(before),
            corpus(after),
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (POLICY,),
                    (POLICY,),
                    SCOPE,
                ),
            ),
            (
                SemanticProposal(
                    POLICY,
                    3,
                    4,
                    "Change meaning.",
                    after.structural_digest,
                ),
            ),
        )[0]
        shared = edge("impact.shared", POLICY, "consumer.shared", "normative-consumer", POLICY_IMPACT)
        accepted = self.registry(
            corpus(before),
            (
                edge("impact.old", POLICY, "consumer.old", "normative-consumer", POLICY_IMPACT),
                shared,
            ),
        )
        proposed = self.registry(
            corpus(after),
            (
                edge("impact.new", POLICY, "consumer.new", "normative-consumer", POLICY_IMPACT),
                shared,
            ),
        )

        result = select_impact(change, accepted, proposed)

        self.assertEqual(
            tuple(candidate.edge_id for candidate in result.candidates),
            ("impact.new", "impact.old", "impact.shared"),
        )
        shared_candidate = result.candidates[2]
        self.assertEqual(tuple(trace.graph for trace in shared_candidate.traces), ("accepted", "proposed"))
        self.assertTrue(all(trace.seed == POLICY for trace in shared_candidate.traces))
        self.assertTrue(all(trace.path_nodes == (POLICY, "consumer.shared") for trace in shared_candidate.traces))
        self.assertTrue(all(trace.provenance_source == SOURCE_ID for trace in shared_candidate.traces))

    def test_addition_uses_policy_impact_and_transitive_owner_context_groups(self) -> None:
        added = policy_unit(revision=1)
        change = classify_changes(
            corpus(),
            corpus(added),
            (ChangeDescriptor(ChangeKind.ADDITION, (), (POLICY,), SCOPE),),
            (
                SemanticProposal(
                    POLICY,
                    None,
                    1,
                    "Create policy.",
                    added.structural_digest,
                ),
            ),
        )[0]
        proposed_edges = (
            edge("impact.consumer", POLICY, "consumer", "normative-consumer", POLICY_IMPACT),
            edge("requires.core", MODULE, "core", "requires", STANDARDS_REQUIRES),
            edge("requires.foundation", "core", "foundation", "requires", STANDARDS_REQUIRES),
            edge("specializes.base", MODULE, "base", "specializes", STANDARDS_SPECIALIZES),
            edge("outside", POLICY, "ignored", "other", "other-group"),
        )
        # The unrelated group is registered only to prove selected groups remain bounded.
        other_group = EdgeGroup(
            "other-group",
            "Unselected relationships.",
            TraversalPolicy(frozenset((Direction.INCOMING, Direction.OUTGOING)), True),
            PROVENANCE,
        )

        @dataclass(frozen=True, slots=True)
        class AdditionSource(RelationshipSource):
            def load(self) -> GraphContribution:
                contribution = RelationshipSource.load(self)
                return GraphContribution(
                    contribution.nodes,
                    (*contribution.groups, other_group),
                    contribution.edges,
                )

        endpoints = tuple(
            sorted(
                {
                    endpoint
                    for selected in proposed_edges
                    for endpoint in (selected.source, selected.target)
                }
                - {POLICY}
            )
        )
        proposed = EdgeRegistry(
            self.root,
            (PolicyUnitGraphSource(corpus(added)), AdditionSource(proposed_edges, endpoints)),
        )
        accepted = self.registry(corpus(), extra_nodes=(MODULE,))

        result = select_impact(change, accepted, proposed)

        self.assertEqual(
            tuple(candidate.edge_id for candidate in result.candidates),
            (
                "impact.consumer",
                "requires.core",
                "requires.foundation",
                "specializes.base",
            ),
        )
        foundation = next(item for item in result.candidates if item.edge_id == "requires.foundation")
        self.assertEqual(foundation.traces[0].seed, MODULE)
        self.assertEqual(foundation.traces[0].path_nodes, (MODULE, "core", "foundation"))

    def test_removal_traverses_only_accepted_policy_impact(self) -> None:
        before = policy_unit()
        retired = PolicyUnitTombstone(POLICY, 3, (), "review.retirement", "units.toml")
        change = classify_changes(
            corpus(before),
            corpus(tombstones=(retired,)),
            (ChangeDescriptor(ChangeKind.REMOVAL, (POLICY,), (), ReviewScope("whole-artifact")),),
        )[0]
        accepted = self.registry(
            corpus(before),
            (edge("impact.former", POLICY, "consumer.former", "normative-consumer", POLICY_IMPACT),),
        )
        proposed = self.registry(corpus(tombstones=(retired,)))

        result = select_impact(change, accepted, proposed)

        self.assertEqual(tuple(item.edge_id for item in result.candidates), ("impact.former",))
        self.assertEqual(result.candidates[0].traces[0].graph, "accepted")

    def test_missing_seed_or_group_is_a_typed_analysis_failure(self) -> None:
        selected = policy_unit()
        change = classify_changes(
            corpus(selected),
            corpus(selected),
            (ChangeDescriptor(ChangeKind.MODIFICATION, (POLICY,), (POLICY,), SCOPE),),
        )[0]
        missing_seed = EdgeRegistry(
            self.root,
            (RelationshipSource((), ("unrelated",)),),
        )

        with self.assertRaises(AnalysisError) as caught:
            select_impact(change, missing_seed, missing_seed)
        self.assertEqual(caught.exception.failure.code, "IMPACT.GRAPH_INVALID")

    def test_compiled_policy_edge_requires_and_retains_matching_semantics(self) -> None:
        selected = policy_unit()
        change = classify_changes(
            corpus(selected),
            corpus(selected),
            (ChangeDescriptor(ChangeKind.MODIFICATION, (POLICY,), (POLICY,), SCOPE),),
        )[0]
        edge_id = "policy-impact:v1/workflow.test.policy/normative-consumer/consumer"
        policy_edge = Edge(
            edge_id,
            POLICY,
            "consumer",
            "normative-consumer",
            (POLICY_IMPACT,),
            Provenance(POLICY_IMPACT_SOURCE_ID, "generator", "declarations.toml"),
        )
        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "fixture.applicability",
                "version": 1,
                "facts": [],
            }
        )
        semantics = PolicyImpactSemantics(
            edge_id,
            POLICY,
            "consumer",
            "normative-consumer",
            fact_schema.compile({"operator": "always"}),
            None,
            None,
            "source-to-consumer",
            "suite:evidence",
            "Fixture semantics.",
            "declarations.toml",
            "sha256:" + "d" * 64,
        )
        compiled = CompiledPolicyImpactSet(
            GraphContribution((), (), (policy_edge,)),
            {edge_id: semantics},
            fact_schema,
            "catalog.toml",
            ("declarations.toml",),
            ("registry.toml", "catalog.toml", "declarations.toml"),
            "sha256:" + "e" * 64,
            "sha256:" + "f" * 64,
        )
        graph = EdgeRegistry(
            self.root,
            (
                PolicyUnitGraphSource(corpus(selected)),
                RelationshipSource((), ("consumer",)),
                PolicyImpactSource(compiled),
            ),
        )

        with self.assertRaises(AnalysisError) as caught:
            select_impact(change, graph, graph)
        self.assertEqual(
            caught.exception.failure.code,
            "IMPACT.POLICY_SEMANTICS_MISSING",
        )

        result = select_impact(change, graph, graph, compiled, compiled)

        self.assertEqual(result.candidates[0].traces[0].policy_semantics, semantics)

    def test_unknown_applicability_remains_unknown_and_creates_exact_resolution_work(self) -> None:
        declarations = [
            {
                "id": "change.requires_review",
                "type": "boolean",
                "nullable": False,
                "aliases": [],
            }
        ]
        graph, compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={
                "operator": "equals",
                "fact": "change.requires_review",
                "value": True,
            },
            fact_declarations=declarations,
        )

        selection = select_impact(
            self.modification(),
            graph,
            graph,
            compiled,
            compiled,
            compiled.fact_schema.bind({}),
        )

        candidate = selection.candidates[0]
        self.assertEqual(candidate.applicability, "unknown")
        self.assertEqual(candidate.unresolved_facts, ("change.requires_review",))
        self.assertEqual(
            candidate.conservative_review_scope,
            ReviewScope("whole-artifact"),
        )
        work = generate_applicability_resolution_work((selection,))
        self.assertEqual([item.fact for item in work.questions], ["change.requires_review"])
        self.assertEqual(len(work.obligations), 1)
        obligation = work.obligations[0].as_contract()
        self.assertEqual(obligation["applicability"], "unknown")
        self.assertEqual(obligation["scope"], {"kind": "whole-artifact"})
        self.assertEqual(obligation["reason"]["fact"], "change.requires_review")
        validate(SCHEMA, SCHEMA["$defs"]["Question"], work.questions[0].as_contract(), "$question")
        validate(SCHEMA, SCHEMA["$defs"]["Obligation"], obligation, "$obligation")

    def test_false_applicability_creates_no_resolution_work(self) -> None:
        declarations = [
            {
                "id": "change.requires_review",
                "type": "boolean",
                "nullable": False,
                "aliases": [],
            }
        ]
        graph, compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={
                "operator": "equals",
                "fact": "change.requires_review",
                "value": True,
            },
            fact_declarations=declarations,
        )
        facts = compiled.fact_schema.bind(
            {
                "change.requires_review": {
                    "type": "boolean",
                    "state": "known",
                    "value": False,
                }
            }
        )

        selection = select_impact(
            self.modification(), graph, graph, compiled, compiled, facts
        )

        self.assertEqual(selection.candidates[0].applicability, "false")
        self.assertIsNone(selection.candidates[0].conservative_review_scope)
        self.assertEqual(
            generate_applicability_resolution_work((selection,)).obligations,
            (),
        )

    def test_only_material_unknown_facts_create_resolution_work(self) -> None:
        declarations = [
            {
                "id": "change.confirmed",
                "type": "boolean",
                "nullable": False,
                "aliases": [],
            },
            {
                "id": "change.requires_review",
                "type": "boolean",
                "nullable": False,
                "aliases": [],
            },
        ]
        graph, compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={
                "operator": "any",
                "expressions": [
                    {
                        "operator": "equals",
                        "fact": "change.confirmed",
                        "value": True,
                    },
                    {
                        "operator": "equals",
                        "fact": "change.requires_review",
                        "value": True,
                    },
                ],
            },
            fact_declarations=declarations,
        )
        facts = compiled.fact_schema.bind(
            {
                "change.confirmed": {
                    "type": "boolean",
                    "state": "known",
                    "value": False,
                }
            }
        )

        selection = select_impact(
            self.modification(), graph, graph, compiled, compiled, facts
        )
        work = generate_applicability_resolution_work((selection,))

        self.assertEqual(selection.candidates[0].unresolved_facts, ("change.requires_review",))
        self.assertEqual([item.fact for item in work.questions], ["change.requires_review"])
        self.assertEqual(
            [item.reason["fact"] for item in work.obligations],
            ["change.requires_review"],
        )

    def test_accepted_true_trace_dominates_proposed_unknown_trace(self) -> None:
        declarations = [
            {
                "id": "change.requires_review",
                "type": "boolean",
                "nullable": False,
                "aliases": [],
            }
        ]
        accepted_graph, accepted_compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={"operator": "always"},
            fact_declarations=declarations,
        )
        proposed_graph, proposed_compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={
                "operator": "equals",
                "fact": "change.requires_review",
                "value": True,
            },
            fact_declarations=declarations,
        )

        selection = select_impact(
            self.modification(),
            accepted_graph,
            proposed_graph,
            accepted_compiled,
            proposed_compiled,
            accepted_compiled.fact_schema.bind({}),
        )

        self.assertEqual(selection.candidates[0].applicability, "true")
        self.assertEqual(selection.candidates[0].unresolved_facts, ())
        self.assertEqual(
            generate_applicability_resolution_work((selection,)).questions,
            (),
        )

    def test_fact_schema_evolution_rejects_instead_of_guessing(self) -> None:
        accepted_graph, accepted_compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={"operator": "always"},
            fact_schema_id="fixture.accepted.facts",
        )
        proposed_graph, proposed_compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={"operator": "always"},
            fact_schema_id="fixture.proposed.facts",
        )

        with self.assertRaises(AnalysisError) as caught:
            select_impact(
                self.modification(),
                accepted_graph,
                proposed_graph,
                accepted_compiled,
                proposed_compiled,
            )
        self.assertEqual(
            caught.exception.failure.code,
            "IMPACT.FACT_SCHEMA_EVOLUTION_UNSUPPORTED",
        )

    def test_fact_set_from_another_schema_is_rejected(self) -> None:
        graph, compiled = self.compiled_policy_graph(
            corpus(policy_unit()),
            expression={"operator": "always"},
        )
        incompatible = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "fixture.other.facts",
                "version": 1,
                "facts": [],
            }
        ).bind({})

        with self.assertRaises(AnalysisError) as caught:
            select_impact(
                self.modification(),
                graph,
                graph,
                compiled,
                compiled,
                incompatible,
            )
        self.assertEqual(caught.exception.failure.code, "IMPACT.FACT_SET_INVALID")

    def test_cross_module_move_unions_policy_and_owner_context(self) -> None:
        before = policy_unit()
        after = policy_unit(module="workflow.destination", heading=("Moved",))
        change = classify_changes(
            corpus(before),
            corpus(after),
            (
                ChangeDescriptor(
                    ChangeKind.MOVE,
                    (POLICY,),
                    (POLICY,),
                    SCOPE,
                    MODULE,
                    after.module,
                ),
            ),
        )[0]
        accepted = self.registry(
            corpus(before),
            (
                edge("impact.before", POLICY, "consumer.before", "normative-consumer", POLICY_IMPACT),
                edge("requires.before", MODULE, "core.before", "requires", STANDARDS_REQUIRES),
            ),
        )
        proposed = self.registry(
            corpus(after),
            (
                edge("impact.after", POLICY, "consumer.after", "normative-consumer", POLICY_IMPACT),
                edge(
                    "specializes.after",
                    after.module,
                    "base.after",
                    "specializes",
                    STANDARDS_SPECIALIZES,
                ),
            ),
        )

        result = select_impact(change, accepted, proposed)

        self.assertEqual(
            [item.edge_id for item in result.candidates],
            [
                "impact.after",
                "impact.before",
                "requires.before",
                "specializes.after",
            ],
        )

    def test_split_unions_predecessor_and_every_successor_impact(self) -> None:
        predecessor = policy_unit("workflow.test.combined")
        first = policy_unit(
            "workflow.test.first",
            revision=1,
            heading=("First",),
            predecessors=(predecessor.id,),
        )
        second = policy_unit(
            "workflow.test.second",
            revision=1,
            heading=("Second",),
            predecessors=(predecessor.id,),
        )
        tombstone = PolicyUnitTombstone(
            predecessor.id,
            predecessor.semantic_revision,
            (first.id, second.id),
            "review.split",
            "units.toml",
        )
        change = classify_changes(
            corpus(predecessor),
            corpus(first, second, tombstones=(tombstone,)),
            (
                ChangeDescriptor(
                    ChangeKind.SPLIT,
                    (predecessor.id,),
                    (first.id, second.id),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (
                SemanticProposal(first.id, None, 1, "First successor.", first.structural_digest),
                SemanticProposal(second.id, None, 1, "Second successor.", second.structural_digest),
            ),
        )[0]
        accepted = self.registry(
            corpus(predecessor),
            (edge("impact.combined", predecessor.id, "consumer.old", "normative-consumer", POLICY_IMPACT),),
        )
        proposed = self.registry(
            corpus(first, second, tombstones=(tombstone,)),
            (
                edge("impact.first", first.id, "consumer.first", "normative-consumer", POLICY_IMPACT),
                edge("impact.second", second.id, "consumer.second", "normative-consumer", POLICY_IMPACT),
            ),
        )

        result = select_impact(change, accepted, proposed)

        self.assertEqual(
            [item.edge_id for item in result.candidates],
            ["impact.combined", "impact.first", "impact.second"],
        )

    def test_merge_unions_every_predecessor_and_successor_impact(self) -> None:
        first = policy_unit("workflow.test.first")
        second = policy_unit("workflow.test.second", heading=("Second",))
        merged = policy_unit(
            "workflow.test.merged",
            revision=1,
            heading=("Merged",),
            predecessors=(first.id, second.id),
        )
        tombstones = (
            PolicyUnitTombstone(first.id, first.semantic_revision, (merged.id,), "review.merge", "units.toml"),
            PolicyUnitTombstone(second.id, second.semantic_revision, (merged.id,), "review.merge", "units.toml"),
        )
        change = classify_changes(
            corpus(first, second),
            corpus(merged, tombstones=tombstones),
            (
                ChangeDescriptor(
                    ChangeKind.MERGE,
                    (first.id, second.id),
                    (merged.id,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (
                SemanticProposal(merged.id, None, 1, "Merged successor.", merged.structural_digest),
            ),
        )[0]
        accepted = self.registry(
            corpus(first, second),
            (
                edge("impact.first", first.id, "consumer.first", "normative-consumer", POLICY_IMPACT),
                edge("impact.second", second.id, "consumer.second", "normative-consumer", POLICY_IMPACT),
            ),
        )
        proposed = self.registry(
            corpus(merged, tombstones=tombstones),
            (edge("impact.merged", merged.id, "consumer.merged", "normative-consumer", POLICY_IMPACT),),
        )

        result = select_impact(change, accepted, proposed)

        self.assertEqual(
            [item.edge_id for item in result.candidates],
            ["impact.first", "impact.merged", "impact.second"],
        )


if __name__ == "__main__":
    unittest.main()
