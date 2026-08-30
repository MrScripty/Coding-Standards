from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol

from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_identity, analysis_value_digest


AUTHORIZATION_DOMAIN = "coding-standards:authorization-record:v1"


def _error(code: str, message: str, *, outcome: str = "invalid") -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message))


def _nonempty(value: str, field: str) -> None:
    if type(value) is not str or not value:
        raise _error(
            "ANALYSIS.INVALID_TRUST_CONTRACT",
            f"{field} must be a nonempty string.",
        )


@dataclass(frozen=True, slots=True, order=True)
class EvidenceContractKey:
    provider_contract: str
    provider_contract_version: str

    def __post_init__(self) -> None:
        _nonempty(self.provider_contract, "provider_contract")
        _nonempty(self.provider_contract_version, "provider_contract_version")


@dataclass(frozen=True, slots=True, order=True)
class EvidenceReference:
    id: str
    digest: str
    provider_contract: str
    provider_contract_version: str

    def __post_init__(self) -> None:
        for field, value in (
            ("id", self.id),
            ("provider_contract", self.provider_contract),
            ("provider_contract_version", self.provider_contract_version),
        ):
            _nonempty(value, field)
        if (
            not self.digest.startswith("sha256:")
            or len(self.digest) != len("sha256:") + 64
        ):
            raise _error(
                "ANALYSIS.INVALID_EVIDENCE",
                "Evidence digest must be a SHA-256 digest.",
            )

    def as_contract(self) -> dict[str, str]:
        return {
            "id": self.id,
            "digest": self.digest,
            "provider_contract": self.provider_contract,
            "provider_contract_version": self.provider_contract_version,
        }


@dataclass(frozen=True, slots=True)
class ResolvedEvidence:
    reference: EvidenceReference
    content: bytes

    def __post_init__(self) -> None:
        if type(self.content) is not bytes:
            raise _error(
                "ANALYSIS.INVALID_EVIDENCE",
                "Resolved evidence content must be exact bytes.",
            )
        digest = "sha256:" + hashlib.sha256(self.content).hexdigest()
        if digest != self.reference.digest:
            raise _error(
                "ANALYSIS.EVIDENCE_DIGEST_MISMATCH",
                "Resolved evidence bytes do not match the declared digest.",
            )


@dataclass(frozen=True, slots=True)
class AuthorizationAuthorityContract:
    issuer_id: str
    issuer_semantic_revision: int
    principal_id: str
    authorization_contract: str
    authorization_evidence_contracts: tuple[EvidenceContractKey, ...]
    revocation_authority_id: str
    revocation_authority_semantic_revision: int
    revocation_contract: str
    revocation_evidence_contracts: tuple[EvidenceContractKey, ...]

    def __post_init__(self) -> None:
        for field, value in (
            ("issuer_id", self.issuer_id),
            ("principal_id", self.principal_id),
            ("authorization_contract", self.authorization_contract),
            ("revocation_authority_id", self.revocation_authority_id),
            ("revocation_contract", self.revocation_contract),
        ):
            _nonempty(value, field)
        for field, value in (
            ("issuer_semantic_revision", self.issuer_semantic_revision),
            (
                "revocation_authority_semantic_revision",
                self.revocation_authority_semantic_revision,
            ),
        ):
            if type(value) is not int or value < 1:
                raise _error(
                    "ANALYSIS.INVALID_TRUST_CONTRACT",
                    f"{field} must be a positive integer.",
                )
        if self.authorization_contract != "authorization-grant.v1":
            raise _error(
                "ANALYSIS.AUTHORIZATION_CONTRACT_UNSUPPORTED",
                "The authorization contract is unsupported.",
                outcome="unsupported",
            )
        if self.revocation_contract != "authorization-revocation.v1":
            raise _error(
                "ANALYSIS.REVOCATION_CONTRACT_UNSUPPORTED",
                "The revocation contract is unsupported.",
                outcome="unsupported",
            )
        for field, values in (
            ("authorization_evidence_contracts", self.authorization_evidence_contracts),
            ("revocation_evidence_contracts", self.revocation_evidence_contracts),
        ):
            if not values or values != tuple(sorted(set(values))):
                raise _error(
                    "ANALYSIS.INVALID_TRUST_CONTRACT",
                    f"{field} must be nonempty, sorted, and unique.",
                )

    def as_contract(self) -> dict[str, object]:
        return {
            "issuer_id": self.issuer_id,
            "issuer_semantic_revision": self.issuer_semantic_revision,
            "principal_id": self.principal_id,
            "authorization_contract": self.authorization_contract,
            "authorization_evidence_contracts": [
                {
                    "provider_contract": item.provider_contract,
                    "provider_contract_version": item.provider_contract_version,
                }
                for item in self.authorization_evidence_contracts
            ],
            "revocation_authority_id": self.revocation_authority_id,
            "revocation_authority_semantic_revision": (
                self.revocation_authority_semantic_revision
            ),
            "revocation_contract": self.revocation_contract,
            "revocation_evidence_contracts": [
                {
                    "provider_contract": item.provider_contract,
                    "provider_contract_version": item.provider_contract_version,
                }
                for item in self.revocation_evidence_contracts
            ],
        }


