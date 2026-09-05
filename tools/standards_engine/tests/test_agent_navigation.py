from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as contract
from tools.standards_engine.standards_engine.tools import _contracts

ROOT = Path(__file__).resolve().parents[3]


class AgentNavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = StandardsEngine.open_repository(ROOT, durable=False)
        cls.facade = AgentToolFacade(cls.engine, _contracts(ROOT))
        cls.created = cls.facade.create_snapshot({"kind": "create-snapshot"})
        assert cls.created["kind"] == "create-snapshot-result", cls.created
        cls.snapshot = cls.created["snapshot"]["snapshot"]

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_optional_capture_matches_explicit_route_and_preserves_unresolved(self):
        automatic = self.facade.route({"facts": {}})
        native = self.facade.query(
            {
                "snapshot": automatic["snapshot"],
                "request": {"kind": "route", "facts": {}},
            }
        )
        self.assertNotEqual(automatic["snapshot"], self.snapshot)
        self.assertEqual(automatic, native)
        self.assertTrue(automatic["unresolved_questions"])
        selected = {
            r["target"] for r in automatic["reading_plan"] if r["state"] == "selected"
        }
        self.assertIn("core", selected)
        self.assertIn("router", selected)

    def test_complete_explicit_facts_select_reviewed_modules(self):
        facts = {
            f"routing.{name}": {"type": "enum-set", "state": "known", "value": []}
            for name in (
                "activities",
                "workflow-profiles",
                "applications",
                "boundaries",
                "languages",
                "frameworks",
                "topics",
                "details",
            )
        }
        for name, values in {
            "activities": ["implementation", "verification"],
            "applications": ["library"],
            "languages": ["rust"],
        }.items():
            facts[f"routing.{name}"]["value"] = values
        result = self.facade.route({"facts": facts, "snapshot": self.snapshot})
        self.assertEqual(result["unresolved_questions"], [])
        self.assertTrue(
            {
                "core",
                "router",
                "workflow.implementation",
                "workflow.verification",
                "profile.application.library",
                "profile.language.rust",
            }.issubset({r["target"] for r in result["reading_plan"]})
        )
        self.assertEqual(
            result,
            self.facade.query(
                {
                    "snapshot": self.snapshot,
                    "request": {"kind": "route", "facts": facts},
                }
            ),
        )

    def test_supplied_snapshot_never_captures_ambient_authority(self):
        with patch.object(
            self.engine,
            "create_snapshot",
            side_effect=AssertionError("unexpected capture"),
        ):
            first = self.facade.read({"snapshot": self.snapshot, "target": "core"})
            second = self.facade.read(
                {"snapshot": self.snapshot, "target": "workflow.planning"}
            )
        self.assertEqual(first["snapshot"], self.snapshot)
        self.assertEqual(second["snapshot"], self.snapshot)

    def test_compact_read_preserves_text_authority_and_full_detail(self):
        full = self.facade.read(
            {
                "snapshot": self.snapshot,
                "target": "workflow.planning",
                "detail": "full",
                "include_coverage": True,
            }
        )
        compact = self.facade.read(
            {
                "snapshot": self.snapshot,
                "target": "workflow.planning",
                "include_coverage": True,
            }
        )
        self.assertEqual(full["kind"], "read-result")
        self.assertEqual(compact["kind"], "compact-read-result")
        self.assertNotIn("related", compact)
        for field in (
            "snapshot",
            "policy",
            "content",
            "requires",
            "specializes",
            "coverage",
            "next_operations",
        ):
            self.assertEqual(compact[field], full[field], field)
        self.assertGreater(len(full["related"]), 0)
        self.assertLess(len(json.dumps(compact)), len(json.dumps(full)))
        _contracts(ROOT).validate("CompactReadResult", compact)

    def test_related_matches_native_permissions_and_projection(self):
        request = {
            "target": "workflow.planning",
            "groups": ["policy-impact"],
            "direction": "outgoing",
            "transitive": False,
        }
        native = self.facade.query(
            {"snapshot": self.snapshot, "request": {"kind": "related", **request}}
        )
        focused = self.facade.related({"snapshot": self.snapshot, **request})
        self.assertEqual(focused, native)
        self.assertEqual(focused["kind"], "related-result")
        self.assertTrue(focused["relationships"])
        artifact = self.facade.related(
            {"snapshot": self.snapshot, **{**request, "target": "prompts/planning.md"}}
        )
        self.assertEqual(artifact["authoring_target"]["snapshot"], self.snapshot)
        invalid = self.facade.related(
            {"snapshot": self.snapshot, **{**request, "groups": ["invented"]}}
        )
        self.assertEqual(invalid["kind"], "rejected-result")

    def test_capture_rejection_never_advances_to_query(self):
        rejected = contract.RejectedResult.from_value(
            {
                "kind": "rejected-result",
                "code": "SNAPSHOT.UNAVAILABLE",
                "outcome": "unavailable",
                "message": "No snapshot authority",
                "details": {},
                "next_operations": [],
            }
        )
        with (
            patch.object(self.engine, "create_snapshot", return_value=rejected),
            patch.object(self.engine, "query") as query,
        ):
            result = self.facade.read({"target": "core"})
        self.assertEqual(result, rejected.as_contract())
        query.assert_not_called()

    def test_invalid_inputs_cannot_create_snapshot(self):
        with patch.object(self.engine, "create_snapshot") as capture:
            for arguments in (
                {"target": "core", "detail": "summary"},
                {"target": "core", "snapshot": {**self.snapshot, "schema_version": 99}},
                {"target": "core", "extra": True},
            ):
                result = self.facade.read(arguments)
                self.assertEqual(result["kind"], "rejected-result")
            capture.assert_not_called()


if __name__ == "__main__":
    unittest.main()
