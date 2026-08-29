from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisExecutionContext,
    AuthorityEvidence,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    C7ProviderUnavailable,
    EvidenceContractKey,
    FactProviderContract,
    ProviderInputRole,
    ProviderAuthority,
    ProviderNoObservation,
    ProviderObservationClaim,
    ResolvedEvidence,
)
from tools.standards_authority.standards_authority import (
    AuthorityHandle,
    AuthorityRepository,
    MemoryObjectStore,
)
from tools.standards_engine.standards_engine.engine import _codec_sets
from tools.standards_engine.standards_engine import (
    AnalysisRequest,
    ConsumerDispositionSubmission,
    CoverageAttestationSubmission,
    InspectCall,
    ProvideFactSubmission,
    RejectedResult,
    StandardsEngine,
)
from tools.standards_metadata.standards_metadata import (
    load_canonical_standards_corpus,
)
from tools.standards_verifier.standards_verifier.suite_inputs import (
    write_suite_input_projection,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY = "workflow.planning.written-plan-applicability"
FACT_A = "change.fixture-a"
FACT_B = "change.fixture-b"


def _evidence(identifier: str, provider: str = "repository-content") -> AuthorityEvidence:
    content = identifier.encode("utf-8")
    return AuthorityEvidence(
        provider,
        "1",
        identifier,
        "sha256:" + hashlib.sha256(content).hexdigest(),
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
            "grant.fixture",
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (ResolvedEvidence(_evidence("authorization"), b"authorization"),),
            (ResolvedEvidence(_evidence("revocation"), b"revocation"),),
            "not-revoked",
            "allow",
        )


class FixtureProvider:
    contract = FactProviderContract(
        "provider.fixture",
        1,
        "analysis-authority-roots.v1",
        "provider.fixture",
        (ProviderInputRole("current", "requirement"),),
    )

    def __init__(self, *, unavailable: bool = False) -> None:
        self.unavailable = unavailable

    def observe(self, request):
        if request.fact != FACT_A:
            return ProviderNoObservation()
        if self.unavailable:
            return C7ProviderUnavailable("Fixture evidence is unavailable.")
        evidence = _evidence(
            "provider-observation", self.contract.evidence_contract
        )
        return ProviderObservationClaim(
            {"type": "boolean", "state": "known", "value": True},
            (ResolvedEvidence(evidence, b"provider-observation"),),
        )


class AnalysisWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.fixture_root = Path(cls.temporary.name) / "conditional"
        _copy_repository(cls.fixture_root)
        _install_conditional_policy(cls.fixture_root)
        cls.repository = _repository()
        cls.engine = StandardsEngine.open_analysis(
            cls.fixture_root,
            cls.fixture_root,
            repository=cls.repository,
            durable=False,
            execution_context=AnalysisExecutionContext(ExactAuthorizer()),
        )
        cls.request = _request(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_fact_requirements_and_observations_are_publicly_inspectable(self) -> None:
        parent = self.engine.prepare(self.request)
        requirement = _requirement(parent, FACT_A)
        requirement_inspection = self.engine.inspect(InspectCall(requirement.handle))
        self.assertEqual(requirement_inspection.kind, "fact-requirement-inspection-result")

        child = self.engine.resolve(
            parent.handle, _fact_submission(requirement, True, "fact-a-evidence")
        )
        state = self.engine.inspect(InspectCall(child.handle))
        self.assertEqual(state.kind, "analysis-state")
        self.assertEqual(len(state.fact_observations), 1)
        observation = state.fact_observations[0]
        self.assertEqual(observation.requirement, requirement.handle)
        self.assertEqual(
            self.engine.inspect(InspectCall(observation.handle)).kind,
            "fact-observation-inspection-result",
        )

        stale = self.engine.resolve(
            child.handle, _fact_submission(requirement, False, "stale-evidence")
        )
        self.assertIsInstance(stale, RejectedResult)
        self.assertEqual(stale.code, "SUBMISSION.NOT_APPLICABLE")

    def test_fact_authority_is_inspectable_from_a_fresh_process(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            _copy_repository(root)
            _install_conditional_policy(root)
            created = _run_fresh_python(
                root,
                """
import json
import sys
from pathlib import Path

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import InspectCall, StandardsEngine
from tools.standards_engine.tests.test_analysis import (
    FACT_A,
    ExactAuthorizer,
    _fact_submission,
    _request,
    _requirement,
)

root = Path(sys.argv[1])
engine = StandardsEngine.open_analysis(
    root,
    root,
    execution_context=AnalysisExecutionContext(ExactAuthorizer()),
)
parent = engine.prepare(_request(engine))
requirement = _requirement(parent, FACT_A)
child = engine.resolve(
    parent.handle,
    _fact_submission(requirement, True, "fresh-process-fact"),
)
state = engine.inspect(InspectCall(child.handle))
handles = (
    (requirement.handle, "fact-requirement-inspection-result"),
    (state.fact_observations[0].handle, "fact-observation-inspection-result"),
)
print(json.dumps({
    "view": engine.view.as_contract(),
    "analysis_views": [item.as_contract() for item in engine.analysis_views],
    "handles": [
        {"handle": handle.as_contract(), "expected": expected}
        for handle, expected in handles
    ],
}))
""",
            )
            store_path = Path(temporary) / "authority.sqlite3"
            shutil.move(root / ".standards-engine" / "authority.sqlite3", store_path)
            shutil.rmtree(root)
            inspected = _run_fresh_python(
                store_path,
                """
import json
import sys
from pathlib import Path

from tools.standards_engine.standards_engine import (
    InspectCall,
    StandardsAuthorityViewHandle,
    StandardsEngine,
)

store_path = Path(sys.argv[1])
requested = json.loads(sys.stdin.read())
engine = StandardsEngine.open_persisted(
    store_path,
    StandardsAuthorityViewHandle.from_value(requested["view"]),
    analysis_views=tuple(
        StandardsAuthorityViewHandle.from_value(item)
        for item in requested["analysis_views"]
    ),
)
print(json.dumps([
    engine.inspect(InspectCall.from_value({"handle": item["handle"]})).kind
    for item in requested["handles"]
]))
""",
                input_value=created,
            )

            expected = [
                item["expected"] for item in json.loads(created)["handles"]
            ]
            self.assertEqual(json.loads(inspected), expected)

    def test_decision_order_normalizes_and_dormant_observations_survive(self) -> None:
        def transition(order: tuple[str, str], values: dict[str, bool]):
            result = self.engine.prepare(self.request)
            for fact in order:
                requirement = _requirement(result, fact)
                result = self.engine.resolve(
                    result.handle,
                    _fact_submission(
                        requirement,
                        values[fact],
                        f"evidence.{fact}",
                    ),
                )
            return result, self.engine.inspect(InspectCall(result.handle))

        false_values = {FACT_A: False, FACT_B: False}
        left, left_state = transition((FACT_B, FACT_A), false_values)
        right, right_state = transition((FACT_A, FACT_B), false_values)

        self.assertEqual(left.handle, right.handle)
        self.assertEqual(left.as_contract(), right.as_contract())
        self.assertEqual(len(left_state.fact_observations), 2)
        self.assertEqual(left_state.as_contract(), right_state.as_contract())
        self.assertEqual(left.fact_requirements, ())

        dormant, dormant_state = transition(
            (FACT_B, FACT_A), {FACT_A: True, FACT_B: False}
        )
        self.assertEqual(dormant.fact_requirements, ())
        self.assertEqual(len(dormant_state.fact_observations), 2)

    def test_provider_claim_is_canonical_and_unavailability_is_typed(self) -> None:
        views = tuple(_view_handle(item) for item in self.engine.analysis_views)
        provider_engine = StandardsEngine(
            self.repository,
            _view_handle(self.engine.view),
            views,
            AnalysisExecutionContext(ExactAuthorizer(), (FixtureProvider(),)),
        )
        result = provider_engine.prepare(self.request)
        state = provider_engine.inspect(InspectCall(result.handle))
        self.assertEqual(len(state.fact_observations), 1)
        self.assertIn(
            "provider_authority",
            state.fact_observations[0].as_contract(),
        )
        provider_reference = state.fact_observations[0].provider_authority
        provider_authority = self.repository.resolve(
            AuthorityHandle(provider_reference.object_kind, provider_reference.id)
        ).value
        self.assertIsInstance(provider_authority, ProviderAuthority)
        self.assertEqual(
            tuple((item.side, item.role) for item in provider_authority.inputs),
            (("current", "requirement"),),
        )

        unavailable_engine = StandardsEngine(
            self.repository,
            _view_handle(self.engine.view),
            views,
            AnalysisExecutionContext(
                ExactAuthorizer(), (FixtureProvider(unavailable=True),)
            ),
        )
        unavailable = unavailable_engine.prepare(self.request)
        self.assertIsInstance(unavailable, RejectedResult)
        self.assertEqual(unavailable.code, "FACT.PROVIDER_UNAVAILABLE")
        self.assertEqual(unavailable.outcome, "unavailable")

    def test_consumer_disposition_is_fingerprint_bound_and_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            proposed = Path(temporary) / "proposed"
            _copy_repository(proposed)
            _install_semantic_change(proposed)
            write_suite_input_projection(proposed)
            engine = StandardsEngine.open_analysis(
                REPO_ROOT,
                proposed,
                durable=False,
                execution_context=AnalysisExecutionContext(ExactAuthorizer()),
            )
            request = _semantic_request(engine, proposed)
            result = engine.prepare(request)
            while not any(
                item.kind == "consumer-review" and item.state == "required"
                for item in result.obligations
            ):
                coverage = next(
                    item
                    for item in result.obligations
                    if item.kind == "coverage-audit" and item.state == "required"
                )
                result = engine.resolve(
                    result.handle,
                    _coverage_submission(coverage, f"coverage.{coverage.target}"),
                )

            obligation = next(
                item
                for item in result.obligations
                if item.kind == "consumer-review" and item.state == "required"
            )
            wrong = obligation.fingerprint.as_contract()
            wrong["dependencies"][0]["identity"] = "wrong.dependency"
            rejected = engine.resolve(
                result.handle,
                _consumer_submission(obligation, wrong, "wrong-fingerprint"),
            )
            self.assertIsInstance(rejected, RejectedResult)
            self.assertEqual(rejected.code, "SUBMISSION.CONTEXT_MISMATCH")

            successor = engine.resolve(
                result.handle,
                _consumer_submission(
                    obligation,
                    obligation.fingerprint.as_contract(),
                    "consumer-evidence",
                ),
            )
            state = engine.inspect(InspectCall(successor.handle))
            self.assertEqual(
                {item.obligation_id for item in state.dispositions},
                {obligation.id},
            )


def _copy_repository(target: Path) -> None:
    shutil.copytree(
        REPO_ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )


def _replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if content.count(old) != 1:
        raise AssertionError(f"fixture edit did not match exactly once: {path}")
    path.write_text(content.replace(old, new), encoding="utf-8")


def _fact(identifier: str) -> str:
    return f'''\n[[facts]]
id = "{identifier}"
semantic_revision = 1
type = "boolean"
nullable = false
aliases = []
meaning = "Whether {identifier} applies to this standards change."
context_kind = "standards-change"
answer_contract = "fact-value.v1"
evidence_contract = "evidence-reference.v1"
authorization_capability = "standards.analyze"
prompt = "Does {identifier} apply?"
'''


def _install_conditional_policy(root: Path) -> None:
    facts = root / "evaluation/standards-effectiveness/policy-impact-facts.toml"
    facts.write_text(
        'schema_version = 1\nid = "policy-impact.applicability"\n'
        + _fact(FACT_A)
        + _fact(FACT_B),
        encoding="utf-8",
    )
    declaration = (
        root
        / "evaluation/standards-effectiveness/policy-impact/workflow.planning.toml"
    )
    old = f'''source = "{POLICY}"
consumer = "router"
relation = "router-projection"
applicability = {{ operator = "always" }}'''
    new = f'''source = "{POLICY}"
consumer = "router"
relation = "router-projection"
applicability = {{ operator = "any", expressions = [{{ operator = "equals", fact = "{FACT_A}", value = true }}, {{ operator = "equals", fact = "{FACT_B}", value = true }}] }}'''
    _replace_once(declaration, old, new)


def _install_semantic_change(root: Path) -> None:
    _replace_once(
        root / "workflows/planning.md",
        "A boundary\nor file category alone does not satisfy this condition.",
        "A boundary\nor file category alone does not satisfy this condition. The reviewed fixture adds one semantic sentence.",
    )


def _repository() -> AuthorityRepository:
    return AuthorityRepository(MemoryObjectStore(), _codec_sets())


def _run_fresh_python(
    root: Path, script: str, *, input_value: str | None = None
) -> str:
    environment = dict(os.environ)
    environment.update(
        {
            "PYTHONPATH": str(REPO_ROOT),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    completed = subprocess.run(
        (sys.executable, "-P", "-c", script, str(root)),
        cwd=REPO_ROOT,
        env=environment,
        input=input_value,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(
            f"fresh Python process failed ({completed.returncode}):\n"
            f"{completed.stderr}"
        )
    return completed.stdout.strip()


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


def _semantic_request(engine: StandardsEngine, proposed_root: Path) -> AnalysisRequest:
    base, proposed = engine.analysis_views
    unit = load_canonical_standards_corpus(
        proposed_root
    ).policy_unit_corpus.active_by_id(POLICY)
    assert unit is not None
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
            "semantic_proposals": [
                {
                    "policy": POLICY,
                    "accepted_semantic_revision": 1,
                    "proposed_semantic_revision": 2,
                    "intent": "Exercise one reviewed semantic change.",
                    "structural_digest": unit.structural_digest,
                }
            ],
            "contract_version": 3,
        }
    )


def _requirement(result, fact: str):
    return next(
        item.requirement
        for item in result.fact_requirements
        if item.requirement.fact == fact
    )


def _fact_submission(requirement, value: bool, evidence_id: str):
    evidence = _evidence(evidence_id)
    return ProvideFactSubmission.from_value(
        {
            "kind": "provide-fact",
            "requirement": requirement.handle.as_contract(),
            "value": {"type": "boolean", "state": "known", "value": value},
            "evidence": [_evidence_contract(evidence)],
        }
    )


def _coverage_submission(obligation, evidence_id: str):
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
                "evidence": [_evidence_contract(evidence)],
                "explicit_exclusions": [],
                "rationale": "The exact bounded consumer horizon was reviewed.",
                "auditor_provenance": "principal.fixture",
            },
        }
    )


def _consumer_submission(obligation, fingerprint, evidence_id: str):
    evidence = _evidence(evidence_id)
    return ConsumerDispositionSubmission.from_value(
        {
            "kind": "consumer-disposition",
            "obligation_id": obligation.id,
            "result": "reviewed-no-change",
            "rationale": "The selected consumer was reviewed against the change.",
            "evidence": [_evidence_contract(evidence)],
            "fingerprint": fingerprint,
        }
    )


def _evidence_contract(value: AuthorityEvidence) -> dict[str, object]:
    return {
        "id": value.id,
        "digest": value.digest,
        "provider_contract": value.provider_contract,
        "provider_contract_version": value.provider_contract_version,
    }


if __name__ == "__main__":
    unittest.main()