@dataclass(frozen=True, slots=True, order=True)
class ProviderInputRole:
    side: str
    role: str

    def __post_init__(self) -> None:
        _nonempty(self.side, "provider input side")
        _nonempty(self.role, "provider input role")


@dataclass(frozen=True, slots=True)
class FactProviderContract:
    provider_id: str
    semantic_revision: int
    input_contract: str
    evidence_contract: str
    input_roles: tuple[ProviderInputRole, ...]

    def __post_init__(self) -> None:
        for field, value in (
            ("provider_id", self.provider_id),
            ("input_contract", self.input_contract),
            ("evidence_contract", self.evidence_contract),
        ):
            _nonempty(value, field)
        if type(self.semantic_revision) is not int or self.semantic_revision < 1:
            raise _error(
                "ANALYSIS.INVALID_PROVIDER_CONTRACT",
                "semantic_revision must be a positive integer.",
            )
        if self.input_roles != tuple(sorted(set(self.input_roles))):
            raise _error(
                "ANALYSIS.INVALID_PROVIDER_CONTRACT",
                "provider input roles must be sorted and unique.",
            )
        if ProviderInputRole("current", "requirement") not in self.input_roles:
            raise _error(
                "ANALYSIS.INVALID_PROVIDER_CONTRACT",
                "provider input roles must include the current requirement.",
            )

    def as_contract(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "semantic_revision": self.semantic_revision,
            "input_contract": self.input_contract,
            "evidence_contract": self.evidence_contract,
            "input_roles": [
                {"side": item.side, "role": item.role} for item in self.input_roles
            ],
        }

    def reference(self) -> dict[str, object]:
        return {
            "id": self.provider_id,
            "contract": self.input_contract,
            "contract_version": str(self.semantic_revision),
            "input_digest": analysis_value_digest(self.as_contract()),
        }


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    action: str
    subject_kind: str
    subject_id: str
    capability: str
    evidence: tuple[EvidenceReference, ...]


@dataclass(frozen=True, slots=True)
class AuthorizationClaim:
    action: str
    subject_kind: str
    subject_id: str
    capability: str
    submission_evidence: tuple[ResolvedEvidence, ...]
    authorization_evidence: tuple[ResolvedEvidence, ...]
    revocation_evidence: tuple[ResolvedEvidence, ...]
    revocation_state: str
    decision: str


@dataclass(frozen=True, slots=True)
class AuthorizationDenied:
    reason: str


@dataclass(frozen=True, slots=True)
class AuthorizationUnavailable:
    reason: str


@dataclass(frozen=True, slots=True)
class AuthorizationUnsupported:
    reason: str


AuthorizationOutcome = (
    AuthorizationClaim
    | AuthorizationDenied
    | AuthorizationUnavailable
    | AuthorizationUnsupported
)


class AuthorizationAdapter(Protocol):
    contract: AuthorizationAuthorityContract

    def authorize(self, request: AuthorizationRequest) -> AuthorizationOutcome: ...


