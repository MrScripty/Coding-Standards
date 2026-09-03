from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    CreateProposalCall,
    CreateProposalResult,
    CreateSnapshotCall,
    InspectCall,
    PolicyInspectionResult,
    ProposalReadResult,
    ProposalRelatedResult,
    ProposalRouteResult,
    QueryCall,
    QueryProposalCall,
    ReadRequest,
    ReadResult,
    RelatedRequest,
    RelatedResult,
    RejectedResult,
    RouteRequest,
    RouteResult,
    ReviseProposalCall,
    ReviseProposalResult,
    StandardsEngine,
)
from tools.standards_engine.standards_engine.tools import _contracts


REPO_ROOT = Path(__file__).resolve().parents[3]
SUITE_INPUTS = "evaluation/standards-effectiveness/generated/suite-inputs.json"


def _projected_mutations(
    planning: str, manifest_content: bytes
) -> list[dict[str, object]]:
    manifest = json.loads(manifest_content)
    planning_entry = next(
        item for item in manifest["files"] if item["path"] == "workflows/planning.md"
    )
    planning_entry["digest"] = (
        "sha256:" + hashlib.sha256(planning.encode("utf-8")).hexdigest()
    )
    projected_manifest = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    return [
        {
            "op": "replace",
            "path": "workflows/planning.md",
            "value": planning,
        },
        {
            "op": "replace",
            "path": SUITE_INPUTS,
            "value": projected_manifest,
        },
    ]


class NavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.engine = StandardsEngine.open_repository(
            REPO_ROOT,
            store_path=Path(cls.temporary.name) / "standards.sqlite3",
        )
        created = cls.engine.create_snapshot(
            CreateSnapshotCall.from_value({"kind": "create-snapshot"})
        )
        cls.snapshot = created.snapshot.snapshot

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.close()
        cls.temporary.cleanup()

    @staticmethod
    def route_facts(**overrides: object) -> dict[str, object]:
        values: dict[str, object] = {
            "routing.activities": [],
            "routing.workflow-profiles": [],
            "routing.applications": [],
            "routing.boundaries": [],
            "routing.languages": [],
            "routing.frameworks": [],
            "routing.topics": [],
        }
        values.update(overrides)
        return {
            key: (
                value
                if isinstance(value, dict)
                else {"type": "enum-set", "state": "known", "value": value}
            )
            for key, value in values.items()
        }

    def test_route_selects_direct_modules_and_required_closure(self) -> None:
        result = self.engine.query(
            QueryCall(
                self.snapshot,
                RouteRequest(
                    "route",
                    self.route_facts(
                        **{
                            "routing.activities": ["implementation", "verification"],
                            "routing.applications": ["library"],
                            "routing.languages": ["rust"],
                        }
                    ),
                ),
            )
        )

        self.assertIsInstance(result, RouteResult)
        self.assertEqual(result.snapshot, self.snapshot)
        self.assertEqual(result.unresolved_questions, ())
        selected = {item.target for item in result.reading_plan}
        self.assertTrue(
            {
                "core",
                "router",
                "workflow.implementation",
                "workflow.verification",
                "profile.application.library",
                "profile.language.rust",
            }.issubset(selected)
        )
        self.assertEqual(
            [item.target for item in result.reading_plan[:2]], ["core", "router"]
        )

    def test_unknown_and_invalid_route_facts_have_typed_results(self) -> None:
        facts = self.route_facts()
        facts["routing.topics"] = {"type": "enum-set", "state": "unknown"}
        unresolved = self.engine.query(
            QueryCall(self.snapshot, RouteRequest("route", facts))
        )
        self.assertIsInstance(unresolved, RouteResult)
        self.assertEqual(
            [item.id for item in unresolved.unresolved_questions],
            ["question.routing.topics"],
        )

        invalid = self.engine.query(
            QueryCall(
                self.snapshot,
                RouteRequest(
                    "route",
                    {
                        "routing.undeclared": {
                            "type": "boolean",
                            "state": "known",
                            "value": True,
                        }
                    },
                ),
            )
        )
        self.assertIsInstance(invalid, RejectedResult)
        self.assertEqual(invalid.code, "APPLICABILITY.INVALID")

    def test_development_proportionality_routes_directly_and_before_planning(self) -> None:
        direct = self.engine.query(
            QueryCall(
                self.snapshot,
                RouteRequest(
                    "route",
                    self.route_facts(
                        **{"routing.activities": ["uncertainty-reduction"]}
                    ),
                ),
            )
        )
        self.assertIsInstance(direct, RouteResult)
        direct_targets = [item.target for item in direct.reading_plan]
        self.assertIn("workflow.development-proportionality", direct_targets)
        self.assertNotIn("workflow.planning", direct_targets)
        self.assertLess(
            direct_targets.index("workflow.implementation"),
            direct_targets.index("workflow.development-proportionality"),
        )
        self.assertLess(
            direct_targets.index("workflow.verification"),
            direct_targets.index("workflow.development-proportionality"),
        )

        planning = self.engine.query(
            QueryCall(
                self.snapshot,
                RouteRequest(
                    "route", self.route_facts(**{"routing.activities": ["planning"]})
                ),
            )
        )
        self.assertIsInstance(planning, RouteResult)
        planning_targets = [item.target for item in planning.reading_plan]
        self.assertLess(
            planning_targets.index("workflow.development-proportionality"),
            planning_targets.index("workflow.planning"),
        )

    def test_read_related_and_inspect_share_the_snapshot_root(self) -> None:
        read = self.engine.query(
            QueryCall(self.snapshot, ReadRequest("read", "workflow.planning"))
        )
        self.assertIsInstance(read, ReadResult)
        self.assertEqual(read.snapshot, self.snapshot)
        self.assertEqual(read.policy.handle.snapshot, self.snapshot)
        self.assertIn("# Planning Workflow", read.content)

        inspected = self.engine.inspect(InspectCall(read.policy.handle))
        self.assertIsInstance(inspected, PolicyInspectionResult)
        self.assertEqual(inspected.policy.snapshot, self.snapshot)

        related = self.engine.query(
            QueryCall(
                self.snapshot,
                RelatedRequest(
                    "related", "workflow.planning", ("policy-impact",), "both", False
                ),
            )
        )
        self.assertIsInstance(related, RelatedResult)
        self.assertEqual(related.snapshot, self.snapshot)
        self.assertTrue(related.relationships)
        self.assertTrue(
            all(item.handle.snapshot == self.snapshot for item in related.relationships)
        )

    def test_live_worktree_mutation_cannot_change_snapshot_reads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            subprocess.run(
                ("git", "clone", "-q", "--no-hardlinks", str(REPO_ROOT), str(root)),
                check=True,
            )
            engine = StandardsEngine.open_repository(
                root, store_path=Path(temporary) / "standards.sqlite3"
            )
            try:
                created = engine.create_snapshot(
                    CreateSnapshotCall.from_value({"kind": "create-snapshot"})
                )
                snapshot = created.snapshot.snapshot
                call = QueryCall(snapshot, ReadRequest("read", "workflow.planning"))
                before = engine.query(call)
                (root / "workflows/planning.md").write_text(
                    "# Mutated worktree\n", encoding="utf-8"
                )
                after = engine.query(call)
            finally:
                engine.close()

        self.assertIsInstance(before, ReadResult)
        self.assertEqual(before, after)

    def test_proposal_query_projects_every_request_from_an_exact_revision(self) -> None:
        capture = self.engine._snapshots.load_content(
            self.engine._snapshot_id(self.snapshot)
        )
        files = {str(item.path): item.content for item in capture.files}
        planning = files["workflows/planning.md"].decode("utf-8")
        initial_content = planning.replace(
            "Store a planned effort under one directory:",
            "Store an initial proposed effort under one directory:",
        )
        revised_content = planning.replace(
            "Store a planned effort under one directory:",
            "Store a revised proposed effort under one directory:",
        )
        self.assertNotEqual(initial_content, planning)
        created = self.engine.create_proposal(
            CreateProposalCall.from_value(
                {
                    "kind": "create-proposal",
                    "base_snapshot": self.snapshot.as_contract(),
                    "mutations": _projected_mutations(
                        initial_content, files[SUITE_INPUTS]
                    ),
                    "semantic_proposals": [],
                }
            )
        )
        self.assertIsInstance(created, CreateProposalResult)
        counts = self.engine._snapshots._store.counts()

        route = self.engine.query_proposal(
            QueryProposalCall(
                created.revision,
                RouteRequest(
                    "route",
                    self.route_facts(**{"routing.activities": ["planning"]}),
                ),
            )
        )
        self.assertIsInstance(route, ProposalRouteResult)
        self.assertEqual(route.revision, created.revision)
        self.assertTrue(route.next_operations)
        self.assertTrue(
            all(item.authority == "projection" for item in route.reading_plan)
        )
        self.assertTrue(
            all(
                item.operation == "query_proposal" and item.revision == created.revision
                for item in route.next_operations
            )
        )

        read_call = QueryProposalCall(
            created.revision,
            ReadRequest("read", "workflow.planning"),
        )
        read = ProposalReadResult.from_value(
            AgentToolFacade(self.engine, _contracts(REPO_ROOT)).query_proposal(
                read_call.as_contract()
            )
        )
        self.assertEqual(read.content, initial_content)
        self.assertEqual(read.policy.id, "workflow.planning")
        self.assertEqual(read.policy.authority, "projection")
        self.assertEqual(read.summary, "Read projected standard workflow.planning.")
        self.assertEqual(len(read.next_operations), 1)
        self.assertEqual(read.next_operations[0].operation, "query_proposal")
        self.assertNotIn("snapshot", read.as_contract())

        related = self.engine.query_proposal(
            QueryProposalCall(
                created.revision,
                RelatedRequest(
                    "related", "workflow.planning", ("policy-impact",), "both", False
                ),
            )
        )
        self.assertIsInstance(related, ProposalRelatedResult)
        self.assertTrue(related.relationships)
        self.assertTrue(
            all("handle" not in item.as_contract() for item in related.relationships)
        )
        self.assertEqual(self.engine._snapshots._store.counts(), counts)

        revised = self.engine.revise_proposal(
            ReviseProposalCall.from_value(
                {
                    "kind": "revise-proposal",
                    "expected_revision": created.revision.as_contract(),
                    "mutations": _projected_mutations(
                        revised_content, files[SUITE_INPUTS]
                    ),
                    "semantic_proposals": [],
                }
            )
        )
        self.assertIsInstance(revised, ReviseProposalResult)
        revised_counts = self.engine._snapshots._store.counts()
        historical = self.engine.query_proposal(
            QueryProposalCall(
                created.revision,
                ReadRequest("read", "workflow.planning"),
            )
        )
        current = self.engine.query_proposal(
            QueryProposalCall(
                revised.revision,
                ReadRequest("read", "workflow.planning"),
            )
        )
        self.assertIsInstance(historical, ProposalReadResult)
        self.assertIsInstance(current, ProposalReadResult)
        self.assertEqual(historical.content, initial_content)
        self.assertEqual(current.content, revised_content)
        self.assertEqual(self.engine._snapshots._store.counts(), revised_counts)

    def test_proposal_query_returns_typed_failure_for_invalid_projected_content(
        self,
    ) -> None:
        capture = self.engine._snapshots.load_content(
            self.engine._snapshot_id(self.snapshot)
        )
        files = {str(item.path): item.content for item in capture.files}
        invalid_content = "# Planning without canonical metadata\n"
        created = self.engine.create_proposal(
            CreateProposalCall.from_value(
                {
                    "kind": "create-proposal",
                    "base_snapshot": self.snapshot.as_contract(),
                    "mutations": _projected_mutations(
                        invalid_content, files[SUITE_INPUTS]
                    ),
                    "semantic_proposals": [],
                }
            )
        )
        self.assertIsInstance(created, CreateProposalResult)
        counts = self.engine._snapshots._store.counts()

        rejected = self.engine.query_proposal(
            QueryProposalCall(
                created.revision,
                ReadRequest("read", "workflow.planning"),
            )
        )

        self.assertIsInstance(rejected, RejectedResult)
        self.assertEqual(rejected.outcome, "invalid")
        self.assertNotEqual(rejected.code, "INTERFACE.INVALID_ARGUMENTS")
        self.assertEqual(self.engine._snapshots._store.counts(), counts)


if __name__ == "__main__":
    unittest.main()
