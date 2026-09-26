"""Detail reads reuse exact material while preserving each observation boundary."""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import logical_authoring as logical
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.operation_materials import ProposalMaterials
from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer
from tools.standards_engine.tests.test_agent_workflow import reference_change
from tools.standards_engine.tests.test_analysis import POLICY, _clone_tracked_worktree
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change
from tools.standards_snapshots.standards_snapshots import SnapshotId


class WorkflowDetailReuseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix="detail-reuse-fixture-")
        cls.root = Path(cls.fixture.name) / "repository"
        _clone_tracked_worktree(cls.root)
        cls.interface = AgentToolFacade.load_interface(cls.root)
        with closing(CompiledSnapshotCache(cls.root, "authoring")) as cache:
            with AgentToolFacade.open_repository(
                cls.root, purpose="authoring", interface=cls.interface, compiled_cache=cache,
            ) as facade:
                captured = facade.create_snapshot({"kind": "create-snapshot"})
                assert captured["kind"] == "create-snapshot-result", captured
                cls.snapshot = captured["snapshot"]["snapshot"]
                result = facade.propose({
                    "snapshot": cls.snapshot,
                    "change_set": topic_change(cls.root, "detail-reuse", 3),
                    "detail": "full",
                })
                assert result["status"] == "needs-action", result
                for index in range(3):
                    change = reference_change(cls.root, "detail-reuse-history", revision=index > 0)
                    change["edits"][0]["standard"]["body"] += f"Revision {index}.\n"
                    result = facade.revise({
                        "context": result["context"], "change_set": change, "detail": "full",
                    })
                    assert result["status"] == "needs-action", result
                cls.pending = result
                submitted = [
                    {**decision(cls.root, item),
                     "rationale": "Large historical record: " + "x" * 71000
                     if index == 0 else f"Complete decision {index}."}
                    for index, item in enumerate(result["outcome"]["obligations"])
                ]
                cls.complete = facade.resolve_many({
                    "context": result["context"], "submissions": submitted, "detail": "full",
                })
                assert cls.complete["status"] == "complete", cls.complete
        cls.seed = cls.root / ".standards-engine/snapshots-v1.sqlite3"

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="detail-reuse-store-")
        self.addCleanup(self.temporary.cleanup)
        self.store = Path(self.temporary.name) / "test.sqlite3"
        with closing(sqlite3.connect(self.seed)) as source:
            with closing(sqlite3.connect(self.store)) as destination:
                source.backup(destination)
        self.cache = CompiledSnapshotCache(self.root, "authoring")
        self.addCleanup(self.cache.close)
        self.engine = self.open_engine(self.cache)
        self.addCleanup(self.engine.close)
        self.facade = AgentToolFacade(self.engine, self.interface)

    def open_engine(self, cache=None, *, purpose="authoring"):
        return StandardsEngine.open_repository(
            self.root, store_path=self.store, purpose=purpose, compiled_cache=cache,
            execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(self.root)),
        )

    def request(self, *, section="pending_obligations", complete=False, **options):
        return {"analysis": (self.complete if complete else self.pending)["context"],
                "section": section, "limit": 1, **options}

    def warm(self):
        result = self.facade.query_proposal({
            "revision": self.pending["revision"],
            "request": {"kind": "read", "target": "topic.detail-reuse-0"},
        })
        self.assertEqual(result["kind"], "proposal-read-result", result)

    def test_warm_pages_verify_and_evaluate_each_call_without_replaying_draft(self):
        self.warm()
        with (
            patch.object(logical, "_refresh_suite_input_projection",
                         wraps=logical._refresh_suite_input_projection) as refresh,
            patch.object(self.engine._snapshots, "load_content",
                         wraps=self.engine._snapshots.load_content) as load,
            patch.object(self.engine._authoring, "read_revision",
                         wraps=self.engine._authoring.read_revision) as revision,
            patch.object(self.engine, "_evaluate", wraps=self.engine._evaluate) as evaluate,
        ):
            first = self.facade.workflow_details(self.request())
            self.assertEqual(first["kind"], "workflow-details-result", first)
            following = self.facade.workflow_details(first["next"])
            full = self.facade.workflow_details(self.request(detail="full"))
        self.assertEqual(refresh.call_count, 0)
        self.assertEqual(load.call_count, 3)
        self.assertEqual(evaluate.call_count, 3)
        self.assertGreaterEqual(revision.call_count, 6)
        self.assertEqual(first["observation"], following["observation"])
        self.assertEqual(first, full)
        with self.open_engine() as cold:
            facade = AgentToolFacade(cold, self.interface)
            self.assertEqual(facade.workflow_details(self.request()), first)
            self.assertEqual(facade.workflow_details(first["next"]), following)

    def test_disabled_and_evicted_reuse_preserve_complete_page_and_observation(self):
        expected = self.facade.workflow_details(self.request())
        for capacity in (0, 1):
            with self.subTest(capacity=capacity), closing(
                CompiledSnapshotCache(self.root, "authoring", max_entries=capacity)
            ) as cache, self.open_engine(cache) as engine:
                facade = AgentToolFacade(engine, self.interface)
                self.assertEqual(facade.workflow_details(self.request()), expected)
                with patch.object(logical, "_refresh_suite_input_projection",
                                  wraps=logical._refresh_suite_input_projection) as refresh:
                    self.assertEqual(facade.workflow_details(self.request()), expected)
                self.assertEqual(refresh.call_count, 4)
        self.assertLessEqual(self.cache.statistics["entries"], 2)

    def test_oversized_retry_and_contiguous_paging_match_independent_full_replay(self):
        self.warm()
        arguments = self.request(section="dispositions", complete=True, limit=8)
        collected = []
        retried = False
        counts = self.engine._snapshots._store.counts()
        with self.open_engine() as cold:
            reference = AgentToolFacade(cold, self.interface)
            while True:
                page = self.facade.workflow_details(arguments)
                self.assertEqual(page, reference.workflow_details(arguments))
                if page["kind"] == "rejected-result":
                    self.assertEqual(page["code"], "WORKFLOW.RESULT_LIMIT", page)
                    arguments = page["next_operations"][0]["request"]
                    self.assertEqual(arguments["detail"], "full")
                    page = self.facade.workflow_details(arguments)
                    self.assertEqual(page, reference.workflow_details(arguments))
                    retried = True
                self.assertEqual(page["offset"], len(collected))
                collected.extend(page["items"])
                if "next" not in page:
                    break
                arguments = page["next"]
                self.assertNotIn("detail", arguments)
        self.assertTrue(retried)
        self.assertEqual(collected, self.complete["outcome"]["dispositions"])
        self.assertEqual(self.engine._snapshots._store.counts(), counts)

    def test_historical_pages_do_not_select_a_newer_proposal_head(self):
        first = self.facade.workflow_details(self.request())
        change = reference_change(self.root, "detail-reuse-history", revision=True)
        change["edits"][0]["standard"]["body"] += "A different current draft.\n"
        successor = self.facade.revise({"context": self.complete["context"], "change_set": change})
        self.assertEqual(successor["kind"], "workflow-result", successor)
        self.assertNotEqual(successor["revision"], self.pending["revision"])
        self.assertEqual(self.facade.workflow_details(self.request()), first)
        self.assertEqual(self.facade.workflow_status({"context": self.pending["context"]})["status"], "stale")
        self.assertEqual(self.facade.workflow_details(first["next"])["observation"], first["observation"])

    def test_quarantine_and_purge_reject_before_a_warm_lookup(self):
        self.warm()
        hits = self.cache.statistics["hits"]
        snapshot = SnapshotId(self.snapshot["id"])
        self.engine._snapshots.delete_snapshot(snapshot)
        first = self.facade.workflow_details(self.request())
        self.assertEqual(first["kind"], "rejected-result", first)
        self.assertEqual(first["outcome"], "unavailable")
        deadline = self.engine._snapshots.snapshot(snapshot, include_quarantined=True).purge_deadline
        with patch.object(self.engine._snapshots, "_now", return_value=deadline + 1):
            self.assertEqual(self.facade.workflow_details(self.request())["outcome"], "unavailable")
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_base_corruption_is_not_hidden_by_a_warm_detail(self):
        self.warm()
        hits = self.cache.statistics["hits"]
        with closing(sqlite3.connect(self.store)) as connection, connection:
            trigger = connection.execute(
                "SELECT sql FROM sqlite_schema WHERE name='content_files_no_update'"
            ).fetchone()[0]
            connection.execute("DROP TRIGGER content_files_no_update")
            connection.execute(
                "UPDATE content_files SET raw_bytes=?, byte_length=?, sha256=? WHERE logical_path=?",
                (b"corrupt", 7, hashlib.sha256(b"corrupt").hexdigest(), "CORE-STANDARDS.md"),
            )
            connection.execute(trigger)
        result = self.facade.workflow_details(self.request())
        self.assertEqual(result["code"], "SNAPSHOT.CONTENT_ID_MISMATCH", result)
        self.assertEqual(self.cache.statistics["hits"], hits)

    def test_corrupt_stored_revision_rejects_even_after_its_projection_is_warm(self):
        self.warm()
        with closing(sqlite3.connect(self.store)) as connection, connection:
            trigger = connection.execute(
                "SELECT sql FROM sqlite_schema WHERE name='aggregate_records_no_update'"
            ).fetchone()[0]
            identifier = self.pending["revision"]["id"]
            payload = connection.execute(
                "SELECT payload FROM aggregate_records WHERE aggregate_id=?", (identifier,),
            ).fetchone()[0]
            value = json.loads(payload)
            value["change_sets"][-1]["purpose"]["summary"] = "Corrupted retained revision"
            connection.execute("DROP TRIGGER aggregate_records_no_update")
            connection.execute("UPDATE aggregate_records SET payload=? WHERE aggregate_id=?",
                               (json.dumps(value).encode(), identifier))
            connection.execute(trigger)
        result = self.facade.workflow_details(self.request())
        self.assertEqual(result["kind"], "rejected-result", result)
        self.assertEqual(result["outcome"], "invalid", result)

    def test_current_lifecycle_is_checked_after_material_acquisition(self):
        self.warm()
        evaluate = self.engine._evaluate
        def quarantine(state, materials=None):
            self.engine._snapshots.delete_snapshot(SnapshotId(self.snapshot["id"]))
            return evaluate(state, materials)
        with patch.object(self.engine, "_evaluate", side_effect=quarantine):
            result = self.facade.workflow_details(self.request())
        self.assertEqual(result["kind"], "rejected-result", result)
        self.assertEqual(result["outcome"], "unavailable", result)

    def test_reentrant_detail_has_independent_proof_and_scope_cleanup(self):
        self.warm()
        entered = []
        enter = ProposalMaterials.__enter__
        evaluate = self.engine._evaluate
        nested = []
        def capture(scope):
            entered.append(scope)
            return enter(scope)
        def observe(state, materials=None):
            if not nested:
                nested.append(None)
                nested[0] = self.facade.workflow_details(self.request())
            return evaluate(state, materials)
        with (
            patch.object(ProposalMaterials, "__enter__", autospec=True, side_effect=capture),
            patch.object(self.engine, "_evaluate", side_effect=observe),
            patch.object(self.engine._snapshots, "load_content",
                         wraps=self.engine._snapshots.load_content) as load,
        ):
            result = self.facade.workflow_details(self.request())
        self.assertEqual(result, nested[0])
        self.assertEqual(load.call_count, 2)
        self.assertEqual(len(entered), 2)
        self.assertIsNot(entered[0], entered[1])
        self.assertTrue(all(scope._base is None and scope._projection is None for scope in entered))

    def test_scope_is_released_on_projection_exception(self):
        entered = []
        enter = ProposalMaterials.__enter__
        def capture(scope):
            entered.append(scope)
            return enter(scope)
        with (
            patch.object(ProposalMaterials, "__enter__", autospec=True, side_effect=capture),
            patch("tools.standards_engine.standards_engine.workflow_presentation._page",
                  side_effect=RuntimeError("fixture page failure")),
        ):
            with self.assertRaisesRegex(RuntimeError, "fixture page failure"):
                self.facade.workflow_details(self.request())
        self.assertEqual(len(entered), 1)
        self.assertIsNone(entered[0]._base)
        self.assertIsNone(entered[0]._projection)
        self.assertEqual(self.facade.workflow_details(self.request())["kind"], "workflow-details-result")

    def test_snapshot_backed_analysis_needs_no_proposal_projection(self):
        prepared = self.facade.prepare({"request": {
            "kind": "analysis-request", "base_snapshot": self.snapshot,
            "proposed_snapshot": self.snapshot,
            "changes": [{"kind": "modification", "accepted_ids": [POLICY],
                         "proposed_ids": [POLICY], "scope": {"kind": "whole-artifact"}}],
            "semantic_proposals": [], "contract_version": 6,
        }})
        self.assertIn(prepared["kind"], ("pending-result", "complete-result"), prepared)
        arguments = {"analysis": prepared["handle"], "section": "obligations"}
        with self.open_engine() as cold:
            expected = AgentToolFacade(cold, self.interface).workflow_details(arguments)
        with (
            patch.object(self.engine, "_proposal_projection", side_effect=AssertionError("proposal")),
            patch.object(self.engine._snapshots, "load_content",
                         wraps=self.engine._snapshots.load_content) as load,
        ):
            self.assertEqual(self.facade.workflow_details(arguments), expected)
        self.assertEqual(load.call_count, 1)

    def test_application_denial_and_invalid_paging_do_not_gain_authority(self):
        with self.open_engine(purpose="application") as engine:
            facade = AgentToolFacade(engine, self.interface)
            with patch.object(engine._snapshots, "load_content", side_effect=AssertionError("private read")):
                result = facade.workflow_details(self.request())
            self.assertEqual(result["code"], "APPLICATION.OPERATION_UNAVAILABLE", result)
        first = self.facade.workflow_details(self.request())
        invalid = {**first["next"], "observation": "sha256:" + "0" * 64}
        with self.open_engine() as cold:
            expected = AgentToolFacade(cold, self.interface).workflow_details(invalid)
        self.assertEqual(self.facade.workflow_details(invalid), expected)
        self.assertEqual(expected["code"], "WORKFLOW.OBSERVATION_CHANGED")
        original = deepcopy(first)
        first["items"][0]["obligation"]["state"] = "caller mutation"
        self.assertEqual(self.facade.workflow_details(self.request()), original)


if __name__ == "__main__":
    unittest.main()
