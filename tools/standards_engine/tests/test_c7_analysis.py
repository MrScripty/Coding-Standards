from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    ANALYSIS_CODECS,
    AnalysisExecutionContext,
    AuthorityEvidence,
    AuthorizationClaim,
    ResolvedEvidence,
)
from tools.standards_authority.standards_authority import (
    AUTHORITY_CODECS,
    AuthorityHandle,
    AuthorityRepository,
    MemoryObjectStore,
    SQLiteObjectStore,
)
from tools.standards_engine.standards_engine import (
    ENGINE_CODECS,
    AnalysisRequest,
    ConsumerDispositionSubmission,
    CoverageAttestationSubmission,
    InspectCall,
    StandardsEngine,
)
from tools.standards_graph.standards_graph import STANDARDS_GRAPH_CODECS
from tools.standards_metadata.standards_metadata import METADATA_CODECS
from tools.standards_policy_impact.standards_policy_impact import (
    POLICY_IMPACT_CODECS,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY = "workflow.commit.commit-message"


def _evidence(identifier: str) -> AuthorityEvidence:
    content = identifier.encode("utf-8")
    return AuthorityEvidence(
        "fixture.evidence",
        "1",
        identifier,
        "sha256:" + hashlib.sha256(content).hexdigest(),
    )


class ExactAuthorizer:
    def authorize(self, request):
        return AuthorizationClaim(
            "issuer.fixture",
            1,
            "grant.fixture",
            "principal.fixture",
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (ResolvedEvidence(_evidence("authorization"), b"authorization"),),
            "revocation.fixture",
            1,
            (ResolvedEvidence(_evidence("revocation"), b"revocation"),),
        )


class C7AnalysisLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = _repository(MemoryObjectStore())
        cls.engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            repository=cls.repository,
            durable=False,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        cls.request = _request(cls.engine)

    def test_prepare_and_authorized_transition_are_deterministic(self) -> None:
        parent = self.engine.prepare(self.request)
        self.assertEqual(parent.kind, "pending-result")

        first = _complete(self.engine, parent, "deterministic")
        second = _complete(self.engine, parent, "deterministic")

        self.assertEqual(first.kind, "complete-result")
        self.assertEqual(first.handle, second.handle)
        self.assertEqual(first.as_contract(), second.as_contract())
        self.assertEqual(len(first.coverage_certificates), 1)

    def test_different_valid_decisions_form_independent_branches(self) -> None:
        parent = self.engine.prepare(self.request)
        first = _complete(self.engine, parent, "branch-one")
        second = _complete(self.engine, parent, "branch-two")

        self.assertEqual(first.kind, "complete-result")
        self.assertEqual(second.kind, "complete-result")
        self.assertNotEqual(first.handle, second.handle)
        self.assertEqual(
            self.engine.inspect(InspectCall(handle=parent.handle)).kind,
            "analysis-state",
        )

    def test_missing_authorization_publishes_no_successor(self) -> None:
        parent = self.engine.prepare(self.request)
        unavailable = StandardsEngine(
            self.repository,
            _view_handle(self.engine.view),
            tuple(_view_handle(item) for item in self.engine.analysis_views),
        )
        result = unavailable.resolve(
            parent.handle, _submission_for_first(parent, "unavailable")
        )

        self.assertEqual(result.kind, "rejected-result")
        self.assertEqual(result.code, "ANALYSIS.AUTHORIZATION_UNAVAILABLE")
        self.assertEqual(result.outcome, "unavailable")
        self.assertEqual(
            self.engine.inspect(InspectCall(handle=parent.handle)).kind,
            "analysis-state",
        )

    def test_cold_sqlite_reuses_exact_prior_state_without_live_trust(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            with SQLiteObjectStore(path) as store:
                repository = _repository(store)
                engine = StandardsEngine.open_analysis(
                    REPO_ROOT,
                    REPO_ROOT,
                    repository=repository,
                    execution_context=AnalysisExecutionContext(ExactAuthorizer()),
                )
                request = _request(engine)
                parent = engine.prepare(request)
                child = _complete(engine, parent, "cold-replay")
                base, proposed = (
                    _view_handle(item) for item in engine.analysis_views
                )
                current = _view_handle(engine.view)

            with SQLiteObjectStore(path) as reopened:
                cold = StandardsEngine(
                    _repository(reopened), current, (base, proposed)
                )
                replay = cold.prepare(
                    AnalysisRequest.from_value(
                        {
                            **request.as_contract(),
                            "prior_analysis": child.handle.as_contract(),
                        }
                    )
                )

            self.assertEqual(replay.kind, "complete-result")
            self.assertEqual(replay.handle, child.handle)
            self.assertEqual(replay.as_contract(), child.as_contract())


def _repository(store) -> AuthorityRepository:
    return AuthorityRepository(
        store,
        (
            AUTHORITY_CODECS,
            METADATA_CODECS,
            POLICY_IMPACT_CODECS,
            STANDARDS_GRAPH_CODECS,
            ANALYSIS_CODECS,
            ENGINE_CODECS,
        ),
    )


def _view_handle(value) -> AuthorityHandle:
    return AuthorityHandle("standards-authority-view", value.id)


def _request(engine: StandardsEngine) -> AnalysisRequest:
    base, proposed = engine.analysis_views
    return AnalysisRequest.from_value(
        {
            "kind": "analysis-request",
            "base_view": base.as_contract(),
            "proposed_view": proposed.as_contract(),
            "changes": [
                {
                    "kind": "modification",
                    "accepted_ids": [POLICY],
                    "proposed_ids": [POLICY],
                    "scope": {"kind": "whole-artifact"},
                }
            ],
            "semantic_proposals": [],
            "contract_version": 3,
        }
    )


def _consumer_submission(result, evidence_id: str):
    obligation = result.obligations[0]
    evidence = _evidence(evidence_id)
    return ConsumerDispositionSubmission.from_value(
        {
            "kind": "consumer-disposition",
            "obligation_id": obligation.id,
            "result": "reviewed-no-change",
            "rationale": "The selected consumer was reviewed against the change.",
            "evidence": [
                {
                    "id": evidence.id,
                    "digest": evidence.digest,
                    "provider_contract": evidence.provider_contract,
                    "provider_contract_version": evidence.provider_contract_version,
                }
            ],
            "fingerprint": obligation.fingerprint.as_contract(),
        }
    )


def _coverage_submission(result, evidence_id: str):
    obligation = result.obligations[0]
    requirement = next(
        item.identity
        for item in obligation.fingerprint.dependencies
        if item.class_ == "audit"
    )
    evidence = _evidence(evidence_id)
    return CoverageAttestationSubmission.from_value(
        {
            "kind": "coverage-attestation",
            "obligation_id": obligation.id,
            "claim": {
                "requirement": {
                    "kind": "coverage-requirement-handle",
                    "id": requirement,
                    "schema_version": 4,
                },
                "conclusion": "complete",
                "evidence": [
                    {
                        "id": evidence.id,
                        "digest": evidence.digest,
                        "provider_contract": evidence.provider_contract,
                        "provider_contract_version": evidence.provider_contract_version,
                    }
                ],
                "explicit_exclusions": [],
                "rationale": "Exact consumer coverage was reviewed.",
                "auditor_provenance": "principal.fixture",
            },
        }
    )


def _complete(engine: StandardsEngine, result, evidence_id: str):
    current = result
    while current.kind == "pending-result":
        submission = _submission_for_first(current, evidence_id)
        current = engine.resolve(current.handle, submission)
    return current


def _submission_for_first(result, evidence_id: str):
    obligation = result.obligations[0]
    if obligation.kind == "audit-coverage":
        return _coverage_submission(result, f"{evidence_id}.coverage")
    return _consumer_submission(result, f"{evidence_id}.consumer")


if __name__ == "__main__":
    unittest.main()
