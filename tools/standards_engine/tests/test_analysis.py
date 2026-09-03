from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest import mock

from tools.standards_analysis.standards_analysis import (
    AnalysisState as DomainAnalysisState,
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    AuthorizationDenied,
    AuthorizationRequest,
    EvidenceContractKey,
    EvidenceReference,
    ResolvedEvidence,
    SnapshotMaterialRef,
    construct_authorization_record,
)
from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    AnalyzeProposalCall,
    AnalysisChildInspectionResult,
    AnalysisHandle,
    AnalysisInspectionResult,
    ApplyProposalResult,
    CompleteResult,
    CreateProposalCall,
    CreateProposalResult,
    CreateSnapshotCall,
    CreateSnapshotResult,
    InspectCall,
    PendingResult,
    PrepareCall,
    RejectedResult,
    RecoverApplicationResult,
    ResolveCall,
    ReviewProposalResult,
    ReviseProposalCall,
    ReviseProposalResult,
    StandardsEngine,
)
from tools.repository_git.repository_git import (
    GitRepositoryError,
    GitRepositoryFailure,
    MaterializedCandidate,
    RepositoryPath,
    RepositoryRevision,
    git_output,
)
from tools.standards_verifier.standards_verifier import CompleteVerificationResult
from tools.standards_verifier.standards_verifier.diagnostics import Diagnostic
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.standards_engine.authoring import (
    ProposalApplication,
    ProposalRevision,
    REVIEW_CAPABILITIES,
    proposal_commit_message,
    review_decision_subject,
)
from tools.standards_snapshots.standards_snapshots import (
    SnapshotId,
    SnapshotError,
    SnapshotFailure,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY = "workflow.planning.written-plan-applicability"
WRITTEN_PLAN_TITLE = "When A Written Plan Is Required"
ARTIFACT_MODEL_POLICY = "workflow.planning.artifact-model"
ARTIFACT_MODEL_TITLE = "Artifact Model"


def _reference(identifier: str) -> EvidenceReference:
    content = identifier.encode("utf-8")
    return EvidenceReference(
        identifier,
        "sha256:" + hashlib.sha256(content).hexdigest(),
        "repository-content",
        "1",
    )


def _section_body(document: str, title: str) -> str:
    marker = f"## {title}\n"
    if document.count(marker) != 1:
        raise AssertionError(f"expected one registered section {title!r}")
    remainder = document.partition(marker)[2]
    body = remainder.partition("\n## ")[0].strip("\n")
    if not body:
        raise AssertionError(f"registered section {title!r} has no body")
    return body


def _policy_change_set(
    *,
    policy: str,
    title: str,
    body: str,
    accepted_revision: int,
    proposed_revision: int,
    purpose: str,
) -> dict[str, object]:
    return {
        "purpose": {
            "summary": purpose,
            "rationale": "Exercise Analysis over explicit logical standards intent.",
            "evidence": [_reference(f"logical-authoring-{policy}").as_contract()],
        },
        "edits": [
            {
                "kind": "revise-policy-unit",
                "policy": policy,
                "title": title,
                "body": body,
                "semantics": {
                    "kind": "change",
                    "accepted_semantic_revision": accepted_revision,
                    "proposed_semantic_revision": proposed_revision,
                    "intent": purpose,
                },
            }
        ],
    }


def _review_decisions() -> list[dict[str, object]]:
    return [
        {
            "owner": owner,
            "decision": "accept",
            "rationale": f"The {owner} review is satisfied by the completed analysis.",
            "evidence": [_reference(f"proposal-{owner}-review").as_contract()],
        }
        for owner in ("consumer", "impact", "audit")
    ]


def _clone_tracked_worktree(destination: Path) -> None:
    subprocess.run(
        (
            "git",
            "clone",
            "--local",
            "--no-hardlinks",
            "--quiet",
            "--",
            str(REPO_ROOT),
            str(destination),
        ),
        check=True,
    )
    tracked = subprocess.run(
        ("git", "-C", str(REPO_ROOT), "ls-files", "-z"),
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    for encoded in tracked.split(b"\0"):
        if not encoded:
            continue
        relative = Path(os.fsdecode(encoded))
        source = REPO_ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(os.readlink(source))
        else:
            if target.is_symlink():
                target.unlink()
            shutil.copy2(source, target)
    subprocess.run(
        ("git", "-C", str(destination), "add", "--all"),
        check=True,
    )
    changed = subprocess.run(
        ("git", "-C", str(destination), "diff", "--cached", "--quiet"),
        check=False,
    )
    if changed.returncode not in {0, 1}:
        raise AssertionError("fixture Git index could not be compared")
    if changed.returncode == 1:
        subprocess.run(
            (
                "git",
                "-C",
                str(destination),
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=Standards Engine Test",
                "-c",
                "user.email=standards-engine-test@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test: materialize tracked worktree",
            ),
            check=True,
        )


class ExactAuthorizer:
    contract = AuthorizationAuthorityContract(
        "issuer.fixture",
        1,
        "principal.fixture",
        "authorization-grant.v1",
        (EvidenceContractKey("repository-content", "1"),),
        "revocation.fixture",
        1,
        "authorization-revocation.v1",
        (EvidenceContractKey("repository-content", "1"),),
    )

    def authorize(self, request):
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (ResolvedEvidence(_reference("authorization"), b"authorization"),),
            (ResolvedEvidence(_reference("revocation"), b"revocation"),),
            "not-revoked",
            "allow",
        )


class DenyingAuthorizer:
    contract = ExactAuthorizer.contract

    def authorize(self, request):
        del request
        return AuthorizationDenied("The exact application capability was denied.")


class AnalysisWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.store = Path(cls.temporary.name) / "standards.sqlite3"
        cls.engine = StandardsEngine.open_repository(
            REPO_ROOT,
            store_path=cls.store,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        created = cls.engine.create_snapshot(
            CreateSnapshotCall.from_value({"kind": "create-snapshot"})
        )
        cls.snapshot = created.snapshot.snapshot

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.close()
        cls.temporary.cleanup()

    def test_apply_proposal_composes_real_verification_and_cold_readback(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            repository = root / "repository"
            store = root / "standards.sqlite3"
            _clone_tracked_worktree(repository)
            context = AnalysisExecutionContext(ExactAuthorizer())
            engine = StandardsEngine.open_repository(
                repository,
                store_path=store,
                execution_context=context,
            )
            facade = AgentToolFacade(engine, _contracts(repository))
            try:
                expected = engine._repository.branch_revision("main")
                path = "workflows/planning.md"
                planning = (repository / path).read_text(encoding="utf-8")
                snapshot_result = engine.create_snapshot(
                    CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                )
                self.assertIsInstance(snapshot_result, CreateSnapshotResult)
                base = snapshot_result.snapshot.snapshot
                module = engine._compiled_snapshot(
                    engine._snapshot_id(base)
                ).corpus.resolve_module("workflow.planning")
                assert module is not None
                owner_line = f"- Canonical owner: `{module.path}`\n\n"
                body = planning.split(owner_line, 1)[1]
                introduction = (
                    "This standard is maintained through the Standards Engine.\n\n"
                )
                created = CreateProposalResult.from_value(
                    facade.create_proposal(
                        {
                            "kind": "create-proposal",
                            "base_snapshot": base.as_contract(),
                            "change_set": {
                                "purpose": {
                                    "summary": "exercise logical application",
                                    "rationale": "Verify exact local application and recovery.",
                                    "evidence": [
                                        _reference("logical-application").as_contract()
                                    ],
                                },
                                "edits": [
                                    {
                                        "kind": "revise-standard",
                                        "standard": {
                                            "id": module.module_id,
                                            "title": planning.splitlines()[
                                                0
                                            ].removeprefix("# "),
                                            "role": module.role,
                                            "level": module.level,
                                            "applies_when": module.applies_when,
                                            "does_not_apply_when": module.excludes,
                                            "verification": module.verification,
                                            "body": introduction + body,
                                        },
                                    }
                                ],
                            },
                        }
                    )
                )
                analysis = "analysis:sha256:" + "a" * 64
                decisions = _review_decisions()
                authorizations = tuple(
                    construct_authorization_record(
                        context,
                        AuthorizationRequest(
                            "review-proposal",
                            "proposal-review-decision",
                            review_decision_subject(
                                analysis,
                                created.revision.id,
                                decision,
                            ),
                            REVIEW_CAPABILITIES[str(decision["owner"])],
                            (_reference(f"proposal-{decision['owner']}-review"),),
                        ),
                    ).as_contract()
                    for decision in decisions
                )
                readiness = engine._authoring.review_proposal(
                    analysis,
                    created.revision.id,
                    decisions,
                    authorizations,
                    expected,
                )

                with mock.patch.object(
                    engine._authoring,
                    "record_applied",
                    side_effect=SnapshotError(
                        SnapshotFailure(
                            "unavailable",
                            "SNAPSHOT_STORE.PROTOTYPE_INTERRUPTION",
                            "the response was lost before outcome persistence",
                        )
                    ),
                ):
                    response = facade.apply_proposal(
                        {
                            "kind": "apply-proposal",
                            "readiness": {
                                "kind": "readiness-handle",
                                "id": readiness.readiness_id,
                                "schema_version": 1,
                            },
                        }
                    )
                self.assertEqual(
                    response.get("kind"),
                    "application-recovery-required-result",
                    response,
                )
                application = engine._authoring.read_application(
                    response["application"]["id"]
                )
                self.assertEqual(
                    response["code"], "APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE"
                )
                self.assertEqual(application.expected_target, expected)
                self.assertNotEqual(application.candidate, expected)
                self.assertEqual(
                    engine._repository.branch_revision("main"),
                    application.candidate,
                )
                commit = git_output(
                    repository,
                    ("cat-file", "commit", application.candidate.oid),
                )
                headers, separator, message = commit.partition(b"\n\n")
                self.assertEqual(separator, b"\n\n")
                self.assertIn(
                    f"parent {expected.oid}".encode("ascii"), headers.splitlines()
                )
                self.assertEqual(
                    message,
                    proposal_commit_message(
                        engine._authoring.read_revision(created.revision.id)
                    ).encode(),
                )
                applied_planning = engine._repository.read_file(
                    application.candidate,
                    RepositoryPath.parse(path),
                ).decode("utf-8")
                self.assertIn(introduction.strip(), applied_planning)
                self.assertNotEqual(applied_planning, planning)
            finally:
                facade.close()

            reopened = StandardsEngine.open_repository(
                repository,
                store_path=store,
                execution_context=context,
            )
            try:
                cold_facade = AgentToolFacade(reopened, _contracts(repository))
                with (
                    mock.patch.object(
                        reopened._repository, "materialize_candidate"
                    ) as materialize,
                    mock.patch.object(
                        reopened._repository, "publish_candidate"
                    ) as publish,
                    mock.patch.object(reopened, "_application_verifier") as verify,
                ):
                    recovered = RecoverApplicationResult.from_value(
                        cold_facade.recover_application(
                            {
                                "kind": "recover-application",
                                "readiness": {
                                    "kind": "readiness-handle",
                                    "id": readiness.readiness_id,
                                    "schema_version": 1,
                                },
                            }
                        )
                    )
                materialize.assert_not_called()
                publish.assert_not_called()
                verify.assert_not_called()
                cold_application = reopened._authoring.read_application(
                    recovered.application.id
                )
                cold_outcome = reopened._authoring.read_application_outcome(
                    recovered.application.id
                )
            finally:
                reopened.close()
            self.assertEqual(recovered.application.id, application.application_id)
            self.assertEqual(cold_application, application)
            self.assertEqual(cold_outcome.candidate, application.candidate)
            self.assertEqual(cold_outcome.status, "applied")

    def test_apply_create_and_retire_owns_topology_and_commit(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            repository = root / "repository"
            store = root / "standards.sqlite3"
            _clone_tracked_worktree(repository)
            context = AnalysisExecutionContext(ExactAuthorizer())
            engine = StandardsEngine.open_repository(
                repository,
                store_path=store,
                execution_context=context,
            )
            facade = AgentToolFacade(engine, _contracts(repository))
            standard_path = "topics/logical-application-test.md"
            policy_path = (
                "evaluation/standards-effectiveness/policy-units/"
                "topic.logical-application-test.toml"
            )
            impact_path = (
                "evaluation/standards-effectiveness/policy-impact/"
                "topic.logical-application-test.toml"
            )
            relationship = {
                "source_policy": "topic.logical-application-test.policy",
                "consumer": "workflow.planning",
                "relation": "normative-consumer",
                "applicability": {"operator": "always"},
                "source_scope": None,
                "consumer_scope": None,
                "evidence_owner": "suite:core-simplicity",
                "rationale": "Planning consumes the application fixture policy.",
            }

            def readiness_for(
                revision_id: str,
                expected: RepositoryRevision,
                marker: str,
            ):
                analysis = "analysis:sha256:" + marker * 64
                decisions = _review_decisions()
                authorizations = tuple(
                    construct_authorization_record(
                        context,
                        AuthorizationRequest(
                            "review-proposal",
                            "proposal-review-decision",
                            review_decision_subject(analysis, revision_id, decision),
                            REVIEW_CAPABILITIES[str(decision["owner"])],
                            (_reference(f"topology-{marker}-{decision['owner']}"),),
                        ),
                    ).as_contract()
                    for decision in decisions
                )
                return engine._authoring.review_proposal(
                    analysis,
                    revision_id,
                    decisions,
                    authorizations,
                    expected,
                )

            def apply_ready(readiness_id: str) -> ProposalApplication:
                applied = ApplyProposalResult.from_value(
                    facade.apply_proposal(
                        {
                            "kind": "apply-proposal",
                            "readiness": {
                                "kind": "readiness-handle",
                                "id": readiness_id,
                                "schema_version": 1,
                            },
                        }
                    )
                )
                return engine._authoring.read_application(applied.application.id)

            def assert_commit(
                application: ProposalApplication,
                revision: ProposalRevision,
                expected: RepositoryRevision,
            ) -> None:
                commit = git_output(
                    repository,
                    ("cat-file", "commit", application.candidate.oid),
                )
                headers, separator, message = commit.partition(b"\n\n")
                self.assertEqual(separator, b"\n\n")
                self.assertIn(
                    f"parent {expected.oid}".encode("ascii"), headers.splitlines()
                )
                self.assertEqual(message, proposal_commit_message(revision).encode())

            try:
                initial = engine._repository.branch_revision("main")
                base_result = engine.create_snapshot(
                    CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                )
                self.assertIsInstance(base_result, CreateSnapshotResult)
                created = CreateProposalResult.from_value(
                    facade.create_proposal(
                        {
                            "kind": "create-proposal",
                            "base_snapshot": base_result.snapshot.snapshot.as_contract(),
                            "change_set": {
                                "purpose": {
                                    "summary": "add logical application fixture",
                                    "rationale": "Exercise Engine-owned additions and derived standards projections.",
                                    "evidence": [
                                        _reference("topology-create").as_contract()
                                    ],
                                },
                                "edits": [
                                    {
                                        "kind": "create-standard",
                                        "standard": {
                                            "id": "topic.logical-application-test",
                                            "title": "Logical Application Test",
                                            "role": "topic",
                                            "level": "MUST",
                                            "applies_when": "Logical application is tested.",
                                            "does_not_apply_when": "Logical application is not tested.",
                                            "verification": "Standards Engine application tests.",
                                            "body": "## Application Policy\n\nUse the Engine Interface.\n",
                                        },
                                        "requires": ["core"],
                                        "specializes": [],
                                        "policy_units": [
                                            {
                                                "id": "topic.logical-application-test.policy",
                                                "heading_chain": ["Application Policy"],
                                                "semantic_revision": 1,
                                                "intent": "Create one application test policy.",
                                                "aliases": [],
                                                "predecessors": [],
                                                "successors": [],
                                            }
                                        ],
                                    },
                                    {
                                        "kind": "put-policy-relationship",
                                        "relationship": relationship,
                                    },
                                ],
                            },
                        }
                    )
                )
                create_revision = engine._authoring.read_revision(created.revision.id)
                create_ready = readiness_for(created.revision.id, initial, "b")
                create_application = apply_ready(create_ready.readiness_id)
                assert_commit(create_application, create_revision, initial)
                created_paths = {
                    str(path)
                    for path in engine._repository.revision_paths(
                        create_application.candidate
                    )
                }
                self.assertTrue(
                    {standard_path, policy_path, impact_path} <= created_paths
                )
                created_modes = {
                    line.partition(" ")[2]: line.partition(" ")[0]
                    for line in git_output(
                        repository,
                        (
                            "ls-tree",
                            "-r",
                            "--format=%(objectmode) %(path)",
                            create_application.candidate.oid,
                        ),
                    )
                    .decode("utf-8")
                    .splitlines()
                }
                self.assertEqual(
                    {
                        path: created_modes[path]
                        for path in (standard_path, policy_path, impact_path)
                    },
                    {
                        standard_path: "100644",
                        policy_path: "100644",
                        impact_path: "100644",
                    },
                )
                self.assertFalse((repository / standard_path).exists())

                facade.close()
                engine = StandardsEngine.open_repository(
                    repository,
                    store_path=store,
                    execution_context=context,
                )
                facade = AgentToolFacade(engine, _contracts(repository))
                self.assertEqual(
                    engine._repository.branch_revision("main"),
                    create_application.candidate,
                )
                created_snapshot = engine.create_snapshot(
                    CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                )
                self.assertIsInstance(created_snapshot, CreateSnapshotResult)
                created_read = facade.query(
                    {
                        "snapshot": created_snapshot.snapshot.snapshot.as_contract(),
                        "request": {
                            "kind": "read",
                            "target": "topic.logical-application-test",
                        },
                    }
                )
                self.assertEqual(created_read["kind"], "read-result")
                self.assertIn("Use the Engine Interface.", created_read["content"])
                retired = CreateProposalResult.from_value(
                    facade.create_proposal(
                        {
                            "kind": "create-proposal",
                            "base_snapshot": created_snapshot.snapshot.snapshot.as_contract(),
                            "change_set": {
                                "purpose": {
                                    "summary": "retire logical application fixture",
                                    "rationale": "Exercise Engine-owned removals and exact generated cleanup.",
                                    "evidence": [
                                        _reference("topology-retire").as_contract()
                                    ],
                                },
                                "edits": [
                                    {
                                        "kind": "retire-policy-unit",
                                        "policy": "topic.logical-application-test.policy",
                                        "retired_semantic_revision": 1,
                                        "successors": [],
                                        "relationship_dispositions": [
                                            {
                                                "relationship": {
                                                    "kind": "policy-relationship",
                                                    "source_policy": relationship[
                                                        "source_policy"
                                                    ],
                                                    "consumer": relationship[
                                                        "consumer"
                                                    ],
                                                    "relation": relationship[
                                                        "relation"
                                                    ],
                                                },
                                                "disposition": "remove",
                                                "rationale": "Remove the retired policy relationship.",
                                                "evidence": [
                                                    _reference(
                                                        "topology-retire-policy"
                                                    ).as_contract()
                                                ],
                                            }
                                        ],
                                        "evidence": [
                                            _reference(
                                                "topology-retire-policy-unit"
                                            ).as_contract()
                                        ],
                                    },
                                    {
                                        "kind": "retire-standard",
                                        "standard": "topic.logical-application-test",
                                        "successors": [],
                                        "relationship_dispositions": [
                                            {
                                                "relationship": {
                                                    "kind": "module-relationship",
                                                    "source": "topic.logical-application-test",
                                                    "target": "core",
                                                    "relation": "requires",
                                                },
                                                "disposition": "remove",
                                                "rationale": "Remove the retired dependency.",
                                                "evidence": [
                                                    _reference(
                                                        "topology-retire-standard"
                                                    ).as_contract()
                                                ],
                                            }
                                        ],
                                        "evidence": [
                                            _reference(
                                                "topology-retire-module"
                                            ).as_contract()
                                        ],
                                    },
                                ],
                            },
                        }
                    )
                )
                retire_revision = engine._authoring.read_revision(retired.revision.id)
                retire_ready = readiness_for(
                    retired.revision.id,
                    create_application.candidate,
                    "c",
                )
                retire_application = apply_ready(retire_ready.readiness_id)
                assert_commit(
                    retire_application,
                    retire_revision,
                    create_application.candidate,
                )
                retired_paths = {
                    str(path)
                    for path in engine._repository.revision_paths(
                        retire_application.candidate
                    )
                }
                self.assertFalse({standard_path, impact_path} & retired_paths)
                self.assertIn(policy_path, retired_paths)
                retired_policy = engine._repository.read_file(
                    retire_application.candidate,
                    RepositoryPath.parse(policy_path),
                )
                self.assertIn(b"[[tombstone]]", retired_policy)
                self.assertNotIn(b"[[policy_unit]]", retired_policy)
                self.assertFalse((repository / standard_path).exists())

                facade.close()
                engine = StandardsEngine.open_repository(
                    repository,
                    store_path=store,
                    execution_context=context,
                )
                facade = AgentToolFacade(engine, _contracts(repository))
                self.assertEqual(
                    engine._repository.branch_revision("main"),
                    retire_application.candidate,
                )
                retired_snapshot = engine.create_snapshot(
                    CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                )
                self.assertIsInstance(retired_snapshot, CreateSnapshotResult)
                retired_read = facade.query(
                    {
                        "snapshot": retired_snapshot.snapshot.snapshot.as_contract(),
                        "request": {
                            "kind": "read",
                            "target": "topic.logical-application-test",
                        },
                    }
                )
                self.assertEqual(retired_read["code"], "NAVIGATION.UNKNOWN_POLICY")
            finally:
                facade.close()

    def test_prepare_persists_parent_bound_public_work(self) -> None:
        result = self.prepare()

        self.assertIsInstance(result, PendingResult)
        self.assertTrue(result.obligations)
        for obligation in result.obligations:
            self.assertEqual(obligation.handle.analysis, result.handle)
        for operation in result.next_operations:
            if operation.operation == "resolve":
                self.assertEqual(operation.analysis, result.handle)

        state = self.engine.inspect(InspectCall(result.handle))
        self.assertIsInstance(state, AnalysisInspectionResult)
        self.assertEqual(state.state.handle, result.handle)

        child = self.engine.inspect(InspectCall(result.obligations[0].handle))
        self.assertIsInstance(child, AnalysisChildInspectionResult)
        self.assertEqual(child.handle.analysis, result.handle)

    def test_proposal_analysis_derives_inputs_and_replays_exact_revision(self) -> None:
        capture = self.engine._snapshots.load_content(
            self.engine._snapshot_id(self.snapshot)
        )
        files = {str(item.path): item.content for item in capture.files}
        planning = files["workflows/planning.md"].decode("utf-8")
        initial_content = planning.replace(
            "Create a written plan when the change introduces material sequencing,",
            "Create an analyzed proposed plan when the change introduces material sequencing,",
        )
        revised_content = initial_content.replace(
            "Store a planned effort under one directory:",
            "Store a later proposed effort under one directory:",
        )
        self.assertNotEqual(initial_content, planning)
        created = self.engine.create_proposal(
            CreateProposalCall.from_value(
                {
                    "kind": "create-proposal",
                    "base_snapshot": self.snapshot.as_contract(),
                    "change_set": _policy_change_set(
                        policy=POLICY,
                        title=WRITTEN_PLAN_TITLE,
                        body=_section_body(initial_content, WRITTEN_PLAN_TITLE),
                        accepted_revision=1,
                        proposed_revision=2,
                        purpose="Analyze one exact logical policy revision.",
                    ),
                }
            )
        )
        self.assertIsInstance(created, CreateProposalResult)
        facade = AgentToolFacade(self.engine, _contracts(REPO_ROOT))
        initial = PendingResult.from_value(
            facade.analyze_proposal({"revision": created.revision.as_contract()})
        )
        inspected = self.engine.inspect(InspectCall(initial.handle))
        self.assertIsInstance(inspected, AnalysisInspectionResult)
        self.assertEqual(inspected.state.proposed_reference, created.revision)
        self.assertTrue(initial.changes)

        revised = self.engine.revise_proposal(
            ReviseProposalCall.from_value(
                {
                    "kind": "revise-proposal",
                    "expected_revision": created.revision.as_contract(),
                    "change_set": _policy_change_set(
                        policy=ARTIFACT_MODEL_POLICY,
                        title=ARTIFACT_MODEL_TITLE,
                        body=_section_body(revised_content, ARTIFACT_MODEL_TITLE),
                        accepted_revision=1,
                        proposed_revision=2,
                        purpose="Analyze the immutable successor proposal revision.",
                    ),
                }
            )
        )
        self.assertIsInstance(revised, ReviseProposalResult)
        later = self.engine.analyze_proposal(AnalyzeProposalCall(revised.revision))
        self.assertIsInstance(later, PendingResult)
        self.assertNotEqual(initial.handle, later.handle)

        historical = self.engine.inspect(InspectCall(initial.handle))
        self.assertIsInstance(historical, AnalysisInspectionResult)
        self.assertEqual(historical.state.proposed_reference, created.revision)
        reopened = StandardsEngine.open_repository(
            REPO_ROOT,
            store_path=self.store,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        try:
            replayed = reopened._evaluate(reopened._load_analysis(initial.handle))
        finally:
            reopened.close()
        self.assertEqual(replayed.state.analysis_id, initial.handle.id)
        self.assertEqual(
            tuple(item.descriptor.as_contract() for item in replayed.changes),
            tuple(item.as_contract() for item in initial.changes),
        )
        successor = self.engine.resolve(
            self.disposition_submission(initial, "proposal-review-evidence")
        )
        successor_state = self.engine.inspect(InspectCall(successor.handle))
        self.assertIsInstance(successor_state, AnalysisInspectionResult)
        self.assertEqual(successor_state.state.proposed_reference, created.revision)

    def test_policy_free_standard_creation_enters_public_analysis(self) -> None:
        facade = AgentToolFacade(self.engine, _contracts(REPO_ROOT))
        created = facade.create_proposal(
            {
                "kind": "create-proposal",
                "base_snapshot": self.snapshot.as_contract(),
                "change_set": {
                    "purpose": {
                        "summary": "add policy-free standard",
                        "rationale": "Exercise the admitted optional policy-unit boundary.",
                        "evidence": [_reference("policy-free-standard").as_contract()],
                    },
                    "edits": [
                        {
                            "kind": "create-standard",
                            "standard": {
                                "id": "topic.policy-free-test",
                                "title": "Policy Free Test",
                                "role": "topic",
                                "level": "MUST",
                                "applies_when": "Policy-free standard creation is tested.",
                                "does_not_apply_when": "A registered policy unit is required.",
                                "verification": "Standards Engine public workflow tests.",
                                "body": "This standard has no registered policy units.\n",
                            },
                            "requires": ["core"],
                            "specializes": [],
                            "policy_units": [],
                        }
                    ],
                },
            }
        )
        self.assertEqual(created["kind"], "create-proposal-result", created)

        analyzed = PendingResult.from_value(
            facade.analyze_proposal({"revision": created["revision"]})
        )
        self.assertEqual(analyzed.changed_units, ())
        self.assertTrue(
            any(
                change.kind == "module"
                and change.proposed_module == "topic.policy-free-test"
                for change in analyzed.changes
            )
        )

    def test_relationship_only_proposals_enter_a1c_and_replay_cold(self) -> None:
        module_change = {
            "purpose": {
                "summary": "Analyze one explicit module relationship change.",
                "rationale": "Exercise A1c without changing policy text.",
                "evidence": [_reference("module-relationship-change").as_contract()],
            },
            "edits": [
                {
                    "kind": "replace-standard-relationships",
                    "standard": "topic.resilience",
                    "requires": [
                        "core",
                        "topic.contracts",
                        "topic.architecture",
                        "workflow.verification",
                    ],
                    "specializes": [],
                    "rationale": "Verification becomes an explicit prerequisite.",
                }
            ],
        }
        policy_change = {
            "purpose": {
                "summary": "Analyze one explicit policy relationship change.",
                "rationale": "Exercise policy-impact analysis without changing policy text.",
                "evidence": [_reference("policy-relationship-change").as_contract()],
            },
            "edits": [
                {
                    "kind": "put-policy-relationship",
                    "relationship": {
                        "source_policy": "topic.architecture.authority-scope-admission",
                        "consumer": "workflow.verification",
                        "relation": "normative-consumer",
                        "applicability": {"operator": "always"},
                        "source_scope": None,
                        "consumer_scope": None,
                        "evidence_owner": "suite:core-simplicity",
                        "rationale": "Verification consumes authority-scope admission.",
                    },
                }
            ],
        }
        capture = self.engine._snapshots.load_content(
            self.engine._snapshot_id(self.snapshot)
        )
        resilience_text = next(
            item.content.decode("utf-8")
            for item in capture.files
            if str(item.path) == "topics/resilience.md"
        )
        resilience = self.engine._compiled_snapshot(
            self.engine._snapshot_id(self.snapshot)
        ).corpus.resolve_module("topic.resilience")
        assert resilience is not None
        owner_line = f"- Canonical owner: `{resilience.path}`\n\n"
        resilience_body = resilience_text.split(owner_line, 1)[1]
        whole_standard_change = {
            "purpose": {
                "summary": "Analyze one unmapped whole-standard revision.",
                "rationale": "Exercise A1c without inventing a policy owner.",
                "evidence": [_reference("whole-standard-change").as_contract()],
            },
            "edits": [
                {
                    "kind": "revise-standard",
                    "standard": {
                        "id": resilience.module_id,
                        "title": resilience_text.splitlines()[0].removeprefix("# "),
                        "role": resilience.role,
                        "level": resilience.level,
                        "applies_when": resilience.applies_when,
                        "does_not_apply_when": resilience.excludes,
                        "verification": resilience.verification,
                        "body": (
                            "This revision exercises unmapped module analysis.\n\n"
                            + resilience_body
                        ),
                    },
                }
            ],
        }
        results = []
        for index, change_set in enumerate(
            (module_change, policy_change, whole_standard_change)
        ):
            created = self.engine.create_proposal(
                CreateProposalCall.from_value(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": self.snapshot.as_contract(),
                        "change_set": change_set,
                    }
                )
            )
            self.assertIsInstance(created, CreateProposalResult)
            result = self.engine.analyze_proposal(AnalyzeProposalCall(created.revision))
            self.assertIsInstance(result, PendingResult)
            assert isinstance(result, PendingResult)
            self.assertTrue(result.changes)
            evaluation = self.engine._evaluate(
                self.engine._load_analysis(result.handle)
            )
            if index in {0, 2}:
                self.assertTrue(
                    any(
                        change.descriptor.kind.value == "module"
                        and change.changed_units == ()
                        for change in evaluation.changes
                    )
                )
            else:
                self.assertTrue(
                    any(
                        unit.classification.value == "unchanged"
                        for change in evaluation.changes
                        for unit in change.changed_units
                    )
                )
            results.append(result)

        reopened = StandardsEngine.open_repository(
            REPO_ROOT,
            store_path=self.store,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        try:
            replayed = reopened._evaluate(reopened._load_analysis(results[0].handle))
        finally:
            reopened.close()
        self.assertEqual(replayed.state.analysis_id, results[0].handle.id)

    def test_review_composition_publishes_readiness_for_complete_analysis(self) -> None:
        capture = self.engine._snapshots.load_content(
            self.engine._snapshot_id(self.snapshot)
        )
        commit_workflow = next(
            item.content.decode("utf-8")
            for item in capture.files
            if str(item.path) == "workflows/commit.md"
        )
        compiled = self.engine._compiled_snapshot(
            self.engine._snapshot_id(self.snapshot)
        )
        policy = next(
            item
            for item in compiled.corpus.policy_unit_corpus.units
            if item.id == "workflow.commit.commit-message"
        )
        created = self.engine.create_proposal(
            CreateProposalCall.from_value(
                {
                    "kind": "create-proposal",
                    "base_snapshot": self.snapshot.as_contract(),
                    "change_set": _policy_change_set(
                        policy=policy.id,
                        title=policy.heading_path[-1],
                        body=_section_body(commit_workflow, policy.heading_path[-1]),
                        accepted_revision=policy.semantic_revision,
                        proposed_revision=policy.semantic_revision + 1,
                        purpose="Exercise one real A1c semantic review path.",
                    ),
                }
            )
        )
        self.assertIsInstance(created, CreateProposalResult)
        facade = AgentToolFacade(self.engine, _contracts(REPO_ROOT))
        pending = PendingResult.from_value(
            facade.analyze_proposal({"revision": created.revision.as_contract()})
        )

        incomplete_call = {
            "kind": "review-proposal",
            "analysis": pending.handle.as_contract(),
            "decisions": _review_decisions(),
        }
        incomplete = facade.review_proposal(incomplete_call)
        self.assertEqual(incomplete["code"], "AUTHORING.ANALYSIS_INCOMPLETE")

        pending_state = self.engine._load_analysis(pending.handle)
        requires_change = pending_state.with_decisions(
            dispositions=(
                {
                    "obligation_id": "obligation:requires-change",
                    "result": "requires-change",
                },
            )
        )
        self.engine._snapshots.publish_aggregate(requires_change.aggregate(()))
        blocked_call = {
            **incomplete_call,
            "analysis": self.engine._analysis_handle(requires_change.analysis_id),
        }
        with mock.patch.object(
            self.engine,
            "_evaluate",
            return_value=mock.Mock(complete=True),
        ):
            blocked = facade.review_proposal(blocked_call)
        self.assertEqual(blocked["code"], "AUTHORING.REVIEW_NOT_READY")

        coverage_pending = PendingResult.from_value(
            facade.resolve(
                self.disposition_submission(
                    pending, "proposal-review-evidence"
                ).as_contract()
            )
        )
        self.assertEqual(
            {
                item.request_kind
                for item in coverage_pending.next_operations
                if item.operation == "resolve"
            },
            {"coverage-attestation"},
        )
        complete = CompleteResult.from_value(
            facade.resolve(
                self.coverage_submission(
                    coverage_pending, "proposal-audit-evidence"
                ).as_contract()
            )
        )
        call = {
            **incomplete_call,
            "analysis": complete.handle.as_contract(),
        }
        with (
            mock.patch.object(
                self.engine,
                "_evaluate",
                return_value=mock.Mock(complete=True),
            ),
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=mock.Mock(oid="b" * 40),
            ),
        ):
            stale_target = facade.review_proposal(call)
        self.assertEqual(stale_target["code"], "AUTHORING.TARGET_STALE")

        reviewed = ReviewProposalResult.from_value(facade.review_proposal(call))
        with mock.patch.object(
            self.engine,
            "_evaluate",
            return_value=mock.Mock(complete=True),
        ):
            repeated = ReviewProposalResult.from_value(
                facade.review_proposal(
                    {**call, "prior_readiness": reviewed.readiness.as_contract()}
                )
            )

        self.assertEqual(reviewed.revision, created.revision)
        self.assertEqual(repeated.readiness, reviewed.readiness)
        readiness = self.engine._authoring.read_readiness(reviewed.readiness.id)
        self.assertEqual(readiness.analysis_id, complete.handle.id)
        self.assertEqual(readiness.revision_id, created.revision.id)

        revision = self.engine._authoring.read_revision(created.revision.id)
        projection = self.engine._proposal_projection(revision)
        projected_files = dict(projection.source.files)
        uncaptured_path = next(
            path
            for path in revision.base_repository_paths
            if path not in projected_files
        )
        projected_files[uncaptured_path] = b"not captured authority\n"
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=readiness.expected_target,
            ),
            mock.patch.object(
                self.engine,
                "_proposal_projection",
                return_value=mock.Mock(
                    source=mock.Mock(files=tuple(projected_files.items())),
                    repository_paths=projection.repository_paths,
                ),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
            ) as collision_materialization,
        ):
            collision = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(collision["code"], "APPLICATION.TOPOLOGY_INVALID")
        collision_materialization.assert_not_called()

        with mock.patch.object(
            self.engine._repository, "branch_revision"
        ) as unadmitted_observation:
            unadmitted = facade.recover_application(
                {
                    "kind": "recover-application",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(unadmitted["code"], "APPLICATION.NOT_ADMITTED")
        unadmitted_observation.assert_not_called()

        with (
            mock.patch.object(
                self.engine,
                "_execution_context",
                AnalysisExecutionContext(DenyingAuthorizer()),
            ),
            mock.patch.object(
                self.engine._repository, "branch_revision"
            ) as unauthorized_recovery_observation,
        ):
            unauthorized_recovery = facade.recover_application(
                {
                    "kind": "recover-application",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(unauthorized_recovery["code"], "ANALYSIS.UNAUTHORIZED")
        unauthorized_recovery_observation.assert_not_called()

        candidate = MaterializedCandidate(
            Path(self.temporary.name),
            readiness.expected_target,
            RepositoryRevision("c" * 40),
        )
        rejected_counts = self.engine._snapshots._store.counts()
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=RepositoryRevision("d" * 40),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
            ) as stale_materialization,
        ):
            stale_target = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(stale_target["code"], "APPLICATION.TARGET_STALE")
        stale_materialization.assert_not_called()
        self.assertEqual(self.engine._snapshots._store.counts(), rejected_counts)

        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=readiness.expected_target,
            ) as unauthorized_observation,
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
            ) as unauthorized_materialization,
            mock.patch.object(
                self.engine,
                "_execution_context",
                AnalysisExecutionContext(DenyingAuthorizer()),
            ),
        ):
            unauthorized = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(unauthorized["code"], "ANALYSIS.UNAUTHORIZED")
        unauthorized_observation.assert_not_called()
        unauthorized_materialization.assert_not_called()
        self.assertEqual(self.engine._snapshots._store.counts(), rejected_counts)

        counts_before_failure = self.engine._snapshots._store.counts()
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=readiness.expected_target,
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
                return_value=nullcontext(candidate),
            ),
            mock.patch.object(
                self.engine._repository,
                "publish_candidate",
            ) as failed_publish,
            mock.patch.object(
                self.engine,
                "_application_verifier",
                return_value=CompleteVerificationResult(
                    (),
                    0,
                    Diagnostic(
                        "CHECKPOINT.FAILED",
                        "invalid",
                        "/tmp/private-candidate/secret: " + "x" * 4096,
                        suite="suite.fixture",
                        check="check.fixture",
                        path="/tmp/private-candidate/secret",
                        row=42,
                        field="private-field",
                    ),
                    2,
                ),
            ),
        ):
            verification_failed = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(verification_failed["code"], "APPLICATION.VERIFICATION_FAILED")
        self.assertEqual(
            verification_failed["details"],
            {
                "verification_exit_code": 2,
                "verification_code": "CHECKPOINT.FAILED",
                "verification_outcome": "invalid",
                "verification_suite": "suite.fixture",
                "verification_check": "check.fixture",
            },
        )
        failed_publish.assert_not_called()
        self.assertEqual(self.engine._snapshots._store.counts(), counts_before_failure)

        invalid_candidate = GitRepositoryError(
            GitRepositoryFailure(
                "invalid",
                "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                "fixture candidate diverged before publication",
            )
        )
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                side_effect=(
                    readiness.expected_target,
                    readiness.expected_target,
                ),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
                return_value=nullcontext(candidate),
            ),
            mock.patch.object(
                self.engine._authoring,
                "admit_application",
            ) as invalid_admission,
            mock.patch.object(
                self.engine._repository,
                "validate_candidate",
                side_effect=invalid_candidate,
            ),
            mock.patch.object(
                self.engine._repository, "publish_candidate"
            ) as invalid_publish,
            mock.patch.object(
                self.engine,
                "_application_verifier",
                return_value=CompleteVerificationResult((), 0, None, 0),
            ),
        ):
            candidate_rejected = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(
            candidate_rejected["code"], "REPOSITORY_GIT.CANDIDATE_DIVERGED"
        )
        self.assertEqual(candidate_rejected["kind"], "rejected-result")
        self.assertEqual(candidate_rejected["outcome"], "invalid")
        invalid_admission.assert_not_called()
        invalid_publish.assert_not_called()

        unavailable_publication = GitRepositoryError(
            GitRepositoryFailure(
                "unavailable",
                "REPOSITORY_GIT.COMMAND_UNAVAILABLE",
                "fixture publication is unavailable",
            )
        )
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                side_effect=(
                    readiness.expected_target,
                    readiness.expected_target,
                ),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
                return_value=nullcontext(candidate),
            ),
            mock.patch.object(
                self.engine._authoring,
                "admit_application",
                return_value=mock.Mock(application_id="application:sha256:" + "f" * 64),
            ),
            mock.patch.object(
                self.engine._repository,
                "validate_candidate",
            ),
            mock.patch.object(
                self.engine._repository,
                "publish_candidate",
                side_effect=unavailable_publication,
            ),
            mock.patch.object(
                self.engine,
                "_application_verifier",
                return_value=CompleteVerificationResult((), 0, None, 0),
            ),
        ):
            publication_unavailable = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(
            publication_unavailable["code"], "APPLICATION.PUBLICATION_UNAVAILABLE"
        )
        self.assertEqual(
            publication_unavailable["kind"],
            "application-recovery-required-result",
        )
        self.assertIn(
            "REPOSITORY_GIT.COMMAND_UNAVAILABLE",
            publication_unavailable["message"],
        )

        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                side_effect=(
                    readiness.expected_target,
                    readiness.expected_target,
                ),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
                return_value=nullcontext(candidate),
            ),
            mock.patch.object(
                self.engine._authoring,
                "admit_application",
                return_value=mock.Mock(application_id="application:sha256:" + "e" * 64),
            ),
            mock.patch.object(
                self.engine._repository,
                "validate_candidate",
            ),
            mock.patch.object(
                self.engine._repository,
                "publish_candidate",
                return_value="stale",
            ),
            mock.patch.object(
                self.engine,
                "_application_verifier",
                return_value=CompleteVerificationResult((), 0, None, 0),
            ),
        ):
            publication_stale = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(
            publication_stale["code"], "APPLICATION.RECOVERY_TARGET_DIVERGED"
        )
        self.assertEqual(
            publication_stale["kind"], "application-recovery-required-result"
        )

        unavailable_observation = GitRepositoryError(
            GitRepositoryFailure(
                "unavailable",
                "REPOSITORY_GIT.COMMAND_UNAVAILABLE",
                "fixture observation is unavailable",
            )
        )
        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                side_effect=(
                    readiness.expected_target,
                    readiness.expected_target,
                    unavailable_observation,
                ),
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
                return_value=nullcontext(candidate),
            ),
            mock.patch.object(
                self.engine._repository,
                "publish_candidate",
                return_value="updated",
            ),
            mock.patch.object(
                self.engine._repository,
                "validate_candidate",
            ),
            mock.patch.object(
                self.engine,
                "_application_verifier",
                return_value=CompleteVerificationResult((), 0, None, 0),
            ),
        ):
            recovery_required = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(
            recovery_required["kind"],
            "application-recovery-required-result",
        )
        self.assertEqual(
            recovery_required["code"], "APPLICATION.OBSERVATION_UNAVAILABLE"
        )
        persisted_intent = self.engine._authoring.read_application(
            recovery_required["application"]["id"]
        )
        self.assertEqual(persisted_intent.candidate, candidate.revision)

        with (
            mock.patch.object(
                self.engine._repository, "branch_revision"
            ) as repeated_apply_observation,
            mock.patch.object(
                self.engine._repository, "materialize_candidate"
            ) as repeated_apply_materialization,
            mock.patch.object(
                self.engine._repository, "publish_candidate"
            ) as repeated_apply_publication,
            mock.patch.object(
                self.engine, "_application_verifier"
            ) as repeated_apply_verification,
        ):
            repeated_apply = facade.apply_proposal(
                {
                    "kind": "apply-proposal",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(repeated_apply["kind"], "rejected-result")
        self.assertEqual(repeated_apply["code"], "APPLICATION.ALREADY_ADMITTED")
        repeated_apply_observation.assert_not_called()
        repeated_apply_materialization.assert_not_called()
        repeated_apply_publication.assert_not_called()
        repeated_apply_verification.assert_not_called()

        recovery_counts = self.engine._snapshots._store.counts()
        recovery_cases = (
            (
                unavailable_observation,
                "APPLICATION.OBSERVATION_UNAVAILABLE",
            ),
            (
                readiness.expected_target,
                "APPLICATION.RECOVERY_TARGET_UNCERTAIN",
            ),
            (
                RepositoryRevision("e" * 40),
                "APPLICATION.RECOVERY_TARGET_DIVERGED",
            ),
        )
        for observed, expected_code in recovery_cases:
            with mock.patch.object(
                self.engine._repository,
                "branch_revision",
                side_effect=observed
                if isinstance(observed, GitRepositoryError)
                else None,
                return_value=None
                if isinstance(observed, GitRepositoryError)
                else observed,
            ):
                unresolved = facade.recover_application(
                    {
                        "kind": "recover-application",
                        "readiness": reviewed.readiness.as_contract(),
                    }
                )
            self.assertEqual(unresolved["code"], expected_code)
            self.assertEqual(self.engine._snapshots._store.counts(), recovery_counts)

        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=candidate.revision,
            ),
            mock.patch.object(
                self.engine._authoring,
                "record_applied",
                side_effect=SnapshotError(
                    SnapshotFailure(
                        "unavailable",
                        "SNAPSHOT_STORE.PROTOTYPE_INTERRUPTION",
                        "the recovered outcome write was interrupted",
                    )
                ),
            ),
        ):
            interrupted_recovery = facade.recover_application(
                {
                    "kind": "recover-application",
                    "readiness": reviewed.readiness.as_contract(),
                }
            )
        self.assertEqual(
            interrupted_recovery["code"],
            "APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE",
        )
        self.assertEqual(self.engine._snapshots._store.counts(), recovery_counts)

        with (
            mock.patch.object(
                self.engine._repository,
                "branch_revision",
                return_value=candidate.revision,
            ),
            mock.patch.object(
                self.engine._repository,
                "materialize_candidate",
            ) as materialize,
            mock.patch.object(self.engine._repository, "publish_candidate") as publish,
            mock.patch.object(
                self.engine,
                "_application_verifier",
            ) as verifier,
        ):
            recovered = RecoverApplicationResult.from_value(
                facade.recover_application(
                    {
                        "kind": "recover-application",
                        "readiness": reviewed.readiness.as_contract(),
                    }
                )
            )
        materialize.assert_not_called()
        publish.assert_not_called()
        verifier.assert_not_called()
        self.assertEqual(recovered.status, "applied")
        self.assertEqual(
            recovered.application.id, recovery_required["application"]["id"]
        )
        application = self.engine._authoring.read_application(recovered.application.id)
        outcome = self.engine._authoring.read_application_outcome(
            recovered.application.id
        )
        self.assertEqual(application.candidate, candidate.revision)
        self.assertEqual(outcome.candidate, candidate.revision)

        with mock.patch.object(
            self.engine._repository, "branch_revision"
        ) as completed_observation:
            repeated_recovery = RecoverApplicationResult.from_value(
                facade.recover_application(
                    {
                        "kind": "recover-application",
                        "readiness": reviewed.readiness.as_contract(),
                    }
                )
            )
        completed_observation.assert_not_called()
        self.assertEqual(repeated_recovery.application, recovered.application)

    def test_equal_transition_is_idempotent_and_different_evidence_branches(
        self,
    ) -> None:
        parent = self.prepare()
        first_call = self.disposition_submission(parent, "review-evidence-one")

        first = self.engine.resolve(first_call)
        repeated = self.engine.resolve(first_call)
        second = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence-two")
        )

        self.assertEqual(first.handle, repeated.handle)
        self.assertNotEqual(first.handle, second.handle)
        self.assertEqual(parent.handle, first_call.analysis)

    def test_resolved_parent_work_is_not_applicable_to_child(self) -> None:
        parent = self.prepare()
        submission = self.disposition_submission(parent, "review-evidence")
        child = self.engine.resolve(submission)

        stale = self.engine.resolve(
            ResolveCall.from_value(
                {
                    "analysis": child.handle.as_contract(),
                    "submission": submission.submission.as_contract(),
                }
            )
        )

        self.assertIsInstance(stale, RejectedResult)
        self.assertEqual(stale.code, "SUBMISSION.NOT_APPLICABLE")

    def test_prior_analysis_reuses_the_same_valid_decision(self) -> None:
        parent = self.prepare()
        child = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence")
        )

        reused = self.prepare(prior=child.handle.as_contract())

        self.assertEqual(reused.handle, child.handle)

    def test_state_and_children_are_inspectable_in_a_fresh_process(self) -> None:
        parent = self.prepare()
        child = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence")
        )
        root_handle = child.handle.as_contract()
        child_handle = child.obligations[0].handle.as_contract()
        script = """
import json
import sys
from pathlib import Path

from tools.standards_engine.standards_engine import InspectCall, StandardsEngine

request = json.loads(sys.stdin.read())
engine = StandardsEngine.open_repository(
    Path(request["root"]), store_path=Path(request["store"])
)
try:
    result = [
        engine.inspect(InspectCall.from_value({"handle": handle})).as_contract()
        for handle in request["handles"]
    ]
    print(json.dumps(result, sort_keys=True))
finally:
    engine.close()
"""
        environment = dict(os.environ)
        environment.update(
            {
                "PYTHONPATH": str(REPO_ROOT),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        completed = subprocess.run(
            (sys.executable, "-P", "-c", script),
            cwd=REPO_ROOT,
            env=environment,
            input=json.dumps(
                {
                    "root": str(REPO_ROOT),
                    "store": str(self.store),
                    "handles": [root_handle, child_handle],
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        inspected = json.loads(completed.stdout)
        self.assertEqual(inspected[0]["kind"], "analysis-inspection-result")
        self.assertEqual(inspected[1]["kind"], "analysis-child-inspection-result")

    def test_snapshot_creation_rejects_changed_replay_path_closure(self) -> None:
        class Compiled:
            @staticmethod
            def semantic_signature() -> tuple[str]:
                return ("same",)

        calls = 0

        def compile_with_extra_replay_read(source):
            nonlocal calls
            calls += 1
            source.read_bytes("CORE-STANDARDS.md")
            if calls == 2:
                source.read_bytes("STANDARDS-ROUTER.md")
            return Compiled()

        with tempfile.TemporaryDirectory() as temporary:
            engine = StandardsEngine.open_repository(
                REPO_ROOT,
                store_path=Path(temporary) / "standards.sqlite3",
            )
            try:
                with mock.patch.object(
                    StandardsEngine,
                    "_compile",
                    side_effect=compile_with_extra_replay_read,
                ):
                    result = engine.create_snapshot(
                        CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                    )
            finally:
                engine.close()

        self.assertIsInstance(result, RejectedResult)
        self.assertEqual(result.code, "SNAPSHOT.CLOSURE_MISMATCH")

    def test_cold_load_rejects_obsolete_domain_contracts(self) -> None:
        snapshot_id = SnapshotId(self.snapshot.id)
        state = DomainAnalysisState(
            snapshot_id,
            SnapshotMaterialRef(snapshot_id),
            (
                {
                    "kind": "modification",
                    "accepted_ids": [POLICY],
                    "proposed_ids": [POLICY],
                    "scope": {"kind": "whole-artifact"},
                },
            ),
            domain_contracts=(
                *self.engine._domain_contracts(),
                {"id": "obsolete-contract", "version": "1"},
            ),
        )
        self.engine._snapshots.publish_aggregate(state.aggregate(()))
        handle = AnalysisHandle.from_value(
            {
                "kind": "analysis-handle",
                "id": state.analysis_id,
                "schema_version": 6,
            }
        )

        result = self.engine.inspect(InspectCall(handle))

        self.assertIsInstance(result, RejectedResult)
        self.assertEqual(result.code, "ANALYSIS.DOMAIN_CONTRACT_UNSUPPORTED")
        self.assertEqual(result.outcome, "unsupported")

    def prepare(self, *, prior: dict[str, object] | None = None):
        request: dict[str, object] = {
            "kind": "analysis-request",
            "base_snapshot": self.snapshot.as_contract(),
            "proposed_snapshot": self.snapshot.as_contract(),
            "changes": [
                {
                    "kind": "modification",
                    "accepted_ids": [POLICY],
                    "proposed_ids": [POLICY],
                    "scope": {"kind": "whole-artifact"},
                }
            ],
            "semantic_proposals": [],
            "contract_version": 5,
        }
        if prior is not None:
            request["prior_analysis"] = prior
        return self.engine.prepare(PrepareCall.from_value({"request": request}))

    @staticmethod
    def disposition_submission(result, evidence_id: str) -> ResolveCall:
        operation = next(
            item
            for item in result.next_operations
            if item.request_kind == "consumer-disposition"
        )
        obligation = next(
            item for item in result.obligations if item.handle == operation.work
        )
        evidence = _reference(evidence_id)
        return ResolveCall.from_value(
            {
                "analysis": result.handle.as_contract(),
                "submission": {
                    "kind": "consumer-disposition",
                    "obligation": operation.work.as_contract(),
                    "result": "reviewed-no-change",
                    "rationale": "The exact selected consumer was reviewed.",
                    "evidence": [evidence.as_contract()],
                    "fingerprint": obligation.fingerprint.as_contract(),
                },
            }
        )

    @staticmethod
    def coverage_submission(result, evidence_id: str) -> ResolveCall:
        operation = next(
            item
            for item in result.next_operations
            if item.request_kind == "coverage-attestation"
        )
        return ResolveCall.from_value(
            {
                "analysis": result.handle.as_contract(),
                "submission": {
                    "kind": "coverage-attestation",
                    "claim": {
                        "requirement": operation.work.as_contract(),
                        "conclusion": "complete",
                        "evidence": [_reference(evidence_id).as_contract()],
                        "explicit_exclusions": [],
                        "rationale": "The exact changed policy coverage was reviewed.",
                        "auditor_provenance": "standards.review.audit:test-authorized",
                    },
                },
            }
        )


if __name__ == "__main__":
    unittest.main()
