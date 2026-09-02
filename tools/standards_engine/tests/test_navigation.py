from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.standards_engine.standards_engine import (
    CreateSnapshotCall,
    InspectCall,
    PolicyInspectionResult,
    QueryCall,
    ReadRequest,
    ReadResult,
    RelatedRequest,
    RelatedResult,
    RejectedResult,
    RouteRequest,
    RouteResult,
    StandardsEngine,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


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


if __name__ == "__main__":
    unittest.main()
