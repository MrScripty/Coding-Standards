from __future__ import annotations

import tempfile
import textwrap
import json
import tomllib
import unittest
from pathlib import Path

from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    MetadataError,
    load_canonical_standards_corpus,
    load_canonical_module_corpus,
    load_policy_unit_corpus,
    project_unmapped_module,
)
from tools.standards_contracts.standards_contracts import compile_contracts


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)
with (
    REPO_ROOT / "tools/standards_engine/contracts/a1-interface.toml"
).open("rb") as source:
    CONTRACTS = compile_contracts(SCHEMA, tomllib.load(source))


class PolicyUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, value: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(value).lstrip(), encoding="utf-8")

    def module(self, body: str, *, duplicate: bool = False) -> None:
        content = textwrap.dedent(
            """
            # Module

            **Standards metadata**

            - ID: `workflow.test`
            - Role: `workflow`
            - Level: `MUST`
            - Applies when: The fixture applies.
            - Does not apply when: The fixture does not apply.
            - Requires: `none`
            - Specializes: `none`
            - Verification: Policy-unit evidence.
            - Canonical owner: `module.md`

            ## Policy
            """
        ).lstrip() + f"\n{body}\n"
        if duplicate:
            content += f"\n## Policy\n\n{body}\n"
        self.write("module.md", content)
        self.write(
            "corpus.toml",
            'schema_version = 1\nmembers = ["module.md"]\n',
        )

    def declarations(self, value: str) -> None:
        self.write("units/registry.toml", 'schema_version = 1\nsources = ["units/module.toml"]\n')
        self.write("units/module.toml", f"schema_version = 1\n\n{value}")

    def load(self):
        modules = load_canonical_module_corpus(self.root, "corpus.toml")
        return load_policy_unit_corpus(self.root, modules, "units/registry.toml")

    def test_repository_seed_resolves_exact_heading_and_module_path(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)

        corpus = load_policy_unit_corpus(REPO_ROOT, modules)

        unit = corpus.resolve("workflow.verification.acceptance-claims")
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit.document, "workflows/verification.md")
        self.assertEqual(unit.heading_path, ("Acceptance Is A Set Of Claims",))
        CONTRACTS.validate("PolicyUnitDeclaration", unit.as_declaration())

    def test_combined_corpus_resolves_modules_and_policy_units_from_one_snapshot(self) -> None:
        corpus = load_canonical_standards_corpus(REPO_ROOT)

        planning = corpus.resolve_module("workflow.planning")
        admission = corpus.resolve_policy_unit("workflow.planning.written-plan-applicability")
        self.assertIsNotNone(planning)
        self.assertIsNotNone(admission)
        assert planning is not None and admission is not None
        self.assertEqual(admission.module, planning.module_id)
        self.assertIn(admission, corpus.policy_unit_corpus.for_module(planning.module_id))

    def test_rewrapping_changes_representation_not_structure(self) -> None:
        self.module("A policy paragraph uses multiple words.")
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.policy"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """
        )
        first = self.load().units[0]
        self.module("A policy paragraph uses\nmultiple words.")
        second = self.load().units[0]

        self.assertNotEqual(first.representation_digest, second.representation_digest)
        self.assertEqual(first.structural_digest, second.structural_digest)
        self.assertEqual(first.semantic_revision, second.semantic_revision)

    def test_locator_must_resolve_exactly_once(self) -> None:
        self.module("Policy text.", duplicate=True)
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.policy"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """
        )

        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LOCATOR_COUNT")

    def test_split_lifecycle_requires_reciprocal_tombstone_and_predecessors(self) -> None:
        self.module("Policy text.")
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.successor"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            predecessors = ["workflow.test.retired"]

            [[tombstone]]
            id = "workflow.test.retired"
            retired_semantic_revision = 2
            successors = ["workflow.test.successor"]
            evidence = "review.split"
            """
        )

        corpus = self.load()
        self.assertEqual(corpus.tombstones[0].successors, ("workflow.test.successor",))
        self.assertEqual(corpus.tombstones[0].id, "workflow.test.retired")

        path = self.root / "units/module.toml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'successors = ["workflow.test.successor"]', "successors = []"
            ),
            encoding="utf-8",
        )
        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.PREDECESSOR_MISMATCH")

    def test_identity_conflicts_and_legacy_ids_are_rejected(self) -> None:
        self.module("Policy text.")
        self.declarations(
            """
            [[policy_unit]]
            id = "STD-0001"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """
        )
        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LEGACY_ID")

    def test_two_active_ids_cannot_own_the_same_locator(self) -> None:
        self.module("Policy text.")
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.first"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1

            [[policy_unit]]
            id = "workflow.test.second"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """
        )

        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LOCATOR_CONFLICT")

    def test_nested_policy_unit_locators_are_rejected_as_overlapping(self) -> None:
        self.module("### Detail\n\nNested policy text.")
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.policy"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1

            [[policy_unit]]
            id = "workflow.test.detail"
            module = "workflow.test"
            heading_path = ["Policy", "Detail"]
            semantic_revision = 1
            """
        )

        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LOCATOR_OVERLAP")

    def test_unmapped_projection_excludes_exact_policy_unit_scope(self) -> None:
        self.module("Policy text.")
        self.declarations(
            """
            [[policy_unit]]
            id = "workflow.test.policy"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """
        )
        modules = load_canonical_module_corpus(self.root, "corpus.toml")
        units = load_policy_unit_corpus(
            self.root,
            modules,
            "units/registry.toml",
        )
        first = project_unmapped_module(
            self.root,
            CanonicalStandardsCorpus(modules, units),
            "workflow.test",
        )

        self.module("Changed policy text.")
        changed_units = load_policy_unit_corpus(
            self.root,
            modules,
            "units/registry.toml",
        )
        second = project_unmapped_module(
            self.root,
            CanonicalStandardsCorpus(modules, changed_units),
            "workflow.test",
        )
        self.assertEqual(first.digest, second.digest)

        source = self.root / "module.md"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "**Standards metadata**",
                "Unmapped normative text.\n\n**Standards metadata**",
            ),
            encoding="utf-8",
        )
        third = project_unmapped_module(
            self.root,
            CanonicalStandardsCorpus(
                load_canonical_module_corpus(self.root, "corpus.toml"),
                load_policy_unit_corpus(
                    self.root,
                    load_canonical_module_corpus(self.root, "corpus.toml"),
                    "units/registry.toml",
                ),
            ),
            "workflow.test",
        )
        self.assertNotEqual(second.digest, third.digest)

    def test_tombstone_successors_use_policy_identity_rules(self) -> None:
        self.module("Policy text.")
        self.declarations(
            """
            [[tombstone]]
            id = "workflow.test.retired"
            retired_semantic_revision = 1
            successors = ["STD-0001"]
            evidence = "review.retirement"
            """
        )

        with self.assertRaises(MetadataError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LEGACY_ID")


if __name__ == "__main__":
    unittest.main()
