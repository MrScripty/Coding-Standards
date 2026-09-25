"""Cold process and local stdio observations of the qualified application API.

These tests use the real transport and SQLite reader. The separate publication
suite owns the proof that approval enters a snapshot through reviewed Git state.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.standards_engine.tests import test_purpose_projection as fixture

PRIVATE, PUBLIC, ROOT = fixture.PRIVATE, fixture.PUBLIC, fixture.ROOT
from tools.standards_snapshots.standards_snapshots import SnapshotModule, CapturedContent, SnapshotFile, SnapshotPath


class PurposeTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeProjectionTest.setUpClass()
        cls.temp = tempfile.TemporaryDirectory(prefix="purpose-transport-")
        cls.root = Path(cls.temp.name)
        for relative in ("tools/standards_engine/contracts/a1-contract.schema.json",
                         "tools/standards_engine/contracts/a1-interface.toml",
                         "tools/standards_engine/contracts/generated/agent-tools.json",
                         "tools/standards_engine/contracts/examples/a1-examples.json"):
            target = cls.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        store_path = cls.root / ".standards-engine/snapshots-v1.sqlite3"
        store_path.parent.mkdir(parents=True)
        with SnapshotModule.open(store_path) as store:
            captured = store.create_snapshot(CapturedContent("isolated-transport-fixture", (
                SnapshotFile(SnapshotPath.parse(path), value)
                for path, value in fixture.PurposeProjectionTest.files.items())))
            cls.snapshot = fixture.PurposeProjectionTest.engine._snapshot_handle(captured.snapshot)
        cls.expected = fixture.PurposeProjectionTest.files["CORE-STANDARDS.md"].decode()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
        fixture.PurposeProjectionTest.tearDownClass()

    def cli(self, purpose, *arguments, value=None):
        return subprocess.run(
            [sys.executable, "-P", str(ROOT / ".agents/skills/standards-engine/scripts/invoke.py"),
             "--repo-root", str(self.root), "--purpose", purpose, *arguments],
            input=json.dumps(value) if value is not None else "", text=True,
            capture_output=True, env={**os.environ, "PYTHONPATH": str(ROOT)},
            timeout=90,
        )

    def test_two_cold_processes_preserve_exact_application_read(self):
        request = {"snapshot": self.snapshot, "target": "core", "detail": "full"}
        first = self.cli("application", "read", value=request)
        second = self.cli("application", "read", value=request)
        for result in (first, second):
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            value = json.loads(result.stdout)
            self.assertEqual(value["content"], self.expected)
            self.assertIn(PUBLIC, value["content"])
            self.assertNotIn(PRIVATE, result.stdout)
        self.assertEqual(json.loads(first.stdout), json.loads(second.stdout))
        authored = self.cli("authoring", "read", value={"snapshot": self.snapshot, "target": "provenance.fixture"})
        self.assertEqual(authored.returncode, 0, authored.stderr)
        self.assertEqual(json.loads(authored.stdout)["record"]["rationale"], PRIVATE)

    def test_cli_catalog_schema_example_and_denial_share_the_purpose(self):
        listing = self.cli("application", "--list")
        self.assertEqual(listing.returncode, 0, listing.stderr)
        self.assertEqual(set(listing.stdout.splitlines()), {"route", "read", "read_many", "related", "routing_facts", "query", "inspect", "runtime_info"})
        for option in ("--schema", "--example"):
            result = self.cli("application", option, "read")
            self.assertEqual(result.returncode, 0, result.stderr)
            for private in ("rationale", "ChangePurpose", "DecisionProvenanceRecord", PRIVATE):
                self.assertNotIn(private, result.stdout)
        denied = self.cli("application", "apply", value={})
        self.assertEqual(denied.returncode, 2)
        self.assertNotIn(PRIVATE, denied.stderr + denied.stdout)

    def test_actual_stdio_has_qualified_catalog_and_identical_result_encodings(self):
        def request(identifier, method, params):
            return {"jsonrpc": "2.0", "id": identifier, "method": method, "params": params}
        messages = [
            request(1, "initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "purpose-fixture", "version": "1"}}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            request(2, "tools/list", {}),
            request(3, "tools/call", {"name": "read", "arguments": {"snapshot": self.snapshot, "target": "core", "detail": "full"}}),
            request(4, "tools/call", {"name": "read", "arguments": {"snapshot": self.snapshot, "target": "provenance.fixture"}}),
            request(5, "tools/call", {"name": "apply", "arguments": {}}),
        ]
        process = subprocess.run(
            [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
             "--repo-root", str(self.root), "--purpose", "application", "--advanced"],
            input="".join(json.dumps(value) + "\n" for value in messages), text=True,
            capture_output=True, env={**os.environ, "PYTHONPATH": str(ROOT)}, timeout=120,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        self.assertNotIn(PRIVATE, process.stdout)
        values = {value["id"]: value for value in map(json.loads, process.stdout.splitlines())}
        self.assertEqual({tool["name"] for tool in values[2]["result"]["tools"]}, {"route", "read", "read_many", "related", "routing_facts", "query", "inspect", "runtime_info"})
        allowed = values[3]["result"]
        self.assertFalse(allowed["isError"])
        self.assertEqual(allowed["structuredContent"]["content"], self.expected)
        self.assertEqual(json.loads(allowed["content"][0]["text"]), allowed["structuredContent"])
        self.assertTrue(values[4]["result"]["isError"])
        self.assertEqual(values[4]["result"]["structuredContent"]["code"], "APPLICATION.CONTENT_UNAVAILABLE")
        self.assertIn("error", values[5])


    def test_default_capture_reads_accepted_main_instead_of_unpublished_head(self):
        from tools.standards_engine.standards_engine import AgentToolFacade
        with tempfile.TemporaryDirectory(prefix="accepted-purpose-") as temporary:
            root = Path(temporary)
            for relative, content in fixture.PurposeProjectionTest.files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            for relative in ("tools/standards_engine/contracts/a1-contract.schema.json",
                             "tools/standards_engine/contracts/a1-interface.toml"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            def git(*arguments):
                return subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                                       "user.email=fixture@example.invalid", *arguments],
                                      cwd=root, check=True, capture_output=True)
            git("init", "-b", "main")
            git("add", "--all")
            git("commit", "-m", "test: accepted application content")
            git("checkout", "-b", "unpublished")
            core = root / "CORE-STANDARDS.md"
            core.write_text(core.read_text() + "\nUNPUBLISHED_CONTENT_MARKER_15839\n")
            git("add", "--", "CORE-STANDARDS.md")
            git("commit", "-m", "test: leave unreviewed content on a draft branch")
            with AgentToolFacade.open_repository(root, purpose="application") as facade:
                result = facade.read({"target": "core"})
            self.assertEqual(result["kind"], "application-read-result", result)
            self.assertEqual(result["content"], self.expected)
            self.assertNotIn("UNPUBLISHED_CONTENT_MARKER_15839", json.dumps(result))
