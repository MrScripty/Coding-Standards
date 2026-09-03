from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

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
PROPOSAL_KIND = "proposal"
REVISION_KIND = "proposal-revision"
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

    def _summary_from_root(self, root: AggregateRoot) -> ProposalSummary:
        revision = self._revision_from_record(
            self._snapshots.load_aggregate(root.head_id)
        )
        self._validate_root_revision(root, revision)
        return ProposalSummary(revision.proposal, revision.revision_id)

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


__all__ = (
    "AUTHORING_CONTRACT_VERSION",
    "AuthoringError",
    "AuthoringFailure",
    "AuthoringModule",
    "FindProposalsRequest",
    "Mutation",
    "ProposalId",
    "ProposalPage",
    "ProposalRevision",
    "ProposalSummary",
)
