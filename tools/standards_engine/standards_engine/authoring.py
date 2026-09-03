from __future__ import annotations

import json
import re
import time
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from tools.repository_git.repository_git import (
    GitRepositoryError,
    RepositoryRevision,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityError,
    IdentityObject,
    IdentityValue,
    encode_identity_value,
    hash_identity,
)
from tools.standards_snapshots.standards_snapshots import (
    AggregateRecord,
    AggregateRoot,
    FindAggregateRootsRequest,
    SnapshotId,
    SnapshotModule,
    SnapshotPath,
    SnapshotError,
)

AUTHORING_CONTRACT_VERSION = 1
READINESS_CONTRACT_VERSION = 1
APPLICATION_CONTRACT_VERSION = 1
APPLICATION_SELECTION_CONTRACT_VERSION = 1
PROPOSAL_KIND = "proposal"
REVISION_KIND = "proposal-revision"
READINESS_KIND = "proposal-readiness"
APPLICATION_KIND = "proposal-application"
APPLICATION_OUTCOME_KIND = "proposal-application-outcome"
APPLICATION_SELECTION_KIND = "proposal-application-selection"
CANONICAL_TARGET_BRANCH = "main"
CANONICAL_TARGET_REF = "refs/heads/main"
APPLICATION_CAPABILITY = "standards.proposal.apply"
APPLICATION_RECOVERY_CAPABILITY = "standards.proposal.recover"
APPLICATION_VERIFICATION_CONTRACT = IdentityObject(
    (
        ("checkpoint", "complete"),
        ("owner", "standards-verifier"),
        ("semantic_revision", 1),
    )
)
REVIEW_CAPABILITIES = {
    "audit": "standards.review.audit",
    "consumer": "standards.review.consumer",
    "impact": "standards.review.impact",
}
FailureOutcome = Literal["invalid", "unavailable", "unsupported"]


@dataclass(frozen=True, slots=True)
class AuthoringFailure:
    code: str
    outcome: FailureOutcome
    message: str


class AuthoringError(RuntimeError):
    def __init__(self, failure: AuthoringFailure) -> None:
        self.failure = failure
        super().__init__(f"{failure.code}: {failure.message}")


def _invalid(code: str, message: str) -> AuthoringError:
    return AuthoringError(AuthoringFailure(code, "invalid", message))


def _unavailable(code: str, message: str) -> AuthoringError:
    return AuthoringError(AuthoringFailure(code, "unavailable", message))


@dataclass(frozen=True, slots=True, order=True)
class ProposalId:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or not self.value.startswith("proposal:v1:"):
            raise _invalid(
                "AUTHORING.INVALID_PROPOSAL_ID", "proposal ID has an invalid domain"
            )
        raw = self.value.removeprefix("proposal:v1:")
        try:
            parsed = uuid.UUID(raw)
        except (ValueError, AttributeError) as error:
            raise _invalid(
                "AUTHORING.INVALID_PROPOSAL_ID", "proposal ID UUID is invalid"
            ) from error
        if parsed.version != 4 or str(parsed) != raw:
            raise _invalid(
                "AUTHORING.INVALID_PROPOSAL_ID",
                "proposal ID requires canonical UUID version 4",
            )

    @classmethod
    def from_uuid(cls, value: uuid.UUID) -> ProposalId:
        if type(value) is not uuid.UUID or value.version != 4:
            raise _invalid(
                "AUTHORING.INVALID_PROPOSAL_ID",
                "proposal ID source must be UUID version 4",
            )
        return cls(f"proposal:v1:{value}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, order=True)
class Mutation:
    path: SnapshotPath
    value: str

    def __post_init__(self) -> None:
        if type(self.path) is not SnapshotPath or type(self.value) is not str:
            raise _invalid(
                "AUTHORING.INVALID_MUTATION",
                "replacement mutation requires a snapshot path and exact text",
            )
        try:
            self.value.encode("utf-8")
        except UnicodeEncodeError as error:
            raise _invalid(
                "AUTHORING.INVALID_MUTATION",
                "replacement text must contain Unicode scalar values",
            ) from error

    def as_contract(self) -> dict[str, object]:
        return {"op": "replace", "path": str(self.path), "value": self.value}


@dataclass(frozen=True, slots=True, init=False)
class ProposalRevision:
    proposal: ProposalId
    ordinal: int
    base_snapshot: SnapshotId
    mutations: tuple[Mutation, ...]
    semantic_proposals: tuple[IdentityObject, ...]

    def __init__(
        self,
        proposal: ProposalId,
        ordinal: int,
        base_snapshot: SnapshotId,
        mutations: Iterable[Mutation],
        semantic_proposals: Iterable[Mapping[str, object]],
    ) -> None:
        supplied_mutations = tuple(mutations)
        if any(type(item) is not Mutation for item in supplied_mutations):
            raise _invalid(
                "AUTHORING.INVALID_REVISION",
                "proposal revision mutations must be exact Mutation values",
            )
        selected_mutations = tuple(
            sorted(supplied_mutations, key=lambda item: item.path)
        )
        paths = tuple(item.path for item in selected_mutations)
        if (
            type(proposal) is not ProposalId
            or type(ordinal) is not int
            or ordinal < 1
            or type(base_snapshot) is not SnapshotId
            or not selected_mutations
            or len(set(paths)) != len(paths)
        ):
            raise _invalid(
                "AUTHORING.INVALID_REVISION",
                "proposal revision requires unique replacement paths and exact identities",
            )
        try:
            selected_semantic = tuple(
                sorted(
                    {
                        encode_identity_value(_identity_value(item)): _identity_record(
                            item
                        )
                        for item in semantic_proposals
                    }.values(),
                    key=encode_identity_value,
                )
            )
        except IdentityError as error:
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_PROPOSAL",
                "semantic proposal must contain canonical identity values",
            ) from error
        object.__setattr__(self, "proposal", proposal)
        object.__setattr__(self, "ordinal", ordinal)
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "mutations", selected_mutations)
        object.__setattr__(self, "semantic_proposals", selected_semantic)

    @property
    def revision_id(self) -> str:
        return hash_identity(
            "coding-standards:proposal-revision:v1",
            "proposal-revision",
            self.identity_material(),
        )

    def identity_material(self) -> IdentityObject:
        return IdentityObject(
            (
                ("base_snapshot", str(self.base_snapshot)),
                ("contract_version", AUTHORING_CONTRACT_VERSION),
                (
                    "mutations",
                    IdentityArray(
                        _identity_record(item.as_contract()) for item in self.mutations
                    ),
                ),
                ("ordinal", self.ordinal),
                ("proposal", str(self.proposal)),
                ("semantic_proposals", IdentityArray(self.semantic_proposals)),
            )
        )

    def aggregate(self) -> AggregateRecord:
        return AggregateRecord(
            self.revision_id,
            REVISION_KIND,
            encode_identity_value(self.identity_material()),
            (self.base_snapshot,),
        )


