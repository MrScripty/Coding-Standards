from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol

from tools.standards_authority.standards_authority import (
    AuthorityReference,
    ExecutionAuthorityRoot,
)

from .authority import AuthorityEvidence, AuthorizationGrant
from .errors import AnalysisError, AnalysisFailure


@dataclass(frozen=True, slots=True)
class ResolvedEvidence:
    reference: AuthorityEvidence
    content: bytes

    def __post_init__(self) -> None:
        digest = "sha256:" + hashlib.sha256(self.content).hexdigest()
        if digest != self.reference.digest:
            raise _error(
                "ANALYSIS.EVIDENCE_DIGEST_MISMATCH",
                "resolved evidence bytes do not match the declared digest",
            )


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    action: str
    subject_kind: str
    subject_id: str
    capability: str
    evidence: tuple[AuthorityEvidence, ...]


@dataclass(frozen=True, slots=True)
class AuthorizationClaim:
    issuer_id: str
    issuer_semantic_revision: int
    grant_id: str
    principal_id: str
    action: str
    subject_kind: str
    subject_id: str
    capability: str
    submission_evidence: tuple[ResolvedEvidence, ...]
    authorization_evidence: tuple[ResolvedEvidence, ...]
    revocation_authority_id: str
    revocation_authority_semantic_revision: int
    revocation_evidence: tuple[ResolvedEvidence, ...]


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
    def authorize(self, request: AuthorizationRequest) -> AuthorizationOutcome: ...


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    requirement: AuthorityReference
    fact: str
    immutable_inputs: tuple[ExecutionAuthorityRoot, ...]


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
    provider_id: str
    semantic_revision: int
    input_contract: str
    evidence_contract: str

    def observe(self, request: ProviderRequest) -> ProviderOutcome: ...


@dataclass(frozen=True, slots=True)
class AnalysisExecutionContext:
    authorization: AuthorizationAdapter | None = None
    providers: tuple[FactProviderAdapter, ...] = ()

    def __post_init__(self) -> None:
        selected = tuple(sorted(self.providers, key=lambda item: item.provider_id))
        if len({item.provider_id for item in selected}) != len(selected):
            raise _error(
                "ANALYSIS.DUPLICATE_PROVIDER",
                "Fact provider identities must be unique.",
            )
        object.__setattr__(self, "providers", selected)


def construct_authorization_grant(
    context: AnalysisExecutionContext,
    request: AuthorizationRequest,
) -> AuthorizationGrant:
    adapter = context.authorization
    if adapter is None:
        raise _error(
            "ANALYSIS.AUTHORIZATION_UNAVAILABLE",
            "No authorization adapter is bound to this Engine.",
            outcome="unavailable",
        )
    outcome = adapter.authorize(request)
    if isinstance(outcome, AuthorizationDenied):
        raise _error(
            "ANALYSIS.UNAUTHORIZED", outcome.reason, outcome="unauthorized"
        )
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
    return AuthorizationGrant(
        outcome.issuer_id,
        outcome.issuer_semantic_revision,
        outcome.grant_id,
        outcome.principal_id,
        outcome.capability,
        outcome.action,
        outcome.subject_kind,
        outcome.subject_id,
        authorization_evidence,
        outcome.revocation_authority_id,
        outcome.revocation_authority_semantic_revision,
        revocation_evidence,
    )


def _evidence(values: tuple[ResolvedEvidence, ...]) -> tuple[AuthorityEvidence, ...]:
    selected = tuple(sorted((item.reference for item in values)))
    if not selected:
        raise _error(
            "ANALYSIS.EVIDENCE_REQUIRED",
            "Authorization and revocation evidence must be nonempty.",
        )
    return selected


def _error(code: str, message: str, *, outcome: str = "invalid") -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message))


__all__ = (
    "AnalysisExecutionContext",
    "AuthorizationAdapter",
    "AuthorizationClaim",
    "AuthorizationDenied",
    "AuthorizationOutcome",
    "AuthorizationRequest",
    "AuthorizationUnavailable",
    "AuthorizationUnsupported",
    "FactProviderAdapter",
    "ProviderNoObservation",
    "ProviderObservationClaim",
    "ProviderOutcome",
    "ProviderRequest",
    "ProviderUnavailable",
    "ResolvedEvidence",
    "construct_authorization_grant",
)
