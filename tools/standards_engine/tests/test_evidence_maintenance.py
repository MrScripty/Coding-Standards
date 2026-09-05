from __future__ import annotations

import json
import unittest

from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_engine.standards_engine.evidence_maintenance import (
    ATTESTATIONS,
    CATALOG,
    IMPACT,
    REGISTRY,
    _dump,
    revise_evidence,
)


def plan():
    return dict(
        prune_stale_certificates=False,
        retire_suites=[],
        retire_checks=[],
        retire_inputs=[],
        suite_descriptions=[],
        replacement_evidence_owner="suite:graph",
        replacement_evidence_rationale="Checks declared graph integrity only.",
        relationship_updates=[],
        consumer_registrations=[],
    )


def fixture():
    return {
        REGISTRY: _dump(
            {
                "schema_version": 1,
                "suites": [
                    {"id": "old", "path": "suites/old.toml", "requires": ["graph"]},
                    {"id": "graph", "path": "suites/graph.toml", "requires": []},
                    {"id": "caller", "path": "suites/caller.toml", "requires": ["old"]},
                ],
            }
        ),
        "suites/old.toml": _dump({"checks": [{"id": "simulated", "type": "decision"}]}),
        "suites/graph.toml": _dump(
            {"checks": [{"id": "graph", "type": "policy_impact"}]}
        ),
        "suites/caller.toml": _dump(
            {"checks": [{"id": "links", "type": "markdown_links"}]}
        ),
        CATALOG: _dump(
            {
                "schema_version": 2,
                "nodes": [
                    {"id": "old", "metadata": {"repository_path": "suites/old.toml"}}
                ],
            }
        ),
        IMPACT: _dump({"declaration_sources": ["impact.toml"]}),
        "impact.toml": _dump(
            {
                "owner": "topic.owner",
                "relationships": [
                    {
                        "source": "topic.owner.policy",
                        "consumer": "old",
                        "relation": "enforcement-suite-projection",
                        "evidence_owner": "suite:old",
                        "rationale": "Old claim",
                    },
                    {
                        "source": "topic.owner.policy",
                        "consumer": "topic.other",
                        "relation": "normative-consumer",
                        "evidence_owner": "suite:old",
                        "rationale": "Old evidence",
                    },
                ],
            }
        ),
        ATTESTATIONS: _dump(
            {
                "schema_version": 3,
                "sources": ["claims.toml"],
                "engine_sources": ["receipt.json"],
            }
        ),
        "claims.toml": _dump(
            {
                "schema_version": 5,
                "attestations": [
                    {"requirement_id": "current"},
                    {"requirement_id": "stale"},
                ],
            }
        ),
        "receipt.json": json.dumps({"claim": {"requirement_id": "stale"}}).encode(),
    }


class EvidenceMaintenanceTest(unittest.TestCase):
    def test_retirement_preserves_real_dependencies_and_normative_consumers(self):
        import tomllib

        original = fixture()
        request = plan()
        request["retire_checks"] = [{"suite": "old", "check": "simulated"}]
        result = revise_evidence(original, request, set())
        self.assertNotIn("suites/old.toml", result)
        registry = tomllib.loads(result[REGISTRY].decode())
        self.assertEqual(
            next(s for s in registry["suites"] if s["id"] == "caller")["requires"],
            ["graph"],
        )
        relationships = tomllib.loads(result["impact.toml"].decode())["relationships"]
        self.assertEqual(
            [(r["consumer"], r["evidence_owner"]) for r in relationships],
            [("topic.other", "suite:graph")],
        )
        self.assertIn("suites/old.toml", original)

    def test_pruning_preserves_current_claims_and_removes_stale_receipts(self):
        import tomllib

        request = plan()
        request["prune_stale_certificates"] = True
        result = revise_evidence(fixture(), request, {"current"})
        self.assertNotIn("receipt.json", result)
        self.assertEqual(
            tomllib.loads(result["claims.toml"].decode())["attestations"],
            [{"requirement_id": "current"}],
        )
        self.assertEqual(
            tomllib.loads(result[ATTESTATIONS].decode())["engine_sources"], []
        )

    def test_unknown_retirement_does_not_mutate_authority(self):
        original = fixture()
        before = dict(original)
        request = plan()
        request["retire_checks"] = [{"suite": "old", "check": "missing"}]
        with self.assertRaises(AuthoringError) as raised:
            revise_evidence(original, request, set())
        self.assertEqual(raised.exception.failure.code, "EVIDENCE.UNKNOWN_CHECK")
        self.assertEqual(original, before)

    def test_consumer_registration_enters_existing_policy_owner(self):
        import tomllib

        original = fixture()
        original["tools/receipt.py"] = b"content"
        request = plan()
        request["consumer_registrations"] = [
            {
                "path": "tools/receipt.py",
                "artifact_kind": "implementation-artifact",
                "source_policies": ["topic.owner.policy"],
                "relation": "implementation-projection",
                "evidence_owner": "suite:graph",
                "rationale": "Owns receipt validation.",
            }
        ]
        result = revise_evidence(original, request, set())
        self.assertEqual(
            tomllib.loads(result["impact.toml"].decode())["relationships"][-1][
                "consumer"
            ],
            "tools/receipt.py",
        )
        self.assertEqual(
            tomllib.loads(result[CATALOG].decode())["nodes"][-1]["metadata"][
                "repository_path"
            ],
            "tools/receipt.py",
        )


