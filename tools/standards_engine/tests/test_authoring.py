from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.authoring import (
    APPLICATION_CAPABILITY,
    AuthoringError,
    AuthoringFailure,
    AuthoringModule,
    FindProposalsRequest,
    ProposalApplication,
    ProposalId,
    ProposalReadiness,
    application_subject,
    proposal_commit_message,
    review_decision_subject,
)
from tools.standards_engine.standards_engine.logical_authoring import (
    StandardsChangeSet,
)
from tools.repository_git.repository_git import RepositoryRevision
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_snapshots.standards_snapshots import (
    AggregateRecord,
    AggregateRoot,
    CapturedContent,
    SnapshotFile,
    SnapshotModule,
    SnapshotPath,
    SnapshotError,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

_CHANGE_EVIDENCE = {
    "id": "evidence.authoring-test",
    "digest": "sha256:" + "1" * 64,
    "provider_contract": "authoring-test",
    "provider_contract_version": "1",
}


def _capture() -> CapturedContent:
    return CapturedContent(
        "a" * 40,
        (
            SnapshotFile(SnapshotPath.parse("CORE-STANDARDS.md"), b"# Core\n"),
            SnapshotFile(SnapshotPath.parse("workflows/planning.md"), b"# Planning\n"),
        ),
    )


def _snapshot_handle(snapshot: object) -> dict[str, object]:
    return {"kind": "snapshot-handle", "id": str(snapshot), "schema_version": 5}


def _change_set(label: str, *, standard: str = "core") -> StandardsChangeSet:
    return StandardsChangeSet.from_mapping(
        _change_set_contract(label, standard=standard)
    )


def _change_set_contract(
    label: str,
    *,
    standard: str = "core",
) -> dict[str, object]:
    return {
        "purpose": {
            "summary": label,
            "rationale": f"Exercise the {label} authoring transition.",
            "evidence": [_CHANGE_EVIDENCE],
        },
        "edits": [
            {
                "kind": "replace-standard-relationships",
                "standard": standard,
                "requires": [],
                "specializes": [],
                "rationale": f"Keep {standard} relationships explicit for {label}.",
            }
        ],
    }


def _authoring(
    snapshots: SnapshotModule,
    **options: object,
) -> AuthoringModule:
    return AuthoringModule(
        snapshots,
        validate_revision=lambda _revision: None,
        observe_repository_paths=lambda snapshot: (
            str(item.path) for item in snapshots.load_content(snapshot).files
        ),
        **options,  # type: ignore[arg-type]
    )


def _engine_with_stub_authoring(snapshots: SnapshotModule) -> StandardsEngine:
    engine = StandardsEngine(object(), snapshots)  # type: ignore[arg-type]
    engine._authoring = _authoring(snapshots)
    return engine


def _review_decisions() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "owner": owner,
            "decision": "accept",
            "rationale": f"The {owner} review obligations are satisfied.",
            "evidence": [
                {
                    "id": f"evidence.review.{owner}",
                    "digest": "sha256:" + character * 64,
                    "provider_contract": "evidence.review",
                    "provider_contract_version": "1",
                }
            ],
        }
        for owner, character in zip(
            ("consumer", "impact", "audit"),
            ("a", "b", "c"),
            strict=True,
        )
    )