@dataclass(frozen=True, slots=True, order=True)
class ImmutableProviderInput:
    side: str
    role: str
    identity: str
    digest: str


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    requirement_id: str
    fact: str
    immutable_inputs: tuple[ImmutableProviderInput, ...]


@dataclass(frozen=True, slots=True)
class ProviderObservationClaim:
    value: object
    evidence: tuple[ResolvedEvidence, ...]


@dataclass(frozen=True, slots=True)
class ProviderNoObservation:
    pass


@dataclass(frozen=True, slots=True)
class ProviderUnavailable:
    reason: str


ProviderOutcome = (
    ProviderObservationClaim | ProviderNoObservation | ProviderUnavailable
)


class FactProviderAdapter(Protocol):
    contract: FactProviderContract

    def observe(self, request: ProviderRequest) -> ProviderOutcome: ...


@dataclass(frozen=True, slots=True)
class AnalysisExecutionContext:
    authorization: AuthorizationAdapter | None = None
    providers: tuple[FactProviderAdapter, ...] = ()

    def __post_init__(self) -> None:
        selected = tuple(
            sorted(self.providers, key=lambda item: item.contract.provider_id)
        )
        if len({item.contract.provider_id for item in selected}) != len(selected):
            raise _error(
                "ANALYSIS.DUPLICATE_PROVIDER",
                "Fact provider identities must be unique.",
            )
        object.__setattr__(self, "providers", selected)

    def contract_view(self) -> dict[str, object]:
        return {
            "authorization_authority_digest": (
                None
                if self.authorization is None
                else analysis_value_digest(self.authorization.contract.as_contract())
            ),
            "providers": [
                provider.contract.reference() for provider in self.providers
            ],
        }


@dataclass(frozen=True, slots=True)
class AuthorizationRecord:
    reference: dict[str, object]
    issuer_semantic_revision: int
    principal: str
    action: str
    subject_kind: str
    subject_id: str
    authorization_evidence: tuple[EvidenceReference, ...]
    revocation_authority: str
    revocation_authority_semantic_revision: int
    revocation_evidence: tuple[EvidenceReference, ...]

    def as_contract(self) -> dict[str, object]:
        return {
            "reference": self.reference,
            "issuer_semantic_revision": self.issuer_semantic_revision,
            "principal": self.principal,
            "action": self.action,
            "subject_kind": self.subject_kind,
            "subject_id": self.subject_id,
            "authorization_evidence": [
                item.as_contract() for item in self.authorization_evidence
            ],
            "revocation_authority": self.revocation_authority,
            "revocation_authority_semantic_revision": (
                self.revocation_authority_semantic_revision
            ),
            "revocation_evidence": [
                item.as_contract() for item in self.revocation_evidence
            ],
        }