@dataclass(frozen=True, slots=True, order=True)
class ProposalSummary:
    proposal: ProposalId
    head_revision: str

    def __post_init__(self) -> None:
        if type(self.proposal) is not ProposalId or not _revision_id(
            self.head_revision
        ):
            raise _invalid(
                "AUTHORING.INVALID_SUMMARY",
                "proposal summary requires exact proposal and revision identities",
            )


@dataclass(frozen=True, slots=True, init=False)
class ProposalReadiness:
    base_snapshot: SnapshotId
    analysis_id: str
    revision_id: str
    decisions: tuple[IdentityObject, ...]
    authorization_records: tuple[IdentityObject, ...]
    expected_target: RepositoryRevision

    def __init__(
        self,
        base_snapshot: SnapshotId,
        analysis_id: str,
        revision_id: str,
        decisions: Iterable[Mapping[str, object]],
        authorization_records: Iterable[Mapping[str, object]],
        expected_target: RepositoryRevision,
    ) -> None:
        if (
            type(base_snapshot) is not SnapshotId
            or not _analysis_id(analysis_id)
            or not _revision_id(revision_id)
            or type(expected_target) is not RepositoryRevision
        ):
            raise _invalid(
                "AUTHORING.INVALID_READINESS",
                "readiness requires exact base, analysis, revision, and target identities",
            )
        selected_decisions = tuple(
            item
            for _encoded, item in sorted(
                {
                    encode_identity_value(item): item
                    for item in (_review_decision(value) for value in decisions)
                }.items()
            )
        )
        plain_decisions = {
            str(item["owner"]): item
            for item in map(_plain_identity, selected_decisions)
            if type(item) is dict
        }
        if len(selected_decisions) != len(REVIEW_CAPABILITIES) or set(
            plain_decisions
        ) != set(REVIEW_CAPABILITIES):
            raise _invalid(
                "AUTHORING.REVIEW_INCOMPLETE",
                "consumer, impact, and audit decisions must each explicitly accept with rationale and evidence",
            )
        selected_authorizations = _readiness_records(
            authorization_records,
            "review authorization",
        )
        observed_owners: set[str] = set()
        observed_authorization_ids: set[str] = set()
        for item in map(_plain_identity, selected_authorizations):
            if not _authorization_record(item):
                raise _invalid(
                    "AUTHORING.INVALID_REVIEW_AUTHORIZATION",
                    "review authorization must satisfy the exact authorization record contract",
                )
            reference = item.get("reference") if type(item) is dict else None
            capability = (
                reference.get("capability") if type(reference) is dict else None
            )
            owner = next(
                (
                    selected_owner
                    for selected_owner, selected_capability in REVIEW_CAPABILITIES.items()
                    if selected_capability == capability
                ),
                None,
            )
            decision = plain_decisions.get(owner) if owner is not None else None
            subject_id = (
                review_decision_subject(analysis_id, revision_id, decision)
                if decision is not None
                else None
            )
            if (
                type(item) is not dict
                or item.get("action") != "review-proposal"
                or item.get("subject_kind") != "proposal-review-decision"
                or item.get("subject_id") != subject_id
                or capability not in REVIEW_CAPABILITIES.values()
            ):
                raise _invalid(
                    "AUTHORING.INVALID_REVIEW_AUTHORIZATION",
                    "review authorization must bind the exact analysis, revision, decision, and capability",
                )
            if owner is not None:
                observed_owners.add(owner)
            if type(reference) is dict:
                observed_authorization_ids.add(str(reference["id"]))
        if (
            len(selected_authorizations) != len(REVIEW_CAPABILITIES)
            or observed_owners != set(REVIEW_CAPABILITIES)
            or len(observed_authorization_ids) != len(REVIEW_CAPABILITIES)
        ):
            raise _invalid(
                "AUTHORING.INVALID_REVIEW_AUTHORIZATION",
                "readiness requires consumer, impact, and audit authorization",
            )
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "analysis_id", analysis_id)
        object.__setattr__(self, "revision_id", revision_id)
        object.__setattr__(self, "decisions", selected_decisions)
        object.__setattr__(self, "authorization_records", selected_authorizations)
        object.__setattr__(self, "expected_target", expected_target)

    @property
    def readiness_id(self) -> str:
        return hash_identity(
            "coding-standards:proposal-readiness:v1",
            "readiness",
            self.identity_material(),
        )

    def identity_material(self) -> IdentityObject:
        return IdentityObject(
            (
                ("analysis", self.analysis_id),
                ("authorization_records", IdentityArray(self.authorization_records)),
                ("base_snapshot", str(self.base_snapshot)),
                ("contract_version", READINESS_CONTRACT_VERSION),
                ("decisions", IdentityArray(self.decisions)),
                ("expected_target", self.expected_target.oid),
                ("revision", self.revision_id),
                ("target_ref", CANONICAL_TARGET_REF),
                ("verification_contract", APPLICATION_VERIFICATION_CONTRACT),
            )
        )

    def aggregate(self) -> AggregateRecord:
        return AggregateRecord(
            self.readiness_id,
            READINESS_KIND,
            encode_identity_value(self.identity_material()),
            (self.base_snapshot,),
        )


