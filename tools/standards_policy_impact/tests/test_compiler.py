from __future__ import annotations

import csv
import tempfile
import textwrap
import unittest
from dataclasses import replace
from pathlib import Path

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_applicability.standards_applicability import Truth
from tools.standards_graph.standards_graph import (
    PolicyUnitGraphSource,
    metadata_dependency_source,
)
from tools.standards_metadata.standards_metadata import (
    CanonicalModuleCorpus,
    CanonicalStandardsCorpus,
    ModuleMetadata,
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    DEFAULT_AUTHORING_CONTRACT,
    PolicyImpactError,
    PolicyImpactSource,
    compile_policy_impact,
    policy_impact_edge_id,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


class PolicyImpactCompilerTest(unittest.TestCase):
    def test_repository_declarations_compile_one_graph_and_semantics_view(self) -> None:
        corpus = load_canonical_standards_corpus(REPO_ROOT)
        compiled = compile_policy_impact(REPO_ROOT, corpus)

        self.assertEqual(
            {edge.id for edge in compiled.graph.edges},
            set(compiled.semantics),
        )
        self.assertEqual(
            set(compiled.artifacts),
            {node.id for node in compiled.graph.nodes},
        )
        self.assertEqual(
            set(compiled.relationship_kinds),
            {semantics.relation for semantics in compiled.semantics.values()},
        )
        self.assertEqual(
            {group.id for group in compiled.graph.groups},
            {"policy-impact", "semantic"},
        )
        self.assertEqual(
            compiled.artifact_for("prompts/implement-plan.md").artifact_kind,
            "prompt",
        )
        edge_id = (
            "policy-impact:v1/workflow.planning.plan-admission/prompt-projection/"
            "prompts%2Fimplement-plan.md"
        )
        edge = next(edge for edge in compiled.graph.edges if edge.id == edge_id)
        semantics = compiled.semantics_for(edge_id)
        self.assertEqual(edge.metadata, {})
        self.assertEqual(edge.groups, ("policy-impact", "semantic"))
        self.assertEqual(semantics.propagation, "source-to-consumer")
        self.assertEqual(
            semantics.applicability_program.as_expression(),
            {"operator": "always"},
        )
        self.assertEqual(semantics.applicability_program.referenced_facts, ())
        self.assertEqual(
            semantics.evidence_owner,
            "suite:plan-implementation-entrypoint",
        )

    def test_compiled_authority_joins_module_and_policy_unit_graph_sources(self) -> None:
        corpus = load_canonical_standards_corpus(REPO_ROOT)
        compiled = compile_policy_impact(REPO_ROOT, corpus)
        registry = EdgeRegistry(
            REPO_ROOT,
            (
                metadata_dependency_source(corpus.modules),
                PolicyUnitGraphSource(corpus.policy_unit_corpus),
                PolicyImpactSource(compiled),
            ),
        )

        self.assertEqual(
            registry.resolve("workflows/planning.md"),
            "workflow.planning",
        )
        self.assertEqual(
            registry.incident("workflow.planning", ("policy-impact",)),
            registry.incident("workflows/planning.md", ("policy-impact",)),
        )
        self.assertEqual(registry.outgoing("workflow.planning", ("policy-impact",)), ())

    def test_repository_matches_admitted_relationship_migration_identity_sets(self) -> None:
        inventory_path = (
            REPO_ROOT
            / "docs/plans/standards-engine-policy-impact-authority-v2/reports/relationship-migration.tsv"
        )
        with inventory_path.open(encoding="utf-8", newline="") as handle:
            rows = tuple(csv.DictReader(handle, delimiter="\t"))

        self.assertTrue(rows)
        self.assertEqual(
            len({row["old_edge_id"] for row in rows}),
            len(rows),
        )
        self.assertEqual(
            len({row["new_edge_id"] for row in rows}),
            len(rows),
        )

        corpus = load_canonical_standards_corpus(REPO_ROOT)
        compiled = compile_policy_impact(REPO_ROOT, corpus)
        migrated_keys = {
            (row["source"], row["consumer"])
            for row in rows
        }
        actual_ids = {
            edge_id
            for edge_id, semantics in compiled.semantics.items()
            if (semantics.source, semantics.consumer) in migrated_keys
        }
        expected_ids = {row["new_edge_id"] for row in rows}

        self.assertEqual(actual_ids, expected_ids)
        for row in rows:
            with self.subTest(edge=row["new_edge_id"]):
                semantics = compiled.semantics_for(row["new_edge_id"])
                self.assertEqual(semantics.source, row["source"])
                self.assertEqual(semantics.consumer, row["consumer"])
                self.assertEqual(semantics.relation, row["new_relation"])
                self.assertEqual(
                    semantics.declaration_source,
                    row["declaration_source"],
                )
                self.assertEqual(
                    row["disposition"],
                    "retain"
                    if row["old_edge_id"] == row["new_edge_id"]
                    else "reclassify",
                )

    def test_invalid_declarations_reject_with_typed_failures(self) -> None:
        cases = (
            (
                "duplicate",
                self.relationships(
                    self.relationship(),
                    self.relationship(),
                ),
                "POLICY_IMPACT.DUPLICATE_EDGE",
            ),
            (
                "unknown-consumer",
                self.relationships(self.relationship(consumer="missing")),
                "POLICY_IMPACT.UNKNOWN_CONSUMER",
            ),
            (
                "missing-applicability",
                self.relationships(
                    self.relationship().replace(
                        'applicability = { operator = "always" }\n',
                        "",
                    )
                ),
                "POLICY_IMPACT.APPLICABILITY",
            ),
            (
                "unknown-relation",
                self.relationships(self.relationship(relation="missing")),
                "POLICY_IMPACT.RELATION",
            ),
            (
                "missing-evidence",
                self.relationships(
                    self.relationship(evidence="suite:missing")
                ),
                "POLICY_IMPACT.EVIDENCE_OWNER",
            ),
            (
                "incompatible-target",
                self.relationships(self.relationship(relation="template-projection")),
                "POLICY_IMPACT.INCOMPATIBLE_TARGET",
            ),
        )
        for name, declarations, code in cases:
            with self.subTest(name=name):
                with self.fixture(declarations) as (root, modules):
                    with self.assertRaises(PolicyImpactError) as caught:
                        compile_policy_impact(root, modules, "registry.toml")
                self.assertEqual(caught.exception.failure.code, code)

    def test_relationship_sources_require_exact_active_owner_policy_units(self) -> None:
        source_cases = (
            ("workflow.planning", None, "POLICY_IMPACT.MODULE_SOURCE"),
            (
                "workflow.planning.alias",
                "alias",
                "POLICY_IMPACT.NONCANONICAL_SOURCE",
            ),
            (
                "workflow.planning.policy",
                "retired",
                "POLICY_IMPACT.NONCANONICAL_SOURCE",
            ),
        )
        for source, corpus_change, code in source_cases:
            with self.subTest(source=source):
                declaration = self.relationships(
                    self.relationship().replace(
                        'source = "workflow.planning.policy"',
                        f'source = "{source}"',
                    )
                )
                with self.fixture(declaration) as (root, corpus):
                    unit = corpus.policy_unit_corpus.units[0]
                    if corpus_change == "alias":
                        policy_units = replace(
                            corpus.policy_unit_corpus,
                            units=(replace(unit, aliases=(source,)),),
                        )
                        corpus = replace(corpus, policy_unit_corpus=policy_units)
                    elif corpus_change == "retired":
                        policy_units = replace(
                            corpus.policy_unit_corpus,
                            units=(),
                            tombstones=(
                                PolicyUnitTombstone(source, 1, (), "review", "units.toml"),
                            ),
                        )
                        corpus = replace(corpus, policy_unit_corpus=policy_units)
                    with self.assertRaises(PolicyImpactError) as caught:
                        compile_policy_impact(root, corpus, "registry.toml")
                self.assertEqual(caught.exception.failure.code, code)

        with self.fixture(
            self.relationships(self.relationship()).replace(
                'owner = "workflow.planning"',
                'owner = "workflow.other"',
            )
        ) as (root, corpus):
            other = replace(
                corpus.modules[0],
                path="workflows/other.md",
                module_id="workflow.other",
                owner="workflows/other.md",
            )
            modules = replace(
                corpus.module_corpus,
                members=(*corpus.module_corpus.members, other.path),
                modules=(*corpus.modules, other),
            )
            corpus = replace(corpus, module_corpus=modules)
            with self.assertRaises(PolicyImpactError) as caught:
                compile_policy_impact(root, corpus, "registry.toml")
        self.assertEqual(caught.exception.failure.code, "POLICY_IMPACT.CROSS_OWNER_SOURCE")

    def test_v1_and_dual_authority_inputs_reject_without_compatibility(self) -> None:
        with self.fixture(self.relationships(self.relationship())) as (root, modules):
            catalog = root / "catalog.toml"
            catalog.write_text(
                catalog.read_text(encoding="utf-8")
                + textwrap.dedent(
                    """
                    [[edges]]
                    id = "forbidden"
                    source = "prompt"
                    target = "suite"
                    relation = "prompt-projection"
                    groups = ["policy-impact"]
                    traversable = true
                    """
                ),
                encoding="utf-8",
            )
            with self.assertRaises(PolicyImpactError) as caught:
                compile_policy_impact(root, modules, "registry.toml")
            self.assertEqual(caught.exception.failure.code, "POLICY_IMPACT.INVALID")

        with self.fixture(self.relationships(self.relationship())) as (root, corpus):
            declarations = root / "declarations.toml"
            declarations.write_text(
                declarations.read_text(encoding="utf-8").replace(
                    "schema_version = 2",
                    "schema_version = 1",
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(PolicyImpactError) as caught:
                compile_policy_impact(root, corpus, "registry.toml")
            self.assertEqual(
                caught.exception.failure.code,
                "POLICY_IMPACT.UNSUPPORTED_DECLARATION",
            )

    def test_edge_identity_is_injective_for_separator_bearing_ids(self) -> None:
        first = policy_impact_edge_id(
            "a",
            "router-projection",
            "b:router-projection:c",
        )
        second = policy_impact_edge_id(
            "a:router-projection:b",
            "router-projection",
            "c",
        )

        self.assertNotEqual(first, second)
        self.assertEqual(
            first,
            "policy-impact:v1/a/router-projection/b%3Arouter-projection%3Ac",
        )

    def test_conditional_relationship_compiles_and_evaluates_one_program(self) -> None:
        declaration = self.relationship().replace(
            'applicability = { operator = "always" }',
            'applicability = { operator = "equals", fact = "changed", value = true }',
        )
        with self.fixture(self.relationships(declaration)) as (root, modules):
            (root / "facts.toml").write_text(
                textwrap.dedent(
                    """
                    schema_version = 1
                    id = "policy-impact.applicability"

                    [[facts]]
                    id = "changed"
                    semantic_revision = 1
                    type = "boolean"
                    nullable = false
                    aliases = []
                    meaning = "Whether the standards change occurred."
                    context_kind = "standards-change"
                    answer_contract = "fact-value.v1"
                    evidence_contract = "evidence-reference.v1"
                    authorization_capability = "standards.analyze"
                    prompt = "Did the standards change occur?"
                    """
                ).lstrip(),
                encoding="utf-8",
            )
            compiled = compile_policy_impact(root, modules, "registry.toml")

        program = next(iter(compiled.semantics.values())).applicability_program
        fact_schema = compiled.fact_schema
        self.assertEqual(program.referenced_facts, ("changed",))
        self.assertIs(
            program.evaluate(
                fact_schema.bind(
                    {
                        "changed": {
                            "type": "boolean",
                            "state": "known",
                            "value": True,
                        }
                    }
                )
            ).truth,
            Truth.TRUE,
        )
        self.assertEqual(
            program.evaluate(fact_schema.bind({})).unresolved_facts,
            ("changed",),
        )

    @staticmethod
    def relationship(
        *,
        consumer: str = "prompt",
        relation: str = "prompt-projection",
        evidence: str = "suite:evidence",
    ) -> str:
        return textwrap.dedent(
            f"""
            [[relationships]]
            source = "workflow.planning.policy"
            consumer = "{consumer}"
            relation = "{relation}"
            applicability = {{ operator = "always" }}
            evidence_owner = "{evidence}"
            rationale = "Test relationship."
            """
        )

    @staticmethod
    def relationships(*items: str) -> str:
        return 'schema_version = 2\nowner = "workflow.planning"\n' + "".join(items)

    def fixture(self, declarations: str):
        case = tempfile.TemporaryDirectory()
        root = Path(case.name)
        self.write(
            root,
            "registry.toml",
            """
            schema_version = 2
            source_id = "standards.policy-impact"
            authoring_contract = "contract.toml"
            node_catalog = "catalog.toml"
            fact_catalog = "facts.toml"
            suite_registry = "suites.toml"
            declaration_sources = ["declarations.toml"]
            """,
        )
        self.write(
            root,
            "contract.toml",
            (REPO_ROOT / DEFAULT_AUTHORING_CONTRACT).read_text(encoding="utf-8"),
        )
        self.write(
            root,
            "catalog.toml",
            """
            schema_version = 2
            source_id = "standards.policy-impact-catalog"

            [[nodes]]
            id = "prompt"
            metadata = { repository_path = "prompt.md", artifact_kind = "prompt", authority = "projection" }

            [[nodes]]
            id = "suite"
            metadata = { repository_path = "suite.toml", artifact_kind = "enforcement-suite", suite_id = "evidence", authority = "evidence" }
            """,
        )
        self.write(
            root,
            "suites.toml",
            """
            schema_version = 1

            [[suites]]
            id = "evidence"
            path = "suite.toml"
            requires = []
            """,
        )
        self.write(
            root,
            "facts.toml",
            'schema_version = 1\nid = "policy-impact.applicability"\nfacts = []\n',
        )
        self.write(root, "declarations.toml", declarations)
        module = ModuleMetadata(
            "workflows/planning.md",
            "workflow.planning",
            "workflow",
            "MUST",
            "planned",
            "local",
            (),
            (),
            "tests",
            "workflows/planning.md",
        )
        module_corpus = CanonicalModuleCorpus(
            "corpus.toml",
            (module.path,),
            (module,),
        )
        unit = PolicyUnit(
            "workflow.planning.policy",
            "workflow.planning",
            ("Policy",),
            1,
            (),
            (),
            (),
            module.path,
            "## Policy\n",
            "sha256:" + "a" * 64,
            "sha256:" + "b" * 64,
            "units.toml",
        )
        corpus = CanonicalStandardsCorpus(
            module_corpus,
            PolicyUnitCorpus("units.toml", ("units.toml",), (unit,), ()),
        )

        class Fixture:
            def __enter__(self):
                return root, corpus

            def __exit__(self, *_):
                case.cleanup()

        return Fixture()

    @staticmethod
    def write(root: Path, path: str, content: str) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
