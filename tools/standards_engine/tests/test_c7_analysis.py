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
    EvidenceContractKey,
    ResolvedEvidence,
)
from tools.standards_authority.standards_authority import (
    AuthorityHandle,
    AuthorityReference,
    AuthorityRepository,
    decode_envelope,
    ExecutionAuthorityRoot,
    ExecutionClosure,
    MemoryObjectStore,
    SQLiteObjectStore,
)
from tools.standards_engine.standards_engine.engine import _codec_sets
from tools.standards_engine.standards_engine import (
    AnalysisRequest,
    ConsumerDispositionSubmission,
    CoverageAttestationSubmission,
    InspectCall,
    QueryCall,
    ReadRequest,
    StandardsEngine,
)
from tools.standards_engine.standards_engine.authority import (
    OPERATION_AUTHORITY_CODEC,
    OperationAuthorityContract,
    RoleRequirement,
    operation_contracts,
    validate_execution_authority,
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
    contract = AuthorizationAuthorityContract(
        "issuer.fixture",
        1,
        "principal.fixture",
        "authorization-grant.v1",
        (EvidenceContractKey("fixture.evidence", "1"),),
        "revocation.fixture",
        1,
        "authorization-revocation.v1",
        (EvidenceContractKey("fixture.evidence", "1"),),
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


class C7AnalysisLifecycleTests(unittest.TestCase):
    def test_operation_contracts_use_owned_codecs_and_exact_root_sides(self) -> None:
        codecs = tuple(codec for owner in _codec_sets() for codec in owner.codecs)
        codec_kinds = {codec.object_kind for codec in codecs}
        contracts = operation_contracts()
        self.assertTrue(contracts)
        self.assertEqual(
            len({contract.operation for contract in contracts}), len(contracts)
        )
        for codec in codecs:
            with self.subTest(codec=codec.object_kind):
                self.assertLessEqual(codec.allowed_dependency_kinds, codec_kinds)
        for contract in contracts:
            with self.subTest(operation=contract.operation):
                self.assertEqual(
                    OPERATION_AUTHORITY_CODEC.decode(
                        OPERATION_AUTHORITY_CODEC.encode(contract),
                        self.repository.codec_context(),
                    ),
                    contract,
                )
                for requirement in (
                    *contract.required_view_roles,
                    *contract.allowed_dynamic_roles,
                ):
                    self.assertIn(requirement.object_kind, codec_kinds)

        analysis = self.engine.prepare(self.request)
        navigation = self.engine.query(
            QueryCall(self.engine.view, ReadRequest("read", POLICY))
        )
        _complete(self.engine, analysis, "codec-closure")
        for result, expected_side in (
            (analysis, "transition"),
            (navigation, "current"),
        ):
            closure = self.repository.resolve_reference(
                AuthorityReference("execution-closure", result.authority.id)
            ).value
            self.assertIsInstance(closure, ExecutionClosure)
            operation_roots = tuple(
                root for root in closure.roots if root.role == "operation-contract"
            )
            self.assertEqual(len(operation_roots), 1)
            self.assertEqual(operation_roots[0].side, expected_side)

        stored_kinds = {
            decode_envelope(encoded).object_kind
            for _, encoded in self.repository._store._all_rows()
        }
        non_analysis_kinds = {
            codec.object_kind
            for owner in _codec_sets()
            if owner.owner_id != "standards-analysis"
            for codec in owner.codecs
        }
        self.assertLessEqual(non_analysis_kinds, stored_kinds)
        self.repository._verify_all_stored()

    def test_operation_cardinality_evidence_is_derived_from_contracts(self) -> None:
        codec_kinds = {
            codec.object_kind for owner in _codec_sets() for codec in owner.codecs
        }
        for contract in operation_contracts():
            operation = AuthorityReference(
                "operation-authority-contract",
                "operation-authority-contract:sha256:" + "0" * 64,
            )
            operation_side = (
                "transition" if contract.operation == "analysis" else "current"
            )
            required_roots = tuple(
                ExecutionAuthorityRoot(
                    "current",
                    requirement.role,
                    AuthorityReference(
                        requirement.object_kind,
                        f"{requirement.object_kind}:sha256:" + "1" * 64,
                    ),
                )
                for requirement in contract.required_view_roles
            )
            operation_root = ExecutionAuthorityRoot(
                operation_side, "operation-contract", operation
            )
            dynamic_roots = {
                requirement.role: tuple(
                    ExecutionAuthorityRoot(
                        "current",
                        requirement.role,
                        AuthorityReference(
                            requirement.object_kind,
                            f"{requirement.object_kind}:sha256:"
                            + f"{offset + 3:064x}",
                        ),
                    )
                    for offset in range(requirement.minimum_cardinality)
                )
                for requirement in contract.allowed_dynamic_roles
            }
            minimum_dynamic_roots = tuple(
                root
                for requirement in contract.allowed_dynamic_roles
                for root in dynamic_roots[requirement.role]
            )
            closure = ExecutionClosure(
                contract.operation,
                (operation_root, *required_roots, *minimum_dynamic_roots),
            )
            validate_execution_authority(closure, operation, contract, ("current",))

            for index, requirement in enumerate(contract.required_view_roles):
                with self.subTest(
                    operation=contract.operation,
                    role=requirement.role,
                    case="below-minimum",
                ):
                    missing = ExecutionClosure(
                        contract.operation,
                        (
                            operation_root,
                            *(
                                root
                                for offset, root in enumerate(required_roots)
                                if offset != index
                            ),
                            *minimum_dynamic_roots,
                        ),
                    )
                    with self.assertRaisesRegex(Exception, "cardinality"):
                        validate_execution_authority(
                            missing, operation, contract, ("current",)
                        )
                if requirement.maximum_cardinality is not None:
                    with self.subTest(
                        operation=contract.operation,
                        role=requirement.role,
                        case="above-maximum",
                    ):
                        duplicate = ExecutionAuthorityRoot(
                            "current",
                            requirement.role,
                            AuthorityReference(
                                requirement.object_kind,
                                f"{requirement.object_kind}:sha256:" + "2" * 64,
                            ),
                        )
                        excessive = ExecutionClosure(
                            contract.operation,
                            (
                                operation_root,
                                *required_roots,
                                duplicate,
                                *minimum_dynamic_roots,
                            ),
                        )
                        with self.assertRaisesRegex(Exception, "cardinality"):
                            validate_execution_authority(
                                excessive, operation, contract, ("current",)
                            )
                wrong_kind = next(
                    kind for kind in sorted(codec_kinds) if kind != requirement.object_kind
                )
                wrong_root = ExecutionAuthorityRoot(
                    "current",
                    requirement.role,
                    AuthorityReference(
                        wrong_kind, f"{wrong_kind}:sha256:" + "3" * 64
                    ),
                )
                wrong_required = tuple(
                    wrong_root if offset == index else root
                    for offset, root in enumerate(required_roots)
                )
                with self.subTest(
                    operation=contract.operation,
                    role=requirement.role,
                    case="wrong-kind",
                ):
                    with self.assertRaisesRegex(Exception, "wrong authority kind"):
                        validate_execution_authority(
                            ExecutionClosure(
                                contract.operation,
                                (
                                    operation_root,
                                    *wrong_required,
                                    *minimum_dynamic_roots,
                                ),
                            ),
                            operation,
                            contract,
                            ("current",),
                        )
            for requirement in contract.allowed_dynamic_roles:
                other_dynamic_roots = tuple(
                    root
                    for role, roots in dynamic_roots.items()
                    if role != requirement.role
                    for root in roots
                )
                validate_execution_authority(
                    ExecutionClosure(
                        contract.operation,
                        (
                            operation_root,
                            *required_roots,
                            *other_dynamic_roots,
                            *dynamic_roots[requirement.role],
                        ),
                    ),
                    operation,
                    contract,
                    ("current",),
                )
                if requirement.minimum_cardinality:
                    with self.subTest(
                        operation=contract.operation,
                        role=requirement.role,
                        case="dynamic-below-minimum",
                    ):
                        with self.assertRaisesRegex(Exception, "cardinality"):
                            validate_execution_authority(
                                ExecutionClosure(
                                    contract.operation,
                                    (
                                        operation_root,
                                        *required_roots,
                                        *other_dynamic_roots,
                                    ),
                                ),
                                operation,
                                contract,
                                ("current",),
                            )
                if requirement.maximum_cardinality is not None:
                    excessive = tuple(
                        ExecutionAuthorityRoot(
                            "current",
                            requirement.role,
                            AuthorityReference(
                                requirement.object_kind,
                                f"{requirement.object_kind}:sha256:"
                                + f"{offset + 20:064x}",
                            ),
                        )
                        for offset in range(requirement.maximum_cardinality + 1)
                    )
                    with self.subTest(
                        operation=contract.operation,
                        role=requirement.role,
                        case="dynamic-above-maximum",
                    ):
                        with self.assertRaisesRegex(Exception, "cardinality"):
                            validate_execution_authority(
                                ExecutionClosure(
                                    contract.operation,
                                    (
                                        operation_root,
                                        *required_roots,
                                        *other_dynamic_roots,
                                        *excessive,
                                    ),
                                ),
                                operation,
                                contract,
                                ("current",),
                            )
                wrong_kind = next(
                    kind for kind in sorted(codec_kinds) if kind != requirement.object_kind
                )
                with self.subTest(
                    operation=contract.operation,
                    role=requirement.role,
                    case="dynamic-wrong-kind",
                ):
                    with self.assertRaisesRegex(Exception, "wrong authority kind"):
                        validate_execution_authority(
                            ExecutionClosure(
                                contract.operation,
                                (
                                    operation_root,
                                    *required_roots,
                                    *other_dynamic_roots,
                                    ExecutionAuthorityRoot(
                                        "current",
                                        requirement.role,
                                        AuthorityReference(
                                            wrong_kind,
                                            f"{wrong_kind}:sha256:" + "4" * 64,
                                        ),
                                    ),
                                ),
                            ),
                            operation,
                            contract,
                            ("current",),
                        )

    def test_required_execution_role_rejects_multiple_roots(self) -> None:
        operation = AuthorityReference(
            "operation-authority-contract",
            "operation-authority-contract:sha256:" + "0" * 64,
        )
        contract = OperationAuthorityContract(
            "read",
            2,
            (RoleRequirement("metadata", "canonical-standards-corpus", 1, 1),),
            (),
        )
        closure = ExecutionClosure(
            "read",
            (
                ExecutionAuthorityRoot("current", "operation-contract", operation),
                ExecutionAuthorityRoot(
                    "current",
                    "metadata",
                    AuthorityReference(
                        "canonical-standards-corpus",
                        "canonical-standards-corpus:sha256:" + "1" * 64,
                    ),
                ),
                ExecutionAuthorityRoot(
                    "current",
                    "metadata",
                    AuthorityReference(
                        "canonical-standards-corpus",
                        "canonical-standards-corpus:sha256:" + "2" * 64,
                    ),
                ),
            ),
        )

        with self.assertRaisesRegex(Exception, "cardinality"):
            validate_execution_authority(closure, operation, contract, ("current",))

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
                base, proposed = (_view_handle(item) for item in engine.analysis_views)
                current = _view_handle(engine.view)

            with SQLiteObjectStore(path) as reopened:
                cold = StandardsEngine(_repository(reopened), current, (base, proposed))
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

    def test_fresh_process_inspects_public_authority_families(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            shutil.copytree(
                REPO_ROOT,
                root,
                ignore=shutil.ignore_patterns(
                    ".git", ".standards-engine", "__pycache__", "*.pyc"
                ),
            )
            subprocess.run(("git", "init", "-q"), cwd=root, check=True)
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            created = _run_fresh_python(
                root,
                """
import json
import sys
from pathlib import Path

from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import (
    InspectCall,
    QueryCall,
    ReadRequest,
    RelatedRequest,
    StandardsEngine,
)
from tools.standards_engine.tests.test_c7_analysis import (
    ExactAuthorizer,
    _complete,
    _request,
)

root = Path(sys.argv[1])
engine = StandardsEngine.open_analysis(
    root,
    root,
    execution_context=AnalysisExecutionContext(ExactAuthorizer()),
)
parent = engine.prepare(_request(engine))
complete = _complete(engine, parent, "fresh-process")
state = engine.inspect(InspectCall(complete.handle))
certificate_handle = complete.coverage_certificates[0]
certificate = engine.inspect(InspectCall(certificate_handle)).certificate
read = engine.query(
    QueryCall(engine.view, ReadRequest("read", "workflow.verification"))
)
related = engine.query(
    QueryCall(
        engine.view,
        RelatedRequest(
            "related",
            "workflow.verification",
            ("standards-requires",),
            "outgoing",
            False,
        ),
    )
)
handles = (
    (engine.snapshot, "content-snapshot-inspection-result"),
    (engine.view, "standards-authority-view"),
    (read.authority, "execution-closure"),
    (read.handle, "navigation-inspection-result"),
    (read.policy.handle, "policy-inspection-result"),
    (related.relationships[0].handle, "relationship-inspection-result"),
    (complete.context.handle, "analysis-context-inspection-result"),
    (certificate.coverage_view, "coverage-authority-view-inspection-result"),
    (certificate.requirement, "coverage-requirement-inspection-result"),
    (certificate.attestation, "coverage-attestation-inspection-result"),
    (certificate_handle, "certificate-inspection-result"),
    (complete.handle, "analysis-state"),
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

            expected = [item["expected"] for item in json.loads(created)["handles"]]
            self.assertEqual(json.loads(inspected), expected)


def _repository(store) -> AuthorityRepository:
    return AuthorityRepository(store, _codec_sets())


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
            f"fresh Python process failed ({completed.returncode}):\n{completed.stderr}"
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