@dataclass(frozen=True, slots=True, init=False)
class ProposalApplication:
    base_snapshot: SnapshotId
    readiness_id: str
    revision_id: str
    authorization_record: IdentityObject
    expected_target: RepositoryRevision
    candidate: RepositoryRevision

    def __init__(
        self,
        base_snapshot: SnapshotId,
        readiness_id: str,
        revision_id: str,
        authorization_record: Mapping[str, object],
        expected_target: RepositoryRevision,
        candidate: RepositoryRevision,
    ) -> None:
        if (
            type(base_snapshot) is not SnapshotId
            or not _readiness_id(readiness_id)
            or not _revision_id(revision_id)
            or type(expected_target) is not RepositoryRevision
            or type(candidate) is not RepositoryRevision
            or candidate == expected_target
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION",
                "application requires exact distinct readiness, revision, target, and candidate identities",
            )
        selected = _readiness_records(
            (authorization_record,), "application authorization"
        )
        if len(selected) != 1:
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_AUTHORIZATION",
                "application requires exactly one authorization record",
            )
        plain = _plain_identity(selected[0])
        reference = plain.get("reference") if type(plain) is dict else None
        if (
            not _authorization_record(plain)
            or type(plain) is not dict
            or plain.get("action") != "apply-proposal"
            or plain.get("subject_kind") != "proposal-application"
            or plain.get("subject_id")
            != application_subject(readiness_id, revision_id, expected_target)
            or type(reference) is not dict
            or reference.get("capability") != APPLICATION_CAPABILITY
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_AUTHORIZATION",
                "application authorization must bind the readiness, revision, target, action, and capability",
            )
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "readiness_id", readiness_id)
        object.__setattr__(self, "revision_id", revision_id)
        object.__setattr__(self, "authorization_record", selected[0])
        object.__setattr__(self, "expected_target", expected_target)
        object.__setattr__(self, "candidate", candidate)

    @property
    def application_id(self) -> str:
        return hash_identity(
            "coding-standards:proposal-application:v1",
            "application",
            self.identity_material(),
        )

    def identity_material(self) -> IdentityObject:
        return IdentityObject(
            (
                ("authorization_record", self.authorization_record),
                ("base_snapshot", str(self.base_snapshot)),
                ("candidate", self.candidate.oid),
                ("contract_version", APPLICATION_CONTRACT_VERSION),
                ("expected_target", self.expected_target.oid),
                ("readiness", self.readiness_id),
                ("revision", self.revision_id),
                ("target_ref", CANONICAL_TARGET_REF),
                ("verification_contract", APPLICATION_VERIFICATION_CONTRACT),
                ("verification_result", "passed"),
            )
        )

    def aggregate(self) -> AggregateRecord:
        return AggregateRecord(
            self.application_id,
            APPLICATION_KIND,
            encode_identity_value(self.identity_material()),
            (self.base_snapshot,),
        )

    def applied_outcome(self) -> ProposalApplicationOutcome:
        return ProposalApplicationOutcome(
            self.base_snapshot,
            self.application_id,
            self.candidate,
        )

    def selection(self) -> ProposalApplicationSelection:
        return ProposalApplicationSelection(
            self.base_snapshot,
            self.readiness_id,
            self.application_id,
        )


@dataclass(frozen=True, slots=True, init=False)
class ProposalApplicationSelection:
    base_snapshot: SnapshotId
    readiness_id: str
    application_id: str

    def __init__(
        self,
        base_snapshot: SnapshotId,
        readiness_id: str,
        application_id: str,
    ) -> None:
        if (
            type(base_snapshot) is not SnapshotId
            or not _readiness_id(readiness_id)
            or not _application_id(application_id)
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_SELECTION",
                "application selection requires exact snapshot, readiness, and application identities",
            )
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "readiness_id", readiness_id)
        object.__setattr__(self, "application_id", application_id)

    @property
    def selection_id(self) -> str:
        return application_selection_id(self.readiness_id)

    def identity_material(self) -> IdentityObject:
        return IdentityObject(
            (
                ("application", self.application_id),
                ("contract_version", APPLICATION_SELECTION_CONTRACT_VERSION),
                ("readiness", self.readiness_id),
            )
        )

    def aggregate(self) -> AggregateRecord:
        return AggregateRecord(
            self.selection_id,
            APPLICATION_SELECTION_KIND,
            encode_identity_value(self.identity_material()),
            (self.base_snapshot,),
        )


@dataclass(frozen=True, slots=True, init=False)
class ProposalApplicationOutcome:
    base_snapshot: SnapshotId
    application_id: str
    candidate: RepositoryRevision
    status: Literal["applied"]

    def __init__(
        self,
        base_snapshot: SnapshotId,
        application_id: str,
        candidate: RepositoryRevision,
    ) -> None:
        if (
            type(base_snapshot) is not SnapshotId
            or not _application_id(application_id)
            or type(candidate) is not RepositoryRevision
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_OUTCOME",
                "application outcome requires exact application and candidate identities",
            )
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "application_id", application_id)
        object.__setattr__(self, "candidate", candidate)
        object.__setattr__(self, "status", "applied")

    @property
    def outcome_id(self) -> str:
        return hash_identity(
            "coding-standards:proposal-application-outcome:v1",
            "application-outcome",
            self.identity_material(),
        )

    def identity_material(self) -> IdentityObject:
        return IdentityObject(
            (
                ("application", self.application_id),
                ("candidate", self.candidate.oid),
                ("contract_version", APPLICATION_CONTRACT_VERSION),
                ("observed_target", self.candidate.oid),
                ("status", self.status),
                ("target_ref", CANONICAL_TARGET_REF),
            )
        )

    def aggregate(self) -> AggregateRecord:
        return AggregateRecord(
            self.outcome_id,
            APPLICATION_OUTCOME_KIND,
            encode_identity_value(self.identity_material()),
            (self.base_snapshot,),
        )


