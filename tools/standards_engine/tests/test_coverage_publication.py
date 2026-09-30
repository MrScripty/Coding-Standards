from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisExecutionContext,
    AnalysisFailure,
    coverage_requirement_id,
    render_engine_coverage_receipt,
    validate_engine_coverage_receipt_evidence,
)
from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    AnalysisHandle,
    StandardsEngine,
)
from tools.standards_engine.standards_engine.authoring import (
    AuthoringError,
    AuthoringFailure,
)
from tools.standards_engine.standards_engine.tools import (
    LocalAlwaysAllowAuthorizer,
    _contracts,
)
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.repository_git.repository_git import (
    RepositoryPath,
    RepositoryRevision,
    git_output,
)
from tools.standards_snapshots.standards_snapshots import SnapshotId


class EngineAuditPublicationTest(unittest.TestCase):
    def test_review_verify_apply_recover_and_read_without_original_database(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            repository = root / "repository"
            _clone_tracked_worktree(repository)
            context = AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(repository))
            store_path = repository / ".standards-engine" / "snapshots-v1.sqlite3"
            with StandardsEngine.open_repository(
                repository,
                store_path=store_path,
                execution_context=context,
                purpose="authoring",
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
                snapshot = facade.create_snapshot({"kind": "create-snapshot"})
                self.assertEqual(snapshot["kind"], "create-snapshot-result", snapshot)
                snapshot_id = SnapshotId(snapshot["snapshot"]["snapshot"]["id"])
                base_capture = engine._snapshots.load_content(snapshot_id)
                captured_paths = {str(item.path) for item in base_capture.files}
                expected_target = engine._repository.branch_revision("main")
                uncaptured_markdown = sorted(
                    str(path)
                    for path in engine._repository.revision_paths(expected_target)
                    if str(path) not in captured_paths
                    and str(path).endswith(".md")
                    and str(path)[0].isalnum()
                    and all(
                        character.isascii()
                        and (character.isalnum() or character in "._:/-")
                        for character in str(path)
                    )
                    and len(
                        engine._repository.read_file(
                            expected_target, path
                        )
                    ) <= 128 * 1024
                )
                self.assertTrue(uncaptured_markdown)
                evidence_id = uncaptured_markdown[0]
                evidence_path = repository / evidence_id
                evidence_bytes = engine._repository.read_file(
                    expected_target, RepositoryPath.parse(evidence_id)
                )
                reference = {
                    "id": evidence_id,
                    "digest": "sha256:" + hashlib.sha256(evidence_bytes).hexdigest(),
                    "provider_contract": "repository-content",
                    "provider_contract_version": "1",
                }
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
                self.assertEqual(
                    proposal["kind"], "create-proposal-result",
                    {"evidence_id": evidence_id, **proposal},
                )
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
                revision_record = engine._authoring.read_revision(revision["id"])
                projection = engine._proposal_projection(revision_record)
                state = engine._load_analysis(
                    AnalysisHandle.from_value(result["handle"])
                )
                claim = engine._plain(state.coverage_attestations[0])
                subject = next(
                    selected
                    for selected, view in projection.compiled.coverage.views.items()
                    if coverage_requirement_id(
                        projection.compiled.coverage.requirements[selected], view
                    ) == claim["requirement_id"]
                )
                authorization = next(
                    engine._plain(item)
                    for item in state.authorization_records
                    if engine._plain(item)["reference"]["id"] == claim["authorization_id"]
                )
                evidence_id = claim["evidence"][0]["id"]
                destination_base = {
                    str(item.path): item.content
                    for item in engine._snapshots.load_content(
                        revision_record.base_snapshot
                    ).files
                }
                destination_base.update(projection.captured_consumer_files)
                expected_target = RepositoryRevision(
                    engine._snapshots.snapshot(
                        revision_record.base_snapshot
                    ).source_revision
                )
                # Reusing the previous receipt must fail before it can be replaced.
                receipt_path = engine._engine_coverage_receipt_path(subject)
                prior_receipt = render_engine_coverage_receipt(
                    FrozenContentSource({**dict(projection.source.files), evidence_id: evidence_bytes}),
                    projection.compiled.coverage, subject, claim, authorization,
                    state.analysis_id, context,
                    phase="candidate-evidence", source_kind="repository-content",
                    material_identity=revision_record.revision_id,
                )
                publication_files = {**dict(projection.source.files), receipt_path: prior_receipt}
                publication_paths = {*projection.repository_paths, receipt_path}
                publication_projection = mock.Mock(
                    source=FrozenContentSource(publication_files),
                    repository_paths=publication_paths,
                    captured_consumer_files=projection.captured_consumer_files,
                    compiled=projection.compiled,
                )
                complete_evaluation = engine._evaluate(state)
                for overwritten_path in (
                    receipt_path,
                    "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml",
                    "evaluation/standards-effectiveness/generated/suite-inputs.json",
                ):
                    for reference_field in ("evidence", "explicit_exclusions"):
                        with self.subTest(path=overwritten_path, field=reference_field):
                            overwrite_reference = {
                                **reference,
                                "id": overwritten_path,
                                "digest": "sha256:" + hashlib.sha256(
                                    publication_files[overwritten_path]
                                ).hexdigest(),
                            }
                            overwritten_claim = {
                                **claim, reference_field: [overwrite_reference],
                            }
                            overwritten_state = state.with_decisions(
                                coverage_attestations=[overwritten_claim],
                            )
                            with (
                                mock.patch.object(engine, "_load_analysis", return_value=overwritten_state),
                                mock.patch.object(engine, "_evaluate", return_value=complete_evaluation),
                                mock.patch.object(engine, "_proposal_projection", return_value=publication_projection),
                                mock.patch.object(engine._authoring, "review_proposal") as record_readiness,
                                mock.patch("tools.standards_engine.standards_engine.engine.construct_authorization_record") as issue_authorization,
                                mock.patch("tools.standards_analysis.standards_analysis.validate_engine_coverage_receipt_evidence") as validate_evidence,
                            ):
                                rejected_overwrite = facade.review_proposal({
                                    "kind": "review-proposal", "analysis": result["handle"],
                                    "decisions": [{
                                        "owner": owner, "decision": "accept",
                                        "rationale": "Explicit fixture review decision.",
                                        "evidence": [reference],
                                    } for owner in ("consumer", "impact", "audit")],
                                })
                                self.assertEqual(
                                    rejected_overwrite["code"],
                                    "COVERAGE.PUBLICATION_EVIDENCE_OVERWRITTEN",
                                    rejected_overwrite,
                                )
                                self.assertEqual(rejected_overwrite["details"]["validation_phase"], "readiness-preflight")
                                self.assertEqual(rejected_overwrite["details"]["evidence_reference"], overwritten_path)
                                record_readiness.assert_not_called()
                                issue_authorization.assert_not_called()
                                validate_evidence.assert_not_called()
                                with self.assertRaises(AnalysisError) as candidate_failure:
                                    engine._prepare_coverage_publication(
                                        overwritten_state.analysis_id, revision_record,
                                        publication_projection, expected_target, destination_base,
                                        publication_files, publication_paths,
                                        phase="candidate-evidence", state=overwritten_state,
                                    )
                                self.assertEqual(candidate_failure.exception.failure.code, "COVERAGE.PUBLICATION_EVIDENCE_OVERWRITTEN")
                                self.assertEqual(candidate_failure.exception.failure.validation_phase, "candidate-evidence")
                self.assertEqual(publication_files[receipt_path], prior_receipt)
                self.assertNotIn(evidence_id, dict(projection.source.files))
                removed_files = dict(projection.source.files)
                removed_paths = set(projection.repository_paths)
                self.assertIn(evidence_id, revision_record.base_repository_paths)
                self.assertNotIn(evidence_id, destination_base)
                removed_files.pop(evidence_id, None)
                removed_paths.remove(evidence_id)
                with self.assertRaises(AnalysisError) as removed_preflight:
                    engine._prepare_coverage_publication(
                        state.analysis_id,
                        revision_record,
                        projection,
                        expected_target,
                        destination_base,
                        removed_files,
                        removed_paths,
                        phase="readiness-preflight",
                        state=state,
                    )
                self.assertEqual(
                    removed_preflight.exception.failure.code,
                    "COVERAGE.PUBLICATION_EVIDENCE_REMOVED",
                )
                self.assertEqual(
                    removed_preflight.exception.failure.next_action,
                    "restore-reference-to-candidate",
                )
                changed_destination = dict(projection.source.files)
                changed_destination[evidence_id] = b"changed destination evidence\n"
                with mock.patch(
                    "tools.standards_analysis.standards_analysis.coverage_publication.resolve_authorization"
                ) as resolve_authorization:
                    with self.assertRaises(AnalysisError) as failed_preflight:
                        validate_engine_coverage_receipt_evidence(
                            FrozenContentSource(changed_destination),
                            projection.compiled.coverage,
                            subject,
                            claim,
                            authorization,
                            state.analysis_id,
                        phase="readiness-preflight",
                        source_kind="repository-content",
                            material_identity=revision_record.revision_id,
                            next_action="refresh-review-evidence",
                        )
                resolve_authorization.assert_not_called()
                failure = failed_preflight.exception.failure
                self.assertEqual(failure.code, "ANALYSIS.EVIDENCE_DIGEST_MISMATCH")
                self.assertEqual(failure.validation_phase, "readiness-preflight")
                self.assertEqual(failure.evidence_reference, evidence_id)
                self.assertEqual(failure.expected_digest, claim["evidence"][0]["digest"])
                self.assertTrue(failure.observed_digest.startswith("sha256:"))
                projected_failure = engine._domain_rejection(
                    failed_preflight.exception
                ).as_contract()
                self.assertEqual(
                    projected_failure["details"]["validation_phase"],
                    "readiness-preflight",
                )
                self.assertEqual(
                    projected_failure["details"]["evidence_reference"],
                    evidence_id,
                )
                self.assertEqual(
                    projected_failure["details"]["expected_digest"],
                    claim["evidence"][0]["digest"],
                )
                self.assertTrue(
                    projected_failure["details"]["observed_digest"].startswith(
                        "sha256:"
                    )
                )
                self.assertEqual(
                    projected_failure["details"]["source_kind"],
                    "repository-content",
                )
                self.assertEqual(
                    projected_failure["details"]["material_identity"],
                    revision_record.revision_id,
                )
                self.assertEqual(
                    projected_failure["details"]["next_action"],
                    "refresh-review-evidence",
                )
                with (
                    mock.patch.object(
                        engine, "_preflight_proposal_coverage",
                        side_effect=failed_preflight.exception,
                    ),
                    mock.patch.object(engine._authoring, "review_proposal") as record_readiness,
                    mock.patch(
                        "tools.standards_engine.standards_engine.engine.construct_authorization_record"
                    ) as issue_review_authorization,
                ):
                    rejected_review = facade.review_proposal(
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
                self.assertEqual(
                    rejected_review["code"], "ANALYSIS.EVIDENCE_DIGEST_MISMATCH",
                    rejected_review,
                )
                record_readiness.assert_not_called()
                issue_review_authorization.assert_not_called()
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
                    engine._repository,
                    "observe_publication_checkout",
                    side_effect=RuntimeError("fixture observation interruption"),
                ):
                    applied = facade.apply_proposal(apply)
                self.assertEqual(
                    applied["kind"], "apply-proposal-result", applied
                )
                self.assertEqual(applied["publication"]["durable_state"], "applied")
                self.assertEqual(
                    applied["publication"]["target_observation"]["status"],
                    "candidate",
                )
                self.assertEqual(applied["checkout"]["status"], "unavailable")
                self.assertIsNone(applied["checkout"]["publication_path_count"])
                recovered = facade.recover_application(
                    {"kind": "recover-application", "readiness": reviewed["readiness"]}
                )
                self.assertEqual(
                    recovered["kind"], "recover-application-result", recovered
                )
                self.assertEqual(recovered["publication"]["durable_state"], "applied")
                self.assertEqual(
                    recovered["checkout"]["status"], "needs-reconciliation"
                )
            # A new database proves the repository carries the published receipt.
            with StandardsEngine.open_repository(
                repository,
                store_path=root / "independent.sqlite3",
                execution_context=context,
                purpose="authoring",
            ) as independent:
                facade = AgentToolFacade(independent, _contracts(repository))
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
            # Reopening the original database proves applied status survives restart.
            with StandardsEngine.open_repository(
                repository,
                store_path=store_path,
                execution_context=context,
                purpose="authoring",
            ) as cold:
                facade = AgentToolFacade(cold, _contracts(repository))
                status = facade.workflow_status(
                    {"context": reviewed["readiness"]}
                )
                self.assertEqual(status["kind"], "workflow-result", status)
                self.assertEqual(status["status"], "applied", status)
                self.assertNotIn("outcome", status)
                self.assertEqual(status["publication"]["durable_state"], "applied")
                self.assertEqual(status["checkout"]["status"], "needs-reconciliation")
                unavailable_outcome = AuthoringError(AuthoringFailure(
                    "TEST.OUTCOME_UNAVAILABLE",
                    "unavailable",
                    "The fixture cannot read the durable application outcome.",
                ))
                with mock.patch.object(
                    cold._authoring,
                    "application_outcome",
                    side_effect=unavailable_outcome,
                ):
                    unknown_status = facade.workflow_status(
                        {"context": reviewed["readiness"]}
                    )
                    self.assertEqual(
                        unknown_status["status"], "recovery-required", unknown_status
                    )
                    self.assertEqual(
                        unknown_status["publication"]["durable_state"],
                        "unknown",
                        unknown_status,
                    )
                    self.assertEqual(
                        unknown_status["checkout"]["status"],
                        "needs-reconciliation",
                        unknown_status,
                    )
                    recovered_unknown = facade.recover_application(
                        {
                            "kind": "recover-application",
                            "readiness": reviewed["readiness"],
                        }
                    )
                    self.assertEqual(
                        recovered_unknown["kind"],
                        "application-recovery-required-result",
                        recovered_unknown,
                    )
                    self.assertEqual(
                        recovered_unknown["code"],
                        "APPLICATION.OUTCOME_OBSERVATION_UNAVAILABLE",
                        recovered_unknown,
                    )
                    self.assertEqual(
                        recovered_unknown["publication"]["durable_state"],
                        "unknown",
                        recovered_unknown,
                    )
                    self.assertEqual(
                        recovered_unknown["checkout"]["status"],
                        "needs-reconciliation",
                        recovered_unknown,
                    )
            project_root = Path(__file__).resolve().parents[3]
            messages = (
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-11-25",
                        "capabilities": {},
                        "clientInfo": {"name": "publication-restart", "version": "1"},
                    },
                },
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "workflow_status",
                        "arguments": {"context": reviewed["readiness"]},
                    },
                },
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-P",
                    "-m",
                    "tools.standards_engine.standards_engine.mcp",
                    "--repo-root",
                    str(repository),
                    "--purpose",
                    "authoring",
                ],
                input="".join(json.dumps(message) + "\n" for message in messages),
                text=True,
                capture_output=True,
                check=True,
                timeout=60,
                cwd=root,
                env={**os.environ, "PYTHONPATH": str(project_root)},
            )
            responses = [
                json.loads(line) for line in completed.stdout.splitlines()
            ]
            status_response = next(row for row in responses if row.get("id") == 2)
            self.assertNotIn("error", status_response, status_response)
            restarted_status = status_response["result"]["structuredContent"]
            self.assertEqual(restarted_status["kind"], "workflow-result")
            self.assertEqual(restarted_status["status"], "applied")
            self.assertEqual(
                restarted_status["publication"]["durable_state"], "applied"
            )
            self.assertEqual(
                restarted_status["checkout"]["status"], "needs-reconciliation"
            )
            with StandardsEngine.open_repository(
                repository, durable=False, purpose="authoring"
            ) as authoring_engine:
                legacy_failure = AnalysisError(AnalysisFailure(
                    "ANALYSIS.EVIDENCE_UNAVAILABLE",
                    "invalid",
                    "The evidence source is unavailable.",
                    path="evaluation/standards-effectiveness/attestation-sources.toml",
                    field="engine_sources",
                    observed="legacy-source",
                ))
                legacy_details = authoring_engine._domain_rejection(
                    legacy_failure
                ).details
                self.assertEqual(
                    legacy_details,
                    {
                        "path": "evaluation/standards-effectiveness/attestation-sources.toml",
                        "field": "engine_sources",
                        "observed": "legacy-source",
                    },
                )
                unsafe_failure = AnalysisError(AnalysisFailure(
                    "ANALYSIS.EVIDENCE_UNAVAILABLE",
                    "invalid",
                    "The evidence source is unavailable.",
                    path="/private/credentials.txt",
                    field="engine_sources",
                    observed="line one\nline two",
                ))
                self.assertEqual(
                    authoring_engine._domain_rejection(unsafe_failure).details,
                    {"field": "engine_sources"},
                )
                traversal_failure = AnalysisError(AnalysisFailure(
                    "ANALYSIS.EVIDENCE_UNAVAILABLE",
                    "invalid",
                    "The evidence source is unavailable.",
                    path="private\\..\\credentials.txt",
                    field="engine_sources",
                    observed="safe-observation",
                ))
                self.assertEqual(
                    authoring_engine._domain_rejection(traversal_failure).details,
                    {"field": "engine_sources", "observed": "safe-observation"},
                )
            with StandardsEngine.open_repository(
                repository, durable=False, purpose="application"
            ) as application_engine:
                private_failure = AnalysisError(AnalysisFailure(
                    "ANALYSIS.EVIDENCE_DIGEST_MISMATCH",
                    "invalid",
                    "Resolved evidence bytes do not match the declared digest.",
                    validation_phase="readiness-preflight",
                    evidence_reference="private/internal/evidence.md",
                    expected_digest="sha256:" + "a" * 64,
                    observed_digest="sha256:" + "b" * 64,
                    path="/private/internal/evidence.md",
                    field="engine_sources",
                    observed="private-value",
                ))
                redacted = application_engine._domain_rejection(private_failure)
                self.assertEqual(redacted.details, {})


if __name__ == "__main__":
    unittest.main()
