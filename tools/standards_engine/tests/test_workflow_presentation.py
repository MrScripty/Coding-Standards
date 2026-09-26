"""Exact compact projection and lossless, workload-sensitive detail retrieval."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, AnalysisHandle
from tools.standards_engine.standards_engine import analysis_projection as projection
from tools.standards_engine.standards_engine import workflow_presentation as presentation
from tools.standards_engine.tests.test_agent_workflow import reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change


class WorkflowPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="workflow-presentation-")
        cls.root = Path(cls.temp.name) / "repository"
        _clone_tracked_worktree(cls.root)
        cls.facade = AgentToolFacade.open_repository(cls.root, purpose="authoring")
        cls.engine = cls.facade._engine
        capture = cls.facade.create_snapshot({"kind": "create-snapshot"})
        assert capture["kind"] == "create-snapshot-result", capture
        cls.snapshot = capture["snapshot"]["snapshot"]

    @classmethod
    def tearDownClass(cls):
        cls.facade.close()
        cls.temp.cleanup()

    def proposed(self, label, count=1):
        value = self.facade.propose({
            "snapshot": self.snapshot,
            "change_set": topic_change(self.root, label, count), "detail": "full",
        })
        self.assertEqual(value["status"], "needs-action", value)
        return value

    def completed(self, label, rationales):
        original = self.proposed(label, len(rationales))
        submitted = [
            {**decision(self.root, item), "rationale": rationale}
            for item, rationale in zip(original["outcome"]["obligations"], rationales)
        ]
        result = self.facade.resolve_many({
            "context": original["context"], "submissions": submitted, "detail": "full",
        })
        self.assertEqual(result["status"], "complete", result)
        return result

    def assert_summary(self, context):
        full = self.facade.workflow_status({"context": context, "detail": "full"})
        self.assertEqual(full["kind"], "workflow-result", full)
        evaluation = self.engine._evaluate(
            self.engine._load_analysis(AnalysisHandle.from_value(context)))
        expected = presentation.summarize(projection._analysis_result(evaluation))
        self.assertEqual(projection._analysis_summary(evaluation), expected)
        # The compact status path must not build the result it will discard.
        with patch.object(self.engine, "_analysis_result", side_effect=AssertionError("full projection")):
            compact = self.facade.workflow_status({"context": context})
        self.assertEqual(compact["outcome"], expected)
        self.assertEqual({k: v for k, v in full.items() if k != "outcome"},
                         {k: v for k, v in compact.items() if k != "outcome"})
        return compact

    def test_compact_summary_matches_full_pending_complete_requires_change_and_stale(self):
        original = self.proposed("summary-states")
        self.assertEqual(self.assert_summary(original["context"])["status"], "needs-action")
        submission = decision(self.root, original["outcome"]["obligations"][0])
        complete = self.facade.resolve_workflow({
            "context": original["context"], "submission": submission, "detail": "full",
        })
        self.assertEqual(self.assert_summary(complete["context"])["status"], "complete")
        changed = self.facade.resolve_workflow({
            "context": original["context"], "submission": {**submission, "result": "requires-change"},
        })
        self.assertEqual(self.assert_summary(changed["context"])["status"], "requires-change")
        revised = self.facade.revise({
            "context": complete["context"], "change_set": reference_change(self.root, "summary-successor"),
        })
        self.assertEqual(revised["kind"], "workflow-result", revised)
        self.assertEqual(self.assert_summary(original["context"])["status"], "stale")

    def test_compact_status_preserves_invalid_context_rejection(self):
        original = self.proposed("summary-invalid")
        invalid = deepcopy(original["context"])
        invalid["id"] = "analysis:sha256:" + "0" * 64
        compact = self.facade.workflow_status({"context": invalid})
        full = self.facade.workflow_status({"context": invalid, "detail": "full"})
        self.assertEqual(compact, full)
        self.assertEqual(compact["kind"], "rejected-result")

    def test_compact_status_does_not_publish_or_modify_durable_analysis(self):
        result = self.completed("summary-durable", ["A real explicit fixture decision."])
        before = self.facade.inspect({"handle": result["context"]})
        with patch.object(self.engine._snapshots, "publish_aggregate_if_root_head",
                          side_effect=AssertionError("unexpected write")):
            self.assert_summary(result["context"])
        self.assertEqual(self.facade.inspect({"handle": result["context"]}), before)

    def test_byte_pressure_returns_fewer_whole_records_without_gaps(self):
        full = self.completed("adaptive-page", [f"{n}:" + "x" * 27000 for n in range(4)])
        request = {"analysis": full["context"], "section": "dispositions", "limit": 8}
        seen = []
        observations = set()
        while True:
            page = self.facade.workflow_details(request)
            self.assertEqual(page["kind"], "workflow-details-result", page)
            self.assertLessEqual(presentation._page_size(page), presentation.PAGE_BYTES)
            self.assertEqual(page["offset"], len(seen))
            self.assertTrue(page["items"])
            self.assertLess(len(page["items"]), 4)
            observations.add(page["observation"])
            seen.extend(page["items"])
            if "next" not in page:
                break
            self.assertEqual(page["next"]["offset"], len(seen))
            request = page["next"]
        self.assertEqual(len(observations), 1)
        self.assertEqual(seen, full["outcome"]["dispositions"])

    def test_single_oversized_record_has_exact_explicit_full_retry_and_cold_readback(self):
        full = self.completed("oversized-page", ["First record: " + "x" * 71000, "Small second record."])
        analysis = full["context"]
        before = self.facade.inspect({"handle": analysis})
        rejected = self.facade.workflow_details({"analysis": analysis, "section": "dispositions"})
        self.assertEqual(rejected["code"], "WORKFLOW.RESULT_LIMIT", rejected)
        self.assertNotIn("items", rejected)
        continuation = rejected["next_operations"][0]
        self.assertEqual(continuation["operation"], "workflow_details")
        request = continuation["request"]
        self.assertEqual(request["detail"], "full")
        self.assertEqual(request["limit"], 1)
        with AgentToolFacade.open_repository(self.root, purpose="authoring") as cold:
            page = cold.workflow_details(request)
            self.assertEqual(page["kind"], "workflow-details-result", page)
            self.assertEqual(page["items"], full["outcome"]["dispositions"][:1])
            self.assertGreater(presentation._page_size(page), presentation.PAGE_BYTES)
            self.assertNotIn("detail", page["next"])
            following = cold.workflow_details(page["next"])
            self.assertEqual(following["items"], full["outcome"]["dispositions"][1:])
            self.assertLessEqual(presentation._page_size(following), presentation.PAGE_BYTES)
        self.assertEqual(self.facade.inspect({"handle": analysis}), before)

    def test_oversized_item_is_not_skipped_after_a_fitting_prefix(self):
        full = self.completed("mixed-page", ["Small first.", "x" * 71000, "Small last."])
        page = self.facade.workflow_details({"analysis": full["context"], "section": "dispositions"})
        # The canonical disposition order need not equal submission order.
        expected = full["outcome"]["dispositions"]
        collected = []
        while True:
            if page["kind"] == "rejected-result":
                self.assertEqual(page["code"], "WORKFLOW.RESULT_LIMIT")
                page = self.facade.workflow_details(page["next_operations"][0]["request"])
            self.assertEqual(page["offset"], len(collected))
            collected.extend(page["items"])
            if "next" not in page:
                break
            page = self.facade.workflow_details(page["next"])
        self.assertEqual(collected, expected)

    def test_full_detail_is_one_record_and_preserves_observation_binding(self):
        original = self.proposed("full-details", 2)
        first = self.facade.workflow_details({"analysis": original["context"], "section": "obligations"})
        request = {"analysis": original["context"], "section": "obligations", "detail": "full"}
        page = self.facade.workflow_details(request)
        self.assertEqual(page["items"], first["items"][:1])
        self.assertEqual(page["observation"], first["observation"])
        for limit in (2, 8, 16):
            rejected = self.facade.workflow_details({**request, "limit": limit})
            self.assertEqual(rejected["code"], "WORKFLOW.FULL_DETAIL_LIMIT")
        for extra in ({"observation": "sha256:" + "0" * 64}, {"offset": 1}):
            self.assertEqual(self.facade.workflow_details({**request, **extra})["code"],
                             "WORKFLOW.OBSERVATION_CHANGED")
        wrong_section = self.facade.workflow_details({**page["next"], "section": "reading_plan", "detail": "full"})
        self.assertEqual(wrong_section["code"], "WORKFLOW.OBSERVATION_CHANGED")
        with AgentToolFacade.open_repository(self.root, purpose="application") as application:
            self.assertEqual(application.workflow_details(request)["code"], "APPLICATION.OPERATION_UNAVAILABLE")

    def test_unicode_size_and_exact_boundary_include_the_continuation(self):
        full = self.completed("unicode-page", ["🙂漢é\\\"\n" * 5500, "One more."])
        expected = full["outcome"]["dispositions"]
        request = {"analysis": full["context"], "section": "dispositions", "limit": 1, "detail": "full"}
        one = self.facade.workflow_details(request)
        size = presentation._page_size(one)
        bounded_request = {**request, "detail": "compact"}
        with patch.object(presentation, "PAGE_BYTES", size):
            exact = self.facade.workflow_details(bounded_request)
            self.assertEqual(exact, one)
        with patch.object(presentation, "PAGE_BYTES", size - 1):
            rejected = self.facade.workflow_details(bounded_request)
            self.assertEqual(rejected["code"], "WORKFLOW.RESULT_LIMIT")
            retried = self.facade.workflow_details(rejected["next_operations"][0]["request"])
            self.assertEqual(retried["items"], expected[:1])

    def test_schema_integer_numbers_are_normalized_for_slice_indices(self):
        original = self.proposed("integral-json", 2)
        for detail in ("compact", "full"):
            request = {"analysis": original["context"], "section": "obligations",
                       "limit": 1, "offset": 0, "detail": detail}
            expected = self.facade.workflow_details(request)
            observed = self.facade.workflow_details({**request, "limit": 1.0, "offset": 0.0})
            self.assertEqual(observed, expected)
            following = self.facade.workflow_details(expected["next"])
            self.assertEqual(self.facade.workflow_details({
                **expected["next"], "offset": float(expected["next"]["offset"]), "limit": 1.0,
            }), following)
            for invalid in (1.5, True):
                self.assertEqual(self.facade.workflow_details({**request, "limit": invalid})["kind"],
                                 "rejected-result")

    def test_empty_and_terminal_sections_remain_valid(self):
        original = self.proposed("empty-section")
        for detail in ("compact", "full"):
            empty = self.facade.workflow_details({
                "analysis": original["context"], "section": "dispositions", "detail": detail,
            })
            self.assertEqual(empty["items"], [])
            self.assertNotIn("next", empty)
            end = self.facade.workflow_details({
                "analysis": original["context"], "section": "dispositions", "offset": 0,
                "observation": empty["observation"], "detail": detail,
            })
            self.assertEqual(empty, end)
            out_of_range = self.facade.workflow_details({
                "analysis": original["context"], "section": "dispositions", "offset": 1,
                "observation": empty["observation"], "detail": detail,
            })
            self.assertEqual(out_of_range["code"], "WORKFLOW.PAGE_RANGE")

    def test_every_section_full_retry_preserves_exact_item(self):
        original = self.completed("all-sections", ["A stored explicit decision."])
        for section in presentation.SECTIONS:
            request = {"analysis": original["context"], "section": section, "limit": 1}
            page = self.facade.workflow_details(request)
            self.assertEqual(page["kind"], "workflow-details-result", page)
            if not page["items"]:
                continue
            with self.subTest(section=section), patch.object(presentation, "PAGE_BYTES", 1):
                rejected = self.facade.workflow_details(request)
                self.assertEqual(rejected["code"], "WORKFLOW.RESULT_LIMIT")
                full = self.facade.workflow_details(rejected["next_operations"][0]["request"])
                self.assertEqual(full, page)


class SnapshotDetailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools.standards_engine.tests.test_analysis import AnalysisWorkflowTest
        AnalysisWorkflowTest.setUpClass()
        cls.fixture = AnalysisWorkflowTest("test_prepare_persists_parent_bound_public_work")

    @classmethod
    def tearDownClass(cls):
        type(cls.fixture).tearDownClass()

    def test_snapshot_analysis_can_read_oversized_disposition_and_coverage_summary(self):
        from tools.standards_engine.standards_engine import _generated_contract as c
        engine = self.fixture.engine
        parent = self.fixture.prepare()
        request = self.fixture.disposition_submission(parent, "oversized-review").as_contract()
        request["submission"]["rationale"] = "Snapshot review: " + "x" * 71000
        resolved = engine.resolve(c.ResolveCall.from_value(request))
        self.assertIsInstance(resolved, (c.PendingResult, c.CompleteResult))
        counts = engine._snapshots._store.counts()
        rejected = engine.workflow_details(c.WorkflowDetailsCall.from_value({
            "analysis": resolved.handle.as_contract(), "section": "dispositions",
        })).as_contract()
        self.assertEqual(rejected["code"], "WORKFLOW.RESULT_LIMIT")
        page = engine.workflow_details(c.WorkflowDetailsCall.from_value(
            rejected["next_operations"][0]["request"])).as_contract()
        self.assertEqual(page["items"][0]["rationale"], request["submission"]["rationale"])
        self.assertEqual(engine._snapshots._store.counts(), counts)
        evaluation = engine._evaluate(engine._load_analysis(resolved.handle))
        self.assertEqual(projection._analysis_summary(evaluation), presentation.summarize(resolved))
        # Registered corpus content determines whether coverage work is present.
        if isinstance(resolved, c.PendingResult) and any(
            operation.request_kind == "coverage-attestation"
            for operation in resolved.next_operations
        ):
            covered = engine.resolve(self.fixture.coverage_submission(resolved, "coverage-review"))
            self.assertIsInstance(covered, (c.PendingResult, c.CompleteResult))
            evaluation = engine._evaluate(engine._load_analysis(covered.handle))
            self.assertEqual(projection._analysis_summary(evaluation), presentation.summarize(covered))


class DetailTransportTests(unittest.TestCase):
    setUpClass = classmethod(WorkflowPresentationTests.setUpClass.__func__)
    tearDownClass = classmethod(WorkflowPresentationTests.tearDownClass.__func__)
    proposed = WorkflowPresentationTests.proposed
    completed = WorkflowPresentationTests.completed
    def test_oversized_full_retry_through_two_cold_stdio_servers(self):
        import os
        import subprocess
        import sys
        from tools.standards_engine.tests.test_mcp import request
        result = self.completed("oversized-stdio", ["Exact transport material: " + "x" * 71000])
        def call(arguments):
            messages = [
                request("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                        "clientInfo": {"name": "detail-retry-test", "version": "1"}}),
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                request("tools/call", {"name": "workflow_details", "arguments": arguments}, identifier=2),
            ]
            root = Path(__file__).resolve().parents[3]
            run = subprocess.run(
                [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
                 "--repo-root", str(self.root), "--purpose", "authoring"],
                input="".join(json.dumps(item) + "\n" for item in messages),
                text=True, capture_output=True, env={**os.environ, "PYTHONPATH": str(root)},
                check=True,
            )
            self.assertEqual(run.stderr, "")
            wire = json.loads(run.stdout.splitlines()[-1])["result"]
            self.assertEqual(json.loads(wire["content"][0]["text"]), wire["structuredContent"])
            return wire["structuredContent"]
        rejected = call({"analysis": result["context"], "section": "dispositions"})
        self.assertEqual(rejected["code"], "WORKFLOW.RESULT_LIMIT")
        page = call(rejected["next_operations"][0]["request"])
        self.assertEqual(page["kind"], "workflow-details-result", page)
        self.assertEqual(page["items"], result["outcome"]["dispositions"])


if __name__ == "__main__":
    unittest.main()
