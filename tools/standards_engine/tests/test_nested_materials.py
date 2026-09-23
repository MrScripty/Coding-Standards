"""Real proposal composition with operation-scoped immutable material reuse."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine.logical_authoring import StandardsChangeSet
from tools.standards_engine.standards_engine.operation_materials import ProposalMaterials
from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer, _contracts
from tools.standards_engine.tests.test_agent_workflow import (
    evidence, prepare_repository, reference_change,
)
from tools.standards_metadata.standards_metadata import RecordingContentSource


class NestedMaterialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="standards-nested-")
        cls.root = Path(cls.temporary.name) / "repository"
        prepare_repository(cls.root)
        cls.engine = StandardsEngine.open_repository(
            cls.root, purpose="authoring",
            execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(cls.root)),
        )
        cls.facade = AgentToolFacade(cls.engine, _contracts(cls.root))
        captured = cls.facade.create_snapshot({"kind": "create-snapshot"})
        assert captured["kind"] == "create-snapshot-result", captured
        cls.snapshot = captured["snapshot"]["snapshot"]

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()
        cls.temporary.cleanup()

    def change(self, suffix="", *, revision=False, normative=False):
        label = self._testMethodName.removeprefix("test_").replace("_", "-") + suffix
        value = reference_change(self.root, label, revision=revision)
        if normative:
            value["edits"][0]["standard"].update(
                id="topic." + label, role="topic", level="MUST",
                body="This isolated normative fixture has an explicit impact decision.\n",
            )
        return value

    def propose(self, *, suffix="", normative=False):
        result = self.facade.propose({
            "snapshot": self.snapshot, "change_set": self.change(suffix, normative=normative),
        })
        self.assertEqual(result["status"], "needs-action" if normative else "complete", result)
        return result

    def submission(self, proposed):
        obligation = proposed["outcome"]["obligations"][0]
        return {
            "kind": "impact-disposition", "obligation": obligation["handle"],
            "result": "confirmed", "rationale": "The isolated scope was reviewed.",
            "evidence": [evidence(self.root)], "fingerprint": obligation["fingerprint"],
        }

    @contextmanager
    def counts(self):
        with (
            patch.object(self.engine._snapshots, "load_content", wraps=self.engine._snapshots.load_content) as load,
            patch.object(self.engine, "_compiled_snapshot", wraps=self.engine._compiled_snapshot) as compiled,
            patch.object(self.engine, "_proposal_projection", wraps=self.engine._proposal_projection) as project,
            patch.object(self.engine, "_evaluate", wraps=self.engine._evaluate) as evaluate,
        ):
            yield load, compiled, project, evaluate

    def assert_counts(self, counts, *, projections=1, evaluations=1):
        load, compiled, project, evaluate = counts
        self.assertEqual(load.call_count, 1)
        self.assertEqual(compiled.call_count, 1)
        self.assertEqual(project.call_count, projections)
        self.assertEqual(evaluate.call_count, evaluations)

    def test_propose_shares_validation_and_analysis_material(self):
        with self.counts() as counts:
            proposed = self.propose()
        self.assert_counts(counts)
        self.assertEqual(proposed["context"], proposed["outcome"]["handle"])
        self.assertEqual(self.facade.workflow_status({"context": proposed["context"]}), proposed)

    def test_revise_compiles_only_old_and_new_projections(self):
        proposed = self.propose()
        with self.counts() as counts:
            revised = self.facade.revise({
                "context": proposed["context"], "change_set": self.change(revision=True),
            })
        self.assertEqual(revised["status"], "complete", revised)
        self.assert_counts(counts, projections=2, evaluations=2)
        self.assertNotEqual(revised["revision"], proposed["revision"])
        self.assertEqual(self.facade.workflow_status({"context": proposed["context"]})["status"], "stale")
        target = self.change()["edits"][0]["standard"]["id"]
        old = self.facade.query_proposal({"revision": proposed["revision"], "request": {"kind": "read", "target": target}})
        new = self.facade.query_proposal({"revision": revised["revision"], "request": {"kind": "read", "target": target}})
        self.assertNotIn("Revised fixture text.", old["content"])
        self.assertIn("Revised fixture text.", new["content"])

    def test_resolution_reuses_material_with_three_fresh_evaluations(self):
        proposed = self.propose(normative=True)
        with self.counts() as counts:
            resolved = self.facade.resolve_workflow({
                "context": proposed["context"], "submission": self.submission(proposed),
            })
        self.assertEqual(resolved["status"], "complete", resolved)
        self.assert_counts(counts, evaluations=3)
        self.assertNotEqual(resolved["context"], proposed["context"])

    def test_bad_evidence_is_rejected_and_next_call_observes_new_evidence(self):
        proposed = self.propose(normative=True)
        submission = self.submission(proposed)
        bad = {**submission, "evidence": [{**evidence(self.root), "digest": "sha256:" + "0" * 64}]}
        with self.counts() as counts:
            rejected = self.facade.resolve_workflow({"context": proposed["context"], "submission": bad})
        self.assertEqual(rejected["outcome"]["kind"], "rejected-result", rejected)
        self.assertEqual(rejected["context"], proposed["context"])
        self.assert_counts(counts, evaluations=2)
        with self.counts() as fresh:
            resolved = self.facade.resolve_workflow({"context": proposed["context"], "submission": submission})
        self.assertEqual(resolved["status"], "complete", resolved)
        self.assert_counts(fresh, evaluations=3)

    def test_quarantine_during_authorization_blocks_reused_material(self):
        proposed = self.propose(normative=True)
        authorize = self.engine._execution_context.authorization.authorize
        snapshot = self.engine._snapshot_id(c.SnapshotHandle.from_value(self.snapshot))

        def quarantine(request):
            decision = authorize(request)
            self.engine._snapshots.delete_snapshot(snapshot)
            return decision

        try:
            with patch.object(self.engine._execution_context.authorization, "authorize", side_effect=quarantine):
                result = self.facade.resolve_workflow({
                    "context": proposed["context"], "submission": self.submission(proposed),
                })
            outcome = result.get("outcome", result)
            self.assertEqual(outcome["kind"], "rejected-result", result)
            self.assertEqual(outcome["outcome"], "unavailable")
        finally:
            self.engine._snapshots.undelete_snapshot(snapshot)
        self.assertEqual(self.facade.workflow_status({"context": proposed["context"]})["status"], "needs-action")

    def test_head_change_after_preflight_still_rejects_stale_revision(self):
        proposed = self.propose()
        revise = self.engine._authoring.revise_proposal
        competitor = self.change(revision=True)
        competitor["edits"][0]["standard"]["body"] += "Competing revision.\n"

        def advance_head(expected, change_set, *, preparation):
            revise(expected, StandardsChangeSet.from_mapping(competitor), preparation=preparation)
            return revise(expected, change_set, preparation=preparation)

        with patch.object(self.engine._authoring, "revise_proposal", side_effect=advance_head):
            result = self.facade.revise({"context": proposed["context"], "change_set": self.change(revision=True)})
        self.assertEqual(result["outcome"]["code"], "AUTHORING.REVISION_STALE", result)
        self.assertEqual(self.facade.workflow_status({"context": proposed["context"]})["status"], "stale")

    def test_analyze_and_query_each_start_with_fresh_material(self):
        proposed = self.propose()
        with self.counts() as counts:
            analyzed = self.facade.analyze({"context": proposed["revision"]})
        self.assertEqual(analyzed["context"], proposed["context"])
        self.assert_counts(counts)
        with self.counts() as fresh:
            queried = self.facade.query_proposal({
                "revision": proposed["revision"],
                "request": {"kind": "read", "target": self.change()["edits"][0]["standard"]["id"]},
            })
        self.assertEqual(queried["kind"], "proposal-read-result", queried)
        self.assert_counts(fresh, evaluations=0)

    def test_nested_public_reentry_has_independent_operation_material(self):
        first = self.propose(suffix="-first")
        second = self.propose(suffix="-second")
        project = self.engine._proposal_projection
        nested = []
        entered = False

        def reenter(revision, accepted=None):
            nonlocal entered
            if not entered:
                entered = True
                nested.append(self.facade.analyze_proposal({"revision": second["revision"]}))
            return project(revision, accepted)

        with patch.object(self.engine._snapshots, "load_content", wraps=self.engine._snapshots.load_content) as loads:
            with patch.object(self.engine, "_proposal_projection", side_effect=reenter):
                outer = self.facade.analyze({"context": first["revision"]})
        self.assertEqual(loads.call_count, 2)
        self.assertEqual(outer["context"], first["context"])
        self.assertEqual(nested[0]["handle"], second["context"])

    def test_scope_releases_material_after_success_and_exception(self):
        exited = []
        exit_scope = ProposalMaterials.__exit__

        def observe(scope, *args):
            exit_scope(scope, *args)
            exited.append((scope._base, scope._projection))

        with patch.object(ProposalMaterials, "__exit__", observe):
            with patch.object(self.engine, "_proposal_projection", side_effect=RuntimeError("compiler fixture")):
                with self.assertRaisesRegex(RuntimeError, "compiler fixture"):
                    self.propose(suffix="-failed")
            self.propose(suffix="-success")
        self.assertEqual(exited, [(None, None), (None, None)])

    def test_implicit_capture_keeps_independent_record_and_replay_passes(self):
        sources = []
        compile_source = self.engine._compile

        def compile(source):
            sources.append(source)
            return compile_source(source)

        with patch.object(self.engine, "_compile", side_effect=compile):
            result = self.facade.propose({"change_set": self.change()})
        self.assertEqual(result["status"], "complete", result)
        recorders = [source for source in sources if isinstance(source, RecordingContentSource)]
        self.assertEqual(len(recorders), 2)
        self.assertIsNot(recorders[0], recorders[1])
        self.assertEqual(recorders[0].requested_paths, recorders[1].requested_paths)

    def test_public_application_cannot_reach_authoring_reuse(self):
        with StandardsEngine.open_repository(self.root, purpose="application") as application:
            facade = AgentToolFacade(application, _contracts(self.root))
            with patch.object(ProposalMaterials, "__init__", side_effect=AssertionError("authoring preparation")):
                denied = facade.propose({"snapshot": self.snapshot, "change_set": self.change()})
        self.assertEqual(denied["kind"], "application-rejected-result", denied)


if __name__ == "__main__":
    unittest.main()
