"""Grouped reads through the actual purpose projection, SQLite and transports."""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine, render_text
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine import agent_navigation
from tools.standards_engine.standards_engine.context_projection import ApplicationView
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.mcp import tool_catalog
from tools.standards_engine.tests import test_purpose_projection as fixture
from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotId, SnapshotPath

ROOT = Path(__file__).resolve().parents[3]


class ReadManyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeProjectionTest.setUpClass()
        cls.files = fixture.PurposeProjectionTest.files
        cls.reference = fixture.PurposeProjectionTest.reference
        cls.interface = AgentToolFacade.load_interface(ROOT)

    @classmethod
    def tearDownClass(cls):
        fixture.PurposeProjectionTest.tearDownClass()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="read-many-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in ("a1-contract.schema.json", "a1-interface.toml", "generated/agent-tools.json", "examples/a1-examples.json"):
            path = Path("tools/standards_engine/contracts") / relative
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, destination)
        self.store = self.root / ".standards-engine/snapshots-v1.sqlite3"
        self.cache = CompiledSnapshotCache(self.root, "application")
        self.addCleanup(self.cache.close)
        self.app_engine = StandardsEngine.open_repository(self.root, purpose="application", compiled_cache=self.cache)
        self.addCleanup(self.app_engine.close)
        capture = CapturedContent("read-many-fixture", (
            SnapshotFile(SnapshotPath.parse(path), data) for path, data in self.files.items()
        ))
        created = self.app_engine._snapshots.create_snapshot(capture)
        self.snapshot = self.app_engine._snapshot_handle(created.snapshot)
        self.app = AgentToolFacade(self.app_engine, self.interface)
        self.author_engine = StandardsEngine.open_repository(self.root, purpose="authoring")
        self.addCleanup(self.author_engine.close)
        self.author = AgentToolFacade(self.author_engine, self.interface)

    def call(self, facade=None, items=None, **extra):
        return (facade or self.app).read_many({"snapshot": self.snapshot,
            "items": items if items is not None else [{"target": "core"}, {"target": "router", "detail": "full"}], **extra})

    def test_application_results_equal_independent_reads_with_one_durable_load(self):
        items = [{"target": "core"}, {"target": self.reference, "detail": "full"}, {"target": "router"}]
        expected = [self.app.read({"snapshot": self.snapshot, **item}) for item in items]
        with patch.object(self.app_engine._snapshots, "load_content", wraps=self.app_engine._snapshots.load_content) as load:
            result = self.call(items=items)
        self.assertEqual(result["kind"], "application-read-many-result", result)
        self.assertEqual(result["items"], expected)
        self.assertEqual(result["snapshot"], self.snapshot)
        self.assertEqual(load.call_count, 1)
        self.assertNotIn(fixture.PRIVATE, json.dumps(result))
        result["items"][0]["content"] = "caller mutation"
        self.assertEqual(self.call(items=items)["items"], expected)

    def test_authoring_preserves_all_single_read_result_variants(self):
        items = [{"target": "core"}, {"target": "core", "detail": "full", "include_coverage": True},
                 {"target": "router", "include_routing": True}, {"target": "provenance.fixture"},
                 {"target": "prompts/planning.md"}, {"target": "navigation-indexes"}]
        expected = [self.author.read({"snapshot": self.snapshot, **item}) for item in items]
        with patch.object(self.author_engine._snapshots, "load_content", wraps=self.author_engine._snapshots.load_content) as load:
            result = self.call(self.author, items)
        self.assertEqual(result["kind"], "read-many-result", result)
        self.assertEqual(result["items"], expected)
        self.assertEqual(load.call_count, 1)
        self.assertEqual(result["items"][3]["record"]["rationale"], fixture.PRIVATE)
        self.assertEqual(json.loads(render_text(result)), result)

    def test_empty_duplicate_oversized_missing_snapshot_and_privileged_requests_reject_before_load(self):
        for value in [
            {"snapshot": self.snapshot, "items": []},
            {"snapshot": self.snapshot, "items": [{"target": "core"}] * 2},
            {"snapshot": self.snapshot, "items": [{"target": f"fixture.{i}"} for i in range(33)]},
            {"items": [{"target": "core"}]},
            {"snapshot": self.snapshot, "items": [{"target": "core", "purpose": "authoring"}]},
            {"snapshot": self.snapshot, "items": [{"target": "core", "include_coverage": True}]},
            {"snapshot": self.snapshot, "items": [{"target": "core", "snapshot": self.snapshot}]},
        ]:
            with self.subTest(value=value), patch.object(self.app_engine, "_compiled_snapshot", side_effect=AssertionError("unexpected load")):
                result = self.app.read_many(value)
                self.assertEqual(result["code"], "APPLICATION.INPUT_INVALID", result)
                self.assertNotIn("items", result)

    def test_unknown_or_private_item_rejects_whole_set_without_partial_data(self):
        for target in ("does.not.exist", "provenance.fixture"):
            result = self.call(items=[{"target": "core"}, {"target": target}])
            self.assertEqual(result["code"], "APPLICATION.CONTENT_UNAVAILABLE", result)
            self.assertNotIn(fixture.PUBLIC, json.dumps(result))
            self.assertNotIn(fixture.PRIVATE, json.dumps(result))
            self.assertNotIn("items", result)
        result = self.call(self.author, [{"target": "core"}, {"target": "does.not.exist"}])
        self.assertEqual(result["kind"], "rejected-result", result)
        self.assertNotIn("items", result)

    def test_native_application_dispatch_cannot_admit_authoring_items(self):
        call = c.ReadManyCall.from_value({"snapshot": self.snapshot, "items": [{"target": "core", "include_routing": True}]})
        result = self.app_engine.read_many(call).as_contract()
        self.assertEqual(result["code"], "APPLICATION.INPUT_INVALID", result)

    def test_exact_serialized_budget_in_both_purposes(self):
        for facade in (self.app, self.author):
            expected = self.call(facade)
            size = len(json.dumps(expected).encode("utf-8"))
            with patch.object(agent_navigation, "READ_MANY_RESULT_BYTES", size):
                self.assertEqual(self.call(facade), expected)
            with patch.object(agent_navigation, "READ_MANY_RESULT_BYTES", size - 1):
                rejected = self.call(facade)
                self.assertIn(rejected["code"], {"READ_MANY.RESULT_LIMIT", "APPLICATION.RESULT_LIMIT"})
                self.assertNotIn("items", rejected)

    def test_lifecycle_change_between_items_and_after_last_item_rejects(self):
        for at in (1, 2):
            snapshot_id = SnapshotId(self.snapshot["id"])
            original = ApplicationView.read
            count = 0
            def read(view, *args, **kwargs):
                nonlocal count
                value = original(view, *args, **kwargs)
                count += 1
                if count == at:
                    self.app_engine._snapshots.delete_snapshot(snapshot_id)
                return value
            with patch.object(ApplicationView, "read", read):
                result = self.call()
            self.assertEqual(result["kind"], "application-rejected-result", result)
            self.assertNotIn("items", result)
            self.app_engine._snapshots.undelete_snapshot(snapshot_id)

    def test_each_new_operation_rechecks_integrity_even_with_warm_cache(self):
        self.call()
        with closing(sqlite3.connect(self.store)) as connection, connection:
            sql = connection.execute("SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'").fetchone()[0]
            connection.execute("DROP TRIGGER content_files_no_update")
            data = b"corrupt"
            connection.execute("UPDATE content_files SET raw_bytes=?,byte_length=?,sha256=? WHERE logical_path=?",
                               (data, len(data), hashlib.sha256(data).hexdigest(), "CORE-STANDARDS.md"))
            connection.execute(sql)
        result = self.call()
        self.assertEqual(result["kind"], "application-rejected-result", result)
        self.assertNotIn("items", result)
        self.assertEqual(self.cache.statistics["hits"], 0)

    def test_explicit_snapshot_never_captures_main_and_survives_reopening(self):
        with patch.object(self.app_engine, "_capture_snapshot", side_effect=AssertionError("unexpected capture")):
            expected = self.call()
        with StandardsEngine.open_repository(self.root, purpose="application") as engine:
            reopened = AgentToolFacade(engine, self.interface)
            self.assertEqual(self.call(reopened), expected)

    def test_32_item_boundary_and_order(self):
        # The authoring corpus owns enough actual identities to exercise the cap.
        compiled = self.author_engine._compiled_snapshot(SnapshotId(self.snapshot["id"]))
        items = [{"target": module.module_id} for module in compiled.corpus.modules[:32]]
        result = self.call(self.author, items)
        self.assertEqual(result["kind"], "read-many-result", result)
        self.assertEqual(len(result["items"]), 32)
        self.assertEqual([value["policy"]["handle"]["child_id"] for value in result["items"]], [item["target"] for item in items])

    def test_schema_discovery_is_purpose_specific(self):
        for purpose in ("application", "authoring"):
            catalog = {item["name"]: item for item in tool_catalog(self.root, purpose=purpose, interface=self.interface)}
            tool = catalog["read_many"]
            self.assertTrue(tool["annotations"]["readOnlyHint"])
            if purpose == "application":
                encoded = json.dumps(tool)
                for hidden in ("ChangePurpose", "DecisionProvenanceRecord", "rationale", "include_coverage"):
                    self.assertNotIn(hidden, encoded)

    def test_real_cli_and_stdio_return_identical_complete_domain_values(self):
        arguments = {"snapshot": self.snapshot, "items": [{"target": "core"}, {"target": "router", "detail": "full"}]}
        expected = self.call()
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        cli = subprocess.run([sys.executable, "-P", str(ROOT / ".agents/skills/standards-engine/scripts/invoke.py"),
            "--repo-root", str(self.root), "--purpose", "application", "read_many"],
            input=json.dumps(arguments), text=True, capture_output=True, env=env, timeout=60)
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertEqual(json.loads(cli.stdout), expected)
        def message(i, method, params):
            return {"jsonrpc": "2.0", "id": i, "method": method, "params": params}
        messages = [message(1, "initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "multi-read-fixture", "version": "1"}}),
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    message(2, "tools/call", {"name": "read_many", "arguments": arguments}),
                    message(3, "tools/call", {"name": "read_many", "arguments": {**arguments, "items": [{"target": "core"}, {"target": "provenance.fixture"}]}})]
        command = [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", str(self.root), "--purpose", "application"]
        for _ in range(2):
            response = subprocess.run(command, input="".join(json.dumps(m) + "\n" for m in messages), text=True, capture_output=True, env=env, timeout=60)
            self.assertEqual(response.returncode, 0, response.stderr)
            self.assertNotIn(fixture.PRIVATE, response.stdout)
            values = {value["id"]: value for value in map(json.loads, response.stdout.splitlines())}
            returned = values[2]["result"]
            self.assertFalse(returned["isError"])
            self.assertEqual(returned["structuredContent"], expected)
            self.assertEqual(json.loads(returned["content"][0]["text"]), expected)
            self.assertTrue(values[3]["result"]["isError"])
            self.assertNotIn("items", values[3]["result"]["structuredContent"])