class EvidenceMaintenanceInterfaceTest(unittest.TestCase):
    def test_preview_failure_and_overlap_preserve_working_tree_then_apply_prunes(self):
        import hashlib
        import tempfile
        from pathlib import Path
        from unittest import mock
        from tools.repository_git.repository_git import git_output
        from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
        from tools.standards_engine.standards_engine import (
            AgentToolFacade,
            StandardsEngine,
        )
        from tools.standards_engine.standards_engine.tools import (
            LocalAlwaysAllowAuthorizer,
            _contracts,
        )
        from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree

        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            repository = Path(temporary) / "repository"
            _clone_tracked_worktree(repository)
            with StandardsEngine.open_repository(
                repository,
                store_path=Path(temporary) / "engine.sqlite3",
                execution_context=AnalysisExecutionContext(
                    LocalAlwaysAllowAuthorizer(repository)
                ),
            ) as engine:
                facade = AgentToolFacade(engine, _contracts(repository))
                refreshed = facade.verify_repository(
                    {"kind": "verify-repository", "refresh_verification_inputs": True}
                )
                self.assertTrue(refreshed["verification"]["passed"], refreshed)
                git_output(
                    repository,
                    (
                        "add",
                        "--",
                        "evaluation/standards-effectiveness/generated/suite-inputs.json",
                    ),
                )
                git_output(
                    repository,
                    (
                        "-c",
                        "user.name=Evidence Fixture",
                        "-c",
                        "user.email=fixture@example.invalid",
                        "-c",
                        "commit.gpgsign=false",
                        "commit",
                        "--allow-empty",
                        "--quiet",
                        "-m",
                        "test: refresh fixture inputs",
                    ),
                )
                revision = (
                    git_output(repository, ("rev-parse", "HEAD")).decode().strip()
                )
                request = {
                    "kind": "maintain-evidence",
                    "expected_revision": revision,
                    "evidence": [
                        {
                            "id": "CORE-STANDARDS.md",
                            "digest": "sha256:"
                            + hashlib.sha256(
                                (repository / "CORE-STANDARDS.md").read_bytes()
                            ).hexdigest(),
                            "provider_contract": "repository-content",
                            "provider_contract_version": "1",
                        }
                    ],
                    "plan": {
                        **plan(),
                        "prune_stale_certificates": True,
                        "replacement_evidence_owner": "suite:policy-semantic-impact",
                    },
                    "apply": False,
                }
                preview = facade.maintain_evidence(request)
                self.assertEqual(preview["kind"], "maintain-evidence-result", preview)
                self.assertTrue(preview["verification"]["passed"], preview)
                self.assertFalse(preview["applied"])
                self.assertTrue(preview["removed_files"])
                victim = repository / preview["removed_files"][0]
                before = victim.read_bytes()
                victim.write_bytes(before + b"\n# independent edit\n")
                # Candidate verification already ran; exercise post-verification overlap admission.
                original_verifier = engine._application_verifier
                report = original_verifier(repository)
                with mock.patch.object(
                    engine, "_application_verifier", return_value=report
                ):
                    overlap = facade.maintain_evidence({**request, "apply": True})
                    self.assertEqual(
                        overlap["code"], "EVIDENCE.WORKTREE_CHANGED", overlap
                    )
                    self.assertTrue(
                        victim.read_bytes().endswith(b"# independent edit\n")
                    )
                    victim.write_bytes(before)
                    applied = facade.maintain_evidence({**request, "apply": True})
                    self.assertTrue(applied["applied"], applied)
                self.assertFalse(victim.exists())
                self.assertEqual(
                    git_output(repository, ("rev-parse", "HEAD")).decode().strip(),
                    revision,
                )
