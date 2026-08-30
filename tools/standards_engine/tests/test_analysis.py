from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    EvidenceContractKey,
    EvidenceReference,
    ResolvedEvidence,
)
from tools.standards_engine.standards_engine import (
    AnalysisChildInspectionResult,
    AnalysisInspectionResult,
    CreateSnapshotCall,
    InspectCall,
    PendingResult,
    PrepareCall,
    RejectedResult,
    ResolveCall,
    StandardsEngine,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY = "workflow.planning.written-plan-applicability"


def _reference(identifier: str) -> EvidenceReference:
    content = identifier.encode("utf-8")
    return EvidenceReference(
        identifier,
        "sha256:" + hashlib.sha256(content).hexdigest(),
        "repository-content",
        "1",
    )


class ExactAuthorizer:
    contract = AuthorizationAuthorityContract(
        "issuer.fixture",
        1,
        "principal.fixture",
        "authorization-grant.v1",
        (EvidenceContractKey("repository-content", "1"),),
        "revocation.fixture",
        1,
        "authorization-revocation.v1",
        (EvidenceContractKey("repository-content", "1"),),
    )

    def authorize(self, request):
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (ResolvedEvidence(_reference("authorization"), b"authorization"),),
            (ResolvedEvidence(_reference("revocation"), b"revocation"),),
            "not-revoked",
            "allow",
        )


class AnalysisWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.store = Path(cls.temporary.name) / "standards.sqlite3"
        cls.engine = StandardsEngine.open_repository(
            REPO_ROOT,
            store_path=cls.store,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        created = cls.engine.create_snapshot(
            CreateSnapshotCall.from_value({"kind": "create-snapshot"})
        )
        cls.snapshot = created.snapshot.snapshot

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.close()
        cls.temporary.cleanup()

    def test_prepare_persists_parent_bound_public_work(self) -> None:
        result = self.prepare()

        self.assertIsInstance(result, PendingResult)
        self.assertTrue(result.obligations)
        for obligation in result.obligations:
            self.assertEqual(obligation.handle.analysis, result.handle)
        for operation in result.next_operations:
            if operation.operation == "resolve":
                self.assertEqual(operation.analysis, result.handle)

        state = self.engine.inspect(InspectCall(result.handle))
        self.assertIsInstance(state, AnalysisInspectionResult)
        self.assertEqual(state.state.handle, result.handle)

        child = self.engine.inspect(
            InspectCall(result.obligations[0].handle)
        )
        self.assertIsInstance(child, AnalysisChildInspectionResult)
        self.assertEqual(child.handle.analysis, result.handle)

    def test_equal_transition_is_idempotent_and_different_evidence_branches(self) -> None:
        parent = self.prepare()
        first_call = self.disposition_submission(parent, "review-evidence-one")

        first = self.engine.resolve(first_call)
        repeated = self.engine.resolve(first_call)
        second = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence-two")
        )

        self.assertEqual(first.handle, repeated.handle)
        self.assertNotEqual(first.handle, second.handle)
        self.assertEqual(parent.handle, first_call.analysis)

    def test_resolved_parent_work_is_not_applicable_to_child(self) -> None:
        parent = self.prepare()
        submission = self.disposition_submission(parent, "review-evidence")
        child = self.engine.resolve(submission)

        stale = self.engine.resolve(
            ResolveCall.from_value(
                {
                    "analysis": child.handle.as_contract(),
                    "submission": submission.submission.as_contract(),
                }
            )
        )

        self.assertIsInstance(stale, RejectedResult)
        self.assertEqual(stale.code, "SUBMISSION.NOT_APPLICABLE")

    def test_prior_analysis_reuses_the_same_valid_decision(self) -> None:
        parent = self.prepare()
        child = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence")
        )

        reused = self.prepare(prior=child.handle.as_contract())

        self.assertEqual(reused.handle, child.handle)

    def test_state_and_children_are_inspectable_in_a_fresh_process(self) -> None:
        parent = self.prepare()
        child = self.engine.resolve(
            self.disposition_submission(parent, "review-evidence")
        )
        root_handle = child.handle.as_contract()
        child_handle = child.obligations[0].handle.as_contract()
        script = """
import json
import sys
from pathlib import Path

from tools.standards_engine.standards_engine import InspectCall, StandardsEngine

request = json.loads(sys.stdin.read())
engine = StandardsEngine.open_repository(
    Path(request["root"]), store_path=Path(request["store"])
)
try:
    result = [
        engine.inspect(InspectCall.from_value({"handle": handle})).as_contract()
        for handle in request["handles"]
    ]
    print(json.dumps(result, sort_keys=True))
finally:
    engine.close()
"""
        environment = dict(os.environ)
        environment.update(
            {
                "PYTHONPATH": str(REPO_ROOT),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        completed = subprocess.run(
            (sys.executable, "-P", "-c", script),
            cwd=REPO_ROOT,
            env=environment,
            input=json.dumps(
                {
                    "root": str(REPO_ROOT),
                    "store": str(self.store),
                    "handles": [root_handle, child_handle],
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        inspected = json.loads(completed.stdout)
        self.assertEqual(inspected[0]["kind"], "analysis-inspection-result")
        self.assertEqual(inspected[1]["kind"], "analysis-child-inspection-result")

    def prepare(self, *, prior: dict[str, object] | None = None):
        request: dict[str, object] = {
            "kind": "analysis-request",
            "base_snapshot": self.snapshot.as_contract(),
            "proposed_snapshot": self.snapshot.as_contract(),
            "changes": [
                {
                    "kind": "modification",
                    "accepted_ids": [POLICY],
                    "proposed_ids": [POLICY],
                    "scope": {"kind": "whole-artifact"},
                }
            ],
            "semantic_proposals": [],
            "contract_version": 4,
        }
        if prior is not None:
            request["prior_analysis"] = prior
        return self.engine.prepare(
            PrepareCall.from_value({"request": request})
        )

    @staticmethod
    def disposition_submission(result, evidence_id: str) -> ResolveCall:
        operation = next(
            item
            for item in result.next_operations
            if item.request_kind == "consumer-disposition"
        )
        obligation = next(
            item for item in result.obligations if item.handle == operation.work
        )
        evidence = _reference(evidence_id)
        return ResolveCall.from_value(
            {
                "analysis": result.handle.as_contract(),
                "submission": {
                    "kind": "consumer-disposition",
                    "obligation": operation.work.as_contract(),
                    "result": "reviewed-no-change",
                    "rationale": "The exact selected consumer was reviewed.",
                    "evidence": [evidence.as_contract()],
                    "fingerprint": obligation.fingerprint.as_contract(),
                },
            }
        )

if __name__ == "__main__":
    unittest.main()
