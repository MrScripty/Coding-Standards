from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    ChangeDescriptor,
    ChangeKind,
    ReviewScope,
    SemanticProposal,
    UNMAPPED_DECISION_CONTRACT,
    classify_changes,
    generate_unmapped_normative_obligations,
)
from tools.standards_engine.contracts.validate_contracts import validate
from tools.standards_metadata.standards_metadata import (
    load_canonical_standards_corpus,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


class UnmappedNormativeObligationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.accepted = self.root / "accepted"
        self.proposed = self.root / "proposed"
        self.write_fixture(self.accepted, intro="Stable intro.", policy="Policy text.")
        self.write_fixture(self.proposed, intro="Stable intro.", policy="Changed policy text.")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, root: Path, path: str, content: str) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_fixture(self, root: Path, *, intro: str, policy: str) -> None:
        self.write(
            root,
            "module.md",
            f"""
            # Module

            **Standards metadata**

            - ID: `workflow.test`
            - Role: `workflow`
            - Level: `MUST`
            - Applies when: The fixture applies.
            - Does not apply when: The fixture does not apply.
            - Requires: `none`
            - Specializes: `none`
            - Verification: Obligation evidence.
            - Canonical owner: `module.md`

            {intro}

            ## Policy

            {policy}
            """,
        )
        self.write(
            root,
            "corpus.toml",
            'schema_version = 1\nmembers = ["module.md"]\n',
        )
        self.write(
            root,
            "units/registry.toml",
            'schema_version = 1\nsources = ["units/module.toml"]\n',
        )
        self.write(
            root,
            "units/module.toml",
            """
            schema_version = 1

            [[policy_unit]]
            id = "workflow.test.policy"
            module = "workflow.test"
            heading_path = ["Policy"]
            semantic_revision = 1
            """,
        )

    def corpora(self):
        return (
            load_canonical_standards_corpus(
                self.accepted,
                module_registry="corpus.toml",
                policy_unit_registry="units/registry.toml",
            ),
            load_canonical_standards_corpus(
                self.proposed,
                module_registry="corpus.toml",
                policy_unit_registry="units/registry.toml",
            ),
        )

    def classified_policy_change(self, accepted, proposed):
        before = accepted.policy_units[0]
        after = proposed.policy_units[0]
        return classify_changes(
            accepted.policy_unit_corpus,
            proposed.policy_unit_corpus,
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (before.id,),
                    (after.id,),
                    ReviewScope("structured", ("Policy",)),
                ),
            ),
            (
                SemanticProposal(
                    before.id,
                    1,
                    2,
                    "Change the mapped policy.",
                    after.structural_digest,
                ),
            ),
        )

    def test_mapped_policy_change_does_not_create_unmapped_obligation(self) -> None:
        accepted, proposed = self.corpora()
        changes = self.classified_policy_change(accepted, proposed)

        self.assertEqual(
            generate_unmapped_normative_obligations(
                self.accepted,
                accepted,
                self.proposed,
                proposed,
                changes,
            ),
            (),
        )

    def test_unmapped_decision_contract_matches_public_schema(self) -> None:
        validate(
            SCHEMA,
            SCHEMA["$defs"]["DecisionContract"],
            UNMAPPED_DECISION_CONTRACT.as_contract(),
            "$decision_contract",
        )

    def test_unmapped_document_change_creates_mandatory_whole_artifact_obligation(self) -> None:
        self.write_fixture(
            self.proposed,
            intro="Changed unmapped normative text.",
            policy="Changed policy text.",
        )
        accepted, proposed = self.corpora()
        obligations = generate_unmapped_normative_obligations(
            self.accepted,
            accepted,
            self.proposed,
            proposed,
            self.classified_policy_change(accepted, proposed),
        )

        self.assertEqual(len(obligations), 1)
        value = obligations[0].as_contract()
        validate(SCHEMA, SCHEMA["$defs"]["Obligation"], value, "$obligation")
        self.assertEqual(value["kind"], "unmapped-normative-change")
        self.assertEqual(value["target"], "workflow.test")
        self.assertEqual(value["scope"], {"kind": "whole-artifact"})
        self.assertEqual(value["state"], "required")
        self.assertEqual(value["permitted_submissions"], ["impact-disposition"])

    def test_omitted_changed_policy_descriptor_cannot_silently_pass(self) -> None:
        accepted, proposed = self.corpora()

        obligations = generate_unmapped_normative_obligations(
            self.accepted,
            accepted,
            self.proposed,
            proposed,
            (),
        )

        self.assertEqual(
            [obligation.target for obligation in obligations],
            ["workflow.test"],
        )

    def test_reference_only_change_does_not_create_normative_obligation(self) -> None:
        for root, text in (
            (self.accepted, "Accepted reference text."),
            (self.proposed, "Proposed reference text."),
        ):
            source = root / "module.md"
            source.write_text(
                source.read_text(encoding="utf-8")
                .replace("- Role: `workflow`", "- Role: `reference`")
                .replace("- Level: `MUST`", "- Level: `REFERENCE`")
                .replace("Stable intro.", text),
                encoding="utf-8",
            )
        accepted, proposed = self.corpora()

        self.assertEqual(
            generate_unmapped_normative_obligations(
                self.accepted,
                accepted,
                self.proposed,
                proposed,
                (),
            ),
            (),
        )

    def test_added_normative_module_requires_whole_artifact_review(self) -> None:
        self.write(
            self.proposed,
            "added.md",
            """
            # Added

            **Standards metadata**

            - ID: `topic.added`
            - Role: `topic`
            - Level: `MUST`
            - Applies when: The added topic applies.
            - Does not apply when: The added topic does not apply.
            - Requires: `none`
            - Specializes: `none`
            - Verification: Whole-artifact review.
            - Canonical owner: `added.md`

            Added normative content.
            """,
        )
        self.write(
            self.proposed,
            "corpus.toml",
            'schema_version = 1\nmembers = ["module.md", "added.md"]\n',
        )
        accepted, proposed = self.corpora()

        obligations = generate_unmapped_normative_obligations(
            self.accepted,
            accepted,
            self.proposed,
            proposed,
            (),
        )

        self.assertEqual(
            [obligation.target for obligation in obligations],
            ["topic.added", "workflow.test"],
        )


if __name__ == "__main__":
    unittest.main()