@dataclass(frozen=True, slots=True)
class FindProposalsRequest:
    after: ProposalId | None = None
    limit: int = 50

    def __post_init__(self) -> None:
        if self.after is not None and type(self.after) is not ProposalId:
            raise _invalid(
                "AUTHORING.INVALID_CONTINUATION",
                "proposal continuation must be a ProposalId",
            )
        if type(self.limit) is not int or not 1 <= self.limit <= 100:
            raise _invalid(
                "AUTHORING.INVALID_LIMIT",
                "proposal discovery limit must be 1 through 100",
            )


@dataclass(frozen=True, slots=True)
class ProposalPage:
    proposals: tuple[ProposalSummary, ...]
    continuation: ProposalId | None


class AuthoringModule:
    """Owns immutable proposal material and proposal-head coordination."""

    def __init__(
        self,
        snapshots: SnapshotModule,
        *,
        now: Callable[[], int] | None = None,
        proposal_id_factory: Callable[[], ProposalId] | None = None,
    ) -> None:
        self._snapshots = snapshots
        self._now = now or (lambda: int(time.time()))
        self._proposal_id_factory = proposal_id_factory or (
            lambda: ProposalId.from_uuid(uuid.uuid4())
        )

    def create_proposal(
        self,
        base_snapshot: SnapshotId,
        mutations: Iterable[Mutation],
        semantic_proposals: Iterable[Mapping[str, object]],
    ) -> tuple[ProposalSummary, ProposalRevision]:
        proposal = self._proposal_id_factory()
        if type(proposal) is not ProposalId:
            raise _invalid(
                "AUTHORING.INVALID_ID_FACTORY",
                "proposal ID factory must return an exact ProposalId",
            )
        revision = ProposalRevision(
            proposal, 1, base_snapshot, mutations, semantic_proposals
        )
        self._validate_mutation_targets(revision)
        root = AggregateRoot(
            str(proposal),
            PROPOSAL_KIND,
            revision.revision_id,
            (base_snapshot,),
            self._time(),
        )
        self._snapshots.create_aggregate_root(root, revision.aggregate())
        return ProposalSummary(proposal, revision.revision_id), revision

    def find_proposals(self, request: FindProposalsRequest) -> ProposalPage:
        page = self._snapshots.find_aggregate_roots(
            FindAggregateRootsRequest(
                PROPOSAL_KIND,
                None if request.after is None else str(request.after),
                request.limit,
            )
        )
        return ProposalPage(
            tuple(self._summary_from_root(root) for root in page.roots),
            None if page.continuation is None else ProposalId(page.continuation),
        )

    def read_revision(self, revision_id: str) -> ProposalRevision:
        if not _revision_id(revision_id):
            raise _invalid(
                "AUTHORING.INVALID_REVISION_ID",
                "proposal revision ID has an invalid domain or digest",
            )
        revision = self._revision_from_record(
            self._snapshots.load_aggregate(revision_id)
        )
        root = self._snapshots.load_aggregate_root(str(revision.proposal))
        self._validate_root_revision(root, revision)
        return revision

    def revise_proposal(
        self,
        expected_revision: str,
        mutations: Iterable[Mutation],
        semantic_proposals: Iterable[Mapping[str, object]],
    ) -> tuple[ProposalSummary, ProposalRevision]:
        expected = self.read_revision(expected_revision)
        revision = ProposalRevision(
            expected.proposal,
            expected.ordinal + 1,
            expected.base_snapshot,
            mutations,
            semantic_proposals,
        )
        self._validate_mutation_targets(revision)
        advanced = self._snapshots.advance_aggregate_root(
            str(expected.proposal), expected_revision, revision.aggregate()
        )
        if advanced == "stale":
            raise _invalid(
                "AUTHORING.REVISION_STALE",
                "expected proposal revision is no longer the current head",
            )
        return ProposalSummary(expected.proposal, revision.revision_id), revision

    def review_proposal(
        self,
        analysis_id: str,
        revision_id: str,
        decisions: Iterable[Mapping[str, object]],
        authorization_records: Iterable[Mapping[str, object]],
        expected_target: RepositoryRevision,
        *,
        prior_readiness: str | None = None,
    ) -> ProposalReadiness:
        revision = self.read_revision(revision_id)
        readiness = ProposalReadiness(
            revision.base_snapshot,
            analysis_id,
            revision.revision_id,
            decisions,
            authorization_records,
            expected_target,
        )
        if prior_readiness is not None:
            prior = self.read_readiness(prior_readiness)
            if prior != readiness:
                raise _invalid(
                    "AUTHORING.READINESS_MISMATCH",
                    "prior readiness does not match the current review",
                )
        published = self._snapshots.publish_aggregate_if_root_head(
            str(revision.proposal),
            revision.revision_id,
            readiness.aggregate(),
        )
        if published == "stale":
            raise _invalid(
                "AUTHORING.REVISION_STALE",
                "analysis revision is no longer the current proposal head",
            )
        return readiness

    def read_readiness(self, readiness_id: str) -> ProposalReadiness:
        if not _readiness_id(readiness_id):
            raise _invalid(
                "AUTHORING.INVALID_READINESS_ID",
                "readiness ID has an invalid domain or digest",
            )
        readiness = self._readiness_from_record(
            self._snapshots.load_aggregate(readiness_id)
        )
        revision = self.read_revision(readiness.revision_id)
        if revision.base_snapshot != readiness.base_snapshot:
            raise _invalid(
                "AUTHORING.INVALID_STORED_READINESS",
                "stored readiness and revision base snapshots differ",
            )
        return readiness

    def application_revision(
        self, readiness_id: str
    ) -> tuple[ProposalReadiness, ProposalRevision]:
        readiness = self.read_readiness(readiness_id)
        revision = self.read_revision(readiness.revision_id)
        root = self._snapshots.load_aggregate_root(str(revision.proposal))
        self._validate_root_revision(root, revision)
        if root.head_id != revision.revision_id:
            raise _invalid(
                "AUTHORING.READINESS_STALE",
                "readiness revision is no longer the current proposal head",
            )
        return readiness, revision

    def admit_application(
        self,
        readiness_id: str,
        authorization_record: Mapping[str, object],
        candidate: RepositoryRevision,
    ) -> ProposalApplication:
        readiness, revision = self.application_revision(readiness_id)
        application = ProposalApplication(
            readiness.base_snapshot,
            readiness.readiness_id,
            revision.revision_id,
            authorization_record,
            readiness.expected_target,
            candidate,
        )
        try:
            published = self._snapshots.publish_aggregate_set_if_root_head(
                str(revision.proposal),
                revision.revision_id,
                (application.aggregate(), application.selection().aggregate()),
            )
        except SnapshotError as error:
            if error.failure.code != "AGGREGATE.ID_COLLISION":
                raise
            try:
                selected = self._application_selection_from_record(
                    self._snapshots.load_aggregate(
                        application_selection_id(readiness.readiness_id)
                    )
                )
            except SnapshotError:
                raise error
            if selected.application_id != application.application_id:
                raise _invalid(
                    "AUTHORING.APPLICATION_SELECTION_CONFLICT",
                    "one readiness cannot select different verified applications",
                ) from error
            raise
        if published == "stale":
            raise _invalid(
                "AUTHORING.READINESS_STALE",
                "readiness revision is no longer the current proposal head",
            )
        return application

    def read_selected_application(self, readiness_id: str) -> ProposalApplication:
        readiness = self.read_readiness(readiness_id)
        try:
            record = self._snapshots.load_aggregate(
                application_selection_id(readiness.readiness_id)
            )
        except SnapshotError as error:
            if error.failure.code != "AGGREGATE.UNAVAILABLE":
                raise
            raise _unavailable(
                "APPLICATION.NOT_ADMITTED",
                "no verified application was admitted for this readiness",
            ) from error
        selection = self._application_selection_from_record(record)
        if (
            selection.base_snapshot != readiness.base_snapshot
            or selection.readiness_id != readiness.readiness_id
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_SELECTION",
                "stored application selection and readiness authority disagree",
            )
        application = self.read_application(selection.application_id)
        if (
            application.base_snapshot != selection.base_snapshot
            or application.readiness_id != selection.readiness_id
        ):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_SELECTION",
                "stored application selection and application authority disagree",
            )
        return application

    def read_application(self, application_id: str) -> ProposalApplication:
        if not _application_id(application_id):
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_ID",
                "application ID has an invalid domain or digest",
            )
        application = self._application_from_record(
            self._snapshots.load_aggregate(application_id)
        )
        readiness = self.read_readiness(application.readiness_id)
        if (
            readiness.base_snapshot != application.base_snapshot
            or readiness.revision_id != application.revision_id
            or readiness.expected_target != application.expected_target
        ):
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION",
                "stored application and readiness authority disagree",
            )
        return application

    def record_applied(
        self, application: ProposalApplication
    ) -> ProposalApplicationOutcome:
        if type(application) is not ProposalApplication:
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION",
                "applied outcome requires one exact application",
            )
        outcome = application.applied_outcome()
        self._snapshots.publish_aggregate(outcome.aggregate())
        return outcome

    def read_application_outcome(
        self, application_id: str
    ) -> ProposalApplicationOutcome:
        application = self.read_application(application_id)
        expected = application.applied_outcome()
        outcome = self._application_outcome_from_record(
            self._snapshots.load_aggregate(expected.outcome_id)
        )
        if outcome != expected:
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION_OUTCOME",
                "stored application outcome disagrees with its application",
            )
        return outcome

    def application_outcome(
        self, application: ProposalApplication
    ) -> ProposalApplicationOutcome | None:
        if type(application) is not ProposalApplication:
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION",
                "application outcome lookup requires one exact application",
            )
        try:
            return self.read_application_outcome(application.application_id)
        except SnapshotError as error:
            if error.failure.code == "AGGREGATE.UNAVAILABLE":
                return None
            raise

    def _summary_from_root(self, root: AggregateRoot) -> ProposalSummary:
        revision = self._revision_from_record(
            self._snapshots.load_aggregate(root.head_id)
        )
        self._validate_root_revision(root, revision)
        return ProposalSummary(revision.proposal, revision.revision_id)

    @staticmethod
    def _readiness_from_record(record: AggregateRecord) -> ProposalReadiness:
        try:
            material = json.loads(record.payload)
            if (
                type(material) is not dict
                or set(material)
                != {
                    "analysis",
                    "authorization_records",
                    "base_snapshot",
                    "contract_version",
                    "decisions",
                    "expected_target",
                    "revision",
                    "target_ref",
                    "verification_contract",
                }
                or material["contract_version"] != READINESS_CONTRACT_VERSION
                or material["target_ref"] != CANONICAL_TARGET_REF
                or material["verification_contract"]
                != _plain_identity(APPLICATION_VERIFICATION_CONTRACT)
                or type(material["decisions"]) is not list
                or type(material["authorization_records"]) is not list
                or encode_identity_value(_identity_value(material)) != record.payload
            ):
                raise _invalid(
                    "AUTHORING.INVALID_STORED_READINESS",
                    "stored readiness material is not canonical",
                )
            readiness = ProposalReadiness(
                SnapshotId(material["base_snapshot"]),
                material["analysis"],
                material["revision"],
                material["decisions"],
                material["authorization_records"],
                RepositoryRevision(material["expected_target"]),
            )
        except (
            AuthoringError,
            GitRepositoryError,
            IdentityError,
            SnapshotError,
            json.JSONDecodeError,
            UnicodeError,
        ) as error:
            raise _invalid(
                "AUTHORING.INVALID_STORED_READINESS",
                "stored readiness cannot be decoded",
            ) from error
        if record.kind != READINESS_KIND or readiness.aggregate() != record:
            raise _invalid(
                "AUTHORING.INVALID_STORED_READINESS",
                "stored readiness authority disagrees with its identity",
            )
        return readiness

    @staticmethod
    def _application_from_record(record: AggregateRecord) -> ProposalApplication:
        try:
            material = json.loads(record.payload)
            if (
                type(material) is not dict
                or set(material)
                != {
                    "authorization_record",
                    "base_snapshot",
                    "candidate",
                    "contract_version",
                    "expected_target",
                    "readiness",
                    "revision",
                    "target_ref",
                    "verification_contract",
                    "verification_result",
                }
                or material["contract_version"] != APPLICATION_CONTRACT_VERSION
                or material["target_ref"] != CANONICAL_TARGET_REF
                or material["verification_contract"]
                != _plain_identity(APPLICATION_VERIFICATION_CONTRACT)
                or material["verification_result"] != "passed"
                or encode_identity_value(_identity_value(material)) != record.payload
            ):
                raise _invalid(
                    "AUTHORING.INVALID_STORED_APPLICATION",
                    "stored application material is not canonical",
                )
            application = ProposalApplication(
                SnapshotId(material["base_snapshot"]),
                material["readiness"],
                material["revision"],
                material["authorization_record"],
                RepositoryRevision(material["expected_target"]),
                RepositoryRevision(material["candidate"]),
            )
        except (
            AuthoringError,
            GitRepositoryError,
            IdentityError,
            SnapshotError,
            json.JSONDecodeError,
            UnicodeError,
        ) as error:
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION",
                "stored application cannot be decoded",
            ) from error
        if record.kind != APPLICATION_KIND or application.aggregate() != record:
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION",
                "stored application authority disagrees with its identity",
            )
        return application

    @staticmethod
    def _application_selection_from_record(
        record: AggregateRecord,
    ) -> ProposalApplicationSelection:
        try:
            material = json.loads(record.payload)
            if (
                type(material) is not dict
                or set(material)
                != {
                    "application",
                    "contract_version",
                    "readiness",
                }
                or material["contract_version"]
                != APPLICATION_SELECTION_CONTRACT_VERSION
                or encode_identity_value(_identity_value(material)) != record.payload
                or len(record.snapshots) != 1
            ):
                raise _invalid(
                    "AUTHORING.INVALID_APPLICATION_SELECTION",
                    "stored application selection is not canonical",
                )
            selection = ProposalApplicationSelection(
                record.snapshots[0],
                material["readiness"],
                material["application"],
            )
        except (
            AuthoringError,
            IdentityError,
            SnapshotError,
            json.JSONDecodeError,
            UnicodeError,
            IndexError,
        ) as error:
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_SELECTION",
                "stored application selection cannot be decoded",
            ) from error
        if record.kind != APPLICATION_SELECTION_KIND or selection.aggregate() != record:
            raise _invalid(
                "AUTHORING.INVALID_APPLICATION_SELECTION",
                "stored application selection authority disagrees with its identity",
            )
        return selection

    @staticmethod
    def _application_outcome_from_record(
        record: AggregateRecord,
    ) -> ProposalApplicationOutcome:
        try:
            material = json.loads(record.payload)
            if (
                type(material) is not dict
                or set(material)
                != {
                    "application",
                    "candidate",
                    "contract_version",
                    "observed_target",
                    "status",
                    "target_ref",
                }
                or material["contract_version"] != APPLICATION_CONTRACT_VERSION
                or material["target_ref"] != CANONICAL_TARGET_REF
                or material["status"] != "applied"
                or material["candidate"] != material["observed_target"]
                or encode_identity_value(_identity_value(material)) != record.payload
            ):
                raise _invalid(
                    "AUTHORING.INVALID_STORED_APPLICATION_OUTCOME",
                    "stored application outcome is not canonical",
                )
            application = material["application"]
            candidate = RepositoryRevision(material["candidate"])
            base_snapshot = record.snapshots[0]
            outcome = ProposalApplicationOutcome(
                base_snapshot,
                application,
                candidate,
            )
        except (
            AuthoringError,
            GitRepositoryError,
            IdentityError,
            SnapshotError,
            json.JSONDecodeError,
            UnicodeError,
            IndexError,
        ) as error:
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION_OUTCOME",
                "stored application outcome cannot be decoded",
            ) from error
        if record.kind != APPLICATION_OUTCOME_KIND or outcome.aggregate() != record:
            raise _invalid(
                "AUTHORING.INVALID_STORED_APPLICATION_OUTCOME",
                "stored application outcome authority disagrees with its identity",
            )
        return outcome

    @staticmethod
    def _revision_from_record(record: AggregateRecord) -> ProposalRevision:
        try:
            material = json.loads(record.payload)
            if (
                type(material) is not dict
                or set(material)
                != {
                    "base_snapshot",
                    "contract_version",
                    "mutations",
                    "ordinal",
                    "proposal",
                    "semantic_proposals",
                }
                or material["contract_version"] != AUTHORING_CONTRACT_VERSION
                or type(material["mutations"]) is not list
                or type(material["semantic_proposals"]) is not list
                or encode_identity_value(_identity_value(material)) != record.payload
            ):
                raise _invalid(
                    "AUTHORING.INVALID_STORED_REVISION",
                    "stored proposal revision material is not canonical",
                )
            revision = ProposalRevision(
                ProposalId(material["proposal"]),
                material["ordinal"],
                SnapshotId(material["base_snapshot"]),
                (_stored_mutation(item) for item in material["mutations"]),
                material["semantic_proposals"],
            )
        except (
            AuthoringError,
            IdentityError,
            SnapshotError,
            json.JSONDecodeError,
            UnicodeError,
        ) as error:
            raise _invalid(
                "AUTHORING.INVALID_STORED_REVISION",
                "stored proposal revision cannot be decoded",
            ) from error
        if record.kind != REVISION_KIND or revision.aggregate() != record:
            raise _invalid(
                "AUTHORING.INVALID_STORED_REVISION",
                "stored proposal revision authority disagrees with its identity",
            )
        return revision

    @staticmethod
    def _validate_root_revision(
        root: AggregateRoot, revision: ProposalRevision
    ) -> None:
        if (
            root.kind != PROPOSAL_KIND
            or revision.proposal != ProposalId(root.aggregate_id)
            or root.snapshots != (revision.base_snapshot,)
        ):
            raise _invalid(
                "AUTHORING.INVALID_STORED_REVISION",
                "stored proposal root and revision authority disagree",
            )

    def _validate_mutation_targets(self, revision: ProposalRevision) -> None:
        available_paths = {
            item.path
            for item in self._snapshots.load_content(revision.base_snapshot).files
        }
        missing = [
            item.path for item in revision.mutations if item.path not in available_paths
        ]
        if missing:
            raise _invalid(
                "AUTHORING.MUTATION_TARGET_UNAVAILABLE",
                f"replacement target {missing[0]} is unavailable in the base snapshot",
            )

    def _time(self) -> int:
        observed = self._now()
        if type(observed) is not int or observed < 0:
            raise _invalid(
                "AUTHORING.INVALID_TIME", "clock must return a nonnegative integer"
            )
        return observed


