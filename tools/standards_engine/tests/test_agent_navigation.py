from __future__ import annotations

from dataclasses import replace
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
        self.assertEqual(automatic["reading_plan"], native["reading_plan"])
        self.assertEqual(
            [q["id"] for q in automatic["unresolved_questions"]],
            [q["id"] for q in native["unresolved_questions"]],
        )
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
        native = self.facade.query(
            {"snapshot": self.snapshot, "request": {"kind": "route", "facts": facts}}
        )
        self.assertEqual(result["reading_plan"], native["reading_plan"])
        self.assertEqual(
            result["next_operations"],
            [
                {**item, "operation": item["request_kind"]}
                for item in native["next_operations"]
            ],
        )
        self.assertEqual(result["facts"], facts)

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
        self.assertEqual(
            focused,
            {
                **native,
                "next_operations": [
                    {**item, "operation": item["request_kind"]}
                    if item["operation"] == "query"
                    else item
                    for item in native["next_operations"]
                ],
            },
        )
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

    def test_focused_read_continuations_are_callable_against_exact_snapshot(self):
        from tools.standards_engine.standards_engine.mcp import tool_catalog

        catalog = {item["name"] for item in tool_catalog(ROOT)}
        native = self.facade.query(
            {
                "snapshot": self.snapshot,
                "request": {"kind": "read", "target": "workflow.planning"},
            }
        )
        self.assertTrue(
            any(item["operation"] == "query" for item in native["next_operations"])
        )
        for detail in ("compact", "full"):
            result = self.facade.read(
                {
                    "snapshot": self.snapshot,
                    "target": "workflow.planning",
                    "detail": detail,
                }
            )
            for item in result["next_operations"]:
                self.assertIn(item["operation"], catalog)
                if item["operation"] == "read":
                    self.assertEqual(item["snapshot"], self.snapshot)
                    followed = self.facade.read(
                        {"snapshot": item["snapshot"], "target": item["target"]}
                    )
                    self.assertEqual(followed["kind"], "compact-read-result", followed)
                    self.assertEqual(followed["snapshot"], self.snapshot)

    def test_vocabulary_matches_router_and_questions_are_typed(self):
        result = self.facade.routing_facts({"snapshot": self.snapshot})
        router = self.facade.query(
            {
                "snapshot": self.snapshot,
                "request": {
                    "kind": "read",
                    "target": "router",
                    "include_routing": True,
                },
            }
        )
        self.assertEqual(result["facts"], router["routing"]["facts"])
        self.assertNotIn("rules", result)
        unresolved = self.facade.route({"snapshot": self.snapshot, "facts": {}})
        definitions = {fact["id"]: fact for fact in result["facts"]}
        for question in unresolved["unresolved_questions"]:
            self.assertEqual(question["fact"], definitions[question["fact"]["id"]])
            self.assertNotIn("permitted_answers", question)
        rules = {rule["id"]: rule for rule in router["routing"]["rules"]}
        for rule in unresolved["rules"]:
            self.assertEqual(rule["when"], rules[rule["id"]]["when"])
            self.assertEqual(rule["state"], "unresolved")

    def test_boolean_nullable_set_facts_aliases_and_multiple_causes(self):
        from tools.standards_applicability.standards_applicability import (
            compile_fact_schema,
        )
        from tools.standards_analysis.standards_analysis.routing import RouteRule

        compiled = self.engine._compiled_snapshot(
            self.engine._snapshot_id(contract.SnapshotHandle.from_value(self.snapshot))
        )
        declaration = compiled.router.fact_schema.as_declaration()
        common = declaration["facts"][0]
        declaration["facts"] = [
            {
                **common,
                "id": "test.enabled",
                "type": "boolean",
                "nullable": False,
                "values": [],
                "aliases": ["test.on"],
            },
            {
                **common,
                "id": "test.optional",
                "type": "string",
                "nullable": True,
                "values": [],
                "aliases": [],
            },
            {
                **common,
                "id": "test.tags",
                "type": "enum-set",
                "nullable": False,
                "values": ["x", "y"],
                "aliases": [],
            },
        ]
        schema = compile_fact_schema(declaration)
        expressions = [
            {"operator": "equals", "fact": "test.enabled", "value": True},
            {"operator": "exists", "fact": "test.optional"},
            {"operator": "contains", "fact": "test.tags", "value": "x"},
        ]
        router = replace(
            compiled.router,
            facts=schema.definitions,
            fact_schema=schema,
            rules=tuple(
                RouteRule(f"rule.test{i}", "core", schema.compile(expression))
                for i, expression in enumerate(expressions)
            ),
        )
        with patch.object(
            self.engine,
            "_compiled_snapshot",
            return_value=replace(compiled, router=router),
        ):
            missing = self.facade.route({"snapshot": self.snapshot, "facts": {}})
            self.assertEqual(
                {q["fact"]["type"] for q in missing["unresolved_questions"]},
                {"boolean", "string", "enum-set"},
            )
            facts = {
                "test.on": {"type": "boolean", "state": "known", "value": True},
                "test.optional": {"type": "string", "state": "known", "value": None},
                "test.tags": {"type": "enum-set", "state": "known", "value": ["x"]},
            }
            selected = self.facade.route({"snapshot": self.snapshot, "facts": facts})
            self.assertEqual(selected["unresolved_questions"], [])
            self.assertIn("test.enabled", selected["facts"])
            self.assertNotIn("test.on", selected["facts"])
            self.assertEqual([r["state"] for r in selected["rules"]], ["selected"] * 3)
            core = next(r for r in selected["reading_plan"] if r["target"] == "core")
            self.assertEqual(
                len([r for r in core["reasons"] if r["kind"] == "routing-rule"]), 3
            )
            conflict = self.facade.route(
                {
                    "snapshot": self.snapshot,
                    "facts": {**facts, "test.enabled": facts["test.on"]},
                }
            )
            self.assertEqual(conflict["code"], "APPLICABILITY.INVALID")
            facts["test.on"]["value"] = False
            facts["test.tags"]["value"] = []
            negative = self.facade.route({"snapshot": self.snapshot, "facts": facts})
            self.assertNotIn("rule.test0", {r["id"] for r in negative["rules"]})
            self.assertNotIn("rule.test2", {r["id"] for r in negative["rules"]})

    def test_invalid_routing_values_do_not_become_negative_facts(self):
        for facts in (
            {"invented": {"type": "boolean", "state": "known", "value": True}},
            {
                "routing.languages": {
                    "type": "enum-set",
                    "state": "known",
                    "value": ["invented"],
                }
            },
        ):
            result = self.facade.route({"snapshot": self.snapshot, "facts": facts})
            self.assertEqual(result["code"], "APPLICABILITY.INVALID")

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
