"""Agent-facing work is executable, bounded and bound to existing authority."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine import agent_workflow
from tools.standards_contracts.standards_contracts import ContractError
from tools.standards_engine.standards_engine import workflow_presentation as presentation
from tools.standards_engine.tests.test_agent_workflow import reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change


class WorkflowInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="workflow-interaction-")
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

    def proposed(self, label, count=4):
        result = self.facade.propose({
            "snapshot": self.snapshot, "change_set": topic_change(self.root, label, count),
        })
        self.assertEqual(result["status"], "needs-action", result)
        return result

    def assert_work_page(self, result):
        work = result["work"]
        self.assertEqual(work["kind"], "workflow-work-page", work)
        self.assertNotIn("analysis", work)
        self.assertLessEqual(presentation._page_size(work), presentation.PAGE_BYTES)
        self.assertEqual(work["offset"], 0)
        page = self.facade.workflow_details({
            "analysis": result["context"], "section": work["section"],
        })
        expected = {k: v for k, v in page.items() if k not in {"kind", "analysis", "next"}}
        self.assertEqual({k: v for k, v in work.items() if k not in {"kind", "next"}}, expected)
        if "next" in work:
            self.assertNotIn("analysis", work["next"])
            self.assertEqual({"analysis": result["context"], **work["next"]}, page["next"])
        else:
            self.assertNotIn("next", page)
        return work

    def test_inline_projection_reuses_the_issued_result_without_domain_effects(self):
        result = self.proposed("pure-inline", 3)
        full = self.facade.workflow_status({"context": result["context"], "detail": "full"})
        outcome = c.PendingResult.from_value(full["outcome"])
        before = outcome.as_contract()
        bound = agent_workflow.bind(self.engine, c.AnalysisHandle.from_value(result["context"]))
        with (
            patch.object(self.engine, "_evaluate", side_effect=AssertionError("second evaluation")),
            patch.object(self.engine, "_apply_providers", side_effect=AssertionError("provider execution")),
            patch.object(self.engine, "workflow_details", side_effect=AssertionError("nested detail read")),
            patch.object(self.engine, "review_proposal", side_effect=AssertionError("implicit review")),
            patch.object(self.engine, "apply_proposal", side_effect=AssertionError("implicit publication")),
            patch.object(self.engine._snapshots, "publish_aggregate_if_root_head", side_effect=AssertionError("publication")),
        ):
            projected = agent_workflow.view(self.engine, bound, outcome, include_work=True).as_contract()
        self.assertEqual(projected, result)
        self.assertEqual(outcome.as_contract(), before)

    def test_inline_byte_pressure_keeps_whole_records_and_exact_continuation(self):
        result = self.proposed("bounded-inline", 4)
        full = self.facade.workflow_status({"context": result["context"], "detail": "full"})
        outcome = c.PendingResult.from_value(full["outcome"])
        one = self.facade.workflow_details({
            "analysis": result["context"], "section": "pending_obligations", "limit": 1,
        })
        # Inline pages use the same default next-page selection as details.
        one["next"]["limit"] = presentation.DEFAULT_PAGE_ITEMS
        exact_size = presentation._page_size(one)
        with patch.object(presentation, "PAGE_BYTES", exact_size):
            work = presentation.pending_work(outcome)
        self.assertEqual(work["items"], result["work"]["items"][:1])
        self.assertEqual(work["next"]["offset"], 1)
        self.assertEqual(work["total"], 4)
        self.assertEqual(work["observation"], result["work"]["observation"])
        self.assertLessEqual(presentation._page_size(work), exact_size)
        following = self.facade.workflow_details({"analysis": result["context"], **work["next"]})
        self.assertEqual(work["items"] + following["items"], result["work"]["items"])
        with patch.object(presentation, "PAGE_BYTES", exact_size - 1):
            deferred = presentation.pending_work(outcome)
        self.assertEqual(deferred["kind"], "workflow-work-deferred")
        self.assertEqual(deferred["request"]["offset"], 0)
        self.assertEqual(deferred["request"]["observation"], work["observation"])

    def test_new_result_contract_rejects_duplicated_bindings_and_wrong_work(self):
        result = self.proposed("closed-contract", 1)
        self.assertEqual(c.WorkflowResult.from_value(result).as_contract(), result)
        bad = []
        duplicate = deepcopy(result)
        duplicate["next_operations"][0]["context"] = result["context"]
        bad.append(duplicate)
        duplicate = deepcopy(result)
        duplicate["outcome"]["handle"] = result["context"]
        bad.append(duplicate)
        duplicate = deepcopy(result)
        duplicate["outcome"]["details"]["analysis"] = result["context"]
        bad.append(duplicate)
        duplicate = deepcopy(result)
        duplicate["work"]["analysis"] = result["context"]
        bad.append(duplicate)
        duplicate = deepcopy(result)
        duplicate["work"]["items"] *= 9
        bad.append(duplicate)
        duplicate = deepcopy(result)
        duplicate["work"]["section"] = "dispositions"
        bad.append(duplicate)
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ContractError):
                c.WorkflowResult.from_value(value)
        with self.assertRaises(ContractError):
            c.WorkflowDetailsSelection.from_value({
                "analysis": result["context"], "section": "pending_obligations",
            })

    def test_mutation_results_supply_executable_successor_work_without_detail_calls(self):
        result = self.proposed("direct-work", 4)
        self.assertEqual(result["outcome"]["required_obligations"], 4)
        self.assertNotIn("handle", result["outcome"])
        self.assertNotIn("analysis", result["outcome"]["details"])
        for action in result["next_operations"]:
            self.assertNotIn("context", action)
        # The fixture author makes real decisions; the client only carries the
        # new context and the already-issued work handles between rounds.
        with patch.object(self.facade, "workflow_details", side_effect=AssertionError("extra read")):
            for remaining in (2, 0):
                submitted = [decision(self.root, item["obligation"]) for item in result["work"]["items"][:2]]
                result = self.facade.resolve_many({"context": result["context"], "submissions": submitted})
                self.assertEqual(result["outcome"]["required_obligations"], remaining)
                if remaining:
                    self.assertEqual(result["work"]["total"], remaining)
        self.assertEqual(result["status"], "complete")
        self.assertNotIn("work", result)
        self.assertEqual({item["operation"] for item in result["next_operations"]}, {"review", "revise"})

    def test_inline_pages_match_details_and_continue_after_cold_reconnect(self):
        result = self.proposed("inline-paging", 11)
        work = self.assert_work_page(result)
        self.assertEqual(len(work["items"]), 8)
        self.assertEqual(work["total"], 11)
        with AgentToolFacade.open_repository(self.root, purpose="authoring") as cold:
            following = cold.workflow_details({"analysis": result["context"], **work["next"]})
            self.assertEqual(following["offset"], 8)
            self.assertEqual(len(following["items"]), 3)
            self.assertEqual(following["observation"], work["observation"])
            self.assertNotIn("next", following)

    def test_status_and_full_results_remain_workload_sensitive(self):
        result = self.proposed("light-status")
        with patch.object(presentation, "pending_work", side_effect=AssertionError("inline construction")):
            status = self.facade.workflow_status({"context": result["context"]})
            full = self.facade.workflow_status({"context": result["context"], "detail": "full"})
        self.assertNotIn("work", status)
        self.assertNotIn("work", full)
        self.assertEqual(status, {k: v for k, v in result.items() if k != "work"})
        self.assertEqual(full["outcome"]["kind"], "pending-result")
        self.assertEqual(len(full["outcome"]["obligations"]), 4)

    def test_oversized_inline_work_preserves_mutation_and_explicit_full_retry(self):
        # Bound the page tightly without changing the authoritative records.
        with patch.object(presentation, "PAGE_BYTES", 1):
            result = self.proposed("deferred-work", 1)
        work = result["work"]
        self.assertEqual(work["kind"], "workflow-work-deferred")
        self.assertEqual(work["code"], "WORKFLOW.RESULT_LIMIT")
        self.assertEqual(work["total"], 1)
        self.assertEqual(work["request"]["detail"], "full")
        self.assertNotIn("analysis", work["request"])
        with AgentToolFacade.open_repository(self.root, purpose="authoring") as cold:
            page = cold.workflow_details({"analysis": result["context"], **work["request"]})
            self.assertEqual(len(page["items"]), 1)
            self.assertEqual(page["items"][0]["work"]["analysis"], result["context"])
            self.assertEqual(cold.workflow_status({"context": result["context"]})["status"], "needs-action")

    def test_successor_rejects_original_work_and_stale_result_has_no_inline_actions(self):
        original = self.proposed("bound-work", 2)
        old_work = original["work"]["items"]
        next_state = self.facade.resolve_many({
            "context": original["context"], "submissions": [decision(self.root, old_work[0]["obligation"])],
        })
        rejected = self.facade.resolve_many({
            "context": next_state["context"], "submissions": [decision(self.root, old_work[1]["obligation"])],
        })
        self.assertEqual(rejected["kind"], "rejected-result")
        self.assertEqual(rejected["outcome"], "invalid")
        revised = self.facade.revise({
            "context": next_state["context"], "change_set": reference_change(self.root, "bound-successor"),
        })
        self.assertEqual(revised["status"], "needs-action", revised)
        self.assert_work_page(revised)
        stale = self.facade.workflow_status({"context": original["context"]})
        self.assertEqual(stale["status"], "stale")
        self.assertNotIn("work", stale)
        self.assertEqual([a["operation"] for a in stale["next_operations"]], ["resume"])
        tampered = {"analysis": revised["context"], "section": "pending_obligations", "observation": original["work"]["observation"]}
        self.assertEqual(self.facade.workflow_details(tampered)["code"], "WORKFLOW.OBSERVATION_CHANGED")

    def test_single_decision_and_explicit_analyze_also_return_actionable_work(self):
        original = self.proposed("single-work", 3)
        successor = self.facade.resolve_workflow({
            "context": original["context"],
            "submission": decision(self.root, original["work"]["items"][0]["obligation"]),
        })
        self.assertEqual(self.assert_work_page(successor)["total"], 2)
        draft = self.facade.resume({"context": successor["context"]})
        self.assertEqual(draft["status"], "draft")
        analyzed = self.facade.analyze({"context": draft["context"]})
        self.assert_work_page(analyzed)


if __name__ == "__main__":
    unittest.main()
