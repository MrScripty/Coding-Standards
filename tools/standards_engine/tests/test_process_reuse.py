"""Real per-call stores with bounded pure compilation and installed API reuse."""
from __future__ import annotations

from copy import deepcopy
from contextlib import closing
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import os
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_contracts.standards_contracts import ContractError
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import engine as engine_module
from tools.standards_engine.standards_engine import tools as tool_module
from tools.standards_engine.standards_engine.compiled_cache import (
    CompiledSnapshotCache, _retained_size,
)
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_engine.tests.test_agent_workflow import (
    prepare_repository, reference_change,
)
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotId

ROOT = Path(__file__).resolve().parents[3]


class ProcessReuseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix="process-reuse-fixture-")
        cls.root = Path(cls.fixture.name) / "repository"
        prepare_repository(cls.root)
        cls.interface = AgentToolFacade.load_interface(cls.root)
        with AgentToolFacade.open_repository(
            cls.root, purpose="authoring", interface=cls.interface,
        ) as facade:
            result = facade.create_snapshot({"kind": "create-snapshot"})
            assert result["kind"] == "create-snapshot-result", result
            snapshot = SnapshotId(result["snapshot"]["snapshot"]["id"])
            cls.original_snapshot = result["snapshot"]["snapshot"]
            cls.capture = facade._engine._snapshots.load_content(snapshot)

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="process-reuse-store-")
        self.addCleanup(self.temporary.cleanup)
        self.store = Path(self.temporary.name) / "store.sqlite3"
        self.cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(self.cache.close)
        self.engine = self.open_engine()
        self.addCleanup(lambda: self.engine.close())
        summary = self.engine._snapshots.create_snapshot(self.capture)
        self.snapshot = self.engine._snapshot_handle(summary.snapshot)
        self.facade = AgentToolFacade(self.engine, self.interface)

    def open_engine(self, cache=None):
        return StandardsEngine.open_repository(
            self.root, purpose="authoring", store_path=self.store,
            compiled_cache=self.cache if cache is None else cache,
            execution_context=tool_module.AnalysisExecutionContext(
                tool_module.LocalAlwaysAllowAuthorizer(self.root)
            ),
        )

    def read(self, **options):
        return self.facade.read({"snapshot": self.snapshot, "target": "core", **options})

    def test_reuse_still_verifies_all_durable_content_each_call(self):
        with (
            patch.object(self.engine._snapshots, "load_content", wraps=self.engine._snapshots.load_content) as load,
            patch.object(engine_module, "compile_policy_impact", wraps=engine_module.compile_policy_impact) as compile,
        ):
            first = self.read()
            second = self.read()
        self.assertEqual(first, second)
        self.assertEqual(load.call_count, 2)
        self.assertEqual(compile.call_count, 1)
        self.assertEqual(self.cache.statistics["hits"], 1)
        self.assertGreater(self.cache.statistics["accounted_bytes"], 0)
        self.assertLessEqual(self.cache.statistics["accounted_bytes"], 32 * 1024 * 1024)

    def test_closing_borrower_preserves_cache_and_reopens_real_store(self):
        first = self.read()
        self.engine.close()
        self.engine = self.open_engine()
        self.facade = AgentToolFacade(self.engine, self.interface)
        with patch.object(engine_module, "compile_policy_impact", wraps=engine_module.compile_policy_impact) as compile:
            second = self.read()
        self.assertEqual(first, second)
        compile.assert_not_called()
        self.assertEqual(self.cache.statistics["entries"], 1)

    def test_quarantine_and_purge_override_warm_compilation(self):
        self.read()
        snapshot = SnapshotId(self.snapshot["id"])
        self.engine._snapshots.delete_snapshot(snapshot)
        quarantined = self.read()
        self.assertEqual(quarantined["kind"], "rejected-result", quarantined)
        self.assertEqual(quarantined["outcome"], "unavailable")
        deadline = self.engine._snapshots.snapshot(snapshot, include_quarantined=True).purge_deadline
        with patch.object(self.engine._snapshots, "_now", return_value=deadline + 1):
            purged = self.read()
        self.assertEqual(purged["kind"], "rejected-result", purged)
        self.assertEqual(self.cache.statistics["hits"], 0)

    def test_corruption_is_observed_before_cache_lookup(self):
        self.read()
        # Deliberately corrupt this disposable store, then restore its exact DDL.
        with closing(sqlite3.connect(self.store)) as connection, connection:
            trigger = connection.execute("SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'").fetchone()[0]
            connection.execute("DROP TRIGGER content_files_no_update")
            connection.execute(
                "UPDATE content_files SET raw_bytes=?, byte_length=?, sha256=? WHERE logical_path=?",
                (b"corrupt", 7, hashlib.sha256(b"corrupt").hexdigest(), "CORE-STANDARDS.md"),
            )
            connection.execute(trigger)
        rejected = self.read()
        self.assertEqual(rejected["code"], "SNAPSHOT.CONTENT_ID_MISMATCH", rejected)
        self.assertEqual(self.cache.statistics["hits"], 0)

    def test_store_replacement_cannot_be_answered_from_cache(self):
        self.read()
        self.engine.close()
        # Closed fixture store has no active borrowers or sidecar writes.
        self.store.rename(self.store.with_suffix(".retained"))
        self.engine = self.open_engine()
        self.facade = AgentToolFacade(self.engine, self.interface)
        missing = self.read()
        self.assertEqual(missing["kind"], "rejected-result", missing)
        self.assertEqual(missing["outcome"], "unavailable")
        self.assertEqual(self.cache.statistics["hits"], 0)

    def test_new_process_owner_cold_rebuild_matches_retained_result(self):
        first = self.read()
        self.cache.close()
        self.assertEqual(self.cache.statistics["entries"], 0)
        self.engine.close()
        self.cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(self.cache.close)
        self.engine = self.open_engine()
        self.facade = AgentToolFacade(self.engine, self.interface)
        second = self.read()
        self.assertEqual(first, second)
        self.assertEqual(self.cache.statistics["misses"], 1)

    def test_responses_are_independent_of_retained_compilation(self):
        first = self.read(detail="full")
        expected = deepcopy(first)
        first["requires"].append("invented")
        first["related"].clear()
        first["next_operations"].clear()
        self.assertEqual(self.read(detail="full"), expected)

    def test_bounds_eviction_and_disabled_retention_preserve_results(self):
        expected = self.read()
        byte_pressure = self.cache.statistics["accounted_bytes"] * 3 // 2
        for entries, budget in (
            (0, 32 * 1024 * 1024), (2, 1), (1, 32 * 1024 * 1024),
            (4, byte_pressure),
        ):
            with self.subTest(entries=entries, budget=budget):
                cache = CompiledSnapshotCache(self.root, "authoring", max_entries=entries, max_bytes=budget)
                try:
                    with self.open_engine(cache) as engine:
                        facade = AgentToolFacade(engine, self.interface)
                        self.assertEqual(facade.read({"snapshot": self.snapshot, "target": "core"}), expected)
                        different = CapturedContent("different-source-revision", self.capture.files)
                        other = engine._snapshots.create_snapshot(different)
                        facade.read({"snapshot": engine._snapshot_handle(other.snapshot), "target": "core"})
                        self.assertEqual(facade.read({"snapshot": self.snapshot, "target": "core"}), expected)
                    self.assertLessEqual(cache.statistics["entries"], entries)
                    self.assertLessEqual(cache.statistics["accounted_bytes"], budget)
                    if entries in (1, 4):
                        self.assertEqual(cache.statistics["entries"], 1)
                        self.assertEqual(cache.statistics["evictions"], 2)
                    else:
                        self.assertEqual(cache.statistics["uncached"], 3)
                finally:
                    cache.close()

    def test_unknown_size_and_invalid_bounds_have_explicit_dispositions(self):
        from collections import UserDict
        self.assertIsNone(_retained_size(object(), 1024))
        self.assertIsNone(_retained_size(UserDict({"owned": b"payload"}), 1024))
        for value in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                CompiledSnapshotCache(self.root, "authoring", max_bytes=value)

    def test_stateful_compiler_is_computed_without_retaining_hidden_state(self):
        calls = []
        def compiled(source):
            calls.append(source)
            return StandardsEngine._compile(source)
        first = self.cache.compile_verified(self.capture, compiled)
        second = self.cache.compile_verified(self.capture, compiled)
        self.assertEqual(first.semantic_signature(), second.semantic_signature())
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.cache.statistics["entries"], 0)

    def test_real_stdio_restarts_read_the_same_retained_snapshot(self):
        messages = [
            request("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                                   "clientInfo": {"name": "cache-restart-fixture", "version": "1"}}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            request("tools/call", {"name": "read", "arguments": {"snapshot": self.original_snapshot, "target": "core"}}, identifier=2),
            request("tools/call", {"name": "read", "arguments": {"snapshot": self.original_snapshot, "target": "core"}}, identifier=3),
        ]
        observed = []
        for _ in range(2):
            completed = subprocess.run(
                [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
                 "--repo-root", str(self.root), "--purpose", "authoring"],
                input="".join(json.dumps(value) + "\n" for value in messages), text=True,
                capture_output=True, check=True, timeout=60, cwd=self.temporary.name,
                env={**os.environ, "PYTHONPATH": str(ROOT)},
            )
            responses = [json.loads(line) for line in completed.stdout.splitlines()]
            reads = [row["result"] for row in responses if row["id"] in (2, 3)]
            self.assertEqual(len(reads), 2)
            self.assertFalse(any(row["isError"] for row in reads), reads)
            self.assertEqual(reads[0], reads[1])
            observed.append(reads[0])
        self.assertEqual(observed[0], observed[1])
        self.assertEqual(observed[0]["structuredContent"]["snapshot"], self.original_snapshot)

    def test_repository_and_purpose_are_fixed_before_opening_store(self):
        for root, purpose in ((self.root.parent, "authoring"), (self.root, "application")):
            with self.assertRaisesRegex(ValueError, "another repository or purpose"):
                StandardsEngine.open_repository(root, purpose=purpose, compiled_cache=self.cache)

    def test_compilation_failure_is_not_cached(self):
        with patch.object(engine_module, "compile_policy_impact", side_effect=RuntimeError("failed compiler")):
            with self.assertRaisesRegex(RuntimeError, "failed compiler"):
                self.read()
        self.assertEqual(self.cache.statistics["entries"], 0)
        self.assertEqual(self.read()["kind"], "compact-read-result")
        self.assertEqual(self.cache.statistics["misses"], 2)

    def test_warm_cache_preserves_independent_capture_passes(self):
        self.read()
        with patch.object(engine_module, "compile_policy_impact", wraps=engine_module.compile_policy_impact) as compile:
            captured = self.facade.create_snapshot({"kind": "create-snapshot"})
        self.assertEqual(captured["kind"], "create-snapshot-result", captured)
        self.assertEqual(compile.call_count, 2)

    def test_authorization_is_fresh_after_warming_proposal_base(self):
        self.read()
        change = reference_change(self.root, "warm-authority")
        proposed = self.facade.propose({"snapshot": self.snapshot, "change_set": change})
        self.assertEqual(proposed.get("status"), "complete", proposed)
        self.assertGreater(self.cache.statistics["hits"], 0)
        authorize = self.engine._execution_context.authorization.authorize
        calls = []
        def quarantine(request):
            calls.append(request)
            self.engine._snapshots.delete_snapshot(SnapshotId(self.snapshot["id"]))
            return authorize(request)
        # A review's current authority/lifecycle work remains outside the cache.
        from tools.standards_engine.tests.test_agent_workflow import decisions
        with patch.object(self.engine._execution_context.authorization, "authorize", side_effect=quarantine):
            reviewed = self.facade.review({"context": proposed["context"], "decisions": decisions(self.root)})
        self.assertTrue(calls)
        self.assertNotEqual(reviewed.get("status"), "ready", reviewed)


class InstalledInterfaceReuseTest(unittest.TestCase):
    def test_one_interface_compile_per_server_and_fresh_call_validation(self):
        with patch.object(tool_module, "_contracts", wraps=tool_module._contracts) as compiled:
            server = MCPServer(ROOT, purpose="authoring")
            self.addCleanup(server.close)
            initialize(server)
            for _ in range(2):
                result = server.dispatch(request("tools/call", {"name": "read", "arguments": {"extra": True}}))["result"]
                self.assertTrue(result["isError"])
                self.assertEqual(result["structuredContent"]["code"], "INTERFACE.INVALID_ARGUMENTS")
            self.assertEqual(compiled.call_count, 1)

    def test_catalog_and_runtime_share_the_installed_interface(self):
        with tempfile.TemporaryDirectory(prefix="interface-fixed-") as tmp:
            root = Path(tmp) / "repository"
            prepare_repository(root)
            server = MCPServer(root, purpose="application")
            self.addCleanup(server.close)
            initialize(server)
            # The running installation is fixed. A new startup must inspect new bytes.
            schema = root / tool_module.INTERFACE_SCHEMA
            schema.write_text("{}")
            returned = server.dispatch(request("tools/list"))["result"]["tools"]
            returned.clear()
            self.assertTrue(server.dispatch(request("tools/list"))["result"]["tools"])
            bad = server.dispatch(request("tools/call", {"name": "read", "arguments": {"extra": True}}))["result"]
            self.assertEqual(bad["structuredContent"]["code"], "APPLICATION.INPUT_INVALID")
            self.assertNotIn("propose", server.names)
            with self.assertRaises(ContractError):
                MCPServer(root, purpose="application")

    def test_stream_eof_and_write_failure_release_process_resources(self):
        for failing in (False, True):
            server = MCPServer(ROOT, purpose="authoring")
            if failing:
                class FailedOutput(io.StringIO):
                    def write(self, value):
                        raise OSError("closed output")
                with self.assertRaises(OSError):
                    serve(server, io.StringIO(json.dumps(request("ping")) + "\n"), FailedOutput())
            else:
                serve(server, io.StringIO(""), io.StringIO())
            self.assertIsNone(server._interface)
            self.assertEqual(server._compiled_cache.statistics["entries"], 0)
            self.assertEqual(server.dispatch(request("ping"))["error"]["code"], -32000)

    def test_each_tool_call_opens_and_closes_its_own_facade(self):
        server = MCPServer(ROOT, purpose="application")
        self.addCleanup(server.close)
        initialize(server)
        opened = AgentToolFacade.open_repository
        with patch.object(AgentToolFacade, "open_repository", wraps=opened) as calls:
            for _ in range(2):
                value = server.dispatch(request("tools/call", {"name": "read", "arguments": {"extra": True}}))
                self.assertTrue(value["result"]["isError"])
        self.assertEqual(calls.call_count, 2)
        for call in calls.call_args_list:
            self.assertIs(call.kwargs["interface"], server._interface)
            self.assertIs(call.kwargs["compiled_cache"], server._compiled_cache)

    def test_main_advancement_and_cold_historical_read_use_exact_captures(self):
        from tools.standards_verifier.standards_verifier import suite_input_projection_bytes
        with tempfile.TemporaryDirectory(prefix="cache-main-advance-") as tmp:
            root = Path(tmp) / "repository"
            prepare_repository(root)
            for name, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid"), ("commit.gpgsign", "false")):
                subprocess.run(["git", "-C", str(root), "config", name, value], check=True)
            interface = AgentToolFacade.load_interface(root)
            cache = CompiledSnapshotCache(root, "authoring")
            try:
                with AgentToolFacade.open_repository(root, purpose="authoring", interface=interface, compiled_cache=cache) as facade:
                    first = facade.read({"target": "core"})
                    self.assertEqual(first["kind"], "compact-read-result", first)
                    core = root / "CORE-STANDARDS.md"
                    core.write_text(core.read_text() + "\n<!-- New accepted fixture revision. -->\n")
                    manifest = root / "evaluation/standards-effectiveness/generated/suite-inputs.json"
                    manifest.write_bytes(suite_input_projection_bytes(root))
                    subprocess.run(["git", "-C", str(root), "add", "CORE-STANDARDS.md", str(manifest.relative_to(root))], check=True)
                    subprocess.run(["git", "-C", str(root), "commit", "--quiet", "-m", "fixture: advance accepted main"], check=True)
                    with patch.object(engine_module, "compile_policy_impact", wraps=engine_module.compile_policy_impact) as compile:
                        captured = facade.create_snapshot({"kind": "create-snapshot"})
                    self.assertEqual(captured["kind"], "create-snapshot-result", captured)
                    self.assertEqual(compile.call_count, 2)
                    newer = facade.read({"snapshot": captured["snapshot"]["snapshot"], "target": "core"})
                    self.assertNotEqual(first["content"], newer["content"])
                    self.assertEqual(facade.read({"snapshot": first["snapshot"], "target": "core"}), first)
            finally:
                cache.close()
            # Cold code has no cache and the working-tree source is unavailable.
            (root / "CORE-STANDARDS.md").unlink()
            with AgentToolFacade.open_repository(root, purpose="authoring", interface=interface) as cold:
                self.assertEqual(cold.read({"snapshot": first["snapshot"], "target": "core"}), first)

    def test_existing_publication_scenario_with_warm_purpose_isolated_caches(self):
        # Reuse the unchanged assertions, not a second approximate workflow.
        from tools.standards_engine.tests.test_supporting_workflow import SupportingWorkflowTest
        case = SupportingWorkflowTest("test_coordinated_publication_and_provenance_only_revision")
        SupportingWorkflowTest.setUpClass()
        caches = []
        try:
            for name, purpose in (("author", "authoring"), ("app", "application")):
                getattr(case, name).close()
                cache = CompiledSnapshotCache(case.root, purpose)
                caches.append(cache)
                setattr(SupportingWorkflowTest, name, AgentToolFacade.open_repository(
                    case.root, purpose=purpose, compiled_cache=cache,
                ))
            case.test_coordinated_publication_and_provenance_only_revision()
            self.assertTrue(all(cache.statistics["hits"] > 0 for cache in caches))
        finally:
            SupportingWorkflowTest.tearDownClass()
            for cache in caches:
                cache.close()
