from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.tools import (
    LocalAlwaysAllowAuthorizer,
    _contracts,
)
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_snapshots.standards_snapshots import SnapshotError, SnapshotFailure
from tools.repository_git.repository_git import git_output


class EngineAuditPublicationTest(unittest.TestCase):
    def test_review_verify_apply_recover_and_read_without_original_database(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            repository = root / "repository"
            _clone_tracked_worktree(repository)
            context = AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(repository))
            with StandardsEngine.open_repository(
                repository,
                store_path=root / "engine.sqlite3",
                execution_context=context,
            ) as engine:
                facade = AgentToolFacade(engine, _contracts(repository))
                initial = facade.verify_repository(
                    {"kind": "verify-repository", "refresh_verification_inputs": True}
                )
                self.assertTrue(initial["verification"]["passed"], initial)
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
                        "user.name=Audit Fixture",
                        "-c",
                        "user.email=audit@example.invalid",
                        "-c",
                        "commit.gpgsign=false",
                        "commit",
                        "--allow-empty",
                        "--quiet",
                        "-m",
                        "test: refresh fixture verification inputs",
                    ),
                )
                evidence_path = repository / "CORE-STANDARDS.md"
                evidence_bytes = evidence_path.read_bytes()
                reference = {
                    "id": "CORE-STANDARDS.md",
                    "digest": "sha256:" + hashlib.sha256(evidence_bytes).hexdigest(),
                    "provider_contract": "repository-content",
                    "provider_contract_version": "1",
                }
                snapshot = facade.create_snapshot({"kind": "create-snapshot"})
                self.assertEqual(snapshot["kind"], "create-snapshot-result", snapshot)
                policy = "workflow.commit.commit-message"
                proposal = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": snapshot["snapshot"]["snapshot"],
                        "change_set": {
                            "purpose": {
                                "summary": "Publish reviewed policy coverage",
                                "rationale": "Exercise the complete Engine audit publication lifecycle in a fixture.",
                                "evidence": [reference],
                            },
                            "edits": [
                                {
                                    "kind": "audit-policy-unit",
                                    "policy": policy,
                                    "rationale": "Explicit fixture coverage review.",
                                }
                            ],
                        },
                    }
                )
                self.assertEqual(proposal["kind"], "create-proposal-result", proposal)
                revision = proposal["revision"]
                unreviewed = facade.verify_proposal(
                    {"kind": "verify-proposal", "revision": revision}
                )
                self.assertEqual(unreviewed["code"], "VERIFICATION.REVIEW_REQUIRED")
                result = facade.analyze_proposal({"revision": revision})
                for _ in range(10):
                    if result["kind"] == "complete-result":
                        break
                    self.assertEqual(result["kind"], "pending-result", result)
                    operations = [
                        item
                        for item in result["next_operations"]
                        if item["operation"] == "resolve"
                    ]
                    self.assertTrue(operations, result)
                    operation = next(
                        (
                            item
                            for item in operations
                            if item["request_kind"] == "consumer-disposition"
                        ),
                        operations[0],
                    )
                    if operation["request_kind"] == "coverage-attestation":
                        submission = {
                            "kind": "coverage-attestation",
                            "claim": {
                                "requirement": operation["work"],
                                "conclusion": "complete",
                                "evidence": [reference],
                                "explicit_exclusions": [],
                                "rationale": "The fixture explicitly accepts the selected coverage horizon.",
                                "auditor_provenance": "Fixture review context; actual authority is retained independently.",
                            },
                        }
                    else:
                        self.assertEqual(
                            operation["request_kind"], "consumer-disposition", operation
                        )
                        obligation = next(
                            item
                            for item in result["obligations"]
                            if item["handle"] == operation["work"]
                        )
                        submission = {
                            "kind": "consumer-disposition",
                            "obligation": operation["work"],
                            "result": "reviewed-no-change",
                            "rationale": "Explicit fixture consumer decision.",
                            "evidence": [reference],
                            "fingerprint": obligation["fingerprint"],
                        }
                    result = facade.resolve(
                        {"analysis": result["handle"], "submission": submission}
                    )
                self.assertEqual(result["kind"], "complete-result", result)
                reviewed = facade.review_proposal(
                    {
                        "kind": "review-proposal",
                        "analysis": result["handle"],
                        "decisions": [
                            {
                                "owner": owner,
                                "decision": "accept",
                                "rationale": "Explicit fixture review decision.",
                                "evidence": [reference],
                            }
                            for owner in ("consumer", "impact", "audit")
                        ],
                    }
                )
                self.assertEqual(reviewed["kind"], "review-proposal-result", reviewed)
                verified = facade.verify_proposal(
                    {
                        "kind": "verify-proposal",
                        "revision": revision,
                        "readiness": reviewed["readiness"],
                    }
                )
                self.assertEqual(verified["kind"], "verify-proposal-result", verified)
                self.assertTrue(verified["verification"]["passed"], verified)
                before = engine._repository.branch_revision("main")
                apply = {"kind": "apply-proposal", "readiness": reviewed["readiness"]}
                evidence_path.write_bytes(evidence_bytes + b"\nChanged after review.\n")
                rejected = facade.apply_proposal(apply)
                self.assertEqual(
                    rejected.get("code"), "ANALYSIS.EVIDENCE_DIGEST_MISMATCH", rejected
                )
                self.assertEqual(engine._repository.branch_revision("main"), before)
                evidence_path.write_bytes(evidence_bytes)
                with mock.patch.object(
                    engine._authoring,
                    "record_applied",
                    side_effect=SnapshotError(
                        SnapshotFailure(
                            "unavailable",
                            "TEST.INTERRUPTED",
                            "Fixture interruption after publication.",
                        )
                    ),
                ):
                    applied = facade.apply_proposal(apply)
                self.assertEqual(
                    applied["kind"], "application-recovery-required-result", applied
                )
                recovered = facade.recover_application(
                    {"kind": "recover-application", "readiness": reviewed["readiness"]}
                )
                self.assertEqual(
                    recovered["kind"], "recover-application-result", recovered
                )
            # A new store proves the repository carries the receipt and authority.
            with StandardsEngine.open_repository(
                repository,
                store_path=root / "independent.sqlite3",
                execution_context=context,
            ) as cold:
                facade = AgentToolFacade(cold, _contracts(repository))
                captured = facade.create_snapshot({"kind": "create-snapshot"})
                self.assertEqual(captured["kind"], "create-snapshot-result", captured)
                read = facade.query(
                    {
                        "snapshot": captured["snapshot"]["snapshot"],
                        "request": {
                            "kind": "read",
                            "target": policy,
                            "include_coverage": True,
                        },
                    }
                )
                self.assertEqual(read["kind"], "read-result", read)
                self.assertEqual(
                    [
                        (item["subject"], item["status"])
                        for item in read["coverage"]["subjects"]
                    ],
                    [(policy, "current-attestation")],
                )


if __name__ == "__main__":
    unittest.main()
