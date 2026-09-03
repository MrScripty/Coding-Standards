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
    AuthoringError,
    AuthoringModule,
    FindProposalsRequest,
    Mutation,
    ProposalId,
)
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


class AuthoringTests(unittest.TestCase):
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
                StandardsEngine(object(), snapshots),  # type: ignore[arg-type]
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                created = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "workflows/planning.md",
                                "value": "# Revised planning\n",
                            }
                        ],
                        "semantic_proposals": [],
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
                StandardsEngine(object(), snapshots),  # type: ignore[arg-type]
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                created = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "workflows/planning.md",
                                "value": "# Initial proposal\n",
                            }
                        ],
                        "semantic_proposals": [],
                    }
                )

            initial_revision = created["revision"]
            snapshots = SnapshotModule.open(database)
            with AgentToolFacade(
                StandardsEngine(object(), snapshots),  # type: ignore[arg-type]
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                initial_counts = snapshots._store.counts()

                invalid_target = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "missing.md",
                                "value": "missing",
                            }
                        ],
                        "semantic_proposals": [],
                    }
                )
                self.assertEqual(
                    invalid_target["code"], "AUTHORING.MUTATION_TARGET_UNAVAILABLE"
                )
                self.assertEqual(snapshots._store.counts(), initial_counts)

                revised = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "workflows/planning.md",
                                "value": "# Revised proposal\n",
                            }
                        ],
                        "semantic_proposals": [],
                    }
                )
                self.assertEqual(revised["kind"], "revise-proposal-result")
                self.assertEqual(revised["proposal"], created["proposal"])
                after_revision = snapshots._store.counts()

                stale = facade.revise_proposal(
                    {
                        "kind": "revise-proposal",
                        "expected_revision": initial_revision,
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "workflows/planning.md",
                                "value": "# Stale proposal\n",
                            }
                        ],
                        "semantic_proposals": [],
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
                authoring = AuthoringModule(reopened)
                historical = authoring.read_revision(initial_revision["id"])
                current = authoring.read_revision(revised["revision"]["id"])
                self.assertEqual(historical.ordinal, 1)
                self.assertEqual(current.ordinal, 2)
                self.assertEqual(historical.base_snapshot, current.base_snapshot)
                self.assertEqual(current.mutations[0].value, "# Revised proposal\n")

    def test_create_rejects_duplicate_and_missing_replacement_targets(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            authoring = AuthoringModule(
                snapshots,
                proposal_id_factory=lambda: ProposalId.from_uuid(
                    uuid.UUID("00000000-0000-4000-8000-000000000001")
                ),
            )
            planning = Mutation(SnapshotPath.parse("workflows/planning.md"), "one")

            with self.assertRaises(AuthoringError) as duplicate:
                authoring.create_proposal(base, (planning, planning), ())
            self.assertEqual(
                duplicate.exception.failure.code, "AUTHORING.INVALID_REVISION"
            )

            missing = Mutation(SnapshotPath.parse("missing.md"), "new")
            with self.assertRaises(AuthoringError) as unavailable:
                authoring.create_proposal(base, (missing,), ())
            self.assertEqual(
                unavailable.exception.failure.code,
                "AUTHORING.MUTATION_TARGET_UNAVAILABLE",
            )
            self.assertEqual(
                authoring.find_proposals(FindProposalsRequest()).proposals, ()
            )
            snapshots.close()

    def test_create_translates_invalid_semantic_identity_to_a_typed_rejection(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            snapshots = SnapshotModule.open(Path(temporary) / "standards.sqlite3")
            base = snapshots.create_snapshot(_capture()).snapshot
            with AgentToolFacade(
                StandardsEngine(object(), snapshots),  # type: ignore[arg-type]
                _contracts(REPOSITORY_ROOT),
            ) as facade:
                rejected = facade.create_proposal(
                    {
                        "kind": "create-proposal",
                        "base_snapshot": _snapshot_handle(base),
                        "mutations": [
                            {
                                "op": "replace",
                                "path": "CORE-STANDARDS.md",
                                "value": "# Revised core\n",
                            }
                        ],
                        "semantic_proposals": [
                            {
                                "policy": "core",
                                "accepted_semantic_revision": 1,
                                "proposed_semantic_revision": 2,
                                "intent": "\ud800",
                                "structural_digest": "sha256:" + "0" * 64,
                            }
                        ],
                    }
                )

            self.assertEqual(rejected["kind"], "rejected-result")
            self.assertEqual(rejected["code"], "AUTHORING.INVALID_SEMANTIC_PROPOSAL")
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
                AggregateRecord(revision_id, "proposal-revision", b"{}", (base,)),
            )

            with self.assertRaises(AuthoringError) as invalid_revision:
                AuthoringModule(snapshots).find_proposals(FindProposalsRequest())
            self.assertEqual(
                invalid_revision.exception.failure.code,
                "AUTHORING.INVALID_STORED_REVISION",
            )
            snapshots.close()

    def test_discovery_translates_invalid_persisted_unicode_identity(self) -> None:
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
            self.assertEqual(rejected["code"], "AUTHORING.INVALID_STORED_REVISION")
            self.assertEqual(rejected["outcome"], "invalid")

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
                now=lambda: now[0],
                proposal_id_factory=lambda: proposal_id,
            )
            authoring.create_proposal(
                base,
                (Mutation(SnapshotPath.parse("CORE-STANDARDS.md"), "# New core\n"),),
                (),
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
                    (Mutation(SnapshotPath.parse("CORE-STANDARDS.md"), "# Reused\n"),),
                    (),
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
                now=lambda: now[0],
                proposal_id_factory=lambda: next(identifiers),
            )
            mutation = (
                Mutation(SnapshotPath.parse("CORE-STANDARDS.md"), "# New core\n"),
            )
            first, _ = authoring.create_proposal(base, mutation, ())
            now[0] -= 1
            second, _ = authoring.create_proposal(base, mutation, ())

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