def _identity_value(value: object) -> IdentityValue:
    value_type = type(value)
    if value is None or value_type in {bool, int, str}:
        return value  # type: ignore[return-value]
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise _invalid(
                "AUTHORING.INVALID_SEMANTIC_PROPOSAL",
                "semantic proposal keys must be exact strings",
            )
        return IdentityObject(
            (key, _identity_value(item)) for key, item in value.items()
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return IdentityArray(_identity_value(item) for item in value)
    raise _invalid(
        "AUTHORING.INVALID_SEMANTIC_PROPOSAL",
        "semantic proposal contains an unsupported value",
    )


def _identity_record(value: Mapping[str, object]) -> IdentityObject:
    selected = _identity_value(value)
    if type(selected) is not IdentityObject:
        raise _invalid(
            "AUTHORING.INVALID_SEMANTIC_PROPOSAL",
            "semantic proposal must be an object",
        )
    return selected


def _plain_identity(value: IdentityValue) -> object:
    if isinstance(value, IdentityObject):
        return {key: _plain_identity(item) for key, item in value.members}
    if isinstance(value, IdentityArray):
        return [_plain_identity(item) for item in value.values]
    return value


def _readiness_records(
    values: Iterable[Mapping[str, object]],
    label: str,
) -> tuple[IdentityObject, ...]:
    try:
        selected = tuple(_identity_record(item) for item in values)
    except (AuthoringError, TypeError) as error:
        raise _invalid(
            "AUTHORING.INVALID_READINESS",
            f"{label} must contain canonical identity values",
        ) from error
    return tuple(
        item
        for _encoded, item in sorted(
            {encode_identity_value(item): item for item in selected}.items()
        )
    )


def _review_decision(value: Mapping[str, object]) -> IdentityObject:
    try:
        selected = _identity_record(value)
        plain = _plain_identity(selected)
    except (AuthoringError, TypeError) as error:
        raise _invalid(
            "AUTHORING.INVALID_REVIEW_DECISION",
            "review decision must contain canonical identity values",
        ) from error
    evidence = plain.get("evidence") if type(plain) is dict else None
    if (
        type(plain) is not dict
        or set(plain) != {"owner", "decision", "rationale", "evidence"}
        or plain["owner"] not in REVIEW_CAPABILITIES
        or plain["decision"] != "accept"
        or not _nonempty_scalar_string(plain["rationale"])
        or type(evidence) is not list
        or not evidence
        or any(not _evidence_reference(item) for item in evidence)
        or len({encode_identity_value(_identity_value(item)) for item in evidence})
        != len(evidence)
    ):
        raise _invalid(
            "AUTHORING.INVALID_REVIEW_DECISION",
            "review decision requires an exact owner, acceptance, rationale, and unique evidence",
        )
    normalized = dict(plain)
    normalized["evidence"] = sorted(
        evidence,
        key=lambda item: encode_identity_value(_identity_value(item)),
    )
    return _identity_record(normalized)


def review_decision_subject(
    analysis_id: str,
    revision_id: str,
    decision: Mapping[str, object],
) -> str:
    if not _analysis_id(analysis_id) or not _revision_id(revision_id):
        raise _invalid(
            "AUTHORING.INVALID_REVIEW_DECISION",
            "review decision subject requires exact analysis and revision identities",
        )
    return hash_identity(
        "coding-standards:proposal-review-decision:v1",
        "proposal-review-decision",
        IdentityObject(
            (
                ("analysis", analysis_id),
                ("decision", _review_decision(decision)),
                ("revision", revision_id),
            )
        ),
    )


def application_subject(
    readiness_id: str,
    revision_id: str,
    expected_target: RepositoryRevision,
) -> str:
    if (
        not _readiness_id(readiness_id)
        or not _revision_id(revision_id)
        or type(expected_target) is not RepositoryRevision
    ):
        raise _invalid(
            "AUTHORING.INVALID_APPLICATION",
            "application subject requires exact readiness, revision, and target identities",
        )
    return hash_identity(
        "coding-standards:proposal-application-subject:v1",
        "proposal-application",
        IdentityObject(
            (
                ("expected_target", expected_target.oid),
                ("readiness", readiness_id),
                ("revision", revision_id),
                ("target_ref", CANONICAL_TARGET_REF),
                ("verification_contract", APPLICATION_VERIFICATION_CONTRACT),
            )
        ),
    )


def application_selection_id(readiness_id: str) -> str:
    if not _readiness_id(readiness_id):
        raise _invalid(
            "AUTHORING.INVALID_READINESS_ID",
            "application selection requires one exact readiness identity",
        )
    return hash_identity(
        "coding-standards:proposal-application-selection:v1",
        "application-selection",
        IdentityObject((("readiness", readiness_id),)),
    )


def application_recovery_subject(
    readiness_id: str,
    revision_id: str,
    expected_target: RepositoryRevision,
) -> str:
    if (
        not _readiness_id(readiness_id)
        or not _revision_id(revision_id)
        or type(expected_target) is not RepositoryRevision
    ):
        raise _invalid(
            "AUTHORING.INVALID_APPLICATION_RECOVERY",
            "application recovery requires exact readiness, revision, and target identities",
        )
    return hash_identity(
        "coding-standards:proposal-application-recovery-subject:v1",
        "proposal-application-recovery",
        IdentityObject(
            (
                ("expected_target", expected_target.oid),
                ("readiness", readiness_id),
                ("revision", revision_id),
                ("target_ref", CANONICAL_TARGET_REF),
                ("verification_contract", APPLICATION_VERIFICATION_CONTRACT),
            )
        ),
    )


def _evidence_reference(value: object) -> bool:
    if type(value) is not dict or set(value) != {
        "id",
        "digest",
        "provider_contract",
        "provider_contract_version",
    }:
        return False
    return (
        _canonical_id(value["id"])
        and _digest(value["digest"])
        and _canonical_id(value["provider_contract"])
        and _nonempty_scalar_string(value["provider_contract_version"])
    )


def _authorization_record(value: object) -> bool:
    if type(value) is not dict or set(value) != {
        "reference",
        "issuer_semantic_revision",
        "principal",
        "action",
        "subject_kind",
        "subject_id",
        "authorization_evidence",
        "revocation_authority",
        "revocation_authority_semantic_revision",
        "revocation_evidence",
    }:
        return False
    reference = value["reference"]
    if (
        type(reference) is not dict
        or set(reference) != {"id", "issuer", "capability", "authority_digest"}
        or not _digest_id(reference["id"], "authorization:sha256:")
        or not _canonical_id(reference["issuer"])
        or not _canonical_id(reference["capability"])
        or not _digest(reference["authority_digest"])
        or type(value["issuer_semantic_revision"]) is not int
        or value["issuer_semantic_revision"] < 1
        or not _canonical_id(value["principal"])
        or not _canonical_id(value["action"])
        or not _canonical_id(value["subject_kind"])
        or not _nonempty_scalar_string(value["subject_id"])
        or not _canonical_id(value["revocation_authority"])
        or type(value["revocation_authority_semantic_revision"]) is not int
        or value["revocation_authority_semantic_revision"] < 1
    ):
        return False
    for key in ("authorization_evidence", "revocation_evidence"):
        evidence = value[key]
        if (
            type(evidence) is not list
            or not evidence
            or any(not _evidence_reference(item) for item in evidence)
            or len({encode_identity_value(_identity_value(item)) for item in evidence})
            != len(evidence)
        ):
            return False
    return True


def _canonical_id(value: object) -> bool:
    return (
        type(value) is str
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", value) is not None
    )


def _digest(value: object) -> bool:
    return (
        type(value) is str and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None
    )


def _nonempty_scalar_string(value: object) -> bool:
    return (
        type(value) is str
        and bool(value)
        and not any(0xD800 <= ord(character) <= 0xDFFF for character in value)
    )


def _stored_mutation(value: object) -> Mutation:
    if (
        type(value) is not dict
        or set(value) != {"op", "path", "value"}
        or value["op"] != "replace"
        or type(value["path"]) is not str
        or type(value["value"]) is not str
    ):
        raise _invalid(
            "AUTHORING.INVALID_STORED_REVISION",
            "stored proposal mutation is invalid",
        )
    return Mutation(SnapshotPath.parse(value["path"]), value["value"])


def _revision_id(value: object) -> bool:
    if type(value) is not str or not value.startswith("proposal-revision:sha256:"):
        return False
    digest = value.removeprefix("proposal-revision:sha256:")
    return len(digest) == 64 and all(
        character in "0123456789abcdef" for character in digest
    )


def _analysis_id(value: object) -> bool:
    return _digest_id(value, "analysis:sha256:")


def _readiness_id(value: object) -> bool:
    return _digest_id(value, "readiness:sha256:")


def _application_id(value: object) -> bool:
    return _digest_id(value, "application:sha256:")


def _digest_id(value: object, prefix: str) -> bool:
    if type(value) is not str or not value.startswith(prefix):
        return False
    digest = value.removeprefix(prefix)
    return len(digest) == 64 and all(
        character in "0123456789abcdef" for character in digest
    )


__all__ = (
    "APPLICATION_CAPABILITY",
    "APPLICATION_CONTRACT_VERSION",
    "APPLICATION_KIND",
    "APPLICATION_OUTCOME_KIND",
    "APPLICATION_RECOVERY_CAPABILITY",
    "APPLICATION_SELECTION_CONTRACT_VERSION",
    "APPLICATION_SELECTION_KIND",
    "AUTHORING_CONTRACT_VERSION",
    "APPLICATION_VERIFICATION_CONTRACT",
    "CANONICAL_TARGET_BRANCH",
    "CANONICAL_TARGET_REF",
    "AuthoringError",
    "AuthoringFailure",
    "AuthoringModule",
    "FindProposalsRequest",
    "Mutation",
    "ProposalApplication",
    "ProposalApplicationOutcome",
    "ProposalApplicationSelection",
    "ProposalId",
    "ProposalPage",
    "ProposalReadiness",
    "ProposalRevision",
    "ProposalSummary",
    "READINESS_CONTRACT_VERSION",
    "READINESS_KIND",
    "REVIEW_CAPABILITIES",
    "application_recovery_subject",
    "application_selection_id",
    "application_subject",
    "review_decision_subject",
)
