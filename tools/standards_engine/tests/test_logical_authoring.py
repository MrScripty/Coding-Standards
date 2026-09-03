from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.repository_git.repository_git import indexed_paths
from tools.standards_engine.standards_engine.logical_authoring import (
    LogicalAuthoringCompiler,
    LogicalProgram,
    StandardsChangeSet,
    authoring_target_id,
)
from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_engine.standards_engine.engine import StandardsEngine
from tools.standards_metadata.standards_metadata import (
    DirectoryContentSource,
    RecordingContentSource,
    PolicyUnitTombstone,
    file_digest,
)
from tools.standards_verifier.standards_verifier.suite_inputs import (
    suite_input_projection_bytes,
)


_EVIDENCE = {
    "id": "evidence:logical-authoring-test",
    "digest": "sha256:" + "1" * 64,
    "provider_contract": "standards-evidence",
    "provider_contract_version": "1",
}


class _CurrentFilesWithFreshSuiteDigests:
    """Keep this focused test independent of its own generated digest entry."""

    _manifest = "evaluation/standards-effectiveness/generated/suite-inputs.json"

    def __init__(self, root: Path) -> None:
        self._source = DirectoryContentSource(root)
        raw = json.loads(self._source.read_bytes(self._manifest))
        for item in raw["files"]:
            if item["state"] == "present":
                item["digest"] = file_digest(self._source.read_bytes(item["path"]))
        for item in raw["suites"]:
            item["digest"] = file_digest(self._source.read_bytes(item["path"]))
        registry = raw["registry"]
        registry["digest"] = file_digest(self._source.read_bytes(registry["path"]))
        self._manifest_bytes = (
            json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")

    def read_bytes(self, path: str) -> bytes:
        if path == self._manifest:
            return self._manifest_bytes
        return self._source.read_bytes(path)


class LogicalAuthoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[3]
        recording = RecordingContentSource(_CurrentFilesWithFreshSuiteDigests(cls.root))
        StandardsEngine._compile(recording)
        cls.base = recording.freeze()
        cls.compiled = StandardsEngine._compile(cls.base)
        cls.repository_paths = indexed_paths(cls.root)

    def change_set(self, edits: list[dict[str, object]]) -> StandardsChangeSet:
        return StandardsChangeSet.from_mapping(
            {
                "purpose": {
                    "summary": "exercise logical authoring",
                    "rationale": "The focused integration test verifies the admitted operation.",
                    "evidence": [_EVIDENCE],
                },
                "edits": edits,
            }
        )

    def assert_suite_input_projection_is_canonical(self, projection: object) -> None:
        projected_files = dict(projection.source.files)  # type: ignore[attr-defined]
        base_files = set(dict(self.base.files))
        current_files = set(projected_files)
        repository_paths = tuple(
            sorted(
                (set(self.repository_paths) - (base_files - current_files))
                | (current_files - base_files)
            )
        )
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            for path in repository_paths:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
            for path, content in projected_files.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            subprocess.run(
                ("git", "add", "--force", "--all", "--"),
                cwd=root,
                check=True,
            )
            expected = suite_input_projection_bytes(
                root,
                repository_paths=repository_paths,
            )
        self.assertEqual(
            projected_files[
                "evaluation/standards-effectiveness/generated/suite-inputs.json"
            ],
            expected,
        )

    @staticmethod
    def new_standard_edit() -> dict[str, object]:
        return {
            "kind": "create-standard",
            "standard": {
                "id": "topic.logical-authoring-test",
                "title": "Logical Authoring Test",
                "role": "topic",
                "level": "MUST",
                "applies_when": "Logical authoring behavior is tested.",
                "does_not_apply_when": "No logical authoring behavior is tested.",
                "verification": "Standards Engine logical-authoring integration tests.",
                "body": "## Test Policy\n\nUse the Standards Engine Interface.\n",
            },
            "requires": ["core"],
            "specializes": [],
            "policy_units": [
                {
                    "id": "topic.logical-authoring-test.policy",
                    "heading_chain": ["Test Policy"],
                    "semantic_revision": 1,
                    "intent": "Create one registered logical-authoring policy.",
                    "aliases": [],
                    "predecessors": [],
                    "successors": [],
                }
            ],
        }

    @staticmethod
    def new_relationship() -> dict[str, object]:
        return {
            "source_policy": "topic.logical-authoring-test.policy",
            "consumer": "workflow.planning",
            "relation": "normative-consumer",
            "applicability": {"operator": "always"},
            "source_scope": None,
            "consumer_scope": None,
            "evidence_owner": "suite:core-simplicity",
            "rationale": "Planning consumes the logical-authoring policy.",
        }

    @staticmethod
    def target_handle(snapshot: str, consumer: str) -> dict[str, object]:
        return {
            "kind": "authoring-target-handle",
            "snapshot": {
                "kind": "snapshot-handle",
                "id": snapshot,
                "schema_version": 5,
            },
            "id": authoring_target_id(snapshot, consumer),
            "schema_version": 5,
        }

    def test_change_set_is_immutable_and_normalized_before_program_append(self) -> None:
        edits = [
            {
                "kind": "replace-standard-relationships",
                "standard": "topic.architecture",
                "requires": ["topic.contracts", "core"],
                "specializes": [],
                "rationale": "Verification becomes an explicit dependency.",
            },
            {
                "kind": "revise-policy-unit",
                "policy": "topic.architecture.composed-design-admission",
                "title": "Composed Design Admission",
                "body": "Prefer a deep Module with one stable Interface.\n",
                "semantics": {
                    "kind": "change",
                    "accepted_semantic_revision": 1,
                    "proposed_semantic_revision": 2,
                    "intent": "Clarify the accepted depth requirement.",
                },
            },
        ]
        first = StandardsChangeSet.from_mapping(
            {
                "purpose": {
                    "summary": "clarify interface depth",
                    "rationale": "The current wording leaves the caller burden unclear.",
                    "evidence": [_EVIDENCE],
                },
                "edits": edits,
            }
        )
        shuffled = StandardsChangeSet.from_mapping(
            {
                "edits": list(reversed(edits)),
                "purpose": {
                    "evidence": [_EVIDENCE],
                    "rationale": "The current wording leaves the caller burden unclear.",
                    "summary": "clarify interface depth",
                },
            }
        )

        self.assertEqual(first, shuffled)
        self.assertEqual(first.digest, shuffled.digest)
        self.assertEqual(
            [item["kind"] for item in first.as_contract()["edits"]],
            ["revise-policy-unit", "replace-standard-relationships"],
        )
        revision = next(
            item
            for item in first.edits
            if item.as_contract()["kind"] == "revise-policy-unit"
        )
        with self.assertRaises(TypeError):
            revision.semantics["intent"] = "mutated"  # type: ignore[index, union-attr]

        empty = LogicalProgram()
        accumulated = empty.append(first)
        self.assertEqual(empty.change_sets, ())
        self.assertEqual(accumulated.change_sets, (first,))
        self.assertNotEqual(empty.digest, accumulated.digest)

    def test_compiler_projects_module_relationships_through_current_owners(
        self,
    ) -> None:
        change_set = StandardsChangeSet.from_mapping(
            {
                "purpose": {
                    "summary": "route architecture through verification",
                    "rationale": "The standard now relies on verification policy.",
                    "evidence": [_EVIDENCE],
                },
                "edits": [
                    {
                        "kind": "replace-standard-relationships",
                        "standard": "topic.architecture",
                        "requires": [
                            "workflow.verification",
                            "topic.contracts",
                            "core",
                        ],
                        "specializes": [],
                        "rationale": "Verification is a direct prerequisite.",
                    }
                ],
            }
        )

        projection = LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base,
            LogicalProgram().append(change_set),
            base_repository_paths=self.repository_paths,
        )

        module = projection.compiled.corpus.resolve_module("topic.architecture")
        self.assertIsNotNone(module)
        assert module is not None
        self.assertEqual(
            module.requires,
            ("core", "topic.contracts", "workflow.verification"),
        )
        self.assertEqual(projection.analysis_policy_ids, ())
        self.assertEqual(projection.analysis_module_ids, ("topic.architecture",))
        self.assertNotIn("path", change_set.as_contract()["edits"][0])

    def test_compiler_revises_one_registered_policy_and_derives_analysis_input(
        self,
    ) -> None:
        content = (
            "Apply the composed-design admission when a material change alters a "
            "Module Interface or Seam.\n\n"
            "Record Depth, Locality, and the deletion result.\n"
        )
        change_set = StandardsChangeSet.from_mapping(
            {
                "purpose": {
                    "summary": "clarify composed design",
                    "rationale": "The policy needs one direct decision rule.",
                    "evidence": [_EVIDENCE],
                },
                "edits": [
                    {
                        "kind": "revise-policy-unit",
                        "policy": "topic.architecture.composed-design-admission",
                        "title": "Composed Design Admission",
                        "body": content,
                        "semantics": {
                            "kind": "change",
                            "accepted_semantic_revision": 1,
                            "proposed_semantic_revision": 2,
                            "intent": "Clarify when the composed-design admission applies.",
                        },
                    }
                ],
            }
        )

        projection = LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base,
            LogicalProgram().append(change_set),
            base_repository_paths=self.repository_paths,
        )

        unit = projection.compiled.corpus.resolve_policy_unit(
            "topic.architecture.composed-design-admission"
        )
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit.semantic_revision, 1)
        self.assertEqual(
            unit.content,
            "## Composed Design Admission\n\n" + content,
        )
        self.assertEqual(
            projection.semantic_proposals,
            (
                {
                    "policy": "topic.architecture.composed-design-admission",
                    "accepted_semantic_revision": 1,
                    "proposed_semantic_revision": 2,
                    "intent": "Clarify when the composed-design admission applies.",
                    "structural_digest": unit.structural_digest,
                },
            ),
        )

    def test_create_standard_hides_all_required_repository_projections(self) -> None:
        change_set = self.change_set(
            [
                self.new_standard_edit(),
                {
                    "kind": "put-policy-relationship",
                    "relationship": self.new_relationship(),
                },
            ]
        )

        projection = LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base,
            LogicalProgram((change_set,)),
            base_repository_paths=self.repository_paths,
        )

        module = projection.compiled.corpus.resolve_module(
            "topic.logical-authoring-test"
        )
        unit = projection.compiled.corpus.resolve_policy_unit(
            "topic.logical-authoring-test.policy"
        )
        self.assertIsNotNone(module)
        self.assertIsNotNone(unit)
        self.assertEqual(
            sorted(set(dict(projection.source.files)) - set(dict(self.base.files))),
            [
                "evaluation/standards-effectiveness/policy-impact/topic.logical-authoring-test.toml",
                "evaluation/standards-effectiveness/policy-units/topic.logical-authoring-test.toml",
                "topics/logical-authoring-test.md",
            ],
        )
        changed = {
            path
            for path, content in projection.source.files
            if dict(self.base.files).get(path) != content
        }
        self.assertEqual(
            changed,
            {
                "evaluation/standards-effectiveness/canonical-module-corpus.toml",
                "evaluation/standards-effectiveness/generated/suite-inputs.json",
                "evaluation/standards-effectiveness/policy-impact-registry.toml",
                "evaluation/standards-effectiveness/policy-impact/topic.logical-authoring-test.toml",
                "evaluation/standards-effectiveness/policy-units/registry.toml",
                "evaluation/standards-effectiveness/policy-units/topic.logical-authoring-test.toml",
                "topics/logical-authoring-test.md",
            },
        )
        self.assertEqual(
            projection.semantic_proposals[0]["accepted_semantic_revision"], None
        )
        self.assert_suite_input_projection_is_canonical(projection)
        self.assertNotIn("path", json.dumps(change_set.as_contract()))

    def test_move_preserves_identity_and_relocates_relationship_authority(self) -> None:
        change_set = self.change_set(
            [
                {
                    "kind": "move-policy-unit",
                    "policy": "topic.architecture.composed-design-admission",
                    "standard": "topic.contracts",
                    "semantics": {
                        "kind": "preserve",
                        "semantic_revision": 1,
                        "intent": "Move representation without changing policy meaning.",
                    },
                }
            ]
        )

        projection = LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base,
            LogicalProgram((change_set,)),
            base_repository_paths=self.repository_paths,
        )

        unit = projection.compiled.corpus.policy_unit_corpus.active_by_id(
            "topic.architecture.composed-design-admission"
        )
        assert unit is not None
        self.assertEqual(unit.module, "topic.contracts")
        self.assertEqual(unit.semantic_revision, 1)
        self.assertEqual(projection.semantic_proposals, ())
        self.assertEqual(
            {
                item.declaration_source
                for item in projection.compiled.policy_impact.semantics.values()
                if item.source == unit.id
            },
            {"evaluation/standards-effectiveness/policy-impact/topic.contracts.toml"},
        )

    def test_whole_standard_revision_requires_companion_policy_semantics(self) -> None:
        module = self.compiled.corpus.resolve_module("topic.architecture")
        unit = self.compiled.corpus.policy_unit_corpus.active_by_id(
            "topic.architecture.composed-design-admission"
        )
        assert module is not None and unit is not None
        text = dict(self.base.files)[module.path].decode("utf-8")
        owner_line = f"- Canonical owner: `{module.path}`\n\n"
        body = text.split(owner_line, 1)[1]
        revised_body = body.replace(
            "Apply this admission when a material design",
            "Apply this admission whenever a material design",
            1,
        )
        standard = {
            "id": module.module_id,
            "title": text.splitlines()[0].removeprefix("# "),
            "role": module.role,
            "level": module.level,
            "applies_when": module.applies_when,
            "does_not_apply_when": module.excludes,
            "verification": module.verification,
            "body": revised_body,
        }
        compiler = LogicalAuthoringCompiler(StandardsEngine._compile)
        with self.assertRaises(AuthoringError) as raised:
            compiler.compile(
                self.base,
                LogicalProgram(
                    (
                        self.change_set(
                            [{"kind": "revise-standard", "standard": standard}]
                        ),
                    )
                ),
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(raised.exception.failure.code, "AUTHORING.SEMANTICS_REQUIRED")

        policy_body = (
            unit.content.partition("\n")[2]
            .strip()
            .replace(
                "Apply this admission when a material design",
                "Apply this admission whenever a material design",
                1,
            )
        )
        projection = compiler.compile(
            self.base,
            LogicalProgram(
                (
                    self.change_set(
                        [
                            {"kind": "revise-standard", "standard": standard},
                            {
                                "kind": "revise-policy-unit",
                                "policy": unit.id,
                                "title": unit.heading_path[-1],
                                "body": policy_body,
                                "semantics": {
                                    "kind": "change",
                                    "accepted_semantic_revision": 1,
                                    "proposed_semantic_revision": 2,
                                    "intent": "Clarify the composed-design trigger.",
                                },
                            },
                        ]
                    ),
                )
            ),
            base_repository_paths=self.repository_paths,
        )
        proposed = projection.compiled.corpus.policy_unit_corpus.active_by_id(unit.id)
        assert proposed is not None
        self.assertEqual(proposed.semantic_revision, 1)
        self.assertIn("whenever a material design", proposed.content)
        self.assertEqual(
            projection.semantic_proposals,
            (
                {
                    "policy": unit.id,
                    "accepted_semantic_revision": 1,
                    "proposed_semantic_revision": 2,
                    "intent": "Clarify the composed-design trigger.",
                    "structural_digest": proposed.structural_digest,
                },
            ),
        )

    def test_policy_relationship_put_and_remove_replay_cumulatively(self) -> None:
        relationship = {
            "source_policy": "topic.architecture.authority-scope-admission",
            "consumer": "workflow.verification",
            "relation": "normative-consumer",
            "applicability": {"operator": "always"},
            "source_scope": None,
            "consumer_scope": None,
            "evidence_owner": "suite:core-simplicity",
            "rationale": "Verification consumes the authority-scope decision.",
        }
        addition = self.change_set(
            [{"kind": "put-policy-relationship", "relationship": relationship}]
        )
        removal = self.change_set(
            [{"kind": "remove-policy-relationship", "relationship": relationship}]
        )
        compiler = LogicalAuthoringCompiler(StandardsEngine._compile)

        added = compiler.compile(
            self.base,
            LogicalProgram((addition,)),
            base_repository_paths=self.repository_paths,
        )
        removed = compiler.compile(
            self.base,
            LogicalProgram((addition, removal)),
            base_repository_paths=self.repository_paths,
        )

        key = (
            relationship["source_policy"],
            relationship["relation"],
            relationship["consumer"],
        )
        self.assertIn(
            key,
            {
                (item.source, item.relation, item.consumer)
                for item in added.compiled.policy_impact.semantics.values()
            },
        )
        self.assertNotIn(
            key,
            {
                (item.source, item.relation, item.consumer)
                for item in removed.compiled.policy_impact.semantics.values()
            },
        )
        self.assertEqual(
            added.analysis_policy_ids,
            ("topic.architecture.authority-scope-admission",),
        )

    def test_created_standard_can_be_retired_with_complete_explicit_closure(
        self,
    ) -> None:
        relationship = self.new_relationship()
        create = self.change_set(
            [
                self.new_standard_edit(),
                {"kind": "put-policy-relationship", "relationship": relationship},
            ]
        )
        retire = self.change_set(
            [
                {
                    "kind": "retire-policy-unit",
                    "policy": "topic.logical-authoring-test.policy",
                    "retired_semantic_revision": 1,
                    "successors": [],
                    "relationship_dispositions": [
                        {
                            "relationship": {
                                "kind": "policy-relationship",
                                "source_policy": relationship["source_policy"],
                                "consumer": relationship["consumer"],
                                "relation": relationship["relation"],
                            },
                            "disposition": "remove",
                            "rationale": "Retire the policy's explicit relationship.",
                            "evidence": [_EVIDENCE],
                        }
                    ],
                    "evidence": [_EVIDENCE],
                },
                {
                    "kind": "retire-standard",
                    "standard": "topic.logical-authoring-test",
                    "successors": [],
                    "relationship_dispositions": [
                        {
                            "relationship": {
                                "kind": "module-relationship",
                                "source": "topic.logical-authoring-test",
                                "target": "core",
                                "relation": "requires",
                            },
                            "disposition": "remove",
                            "rationale": "Retire the standard's dependency edge.",
                            "evidence": [_EVIDENCE],
                        }
                    ],
                    "evidence": [_EVIDENCE],
                },
            ]
        )

        projection = LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base,
            LogicalProgram((create, retire)),
            base_repository_paths=self.repository_paths,
        )

        self.assertIsNone(
            projection.compiled.corpus.resolve_module("topic.logical-authoring-test")
        )
        self.assertIsInstance(
            projection.compiled.corpus.resolve_policy_unit(
                "topic.logical-authoring-test.policy"
            ),
            PolicyUnitTombstone,
        )
        self.assertNotIn(
            "topics/logical-authoring-test.md", dict(projection.source.files)
        )
        self.assertNotIn(
            "evaluation/standards-effectiveness/policy-impact/topic.logical-authoring-test.toml",
            dict(projection.source.files),
        )
        self.assert_suite_input_projection_is_canonical(projection)

    def test_retired_standard_successor_must_survive_the_final_program(self) -> None:
        first = self.new_standard_edit()
        second = json.loads(json.dumps(first))
        second["standard"]["id"] = "topic.logical-authoring-successor"
        second["standard"]["title"] = "Logical Authoring Successor"
        second["policy_units"][0]["id"] = "topic.logical-authoring-successor.policy"
        create = self.change_set([first, second])

        retire_edits = []
        for standard, policy, successors in (
            (
                "topic.logical-authoring-test",
                "topic.logical-authoring-test.policy",
                ["topic.logical-authoring-successor"],
            ),
            (
                "topic.logical-authoring-successor",
                "topic.logical-authoring-successor.policy",
                [],
            ),
        ):
            retire_edits.extend(
                (
                    {
                        "kind": "retire-policy-unit",
                        "policy": policy,
                        "retired_semantic_revision": 1,
                        "successors": [],
                        "relationship_dispositions": [],
                        "evidence": [_EVIDENCE],
                    },
                    {
                        "kind": "retire-standard",
                        "standard": standard,
                        "successors": successors,
                        "relationship_dispositions": [
                            {
                                "relationship": {
                                    "kind": "module-relationship",
                                    "source": standard,
                                    "target": "core",
                                    "relation": "requires",
                                },
                                "disposition": "remove",
                                "rationale": "Remove the retired dependency.",
                                "evidence": [_EVIDENCE],
                            }
                        ],
                        "evidence": [_EVIDENCE],
                    },
                )
            )

        with self.assertRaises(AuthoringError) as raised:
            LogicalAuthoringCompiler(StandardsEngine._compile).compile(
                self.base,
                LogicalProgram((create, self.change_set(retire_edits))),
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(raised.exception.failure.code, "AUTHORING.INVALID_SUCCESSOR")

    def test_retirement_requires_and_applies_complete_relationship_dispositions(
        self,
    ) -> None:
        snapshot = "snapshot:v1:00000000-0000-4000-8000-000000000000"
        policy = "topic.architecture.composed-design-admission"
        dispositions = []
        for relationship in self.compiled.policy_impact.semantics.values():
            if relationship.source != policy and relationship.consumer != policy:
                continue
            consumer: object = relationship.consumer
            if relationship.consumer in self.compiled.policy_impact.artifacts:
                consumer = self.target_handle(snapshot, relationship.consumer)
            dispositions.append(
                {
                    "relationship": {
                        "kind": "policy-relationship",
                        "source_policy": relationship.source,
                        "consumer": consumer,
                        "relation": relationship.relation,
                    },
                    "disposition": "remove",
                    "rationale": "Retire the relationship with its source policy.",
                    "evidence": [_EVIDENCE],
                }
            )
        edit = {
            "kind": "retire-policy-unit",
            "policy": policy,
            "retired_semantic_revision": 1,
            "successors": [],
            "relationship_dispositions": dispositions,
            "evidence": [_EVIDENCE],
        }
        compiler = LogicalAuthoringCompiler(StandardsEngine._compile)

        projection = compiler.compile(
            self.base,
            LogicalProgram((self.change_set([edit]),)),
            base_snapshot=snapshot,
            base_repository_paths=self.repository_paths,
        )

        retired = projection.compiled.corpus.resolve_policy_unit(policy)
        self.assertIsInstance(retired, PolicyUnitTombstone)
        self.assertFalse(
            any(
                item.source == policy or item.consumer == policy
                for item in projection.compiled.policy_impact.semantics.values()
            )
        )
        incomplete = {**edit, "relationship_dispositions": dispositions[:-1]}
        with self.assertRaises(AuthoringError) as raised:
            compiler.compile(
                self.base,
                LogicalProgram((self.change_set([incomplete]),)),
                base_snapshot=snapshot,
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(
            raised.exception.failure.code, "AUTHORING.MISSING_SEMANTIC_DECISION"
        )

    def test_opaque_consumer_handle_is_snapshot_bound(self) -> None:
        accepted = "snapshot:v1:00000000-0000-4000-8000-000000000000"
        other = "snapshot:v1:00000000-0000-4000-8000-000000000001"
        relationship = {
            "source_policy": "topic.architecture.authority-scope-admission",
            "consumer": self.target_handle(other, "prompts/planning.md"),
            "relation": "prompt-projection",
            "applicability": {"operator": "always"},
            "source_scope": None,
            "consumer_scope": None,
            "evidence_owner": "suite:core-simplicity",
            "rationale": "The prompt projects the authority-scope decision.",
        }

        with self.assertRaises(AuthoringError) as raised:
            LogicalAuthoringCompiler(StandardsEngine._compile).compile(
                self.base,
                LogicalProgram(
                    (
                        self.change_set(
                            [
                                {
                                    "kind": "put-policy-relationship",
                                    "relationship": relationship,
                                }
                            ]
                        ),
                    )
                ),
                base_snapshot=accepted,
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(
            raised.exception.failure.code, "AUTHORING.TARGET_SNAPSHOT_MISMATCH"
        )

    def test_noop_and_cyclic_relationship_changes_are_typed(self) -> None:
        module = self.compiled.corpus.resolve_module("topic.architecture")
        assert module is not None
        no_op = self.change_set(
            [
                {
                    "kind": "replace-standard-relationships",
                    "standard": module.module_id,
                    "requires": list(module.requires),
                    "specializes": list(module.specializes),
                    "rationale": "Bind the current relationship set.",
                }
            ]
        )
        compiler = LogicalAuthoringCompiler(StandardsEngine._compile)
        with self.assertRaises(AuthoringError) as raised:
            compiler.compile(
                self.base,
                LogicalProgram((no_op,)),
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(raised.exception.failure.code, "AUTHORING.NO_EFFECT")

        core = self.compiled.corpus.resolve_module("core")
        assert core is not None
        cycle = self.change_set(
            [
                {
                    "kind": "replace-standard-relationships",
                    "standard": core.module_id,
                    "requires": [*core.requires, module.module_id],
                    "specializes": list(core.specializes),
                    "rationale": "Exercise canonical cycle rejection.",
                }
            ]
        )
        with self.assertRaises(Exception) as cycle_error:
            compiler.compile(
                self.base,
                LogicalProgram((cycle,)),
                base_repository_paths=self.repository_paths,
            )
        self.assertEqual(cycle_error.exception.failure.code, "METADATA.REQUIRES_CYCLE")


if __name__ == "__main__":
    unittest.main()
