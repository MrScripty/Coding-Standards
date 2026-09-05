from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine.tools import (
    LocalAlwaysAllowAuthorizer,
    _contracts,
)

ROOT = Path(__file__).resolve().parents[3]


def prepare_repository(destination):
    subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(destination)],
        check=True,
    )
    for path in (
        "a1-interface.toml",
        "a1-contract.schema.json",
        "generated/agent-tools.json",
    ):
        relative = Path("tools/standards_engine/contracts") / path
        shutil.copyfile(ROOT / relative, destination / relative)


def evidence(root):
    path = "tools/standards_engine/README.md"
    return {
        "id": path,
        "digest": "sha256:" + hashlib.sha256((root / path).read_bytes()).hexdigest(),
        "provider_contract": "repository-content",
        "provider_contract_version": "1",
    }


def reference_change(root, label="fixture", *, revision=False):
    standard = {
        "id": f"reference.testing.{label}",
        "title": "Agent Workflow Fixture",
        "role": "reference",
        "level": "REFERENCE",
        "applies_when": "Testing the agent workflow interface.",
        "does_not_apply_when": "Making production policy decisions.",
        "verification": "Agent workflow acceptance tests.",
        "body": "This is an isolated workflow test reference.\n"
        + ("Revised fixture text.\n" if revision else ""),
    }
    edit = {
        "kind": "revise-standard" if revision else "create-standard",
        "standard": standard,
    }
    if not revision:
        edit.update(requires=["core"], specializes=[], policy_units=[])
    return {
        "purpose": {
            "summary": "Revise an agent workflow fixture"
            if revision
            else "Add an agent workflow fixture",
            "rationale": "Exercise an isolated reference change with no normative policy edits.",
            "evidence": [evidence(root)],
        },
        "edits": [edit],
    }


def decisions(root):
    return [
        {
            "owner": owner,
            "decision": "accept",
            "rationale": "The isolated reference fixture has no normative policy or consumer changes; accept this exact test candidate.",
            "evidence": [evidence(root)],
        }
        for owner in ("consumer", "impact", "audit")
    ]


class AgentWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="standards-workflow-")
        cls.root = Path(cls.temporary.name) / "repository"
        prepare_repository(cls.root)
        cls.engine = StandardsEngine.open_repository(
            cls.root,
            execution_context=AnalysisExecutionContext(
                LocalAlwaysAllowAuthorizer(cls.root)
            ),
        )
        cls.facade = AgentToolFacade(cls.engine, _contracts(cls.root))
        result = cls.facade.create_snapshot({"kind": "create-snapshot"})
        assert result["kind"] == "create-snapshot-result", result
        cls.snapshot = result["snapshot"]["snapshot"]

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()
        cls.temporary.cleanup()

    def propose(self, label):
        result = self.facade.propose(
            {
                "snapshot": self.snapshot,
                "change_set": reference_change(self.root, label),
            }
        )
        self.assertEqual(result["status"], "complete", result)
        self.assertEqual(result["context"], result["outcome"]["handle"])
        self.assertEqual(
            {n["operation"] for n in result["next_operations"]}, {"review", "revise"}
        )
        return result

    def test_reference_proposal_composes_analysis_without_review_or_application(self):
        before = subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "main"]
        )
        with (
            patch.object(
                self.engine,
                "review_proposal",
                side_effect=AssertionError("implicit review"),
            ),
            patch.object(
                self.engine,
                "apply_proposal",
                side_effect=AssertionError("implicit apply"),
            ),
        ):
            result = self.propose("ordinary")
        after = subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "main"]
        )
        self.assertEqual(before, after)
        status = self.facade.workflow_status({"context": result["context"]})
        self.assertEqual(status, result)
        self.assertEqual(
            self.facade.apply({"context": result["context"]})["code"],
            "WORKFLOW.OPERATION_NOT_AVAILABLE",
        )

    def test_revision_advancement_does_not_retarget_old_context(self):
        original = self.propose("revision")
        changed = self.facade.revise(
            {
                "context": original["context"],
                "change_set": reference_change(self.root, "revision", revision=True),
            }
        )
        self.assertEqual(changed["status"], "complete", changed)
        self.assertNotEqual(changed["revision"], original["revision"])
        stale = self.facade.workflow_status({"context": original["context"]})
        self.assertEqual(stale["status"], "stale")
        self.assertEqual(stale["revision"], original["revision"])
        denied = self.facade.review(
            {"context": original["context"], "decisions": decisions(self.root)}
        )
        self.assertEqual(denied["code"], "WORKFLOW.OPERATION_NOT_AVAILABLE")
        resumed = self.facade.resume({"context": original["context"]})
        self.assertEqual(resumed["context"], changed["revision"])
        self.assertEqual(resumed["status"], "draft")
        analyzed = self.facade.analyze({"context": resumed["context"]})
        self.assertEqual(analyzed["context"], changed["context"])

    def test_context_is_immutable_existing_identity_and_foreign_records_reject(self):
        created = self.propose("identity")
        for context in (
            {**created["context"], "schema_version": 999},
            {**created["context"], "id": "analysis:sha256:" + "0" * 64},
            {**created["context"], "revision": created["revision"]},
        ):
            self.assertEqual(
                self.facade.workflow_status({"context": context})["kind"],
                "rejected-result",
            )
        with StandardsEngine.open_repository(self.root, durable=False) as foreign:
            facade = AgentToolFacade(foreign, _contracts(self.root))
            self.assertEqual(
                facade.workflow_status({"context": created["context"]})["kind"],
                "rejected-result",
            )

    def test_review_is_explicit_and_current_authorization_is_required(self):
        created = self.propose("review")
        with StandardsEngine.open_repository(self.root) as denied_engine:
            denied = AgentToolFacade(denied_engine, _contracts(self.root)).review(
                {"context": created["context"], "decisions": decisions(self.root)}
            )
            # Opening with no adapter must never manufacture review authority.
            self.assertIn(denied["kind"], ("workflow-result", "rejected-result"))
            outcome = denied.get("outcome", denied)
            self.assertEqual(outcome["kind"], "rejected-result", denied)
        ready = self.facade.review(
            {"context": created["context"], "decisions": decisions(self.root)}
        )
        self.assertEqual(ready["status"], "ready", ready)
        self.assertEqual(ready["context"]["kind"], "readiness-handle")
        self.assertEqual(ready["revision"], created["revision"])
        self.assertEqual(
            self.facade.workflow_status({"context": ready["context"]})["status"],
            "ready",
        )

        # This projection test establishes that an authoritative native result
        # cannot be obscured by a secondary storage outage. Real publication and
        # cold recovery are covered by the MCP client walkthrough.
        from tools.standards_engine.standards_engine.agent_workflow import bind, view

        bound = bind(self.engine, c.ReadinessHandle.from_value(ready["context"]))
        application = {
            "kind": "application-handle",
            "id": "application:sha256:" + "a" * 64,
            "schema_version": 1,
        }
        outcomes = [
            c.ApplyProposalResult.from_value(
                {
                    "kind": "apply-proposal-result",
                    "application": application,
                    "status": "applied",
                }
            ),
            c.RecoverApplicationResult.from_value(
                {
                    "kind": "recover-application-result",
                    "application": application,
                    "status": "applied",
                }
            ),
            c.ApplicationRecoveryRequiredResult.from_value(
                {
                    "kind": "application-recovery-required-result",
                    "application": application,
                    "status": "recovery-required",
                    "code": "APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE",
                    "outcome": "unavailable",
                    "message": "Fixture interrupted outcome recording",
                }
            ),
        ]
        with patch.object(
            self.engine._authoring,
            "read_selected_application",
            side_effect=AssertionError("secondary store read"),
        ):
            for outcome in outcomes:
                projected = view(self.engine, bound, outcome)
                self.assertEqual(projected.status, outcome.status)
                self.assertEqual(projected.outcome.as_contract(), outcome.as_contract())

    def test_analysis_rejection_retains_the_created_revision(self):
        failure = c.RejectedResult.from_value(
            {
                "kind": "rejected-result",
                "code": "ANALYSIS.FIXTURE_UNAVAILABLE",
                "outcome": "unavailable",
                "message": "Fixture unavailable",
                "details": {},
                "next_operations": [],
            }
        )
        with patch.object(self.engine, "analyze_proposal", return_value=failure):
            result = self.facade.propose(
                {
                    "snapshot": self.snapshot,
                    "change_set": reference_change(self.root, "partial"),
                }
            )
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["context"], result["revision"])
        self.assertEqual(result["outcome"], failure.as_contract())
        status = self.facade.workflow_status({"context": result["context"]})
        self.assertEqual(status["status"], "draft")

    def test_normative_proposal_stops_at_real_pending_work(self):
        change = reference_change(self.root, "normative")
        change["edits"][0]["standard"].update(
            id="topic.agent-workflow-fixture", role="topic", level="MUST"
        )
        change["edits"][0]["standard"]["body"] = (
            "This isolated fixture requires an explicit semantic impact decision.\n"
        )
        result = self.facade.propose({"snapshot": self.snapshot, "change_set": change})
        self.assertEqual(result["status"], "needs-action", result)
        self.assertEqual(result["outcome"]["kind"], "pending-result")
        self.assertTrue(
            result["outcome"]["fact_requirements"] or result["outcome"]["obligations"]
        )
        self.assertNotIn("review", {n["operation"] for n in result["next_operations"]})
        invalid = self.facade.review(
            {"context": result["context"], "decisions": decisions(self.root)}
        )
        self.assertEqual(invalid["code"], "WORKFLOW.OPERATION_NOT_AVAILABLE")
        obligation = result["outcome"]["obligations"][0]
        submission = {
            "kind": "impact-disposition",
            "obligation": obligation["handle"],
            "result": "confirmed",
            "rationale": "The isolated fixture adds one standalone normative module; its new scope is explicitly acknowledged by this test owner.",
            "evidence": [evidence(self.root)],
            "fingerprint": obligation["fingerprint"],
        }
        bad = {
            **submission,
            "evidence": [{**evidence(self.root), "digest": "sha256:" + "0" * 64}],
        }
        rejected = self.facade.resolve_workflow(
            {"context": result["context"], "submission": bad}
        )
        self.assertEqual(rejected["outcome"]["kind"], "rejected-result")
        self.assertEqual(rejected["context"], result["context"])
        resolved = self.facade.resolve_workflow(
            {"context": result["context"], "submission": submission}
        )
        self.assertEqual(resolved["status"], "complete", resolved)
        self.assertNotEqual(resolved["context"], result["context"])
        changed = self.facade.resolve_workflow(
            {
                "context": result["context"],
                "submission": {**submission, "result": "requires-change"},
            }
        )
        self.assertEqual(changed["status"], "requires-change", changed)
        self.assertEqual(
            [n["operation"] for n in changed["next_operations"]], ["revise"]
        )


if __name__ == "__main__":
    unittest.main()