def _review_authorizations(
    analysis: str,
    revision: str,
    decisions: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    capabilities = {
        "consumer": "standards.review.consumer",
        "impact": "standards.review.impact",
        "audit": "standards.review.audit",
    }
    return tuple(
        {
            "reference": {
                "id": f"authorization:sha256:{index:064x}",
                "issuer": "issuer.fixture",
                "capability": capability,
                "authority_digest": "sha256:" + "a" * 64,
            },
            "issuer_semantic_revision": 1,
            "principal": "principal.fixture",
            "action": "review-proposal",
            "subject_kind": "proposal-review-decision",
            "subject_id": review_decision_subject(analysis, revision, decision),
            "authorization_evidence": [
                {
                    "id": "evidence.authorization",
                    "digest": "sha256:" + "d" * 64,
                    "provider_contract": "authorization-grant.v1",
                    "provider_contract_version": "1",
                }
            ],
            "revocation_authority": "revocation.fixture",
            "revocation_authority_semantic_revision": 1,
            "revocation_evidence": [
                {
                    "id": "evidence.revocation",
                    "digest": "sha256:" + "e" * 64,
                    "provider_contract": "authorization-revocation.v1",
                    "provider_contract_version": "1",
                }
            ],
        }
        for index, decision in enumerate(decisions, 1)
        for capability in (capabilities[str(decision["owner"])],)
    )


def _application_authorization(
    readiness: str,
    revision: str,
    target: RepositoryRevision,
) -> dict[str, object]:
    subject = application_subject(readiness, revision, target)
    return {
        "reference": {
            "id": "authorization:sha256:" + "9" * 64,
            "issuer": "issuer.fixture",
            "capability": APPLICATION_CAPABILITY,
            "authority_digest": "sha256:" + "a" * 64,
        },
        "issuer_semantic_revision": 1,
        "principal": "principal.fixture",
        "action": "apply-proposal",
        "subject_kind": "proposal-application",
        "subject_id": subject,
        "authorization_evidence": [
            {
                "id": "evidence.authorization",
                "digest": "sha256:" + "d" * 64,
                "provider_contract": "authorization-grant.v1",
                "provider_contract_version": "1",
            }
        ],
        "revocation_authority": "revocation.fixture",
        "revocation_authority_semantic_revision": 1,
        "revocation_evidence": [
            {
                "id": "evidence.revocation",
                "digest": "sha256:" + "e" * 64,
                "provider_contract": "authorization-revocation.v1",
                "provider_contract_version": "1",
            }
        ],
    }


class AuthoringTests(unittest.TestCase):
    def test_readiness_rejects_invalid_proposal_commit_material(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = _authoring(snapshots)
            _summary, revision = authoring.create_proposal(
                base,
                _change_set("invalid\ncommit subject"),
            )
            analysis = "analysis:sha256:" + "a" * 64
            decisions = _review_decisions()
            before = snapshots._store.counts()

            with self.assertRaises(AuthoringError) as invalid:
                authoring.review_proposal(
                    analysis,
                    revision.revision_id,
                    decisions,
                    _review_authorizations(
                        analysis,
                        revision.revision_id,
                        decisions,
                    ),
                    RepositoryRevision("b" * 40),
                )

            self.assertEqual(
                invalid.exception.failure.code,
                "AUTHORING.INVALID_COMMIT_MATERIAL",
            )
            self.assertEqual(snapshots._store.counts(), before)
            snapshots.close()

    def test_application_intent_is_current_head_guarded_and_records_applied(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            database = Path(temporary) / "standards.sqlite3"
            snapshots = SnapshotModule.open(database)
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = _authoring(snapshots)
            _summary, revision = authoring.create_proposal(
                base,
                _change_set("ready application"),
            )
            analysis = "analysis:sha256:" + "a" * 64
            target = RepositoryRevision("b" * 40)
            decisions = _review_decisions()
            readiness = authoring.review_proposal(
                analysis,
                revision.revision_id,
                decisions,
                _review_authorizations(analysis, revision.revision_id, decisions),
                target,
            )
            with self.assertRaises(AuthoringError) as not_admitted:
                authoring.read_selected_application(readiness.readiness_id)
            self.assertEqual(
                not_admitted.exception.failure.code, "APPLICATION.NOT_ADMITTED"
            )
            application = authoring.admit_application(
                readiness.readiness_id,
                _application_authorization(
                    readiness.readiness_id,
                    revision.revision_id,
                    target,
                ),
                RepositoryRevision("c" * 40),
            )
            self.assertIsInstance(application, ProposalApplication)
            self.assertEqual(
                authoring.read_application(application.application_id),
                application,
            )
            self.assertEqual(
                authoring.read_selected_application(readiness.readiness_id),
                application,
            )
            selection = application.selection().aggregate()
            self.assertEqual(len(selection.payload), 218)
            with self.assertRaises(AuthoringError) as invalid_selection:
                authoring._application_selection_from_record(
                    AggregateRecord(
                        selection.aggregate_id,
                        selection.kind,
                        b"{}",
                        selection.snapshots,
                    )
                )
            self.assertEqual(
                invalid_selection.exception.failure.code,
                "AUTHORING.INVALID_APPLICATION_SELECTION",
            )
            self.assertIsNone(authoring.application_outcome(application))

            conflicting_authorization = _application_authorization(
                readiness.readiness_id,
                revision.revision_id,
                target,
            )
            conflicting_authorization["reference"] = {
                **conflicting_authorization["reference"],
                "id": "authorization:sha256:" + "8" * 64,
            }
            with self.assertRaises(AuthoringError) as conflict:
                authoring.admit_application(
                    readiness.readiness_id,
                    conflicting_authorization,
                    RepositoryRevision("c" * 40),
                )
            self.assertEqual(
                conflict.exception.failure.code,
                "AUTHORING.APPLICATION_SELECTION_CONFLICT",
            )
            outcome = authoring.record_applied(application)
            self.assertEqual(outcome.status, "applied")
            self.assertEqual(
                authoring.read_application_outcome(application.application_id),
                outcome,
            )
            self.assertEqual(authoring.application_outcome(application), outcome)

            snapshots.close()
            with SnapshotModule.open(database) as reopened:
                cold = _authoring(reopened)
                self.assertEqual(
                    cold.read_application(application.application_id),
                    application,
                )
                self.assertEqual(
                    cold.read_selected_application(readiness.readiness_id),
                    application,
                )
                self.assertEqual(
                    cold.read_application_outcome(application.application_id),
                    outcome,
                )

    def test_stale_readiness_cannot_publish_application_intent(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = _authoring(snapshots)
            _summary, revision = authoring.create_proposal(
                base,
                _change_set("ready stale application"),
            )
            analysis = "analysis:sha256:" + "a" * 64
            target = RepositoryRevision("b" * 40)
            decisions = _review_decisions()
            readiness = authoring.review_proposal(
                analysis,
                revision.revision_id,
                decisions,
                _review_authorizations(analysis, revision.revision_id, decisions),
                target,
            )
            authoring.revise_proposal(
                revision.revision_id,
                _change_set("later application"),
            )
            before = snapshots._store.counts()

            with self.assertRaises(AuthoringError) as stale:
                authoring.admit_application(
                    readiness.readiness_id,
                    _application_authorization(
                        readiness.readiness_id,
                        revision.revision_id,
                        target,
                    ),
                    RepositoryRevision("c" * 40),
                )

            self.assertEqual(stale.exception.failure.code, "AUTHORING.READINESS_STALE")
            self.assertEqual(snapshots._store.counts(), before)
            snapshots.close()

    def test_readiness_is_content_bound_durable_and_current_head_guarded(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            database = Path(temporary) / "standards.sqlite3"
            snapshots = SnapshotModule.open(database)
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = _authoring(snapshots)
            _summary, revision = authoring.create_proposal(
                base,
                _change_set("ready review"),
            )
            analysis = "analysis:sha256:" + "a" * 64
            target = RepositoryRevision("b" * 40)
            decisions = _review_decisions()
            authorizations = _review_authorizations(
                analysis,
                revision.revision_id,
                decisions,
            )
            readiness = authoring.review_proposal(
                analysis,
                revision.revision_id,
                decisions,
                authorizations,
                target,
            )
            repeated = authoring.review_proposal(
                analysis,
                revision.revision_id,
                decisions,
                authorizations,
                target,
                prior_readiness=readiness.readiness_id,
            )
            changed_decisions = tuple(
                {
                    **decision,
                    "rationale": (
                        "The audit was independently re-evaluated."
                        if decision["owner"] == "audit"
                        else decision["rationale"]
                    ),
                }
                for decision in decisions
            )
            before_mismatch = snapshots._store.counts()
            with self.assertRaises(AuthoringError) as mismatch:
                authoring.review_proposal(
                    analysis,
                    revision.revision_id,
                    changed_decisions,
                    _review_authorizations(
                        analysis,
                        revision.revision_id,
                        changed_decisions,
                    ),
                    target,
                    prior_readiness=readiness.readiness_id,
                )

            self.assertEqual(repeated, readiness)
            expanded_decisions = tuple(
                {
                    **decision,
                    "evidence": [
                        *decision["evidence"],
                        {
                            "id": f"evidence.review.{decision['owner']}.second",
                            "digest": "sha256:" + "f" * 64,
                            "provider_contract": "evidence.review",
                            "provider_contract_version": "1",
                        },
                    ],
                }
                for decision in decisions
            )
            reordered_decisions = tuple(
                {**decision, "evidence": list(reversed(decision["evidence"]))}
                for decision in expanded_decisions
            )
            expanded = ProposalReadiness(
                base,
                analysis,
                revision.revision_id,
                expanded_decisions,
                _review_authorizations(
                    analysis,
                    revision.revision_id,
                    expanded_decisions,
                ),
                target,
            )
            reordered = ProposalReadiness(
                base,
                analysis,
                revision.revision_id,
                reordered_decisions,
                _review_authorizations(
                    analysis,
                    revision.revision_id,
                    reordered_decisions,
                ),
                target,
            )
            self.assertEqual(reordered, expanded)
            self.assertEqual(
                mismatch.exception.failure.code,
                "AUTHORING.READINESS_MISMATCH",
            )
            self.assertEqual(snapshots._store.counts(), before_mismatch)
            self.assertEqual(readiness.aggregate().snapshots, (base,))
            snapshots.close()
            with SnapshotModule.open(database) as reopened:
                reconstructed = _authoring(reopened).read_readiness(
                    readiness.readiness_id
                )
                self.assertEqual(reconstructed, readiness)

                current = _authoring(reopened)
                current.revise_proposal(
                    revision.revision_id,
                    _change_set("later review"),
                )
                before = reopened._store.counts()
                with self.assertRaises(AuthoringError) as stale:
                    current.review_proposal(
                        "analysis:sha256:" + "c" * 64,
                        revision.revision_id,
                        decisions,
                        _review_authorizations(
                            "analysis:sha256:" + "c" * 64,
                            revision.revision_id,
                            decisions,
                        ),
                        target,
                    )
                self.assertEqual(
                    stale.exception.failure.code, "AUTHORING.REVISION_STALE"
                )
                self.assertEqual(reopened._store.counts(), before)

    def test_readiness_rejects_incomplete_decisions_without_persistence(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = _authoring(snapshots)
            _summary, revision = authoring.create_proposal(
                base,
                _change_set("ready incomplete review"),
            )
            before = snapshots._store.counts()
            analysis = "analysis:sha256:" + "a" * 64
            decisions = _review_decisions()

            with self.assertRaises(AuthoringError) as incomplete:
                ProposalReadiness(
                    base,
                    analysis,
                    revision.revision_id,
                    (decisions[2],),
                    _review_authorizations(
                        analysis,
                        revision.revision_id,
                        decisions,
                    ),
                    RepositoryRevision("b" * 40),
                )

            self.assertEqual(
                incomplete.exception.failure.code,
                "AUTHORING.REVIEW_INCOMPLETE",
            )
            self.assertEqual(snapshots._store.counts(), before)
            snapshots.close()

    def test_create_and_find_are_durable_through_the_public_facade(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            repository = Path(temporary) / "repository"
            contract_root = repository / "tools/standards_engine/contracts"
            contract_root.mkdir(parents=True)
            for name in ("a1-contract.schema.json", "a1-interface.toml"):
                shutil.copy2(
                    REPOSITORY_ROOT / "tools/standards_engine/contracts" / name,
                    contract_root / name,
                )
            subprocess.run(("git", "init", "-q", str(repository)), check=True)
            database = repository / ".standards-engine/snapshots-v1.sqlite3"
            snapshots = SnapshotModule.open(database)
            base = snapshots.create_snapshot(_capture()).snapshot
            with AgentToolFacade(
                _engine_with_stub_authoring(snapshots),
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                created = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "change_set": _change_set_contract("durable creation"),
                    }
                )

            self.assertEqual(created["kind"], "create-proposal-result")
            script = """
import json
import sys
from pathlib import Path
from tools.standards_engine.standards_engine import AgentToolFacade

request = json.loads(sys.stdin.read())
with AgentToolFacade.open_repository(Path(request["root"])) as facade:
    print(json.dumps(facade.find_proposals({"kind": "find-proposals"}), sort_keys=True))
"""
            environment = dict(os.environ)
            environment.update(
                {
                    "PYTHONPATH": str(REPOSITORY_ROOT),
                    "PYTHONDONTWRITEBYTECODE": "1",
                }
            )
            completed = subprocess.run(
                (sys.executable, "-P", "-c", script),
                cwd=REPOSITORY_ROOT,
                env=environment,
                input=json.dumps({"root": str(repository)}),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            found = json.loads(completed.stdout)

            self.assertEqual(found["kind"], "find-proposals-result")
            self.assertEqual(
                found["proposals"],
                [
                    {
                        "proposal": created["proposal"],
                        "head_revision": created["revision"],
                    }
                ],
            )

    def test_revise_is_durable_and_stale_writes_leave_no_partial_record(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            database = Path(temporary) / "standards.sqlite3"
            snapshots = SnapshotModule.open(database)
            base = snapshots.create_snapshot(_capture()).snapshot
            with AgentToolFacade(
                _engine_with_stub_authoring(snapshots),
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                created = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "change_set": _change_set_contract("initial proposal"),
                    }
                )

            initial_revision = created["revision"]
            snapshots = SnapshotModule.open(database)
            engine = _engine_with_stub_authoring(snapshots)

            def validate_revision(revision: object) -> None:
                change_sets = getattr(revision, "change_sets")
                standard = change_sets[-1].as_contract()["edits"][0]["standard"]
                if standard == "missing":
                    raise AuthoringError(
                        AuthoringFailure(
                            "AUTHORING.STANDARD_UNAVAILABLE",
                            "unavailable",
                            "logical standard target is unavailable",
                        )
                    )

            engine._authoring = AuthoringModule(
                snapshots,
                validate_revision=validate_revision,
                observe_repository_paths=lambda snapshot: (
                    str(item.path) for item in snapshots.load_content(snapshot).files
                ),
            )
            with AgentToolFacade(
                engine,
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                initial_counts = snapshots._store.counts()

                invalid_target = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "change_set": _change_set_contract(
                            "invalid revision",
                            standard="missing",
                        ),
                    }
                )
                self.assertEqual(
                    invalid_target["code"], "AUTHORING.STANDARD_UNAVAILABLE"
                )
                self.assertEqual(snapshots._store.counts(), initial_counts)

                revised = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "change_set": _change_set_contract("revised proposal"),
                    }
                )
                self.assertEqual(revised["kind"], "revise-proposal-result")
                self.assertEqual(revised["proposal"], created["proposal"])
                after_revision = snapshots._store.counts()

                stale = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "change_set": _change_set_contract("stale proposal"),
                    }
                )
                self.assertEqual(stale["kind"], "rejected-result")
                self.assertEqual(stale["code"], "AUTHORING.REVISION_STALE")
                self.assertEqual(stale["outcome"], "invalid")
                self.assertEqual(snapshots._store.counts(), after_revision)
                found = facade.find_proposals({"kind": "find-proposals"})
                self.assertEqual(
                    found["proposals"][0]["head_revision"], revised["revision"]
                )

            with SnapshotModule.open(database) as reopened:
                authoring = _authoring(reopened)
                historical = authoring.read_revision(initial_revision["id"])
                current = authoring.read_revision(revised["revision"]["id"])
                self.assertEqual(historical.ordinal, 1)
                self.assertEqual(current.ordinal, 2)
                self.assertEqual(historical.base_snapshot, current.base_snapshot)
                self.assertEqual(
                    historical.base_repository_paths,
                    ("CORE-STANDARDS.md", "workflows/planning.md"),
                )
                self.assertEqual(
                    historical.base_repository_paths,
                    current.base_repository_paths,
                )
                self.assertEqual(len(historical.change_sets), 1)
                self.assertEqual(len(current.change_sets), 2)
                self.assertEqual(
                    current.change_sets[-1].purpose.summary,
                    "revised proposal",
                )
                historical_message = proposal_commit_message(historical)
                current_message = proposal_commit_message(current)
                self.assertEqual(
                    historical_message.subject,
                    "feat(standards): apply standards change: initial proposal",
                )
                self.assertEqual(
                    historical_message.body,
                    "Exercise the initial proposal authoring transition.",
                )
                self.assertEqual(
                    current_message.subject,
                    "feat(standards): apply standards change: revised proposal",
                )
                self.assertEqual(
                    current_message.body,
                    "Exercise the initial proposal authoring transition.\n\n"
                    "Exercise the revised proposal authoring transition.",
                )

    def test_create_rejects_duplicate_facets_and_validator_failure_is_atomic(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot

            duplicate_contract = _change_set_contract("duplicate facets")
            duplicate_contract["edits"] = [
                *duplicate_contract["edits"],  # type: ignore[misc]
                {
                    "kind": "replace-standard-relationships",
                    "standard": "core",
                    "requires": ["topic.contracts"],
                    "specializes": [],
                    "rationale": "A second write to the same logical facet.",
                },
            ]
            with self.assertRaises(AuthoringError) as duplicate:
                StandardsChangeSet.from_mapping(duplicate_contract)
            self.assertEqual(
                duplicate.exception.failure.code,
                "AUTHORING.DUPLICATE_EDIT",
            )

            def reject_unavailable(_revision: object) -> None:
                raise AuthoringError(
                    AuthoringFailure(
                        "AUTHORING.STANDARD_UNAVAILABLE",
                        "unavailable",
                        "logical standard target is unavailable",
                    )
                )

            authoring = AuthoringModule(
                snapshots,
                validate_revision=reject_unavailable,
                observe_repository_paths=lambda snapshot: (
                    str(item.path) for item in snapshots.load_content(snapshot).files
                ),
                proposal_id_factory=lambda: ProposalId.from_uuid(
                    uuid.UUID("00000000-0000-4000-8000-000000000001")
                ),
            )

            with self.assertRaises(AuthoringError) as unavailable:
                authoring.create_proposal(
                    base,
                    _change_set("missing standard", standard="missing"),
                )
            self.assertEqual(
                unavailable.exception.failure.code,
                "AUTHORING.STANDARD_UNAVAILABLE",
            )
            self.assertEqual(
                authoring.find_proposals(FindProposalsRequest()).proposals, ()
            )
            snapshots.close()

    def test_create_translates_invalid_change_set_unicode_to_a_typed_rejection(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            invalid_change_set = _change_set_contract("invalid Unicode")
            purpose = invalid_change_set["purpose"]
            assert isinstance(purpose, dict)
            purpose["summary"] = "\ud800"
            with AgentToolFacade(
                _engine_with_stub_authoring(snapshots),
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                rejected = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "change_set": invalid_change_set,
                    }
                )

            self.assertEqual(rejected["kind"], "rejected-result")
            self.assertEqual(rejected["code"], "AUTHORING.INVALID_ARGUMENTS")
            self.assertEqual(rejected["outcome"], "invalid")

    def test_discovery_rejects_a_revision_without_content_bound_authority(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            proposal = ProposalId.from_uuid(
                uuid.UUID("00000000-0000-4000-8000-000000000001")
            )
            revision_id = "proposal-revision:sha256:" + "0" * 64
            snapshots.create_aggregate_root(
                AggregateRoot(str(proposal), "proposal", revision_id, (base,), 1),
                AggregateRecord(
                    revision_id,
                    "proposal-revision",
                    b'{"contract_version":2}',
                    (base,),
                ),
            )

            with self.assertRaises(AuthoringError) as invalid_revision:
                _authoring(snapshots).find_proposals(FindProposalsRequest())
            self.assertEqual(
                invalid_revision.exception.failure.code,
                "AUTHORING.INVALID_STORED_REVISION",
            )
            snapshots.close()

    def test_discovery_rejects_the_old_revision_contract_as_unsupported(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            proposal = ProposalId.from_uuid(
                uuid.UUID("00000000-0000-4000-8000-000000000001")
            )
            revision_id = "proposal-revision:sha256:" + "0" * 64
            payload = json.dumps(
                {
                    "base_snapshot": str(base),
                    "contract_version": 1,
                    "mutations": [
                        {
                            "op": "replace",
                            "path": "CORE-STANDARDS.md",
                            "value": "# Revised core\n",
                        }
                    ],
                    "ordinal": 1,
                    "proposal": str(proposal),
                    "semantic_proposals": [
                        {
                            "policy": "core",
                            "accepted_semantic_revision": 1,
                            "proposed_semantic_revision": 2,
                            "intent": "\ud800",
                            "structural_digest": "sha256:" + "0" * 64,
                        }
                    ],
                },
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("ascii")
            snapshots.create_aggregate_root(
                AggregateRoot(str(proposal), "proposal", revision_id, (base,), 1),
                AggregateRecord(revision_id, "proposal-revision", payload, (base,)),
            )
            with AgentToolFacade(
                StandardsEngine(object(), snapshots),  # type: ignore[arg-type]
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                rejected = facade.find_proposals({"kind": "find-proposals"})

            self.assertEqual(rejected["kind"], "rejected-result")
            self.assertEqual(
                rejected["code"],
                "AUTHORING.STORED_REVISION_CONTRACT_UNSUPPORTED",
            )
            self.assertEqual(rejected["outcome"], "unsupported")

    def test_proposals_follow_snapshot_quarantine_and_purge_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            snapshots = SnapshotModule.open(
                Path(temporary) / "standards.sqlite3",
                now=lambda: now[0],
                quarantine_seconds=1,
            )
            base = snapshots.create_snapshot(_capture()).snapshot
            proposal_id = ProposalId.from_uuid(
                uuid.UUID("00000000-0000-4000-8000-000000000001")
            )
            authoring = AuthoringModule(
                snapshots,
                validate_revision=lambda _revision: None,
                observe_repository_paths=lambda snapshot: (
                    str(item.path) for item in snapshots.load_content(snapshot).files
                ),
                now=lambda: now[0],
                proposal_id_factory=lambda: proposal_id,
            )
            authoring.create_proposal(
                base,
                _change_set("new core"),
            )

            snapshots.delete_snapshot(base)
            self.assertEqual(
                authoring.find_proposals(FindProposalsRequest()).proposals, ()
            )
            snapshots.undelete_snapshot(base)
            self.assertEqual(
                len(authoring.find_proposals(FindProposalsRequest()).proposals), 1
            )
            snapshots.delete_snapshot(base)
            now[0] += 1
            snapshots.maintain()
            self.assertEqual(
                authoring.find_proposals(FindProposalsRequest()).proposals, ()
            )
            replacement_base = snapshots.create_snapshot(_capture()).snapshot
            with self.assertRaises(SnapshotError) as reused:
                authoring.create_proposal(
                    replacement_base,
                    _change_set("reused proposal ID"),
                )
            self.assertEqual(
                reused.exception.failure.code, "AGGREGATE.ROOT_ID_COLLISION"
            )
            snapshots.close()

    def test_proposal_discovery_uses_opaque_keyset_continuations(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            identifiers = iter(
                (
                    ProposalId.from_uuid(
                        uuid.UUID("00000000-0000-4000-8000-000000000002")
                    ),
                    ProposalId.from_uuid(
                        uuid.UUID("00000000-0000-4000-8000-000000000001")
                    ),
                )
            )
            now = [2_000_000_000]
            authoring = AuthoringModule(
                snapshots,
                validate_revision=lambda _revision: None,
                observe_repository_paths=lambda snapshot: (
                    str(item.path) for item in snapshots.load_content(snapshot).files
                ),
                now=lambda: now[0],
                proposal_id_factory=lambda: next(identifiers),
            )
            change_set = _change_set("pagination")
            first, _ = authoring.create_proposal(base, change_set)
            now[0] -= 1
            second, _ = authoring.create_proposal(base, change_set)

            first_page = authoring.find_proposals(FindProposalsRequest(limit=1))
            self.assertEqual(first_page.proposals, (first,))
            self.assertEqual(first_page.continuation, first.proposal)
            self.assertEqual(
                authoring.find_proposals(
                    FindProposalsRequest(first_page.continuation, 1)
                ).proposals,
                (second,),
            )
            snapshots.close()


if __name__ == "__main__":
    unittest.main()