def construct_authorization_record(
    context: AnalysisExecutionContext,
    request: AuthorizationRequest,
) -> AuthorizationRecord:
    adapter = context.authorization
    if adapter is None:
        raise _error(
            "ANALYSIS.AUTHORIZATION_UNAVAILABLE",
            "No authorization adapter is bound to this Engine.",
            outcome="unavailable",
        )
    authority = adapter.contract
    outcome = adapter.authorize(request)
    if isinstance(outcome, AuthorizationDenied):
        raise _error("ANALYSIS.UNAUTHORIZED", outcome.reason, outcome="unauthorized")
    if isinstance(outcome, AuthorizationUnavailable):
        raise _error(
            "ANALYSIS.AUTHORIZATION_UNAVAILABLE",
            outcome.reason,
            outcome="unavailable",
        )
    if isinstance(outcome, AuthorizationUnsupported):
        raise _error(
            "ANALYSIS.AUTHORIZATION_UNSUPPORTED",
            outcome.reason,
            outcome="unsupported",
        )
    if not isinstance(outcome, AuthorizationClaim):
        raise _error(
            "ANALYSIS.AUTHORIZATION_INVALID",
            "Authorization adapter returned an unrecognized outcome.",
        )
    if outcome.decision != "allow" or outcome.revocation_state != "not-revoked":
        raise _error(
            "ANALYSIS.UNAUTHORIZED",
            "Authorization does not permit the requested work.",
            outcome="unauthorized",
        )
    expected = (
        request.action,
        request.subject_kind,
        request.subject_id,
        request.capability,
    )
    observed = (
        outcome.action,
        outcome.subject_kind,
        outcome.subject_id,
        outcome.capability,
    )
    if observed != expected:
        raise _error(
            "ANALYSIS.AUTHORIZATION_CONTEXT_MISMATCH",
            "Authorization claim does not bind the exact current work.",
        )
    supplied = tuple(item.reference for item in outcome.submission_evidence)
    if supplied != request.evidence:
        raise _error(
            "ANALYSIS.EVIDENCE_CONTEXT_MISMATCH",
            "Authorization claim does not resolve the exact submitted evidence.",
        )
    authorization_evidence = _evidence(outcome.authorization_evidence)
    revocation_evidence = _evidence(outcome.revocation_evidence)
    _require_evidence_contracts(
        authorization_evidence,
        authority.authorization_evidence_contracts,
        "authorization",
    )
    _require_evidence_contracts(
        revocation_evidence,
        authority.revocation_evidence_contracts,
        "revocation",
    )
    authority_digest = analysis_value_digest(authority.as_contract())
    identity_material = {
        "issuer": authority.issuer_id,
        "issuer_semantic_revision": authority.issuer_semantic_revision,
        "principal": authority.principal_id,
        "capability": request.capability,
        "action": request.action,
        "subject_kind": request.subject_kind,
        "subject_id": request.subject_id,
        "authority_digest": authority_digest,
        "authorization_evidence": [
            item.as_contract() for item in authorization_evidence
        ],
        "revocation_authority": authority.revocation_authority_id,
        "revocation_authority_semantic_revision": (
            authority.revocation_authority_semantic_revision
        ),
        "revocation_evidence": [
            item.as_contract() for item in revocation_evidence
        ],
    }
    reference = {
        "id": analysis_identity(
            AUTHORIZATION_DOMAIN,
            "authorization",
            identity_material,
        ),
        "issuer": authority.issuer_id,
        "capability": request.capability,
        "authority_digest": authority_digest,
    }
    return AuthorizationRecord(
        reference,
        authority.issuer_semantic_revision,
        authority.principal_id,
        request.action,
        request.subject_kind,
        request.subject_id,
        authorization_evidence,
        authority.revocation_authority_id,
        authority.revocation_authority_semantic_revision,
        revocation_evidence,
    )


def _require_evidence_contracts(
    evidence: tuple[EvidenceReference, ...],
    expected: tuple[EvidenceContractKey, ...],
    label: str,
) -> None:
    observed = tuple(
        sorted(
            {
                EvidenceContractKey(
                    item.provider_contract,
                    item.provider_contract_version,
                )
                for item in evidence
            }
        )
    )
    if observed != expected:
        raise _error(
            "ANALYSIS.EVIDENCE_CONTRACT_MISMATCH",
            f"{label} evidence does not match the injected authority contract.",
        )


def _evidence(values: tuple[ResolvedEvidence, ...]) -> tuple[EvidenceReference, ...]:
    selected = tuple(sorted(item.reference for item in values))
    if not selected:
        raise _error(
            "ANALYSIS.EVIDENCE_REQUIRED",
            "Authorization and revocation evidence must be nonempty.",
        )
    return selected


__all__ = (
    "AnalysisExecutionContext",
    "AuthorizationAdapter",
    "AuthorizationAuthorityContract",
    "AuthorizationClaim",
    "AuthorizationDenied",
    "AuthorizationOutcome",
    "AuthorizationRecord",
    "AuthorizationRequest",
    "AuthorizationUnavailable",
    "AuthorizationUnsupported",
    "EvidenceContractKey",
    "EvidenceReference",
    "FactProviderAdapter",
    "FactProviderContract",
    "ImmutableProviderInput",
    "ProviderInputRole",
    "ProviderNoObservation",
    "ProviderObservationClaim",
    "ProviderOutcome",
    "ProviderRequest",
    "ProviderUnavailable",
    "ResolvedEvidence",
    "construct_authorization_record",
)
