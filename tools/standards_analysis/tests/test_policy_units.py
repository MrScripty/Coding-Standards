from __future__ import annotations

import tempfile
import textwrap
import unittest
import json
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    load_policy_unit_corpus,
)
from tools.standards_metadata.standards_metadata import load_canonical_module_corpus
from tools.standards_engine.contracts.validate_contracts import validate


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


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
        validate(
            SCHEMA,
            SCHEMA["$defs"]["PolicyUnitDeclaration"],
            unit.as_declaration(),
            "$policy_unit",
        )

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

        with self.assertRaises(AnalysisError) as caught:
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
        validate(
            SCHEMA,
            SCHEMA["$defs"]["PolicyUnitTombstone"],
            corpus.tombstones[0].as_declaration(),
            "$tombstone",
        )

        path = self.root / "units/module.toml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'successors = ["workflow.test.successor"]', "successors = []"
            ),
            encoding="utf-8",
        )
        with self.assertRaises(AnalysisError) as caught:
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
        with self.assertRaises(AnalysisError) as caught:
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

        with self.assertRaises(AnalysisError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LOCATOR_CONFLICT")

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

        with self.assertRaises(AnalysisError) as caught:
            self.load()
        self.assertEqual(caught.exception.failure.code, "POLICY_UNIT.LEGACY_ID")


if __name__ == "__main__":
    unittest.main()
