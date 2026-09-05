"""Portable, evidence-bound Engine audit receipts; no filesystem or Git writes."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from typing import Mapping

from tools.standards_metadata.standards_metadata import ContentSource
from .coverage import (
    CoverageDefinitionIndex,
    _claim_evidence,
    _exact,
    _error,
    _text,
    coverage_requirement_id,
)
from .trust import (
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    AuthorizationRequest,
    EvidenceContractKey,
    EvidenceReference,
    ResolvedEvidence,
    construct_authorization_record,
    resolve_authorization,
)
from .keys import analysis_identity


def _references(claim: Mapping[str, object]) -> tuple[EvidenceReference, ...]:
    return (
        *_claim_evidence(
            claim["evidence"], path="Engine receipt", field="evidence", version=6
        ),
        *_claim_evidence(
            claim["explicit_exclusions"],
            path="Engine receipt",
            field="explicit_exclusions",
            version=6,
            allow_empty=True,
        ),
    )


def _request(claim: Mapping[str, object]) -> AuthorizationRequest:
    return AuthorizationRequest(
        "coverage-attestation",
        "coverage-requirement",
        claim["requirement_id"],
        "standards.review.audit",
        _references(claim),
    )


def _publication_request(
    subject: str,
    claim: Mapping[str, object],
    analysis_id: str,
    review_authorization: Mapping[str, object],
) -> AuthorizationRequest:
    _text(analysis_id, path="Engine receipt", field="analysis_id")
    identity = analysis_identity(
        "coding-standards:coverage-publication:v1",
        "coverage-publication",
        {
            "subject": subject,
            "claim": dict(claim),
            "analysis_id": analysis_id,
            "review_authorization": dict(review_authorization),
        },
    )
    return AuthorizationRequest(
        "publish-coverage",
        "coverage-publication",
        identity,
        "standards.review.audit",
        _references(claim),
    )


def _bound_claim(
    subject: str, claim: Mapping[str, object], definitions: CoverageDefinitionIndex
) -> None:
    if subject not in definitions.views or claim.get(
        "requirement_id"
    ) != coverage_requirement_id(
        definitions.requirements[subject], definitions.views[subject]
    ):
        raise _error(
            "COVERAGE.PUBLICATION_STALE",
            "Reviewed coverage does not match the destination requirement.",
            observed=subject,
        )
    fields = {
        "requirement_id",
        "conclusion",
        "evidence",
        "explicit_exclusions",
        "rationale",
        "auditor_provenance",
        "schema_version",
        "authorization_id",
    }
    _exact(claim, required=fields, allowed=fields, path="Engine receipt", field="claim")
    if claim["conclusion"] != "complete" or claim["schema_version"] != 4:
        raise _error(
            "COVERAGE.INVALID_ATTESTATION",
            "Engine publication requires a complete reviewed claim.",
        )
    _references(claim)
    for field in ("rationale", "auditor_provenance"):
        _text(claim[field], path="Engine receipt", field=field)


def _resolved_value(evidence: ResolvedEvidence) -> dict[str, object]:
    return {
        "reference": evidence.reference.as_contract(),
        "content_hex": evidence.content.hex(),
    }


def render_engine_coverage_receipt(
    source: ContentSource,
    definitions: CoverageDefinitionIndex,
    subject: str,
    claim: Mapping[str, object],
    review_authorization: Mapping[str, object],
    analysis_id: str,
    context: AnalysisExecutionContext,
) -> bytes:
    """Reauthorize an exact reviewed claim and retain its current authority proof."""
    _bound_claim(subject, claim, definitions)
    request = _request(claim)
    # The destination bytes, not the authorizer's working tree, must match too.
    for reference in request.evidence:
        ResolvedEvidence(reference, source.read_bytes(reference.id))
    resolved = resolve_authorization(context, request)
    authorization = resolved.record.as_contract()
    if (
        authorization != review_authorization
        or claim["authorization_id"] != authorization["reference"]["id"]
    ):
        raise _error(
            "COVERAGE.PUBLICATION_AUTHORITY_CHANGED",
            "Publication requires the exact Engine authority that authorized the review.",
        )
    publication = resolve_authorization(
        context, _publication_request(subject, claim, analysis_id, authorization)
    )
    value = {
        "schema_version": 1,
        "subject": subject,
        "analysis_id": analysis_id,
        "claim": dict(claim),
        "authority": resolved.authority.as_contract(),
        "authorization": authorization,
        "authorization_evidence": [
            _resolved_value(item) for item in resolved.claim.authorization_evidence
        ],
        "revocation_evidence": [
            _resolved_value(item) for item in resolved.claim.revocation_evidence
        ],
        "publication": {
            "authorization": publication.record.as_contract(),
            "authorization_evidence": [
                _resolved_value(item)
                for item in publication.claim.authorization_evidence
            ],
            "revocation_evidence": [
                _resolved_value(item) for item in publication.claim.revocation_evidence
            ],
        },
    }
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def _evidence(value: object) -> tuple[ResolvedEvidence, ...]:
    if not isinstance(value, list):
        raise ValueError("receipt evidence must be an array")
    result = []
    for item in value:
        _exact(
            item,
            required={"reference", "content_hex"},
            allowed={"reference", "content_hex"},
            path="Engine receipt",
            field="proof",
        )
        result.append(
            ResolvedEvidence(
                EvidenceReference(**item["reference"]),
                bytes.fromhex(item["content_hex"]),
            )
        )
    return tuple(result)


@dataclass(frozen=True)
class _ReceiptAuthority:
    source: ContentSource
    contract: AuthorizationAuthorityContract
    authorization_evidence: tuple[ResolvedEvidence, ...]
    revocation_evidence: tuple[ResolvedEvidence, ...]

    def authorize(self, request: AuthorizationRequest) -> AuthorizationClaim:
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(ref, self.source.read_bytes(ref.id))
                for ref in request.evidence
            ),
            self.authorization_evidence,
            self.revocation_evidence,
            "not-revoked",
            "allow",
        )


def load_engine_coverage_receipt(
    source: ContentSource,
    path: str,
    definitions: CoverageDefinitionIndex,
    revoked: frozenset[str],
) -> tuple[str, dict[str, object], dict[str, object], tuple[str, ...]] | None:
    """Registry membership supplies repository trust; validate its exact recorded proof."""
    try:
        value = json.loads(source.read_bytes(path))
        fields = {
            "schema_version",
            "subject",
            "analysis_id",
            "claim",
            "authority",
            "authorization",
            "authorization_evidence",
            "revocation_evidence",
            "publication",
        }
        _exact(
            value, required=fields, allowed=fields, path=path, field="Engine receipt"
        )
        if type(value["schema_version"]) is not int or value["schema_version"] != 1:
            raise ValueError("unsupported Engine receipt version")
        subject, claim = value["subject"], value["claim"]
        # Obsolete requirements are retained for history, never renewed on load.
        if subject not in definitions.views or claim[
            "requirement_id"
        ] != coverage_requirement_id(
            definitions.requirements[subject], definitions.views[subject]
        ):
            return None
        _bound_claim(subject, claim, definitions)
        raw = dict(value["authority"])
        for key in (
            "authorization_evidence_contracts",
            "revocation_evidence_contracts",
        ):
            raw[key] = tuple(EvidenceContractKey(**item) for item in raw[key])
        authority = _ReceiptAuthority(
            source,
            AuthorizationAuthorityContract(**raw),
            _evidence(value["authorization_evidence"]),
            _evidence(value["revocation_evidence"]),
        )
        record = construct_authorization_record(
            AnalysisExecutionContext(authority), _request(claim)
        ).as_contract()
        if (
            record != value["authorization"]
            or claim["authorization_id"] != record["reference"]["id"]
        ):
            raise ValueError("receipt authorization does not bind the reviewed claim")
        publication = value["publication"]
        proof_fields = {
            "authorization",
            "authorization_evidence",
            "revocation_evidence",
        }
        _exact(
            publication,
            required=proof_fields,
            allowed=proof_fields,
            path=path,
            field="publication",
        )
        publishing_authority = replace(
            authority,
            authorization_evidence=_evidence(publication["authorization_evidence"]),
            revocation_evidence=_evidence(publication["revocation_evidence"]),
        )
        publishing_record = construct_authorization_record(
            AnalysisExecutionContext(publishing_authority),
            _publication_request(subject, claim, value["analysis_id"], record),
        ).as_contract()
        if publishing_record != publication["authorization"]:
            raise ValueError(
                "publication authorization does not bind the exact reviewed claim"
            )
        if (
            record["reference"]["id"] in revoked
            or publishing_record["reference"]["id"] in revoked
        ):
            raise _error(
                "COVERAGE.AUTHORIZATION_REVOKED",
                "Engine coverage authorization is revoked.",
                path=path,
            )
        return subject, dict(claim), record, tuple(ref.id for ref in _references(claim))
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise _error(
            "COVERAGE.ENGINE_RECEIPT_INVALID",
            "Engine audit receipt is malformed or its authorization is inconsistent.",
            path=path,
        ) from error
