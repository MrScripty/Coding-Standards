"""Exact draft retention preserves live authority and independent cold replay."""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import logical_authoring as logical
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer
from tools.standards_engine.tests.test_agent_workflow import (
    decisions, evidence, prepare_repository, reference_change,
)
from tools.standards_engine.tests.test_mcp import request
from tools.standards_snapshots.standards_snapshots import SnapshotId

ROOT = Path(__file__).resolve().parents[3]


class ProposalReuseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix="proposal-cache-fixture-")
        cls.root = Path(cls.fixture.name) / "repository"
        prepare_repository(cls.root)
        cls.interface = AgentToolFacade.load_interface(cls.root)
        with AgentToolFacade.open_repository(
            cls.root, purpose="authoring", interface=cls.interface,
        ) as facade:
            captured = facade.create_snapshot({"kind": "create-snapshot"})
            assert captured["kind"] == "create-snapshot-result", captured
            cls.snapshot = captured["snapshot"]["snapshot"]
            cls.first = facade.propose({
                "snapshot": cls.snapshot,
                "change_set": reference_change(cls.root, "projection-cache"),
            })
            assert cls.first["status"] == "complete", cls.first
            cls.latest = facade.revise({
                "context": cls.first["context"],
                "change_set": reference_change(cls.root, "projection-cache", revision=True),
            })
            assert cls.latest["status"] == "complete", cls.latest
            change = reference_change(cls.root, "projection-normative")
            change["edits"][0]["standard"].update(
                id="topic.projection-normative", role="topic", level="MUST",
            )
            cls.normative = facade.propose({"snapshot": cls.snapshot, "change_set": change})
            assert cls.normative["status"] == "needs-action", cls.normative
        cls.seed = cls.root / ".standards-engine/snapshots-v1.sqlite3"
        cls.target = "reference.testing.projection-cache"

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="proposal-cache-store-")
        self.addCleanup(self.temporary.cleanup)
        self.store = Path(self.temporary.name) / "test.sqlite3"
        with closing(sqlite3.connect(self.seed)) as source:
            with closing(sqlite3.connect(self.store)) as destination:
                source.backup(destination)
        self.cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(self.cache.close)
        self.engine = self.open_engine()
        self.addCleanup(lambda: self.engine.close())
        self.facade = AgentToolFacade(self.engine, self.interface)

    def open_engine(self, cache=None):
        return StandardsEngine.open_repository(
            self.root, store_path=self.store, purpose="authoring",
            compiled_cache=self.cache if cache is None else cache,
            execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(self.root)),
        )

    def query(self, selection=None):
        return self.facade.query_proposal({
            "revision": (selection or self.latest)["revision"],
            "request": {"kind": "read", "target": self.target},
        })

    def test_repeated_read_validates_base_and_revision_without_replaying_history(self):
        with (
            patch.object(self.engine._snapshots, "load_content", wraps=self.engine._snapshots.load_content) as load,
            patch.object(self.engine._authoring, "read_revision", wraps=self.engine._authoring.read_revision) as revision,
            patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh,
        ):
            first = self.query()
            self.assertEqual(first["kind"], "proposal-read-result", first)
            self.assertEqual(refresh.call_count, 2)
            refresh.reset_mock()
            self.assertEqual(self.query(), first)
            self.assertEqual(refresh.call_count, 0)
            self.assertEqual(load.call_count, 2)
            self.assertEqual(revision.call_count, 2)
        self.assertEqual(self.cache.statistics["entries"], 2)

    def test_status_retains_fresh_evaluation_on_each_hit(self):
        self.query()
        with (
            patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh,
            patch.object(self.engine, "_evaluate", wraps=self.engine._evaluate) as evaluate,
        ):
            first = self.facade.workflow_status({"context": self.latest["context"]})
            second = self.facade.workflow_status({"context": self.latest["context"]})
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "complete", first)
        refresh.assert_not_called()
        self.assertEqual(evaluate.call_count, 2)

    def successor_change(self):
        change = reference_change(self.root, "projection-cache", revision=True)
        change["edits"][0]["standard"]["body"] += "Incremental successor.\n"
        return change

    def test_native_revision_uses_warm_exact_predecessor_without_preflight_replay(self):
        old = self.query()
        with (
            patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh,
            patch.object(self.engine._snapshots, "load_content", wraps=self.engine._snapshots.load_content) as load,
            patch.object(self.engine._authoring, "read_revision", wraps=self.engine._authoring.read_revision) as read,
            patch.object(logical.LogicalAuthoringCompiler, "_apply_edit", autospec=True,
                         side_effect=logical.LogicalAuthoringCompiler._apply_edit) as edit,
        ):
            revised = self.facade.revise_proposal({
                "kind": "revise-proposal",
                "expected_revision": self.latest["revision"], "change_set": self.successor_change(),
            })
        self.assertEqual(revised["kind"], "revise-proposal-result", revised)
        self.assertEqual(refresh.call_count, 1)
        self.assertEqual(edit.call_count, 1)
        self.assertGreaterEqual(read.call_count, 1)
        self.assertEqual(load.call_count, 1)
        self.assertIn("Incremental successor.", self.query(revised)["content"])
        self.assertEqual(self.query(), old)
        self.assertEqual(self.facade.workflow_status({"context": self.latest["context"]})["status"], "stale")

    def test_native_revision_with_a_new_cache_reconstructs_the_complete_program(self):
        self.query()
        cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(cache.close)
        with self.open_engine(cache) as engine:
            facade = AgentToolFacade(engine, self.interface)
            with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
                revised = facade.revise_proposal({
                    "kind": "revise-proposal",
                    "expected_revision": self.latest["revision"], "change_set": self.successor_change(),
                })
            self.assertEqual(revised["kind"], "revise-proposal-result", revised)
            self.assertEqual(refresh.call_count, 3)

    def test_evicted_predecessor_selects_full_replay_without_changing_the_result(self):
        cache = CompiledSnapshotCache(self.root, "authoring", max_entries=1)
        self.addCleanup(cache.close)
        with self.open_engine(cache) as engine:
            facade = AgentToolFacade(engine, self.interface)
            warm = facade.query_proposal({
                "revision": self.latest["revision"], "request": {"kind": "read", "target": self.target},
            })
            self.assertEqual(warm["kind"], "proposal-read-result", warm)
            with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
                revised = facade.revise_proposal({
                    "kind": "revise-proposal",
                    "expected_revision": self.latest["revision"], "change_set": self.successor_change(),
                })
            self.assertEqual(revised["kind"], "revise-proposal-result", revised)
            # Fresh original-base compilation occupies the sole slot before
            # successor construction; the draft was therefore evicted.
            self.assertEqual(refresh.call_count, 3)
            self.assertLessEqual(cache.statistics["entries"], 1)
            self.assertIn("Incremental successor.", facade.query_proposal({
                "revision": revised["revision"], "request": {"kind": "read", "target": self.target},
            })["content"])

    def test_invalid_native_suffix_keeps_the_exact_predecessor_and_head(self):
        old = self.query()
        no_effect = reference_change(self.root, "projection-cache", revision=True)
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            rejected = self.facade.revise_proposal({
                "kind": "revise-proposal",
                "expected_revision": self.latest["revision"], "change_set": no_effect,
            })
            self.assertEqual(rejected["code"], "AUTHORING.NO_EFFECT", rejected)
            refresh.assert_not_called()
            self.assertEqual(self.query(), old)
            refresh.assert_not_called()
        self.assertEqual(self.facade.workflow_status({"context": self.latest["context"]})["status"], "complete")

    def test_stale_native_head_is_rejected_before_continuation(self):
        self.query()
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            rejected = self.facade.revise_proposal({
                "kind": "revise-proposal",
                "expected_revision": self.first["revision"], "change_set": self.successor_change(),
            })
        self.assertEqual(rejected["code"], "AUTHORING.REVISION_STALE", rejected)
        refresh.assert_not_called()

    def test_cumulative_review_obligations_match_a_fresh_engine_after_continuation(self):
        warm = self.facade.workflow_status({"context": self.normative["context"]})
        self.assertEqual(warm["status"], "needs-action", warm)
        change = reference_change(self.root, "projection-normative", revision=True)
        change["edits"][0]["standard"].update(
            id="topic.projection-normative", role="topic", level="MUST",
        )
        revised = self.facade.revise({"context": self.normative["context"], "change_set": change})
        self.assertEqual(revised["status"], "needs-action", revised)
        with StandardsEngine.open_repository(
            self.root, store_path=self.store, purpose="authoring",
            execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(self.root)),
        ) as engine:
            cold = AgentToolFacade(engine, self.interface).workflow_status({"context": revised["context"]})
        self.assertEqual(cold["status"], revised["status"])
        self.assertTrue(revised["outcome"]["obligations"])
        self.assertEqual(cold["outcome"]["obligations"], revised["outcome"]["obligations"])

    def test_independent_projection_boundary_ignores_an_offered_predecessor(self):
        base = self.engine._compiled_snapshot(SnapshotId(self.snapshot["id"]))
        first = self.engine._authoring.read_revision(self.first["revision"]["id"])
        latest = self.engine._authoring.read_revision(self.latest["revision"]["id"])
        prefix = self.engine._proposal_projection(first, base, reuse=True)
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            replayed = self.engine._proposal_projection(latest, base, predecessor=prefix)
        self.assertEqual(refresh.call_count, 2)
        self.assertEqual(replayed.source.files, self.engine._proposal_projection(latest, base).source.files)

    def test_new_revision_misses_while_old_results_and_stale_status_stay_exact(self):
        old = self.query()
        change = reference_change(self.root, "projection-cache", revision=True)
        change["edits"][0]["standard"]["body"] += "Independent third revision.\n"
        revised = self.facade.revise({"context": self.latest["context"], "change_set": change})
        self.assertEqual(revised["status"], "complete", revised)
        self.assertNotEqual(revised["revision"], self.latest["revision"])
        self.assertEqual(self.query(), old)
        self.assertIn("Independent third revision.", self.query(revised)["content"])
        self.assertEqual(self.facade.workflow_status({"context": self.latest["context"]})["status"], "stale")

    def test_request_and_response_mutation_cannot_change_the_next_result(self):
        first = self.query()
        expected = deepcopy(first)
        first["content"] = "altered caller output"
        first["requires"].append("invented")
        first["next_operations"].clear()
        self.assertEqual(self.query(), expected)

    def test_cached_semantic_intent_maps_are_private_to_each_operation(self):
        snapshot = SnapshotId(self.snapshot["id"])
        base = self.engine._compiled_snapshot(snapshot)
        old = self.engine._authoring.read_revision(self.latest["revision"]["id"])
        change = logical.StandardsChangeSet.from_mapping({
            "purpose": reference_change(self.root)["purpose"],
            "edits": [{"kind": "move-policy-unit",
                       "policy": "topic.architecture.composed-design-admission",
                       "standard": "topic.contracts",
                       "semantics": {"kind": "preserve", "semantic_revision": 1,
                                     "intent": "Move representation without changing meaning."}}],
        })
        from tools.standards_engine.standards_engine.authoring import ProposalRevision
        revision = ProposalRevision(old.proposal, 1, snapshot, old.base_repository_paths, (change,))
        first = self.cache.project_verified(revision, base, self.engine._logical_authoring)
        expected = deepcopy(first.semantic_proposals)
        self.assertTrue(expected)
        first.semantic_proposals[0]["intent"] = "first caller mutation"
        second = self.cache.project_verified(revision, base, self.engine._logical_authoring)
        self.assertEqual(second.semantic_proposals, expected)
        second.semantic_proposals[0]["intent"] = "second caller mutation"
        third = self.cache.project_verified(revision, base, self.engine._logical_authoring)
        self.assertEqual(third.semantic_proposals, expected)

    def test_quarantine_and_purge_are_observed_before_projection_hits(self):
        self.query()
        snapshot = SnapshotId(self.snapshot["id"])
        hits = self.cache.statistics["hits"]
        self.engine._snapshots.delete_snapshot(snapshot)
        self.assertEqual(self.query()["outcome"], "unavailable")
        deadline = self.engine._snapshots.snapshot(snapshot, include_quarantined=True).purge_deadline
        with patch.object(self.engine._snapshots, "_now", return_value=deadline + 1):
            self.assertEqual(self.query()["outcome"], "unavailable")
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_corrupt_base_is_rejected_before_using_either_retained_entry(self):
        self.query()
        hits = self.cache.statistics["hits"]
        with closing(sqlite3.connect(self.store)) as connection, connection:
            trigger = connection.execute("SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'").fetchone()[0]
            connection.execute("DROP TRIGGER content_files_no_update")
            connection.execute(
                "UPDATE content_files SET raw_bytes=?, byte_length=?, sha256=? WHERE logical_path=?",
                (b"corrupt", 7, hashlib.sha256(b"corrupt").hexdigest(), "CORE-STANDARDS.md"),
            )
            connection.execute(trigger)
        self.assertEqual(self.query()["code"], "SNAPSHOT.CONTENT_ID_MISMATCH")
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_corrupt_revision_is_not_hidden_by_an_exact_projection_hit(self):
        self.query()
        hits = self.cache.statistics["hits"]
        with closing(sqlite3.connect(self.store)) as connection, connection:
            trigger = connection.execute("SELECT sql FROM sqlite_schema WHERE name='aggregate_records_no_update'").fetchone()[0]
            payload = connection.execute("SELECT payload FROM aggregate_records WHERE aggregate_id=?", (self.latest["revision"]["id"],)).fetchone()[0]
            value = json.loads(payload)
            value["change_sets"][-1]["purpose"]["summary"] = "Corrupt exact revision"
            connection.execute("DROP TRIGGER aggregate_records_no_update")
            connection.execute("UPDATE aggregate_records SET payload=? WHERE aggregate_id=?", (json.dumps(value).encode(), self.latest["revision"]["id"]))
            connection.execute(trigger)
        result = self.query()
        self.assertEqual(result["kind"], "rejected-result", result)
        self.assertEqual(result["outcome"], "invalid", result)
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_store_replacement_has_no_revision_to_reuse(self):
        self.query()
        hits = self.cache.statistics["hits"]
        self.engine.close()
        self.store.rename(self.store.with_suffix(".retained"))
        self.engine = self.open_engine()
        self.facade = AgentToolFacade(self.engine, self.interface)
        self.assertEqual(self.query()["outcome"], "unavailable")
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_borrower_close_preserves_replay_but_still_reopens_storage(self):
        expected = self.query()
        self.engine.close()
        self.engine = self.open_engine()
        self.facade = AgentToolFacade(self.engine, self.interface)
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            self.assertEqual(self.query(), expected)
        refresh.assert_not_called()

    def test_snapshot_and_projections_share_entry_and_byte_budgets(self):
        expected = self.query()
        used = self.cache.statistics["accounted_bytes"]
        for entries, budget in ((0, used), (2, 1), (1, used), (4, used // 2)):
            with self.subTest(entries=entries, budget=budget):
                cache = CompiledSnapshotCache(self.root, "authoring", max_entries=entries, max_bytes=budget)
                try:
                    with self.open_engine(cache) as engine:
                        facade = AgentToolFacade(engine, self.interface)
                        for _ in range(2):
                            observed = facade.query_proposal({"revision": self.latest["revision"], "request": {"kind": "read", "target": self.target}})
                            self.assertEqual(observed, expected)
                    self.assertLessEqual(cache.statistics["entries"], entries)
                    self.assertLessEqual(cache.statistics["accounted_bytes"], budget)
                    self.assertTrue(cache.statistics["evictions"] or cache.statistics["uncached"])
                finally:
                    cache.close()
                self.assertEqual(cache.statistics["accounted_bytes"], 0)

    def test_failed_replay_is_not_cached(self):
        with patch.object(logical, "_refresh_suite_input_projection", side_effect=RuntimeError("failed replay")):
            with self.assertRaisesRegex(RuntimeError, "failed replay"):
                self.query()
        self.assertEqual(self.cache.statistics["entries"], 1)  # Verified base only.
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            self.assertEqual(self.query()["kind"], "proposal-read-result")
        self.assertEqual(refresh.call_count, 2)

    def test_stateful_compiler_does_not_acquire_retention_authority(self):
        base = self.engine._compiled_snapshot(SnapshotId(self.snapshot["id"]))
        revision = self.engine._authoring.read_revision(self.latest["revision"]["id"])
        calls = []
        def compile_authorities(source):
            calls.append(source)
            return StandardsEngine._compile(source)
        compiler = logical.LogicalAuthoringCompiler(compile_authorities)
        for _ in range(2):
            self.cache.project_verified(revision, base, compiler)
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.cache.statistics["uncached"], 2)
        self.assertEqual(self.cache.statistics["entries"], 1)

    def test_rejected_prospective_revision_is_not_published_by_cache_retention(self):
        from tools.standards_engine.standards_engine.authoring import ProposalRevision
        old = self.engine._authoring.read_revision(self.latest["revision"]["id"])
        change = reference_change(self.root, "projection-cache", revision=True)
        change["edits"][0]["standard"]["body"] += "Prospective revision.\n"
        prospective = ProposalRevision(
            old.proposal, old.ordinal + 1, old.base_snapshot,
            old.base_repository_paths,
            (*old.change_sets, logical.StandardsChangeSet.from_mapping(change)),
        )
        with patch.object(self.engine._snapshots, "advance_aggregate_root", return_value="stale"):
            result = self.facade.revise({"context": self.latest["context"], "change_set": change})
        self.assertEqual(result["outcome"]["code"], "AUTHORING.REVISION_STALE", result)
        observed = self.facade.query_proposal({
            "revision": self.engine._proposal_revision_handle(prospective.revision_id),
            "request": {"kind": "read", "target": self.target},
        })
        self.assertEqual(observed["outcome"], "unavailable", observed)
        self.assertEqual(self.facade.workflow_status({"context": self.latest["context"]})["status"], "complete")

    def test_compiler_recipe_changes_miss_and_unknown_instance_state_stays_cold(self):
        base = self.engine._compiled_snapshot(SnapshotId(self.snapshot["id"]))
        revision = self.engine._authoring.read_revision(self.latest["revision"]["id"])
        first = self.cache.project_verified(revision, base, self.engine._logical_authoring)
        # This stateless alternate installation has a distinct recipe identity.
        def alternate(source):
            return StandardsEngine._compile(source)
        compiler = logical.LogicalAuthoringCompiler(alternate)
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            second = self.cache.project_verified(revision, base, compiler)
        self.assertEqual(refresh.call_count, 2)
        self.assertEqual(first.source.files, second.source.files)
        compiler.extra_context = object()
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            self.cache.project_verified(revision, base, compiler)
            self.cache.project_verified(revision, base, compiler)
        self.assertEqual(refresh.call_count, 4)

    def test_advancing_main_preserves_draft_base_through_warm_and_cold_reads(self):
        from tools.standards_verifier.standards_verifier import suite_input_projection_bytes
        root = Path(self.temporary.name) / "advanced-main"
        prepare_repository(root)
        store = root / ".standards-engine/snapshots-v1.sqlite3"
        store.parent.mkdir(exist_ok=True)
        with closing(sqlite3.connect(self.store)) as source:
            with closing(sqlite3.connect(store)) as destination:
                source.backup(destination)
        cache = CompiledSnapshotCache(root, "authoring")
        self.addCleanup(cache.close)
        arguments = {"revision": self.latest["revision"], "request": {"kind": "read", "target": self.target}}
        with AgentToolFacade.open_repository(root, purpose="authoring", compiled_cache=cache) as facade:
            first = facade.query_proposal(arguments)
            core = root / "CORE-STANDARDS.md"
            core.write_text(core.read_text() + "\n<!-- New fixture main. -->\n")
            manifest = root / "evaluation/standards-effectiveness/generated/suite-inputs.json"
            manifest.write_bytes(suite_input_projection_bytes(root))
            subprocess.run(["git", "-C", str(root), "add", "CORE-STANDARDS.md", str(manifest.relative_to(root))], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "fixture: advance accepted main"], check=True)
            self.assertEqual(facade.query_proposal(arguments), first)
        cache.close()
        (root / "CORE-STANDARDS.md").unlink()
        with AgentToolFacade.open_repository(root, purpose="authoring") as cold:
            self.assertEqual(cold.query_proposal(arguments), first)

    def test_authorization_and_invalid_evidence_remain_fresh_on_warm_status(self):
        context = self.normative["context"]
        self.facade.workflow_status({"context": context})
        obligation = self.normative["outcome"]["obligations"][0]
        submission = {"kind": "impact-disposition", "obligation": obligation["handle"],
                      "result": "confirmed", "rationale": "Reviewed isolated test scope.",
                      "fingerprint": obligation["fingerprint"], "evidence": [evidence(self.root)]}
        bad = {**submission, "evidence": [{**evidence(self.root), "digest": "sha256:" + "0" * 64}]}
        rejected = self.facade.resolve_workflow({"context": context, "submission": bad})
        self.assertEqual(rejected["outcome"]["code"], "ANALYSIS.EVIDENCE_DIGEST_MISMATCH", rejected)
        authorize = self.engine._execution_context.authorization.authorize
        def quarantine(request):
            decision = authorize(request)
            self.engine._snapshots.delete_snapshot(SnapshotId(self.snapshot["id"]))
            return decision
        with patch.object(self.engine._execution_context.authorization, "authorize", side_effect=quarantine) as calls:
            rejected = self.facade.resolve_workflow({"context": context, "submission": submission})
        self.assertTrue(calls.call_count)
        self.assertEqual(rejected.get("outcome", rejected)["outcome"], "unavailable", rejected)

    def test_review_keeps_fresh_replay_instead_of_borrowing_a_draft_entry(self):
        self.query()
        with patch.object(logical, "_refresh_suite_input_projection", wraps=logical._refresh_suite_input_projection) as refresh:
            reviewed = self.facade.review({"context": self.latest["context"], "decisions": decisions(self.root)})
        self.assertEqual(reviewed["status"], "ready", reviewed)
        self.assertGreaterEqual(refresh.call_count, 2)

    def test_application_cannot_read_authoring_entries(self):
        self.query()
        with self.assertRaisesRegex(ValueError, "another repository or purpose"):
            StandardsEngine.open_repository(self.root, store_path=self.store, purpose="application", compiled_cache=self.cache)
        with StandardsEngine.open_repository(self.root, store_path=self.store, purpose="application") as engine:
            result = AgentToolFacade(engine, self.interface).query_proposal({"revision": self.latest["revision"], "request": {"kind": "read", "target": self.target}})
        self.assertEqual(result["code"], "APPLICATION.OPERATION_UNAVAILABLE")

    def test_capture_keeps_both_compiler_passes_with_warm_draft_material(self):
        self.query()
        from tools.standards_engine.standards_engine import engine as engine_module
        with patch.object(engine_module, "compile_policy_impact", wraps=engine_module.compile_policy_impact) as compile:
            result = self.facade.create_snapshot({"kind": "create-snapshot"})
        self.assertEqual(result["kind"], "create-snapshot-result", result)
        self.assertEqual(compile.call_count, 2)

    def test_two_fresh_stdio_servers_reproduce_same_historical_draft(self):
        messages = [request("initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "projection-test", "version": "1"}}),
                    {"jsonrpc": "2.0", "method": "notifications/initialized"}]
        args = {"revision": self.latest["revision"], "request": {"kind": "read", "target": self.target}}
        messages += [request("tools/call", {"name": "query_proposal", "arguments": args}, i) for i in (2, 3)]
        observed = []
        for _ in range(2):
            process = subprocess.run(
                [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", str(self.root), "--purpose", "authoring"],
                input="".join(json.dumps(item) + "\n" for item in messages), text=True,
                capture_output=True, check=True, timeout=90,
                env={**os.environ, "PYTHONPATH": str(ROOT)}, cwd=self.temporary.name,
            )
            replies = [json.loads(line) for line in process.stdout.splitlines()]
            rows = [item["result"] for item in replies if item["id"] in (2, 3)]
            self.assertFalse(any(item["isError"] for item in rows), rows)
            self.assertEqual(rows[0], rows[1])
            self.assertEqual(json.loads(rows[0]["content"][0]["text"]), rows[0]["structuredContent"])
            observed.append(rows[0])
        self.assertEqual(observed[0], observed[1])


if __name__ == "__main__":
    unittest.main()
