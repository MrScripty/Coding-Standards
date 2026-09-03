from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from tools.standards_identity.standards_identity import IdentityObject
from tools.standards_snapshots.standards_snapshots import (
    AggregateChild,
    AggregateRecord,
    SnapshotId,
)

from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_identity, analysis_key, analysis_key_bytes, raw_digest


ANALYSIS_CONTRACT_VERSION = 6
ANALYSIS_IDENTITY_DOMAIN = "coding-standards:analysis:v6"
ANALYSIS_AGGREGATE_KIND = "analysis-state"
ANALYSIS_STATE_FIELDS = {
    "base_snapshot",
    "proposed_material",
    "changes",
    "semantic_proposals",
    "fact_observations",
    "dispositions",
    "coverage_attestations",
    "authorization_records",
    "domain_contracts",
    "execution_contracts",
    "contract_version",
}
_PROPOSAL_REVISION_ID = re.compile(r"^proposal-revision:sha256:[0-9a-f]{64}$")


def _error(code: str, message: str) -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, "invalid", message))


def _plain(value: object) -> object:
    if isinstance(value, IdentityObject):
        return {key: _plain(item) for key, item in value.members}
    values = getattr(value, "values", None)
    if type(values) is tuple:
        return [_plain(item) for item in values]
    return value


def _record(value: Mapping[str, object], label: str) -> IdentityObject:
    selected = analysis_key(value)
    if not isinstance(selected, IdentityObject):
        raise TypeError(f"{label} must be an object")
    return selected


def _record_bytes(value: IdentityObject) -> bytes:
    return analysis_key_bytes(_plain(value))


def _records(
    values: Iterable[Mapping[str, object] | IdentityObject],
    *,
    label: str,
    key: str,
) -> tuple[IdentityObject, ...]:
    selected = []
    by_key: dict[str, bytes] = {}
    for supplied in values:
        item = (
            supplied
            if isinstance(supplied, IdentityObject)
            else _record(supplied, label)
        )
        plain = _plain(item)
        if not isinstance(plain, dict) or type(plain.get(key)) is not str:
            raise _error(
                "ANALYSIS.INVALID_DECISION",
                f"{label} requires a nonempty {key}.",
            )
        decision_key = plain[key]
        encoded = _record_bytes(item)
        previous = by_key.get(decision_key)
        if previous is not None and previous != encoded:
            raise _error(
                "ANALYSIS.CONFLICTING_DECISION",
                f"{label} contains conflicting decisions for {decision_key}.",
            )
        by_key[decision_key] = encoded
        selected.append(item)
    return tuple(
        item
        for _, item in sorted({_record_bytes(item): item for item in selected}.items())
    )


def _authorization_records(
    values: Iterable[Mapping[str, object] | IdentityObject],
) -> tuple[IdentityObject, ...]:
    selected: dict[str, tuple[bytes, IdentityObject]] = {}
    for supplied in values:
        item = (
            supplied
            if isinstance(supplied, IdentityObject)
            else _record(supplied, "authorization record")
        )
        plain = _plain(item)
        reference = plain.get("reference") if isinstance(plain, dict) else None
        identifier = reference.get("id") if isinstance(reference, dict) else None
        if type(identifier) is not str or not identifier:
            raise _error(
                "ANALYSIS.INVALID_AUTHORIZATION",
                "Authorization record requires an exact reference ID.",
            )
        encoded = _record_bytes(item)
        previous = selected.get(identifier)
        if previous is not None and previous[0] != encoded:
            raise _error(
                "ANALYSIS.CONFLICTING_AUTHORIZATION",
                f"Authorization {identifier} has conflicting records.",
            )
        selected[identifier] = (encoded, item)
    return tuple(item for _, item in sorted(selected.values()))


@dataclass(frozen=True, slots=True)
class SnapshotMaterialRef:
    snapshot: SnapshotId

    def __post_init__(self) -> None:
        if type(self.snapshot) is not SnapshotId:
            raise _error(
                "ANALYSIS.INVALID_MATERIAL",
                "Snapshot material requires an exact snapshot root.",
            )

    def as_contract(self) -> dict[str, object]:
        return {"kind": "snapshot", "snapshot": str(self.snapshot)}


@dataclass(frozen=True, slots=True)
class ProjectedRevisionMaterialRef:
    revision_id: str
    base_snapshot: SnapshotId

    def __post_init__(self) -> None:
        if (
            type(self.revision_id) is not str
            or _PROPOSAL_REVISION_ID.fullmatch(self.revision_id) is None
            or type(self.base_snapshot) is not SnapshotId
        ):
            raise _error(
                "ANALYSIS.INVALID_MATERIAL",
                "Projected material requires an exact proposal revision and base root.",
            )

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "projected-revision",
            "revision_id": self.revision_id,
            "base_snapshot": str(self.base_snapshot),
        }


ProposedMaterialRef = SnapshotMaterialRef | ProjectedRevisionMaterialRef


def _material_ref(value: object) -> ProposedMaterialRef:
    if type(value) is not dict or type(value.get("kind")) is not str:
        raise _error(
            "ANALYSIS.INVALID_MATERIAL",
            "Proposed material reference is invalid.",
        )
    if value["kind"] == "snapshot" and set(value) == {"kind", "snapshot"}:
        return SnapshotMaterialRef(SnapshotId(value["snapshot"]))
    if value["kind"] == "projected-revision" and set(value) == {
        "kind",
        "revision_id",
        "base_snapshot",
    }:
        return ProjectedRevisionMaterialRef(
            value["revision_id"],
            SnapshotId(value["base_snapshot"]),
        )
    raise _error(
        "ANALYSIS.INVALID_MATERIAL",
        "Proposed material reference kind or fields are invalid.",
    )


@dataclass(frozen=True, slots=True, init=False)
class AnalysisState:
    base_snapshot: SnapshotId
    proposed_material: ProposedMaterialRef
    changes: tuple[IdentityObject, ...]
    semantic_proposals: tuple[IdentityObject, ...]
    fact_observations: tuple[IdentityObject, ...]
    dispositions: tuple[IdentityObject, ...]
    coverage_attestations: tuple[IdentityObject, ...]
    authorization_records: tuple[IdentityObject, ...]
    domain_contracts: tuple[IdentityObject, ...]
    execution_contracts: IdentityObject

    def __init__(
        self,
        base_snapshot: SnapshotId,
        proposed_material: ProposedMaterialRef,
        changes: Iterable[Mapping[str, object] | IdentityObject],
        semantic_proposals: Iterable[Mapping[str, object] | IdentityObject] = (),
        fact_observations: Iterable[Mapping[str, object] | IdentityObject] = (),
        dispositions: Iterable[Mapping[str, object] | IdentityObject] = (),
        coverage_attestations: Iterable[Mapping[str, object] | IdentityObject] = (),
        authorization_records: Iterable[Mapping[str, object] | IdentityObject] = (),
        domain_contracts: Iterable[Mapping[str, object] | IdentityObject] = (),
        execution_contracts: Mapping[str, object] | IdentityObject | None = None,
    ) -> None:
        if type(base_snapshot) is not SnapshotId or not isinstance(
            proposed_material,
            (SnapshotMaterialRef, ProjectedRevisionMaterialRef),
        ):
            raise _error(
                "ANALYSIS.INVALID_MATERIAL",
                "AnalysisState requires an exact base and proposed material.",
            )
        if (
            isinstance(proposed_material, ProjectedRevisionMaterialRef)
            and proposed_material.base_snapshot != base_snapshot
        ):
            raise _error(
                "ANALYSIS.MATERIAL_BASE_MISMATCH",
                "Projected material must use the analysis base snapshot.",
            )
        selected_changes = tuple(
            sorted(
                {
                    _record_bytes(item): item
                    for item in (
                        value
                        if isinstance(value, IdentityObject)
                        else _record(value, "change")
                        for value in changes
                    )
                }.values(),
                key=_record_bytes,
            )
        )
        if not selected_changes:
            raise _error("ANALYSIS.EMPTY_CHANGE", "AnalysisState requires a change.")
        selected_proposals = tuple(
            sorted(
                {
                    _record_bytes(item): item
                    for item in (
                        value
                        if isinstance(value, IdentityObject)
                        else _record(value, "semantic proposal")
                        for value in semantic_proposals
                    )
                }.values(),
                key=_record_bytes,
            )
        )
        selected_domain_contracts = _records(
            domain_contracts,
            label="domain contract",
            key="id",
        )
        if not selected_domain_contracts:
            raise _error(
                "ANALYSIS.EMPTY_DOMAIN_CONTRACTS",
                "AnalysisState requires material domain contracts.",
            )
        selected_execution_contracts = (
            _record(
                {
                    "authorization_authority_digest": None,
                    "providers": [],
                },
                "execution contracts",
            )
            if execution_contracts is None
            else (
                execution_contracts
                if isinstance(execution_contracts, IdentityObject)
                else _record(execution_contracts, "execution contracts")
            )
        )
        object.__setattr__(self, "base_snapshot", base_snapshot)
        object.__setattr__(self, "proposed_material", proposed_material)
        object.__setattr__(self, "changes", selected_changes)
        object.__setattr__(self, "semantic_proposals", selected_proposals)
        object.__setattr__(
            self,
            "fact_observations",
            _records(fact_observations, label="fact observation", key="requirement_id"),
        )
        object.__setattr__(
            self,
            "dispositions",
            _records(dispositions, label="disposition", key="obligation_id"),
        )
        object.__setattr__(
            self,
            "coverage_attestations",
            _records(
                coverage_attestations,
                label="coverage attestation",
                key="requirement_id",
            ),
        )
        object.__setattr__(
            self,
            "authorization_records",
            _authorization_records(authorization_records),
        )
        object.__setattr__(self, "domain_contracts", selected_domain_contracts)
        object.__setattr__(self, "execution_contracts", selected_execution_contracts)

    @property
    def analysis_id(self) -> str:
        return analysis_identity(
            ANALYSIS_IDENTITY_DOMAIN,
            "analysis",
            self.identity_material(),
        )

    def identity_material(self) -> dict[str, object]:
        return {
            "base_snapshot": str(self.base_snapshot),
            "proposed_material": self.proposed_material.as_contract(),
            "changes": [_plain(item) for item in self.changes],
            "semantic_proposals": [_plain(item) for item in self.semantic_proposals],
            "fact_observations": [_plain(item) for item in self.fact_observations],
            "dispositions": [_plain(item) for item in self.dispositions],
            "coverage_attestations": [
                _plain(item) for item in self.coverage_attestations
            ],
            "authorization_records": [
                _plain(item) for item in self.authorization_records
            ],
            "domain_contracts": [_plain(item) for item in self.domain_contracts],
            "execution_contracts": _plain(self.execution_contracts),
            "contract_version": ANALYSIS_CONTRACT_VERSION,
        }

    def encode(self) -> bytes:
        return analysis_key_bytes(self.identity_material())

    @classmethod
    def decode(cls, payload: bytes) -> AnalysisState:
        if type(payload) is not bytes:
            raise _error(
                "ANALYSIS.INVALID_STATE", "Analysis state payload must be bytes."
            )
        try:
            raw = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise _error(
                "ANALYSIS.INVALID_STATE", "Analysis state payload is invalid."
            ) from error
        if type(raw) is not dict or type(raw.get("contract_version")) is not int:
            raise _error(
                "ANALYSIS.INVALID_STATE",
                "Analysis state requires an integer contract version.",
            )
        if raw["contract_version"] != ANALYSIS_CONTRACT_VERSION:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.STATE_CONTRACT_UNSUPPORTED",
                    "unsupported",
                    "Analysis state contract is unsupported.",
                )
            )
        if set(raw) != ANALYSIS_STATE_FIELDS:
            raise _error(
                "ANALYSIS.INVALID_STATE",
                "Analysis state fields are invalid.",
            )
        try:
            state = cls(
                SnapshotId(raw["base_snapshot"]),
                _material_ref(raw["proposed_material"]),
                raw["changes"],
                raw["semantic_proposals"],
                raw["fact_observations"],
                raw["dispositions"],
                raw["coverage_attestations"],
                raw["authorization_records"],
                raw["domain_contracts"],
                raw["execution_contracts"],
            )
        except (AnalysisError, KeyError, TypeError, ValueError) as error:
            raise _error(
                "ANALYSIS.INVALID_STATE",
                "Analysis state fields do not satisfy the current contract.",
            ) from error
        if state.encode() != payload:
            raise _error(
                "ANALYSIS.NONCANONICAL_STATE",
                "Analysis state payload is not canonical.",
            )
        return state

    def with_decisions(
        self,
        *,
        fact_observations: Iterable[Mapping[str, object] | IdentityObject]
        | None = None,
        dispositions: Iterable[Mapping[str, object] | IdentityObject] | None = None,
        coverage_attestations: Iterable[Mapping[str, object] | IdentityObject]
        | None = None,
        authorization_records: Iterable[Mapping[str, object] | IdentityObject]
        | None = None,
    ) -> AnalysisState:
        return AnalysisState(
            self.base_snapshot,
            self.proposed_material,
            self.changes,
            self.semantic_proposals,
            self.fact_observations if fact_observations is None else fact_observations,
            self.dispositions if dispositions is None else dispositions,
            (
                self.coverage_attestations
                if coverage_attestations is None
                else coverage_attestations
            ),
            (
                self.authorization_records
                if authorization_records is None
                else authorization_records
            ),
            self.domain_contracts,
            self.execution_contracts,
        )

    def aggregate(
        self,
        children: Iterable[tuple[str, str, Mapping[str, object]]],
    ) -> AggregateRecord:
        dependencies = {self.base_snapshot}
        if isinstance(self.proposed_material, SnapshotMaterialRef):
            dependencies.add(self.proposed_material.snapshot)
        return AggregateRecord(
            self.analysis_id,
            ANALYSIS_AGGREGATE_KIND,
            self.encode(),
            dependencies,
            (
                AggregateChild(kind, child_id, analysis_key_bytes(payload))
                for kind, child_id, payload in children
            ),
        )


def analysis_handle(analysis_id: str) -> dict[str, object]:
    return {
        "kind": "analysis-handle",
        "id": analysis_id,
        "schema_version": 6,
    }


def child_handle(
    analysis_id: str,
    child_kind: str,
    child_id: str,
) -> dict[str, object]:
    return {
        "kind": "analysis-child-handle",
        "analysis": analysis_handle(analysis_id),
        "child_kind": child_kind,
        "child_id": child_id,
        "schema_version": 6,
    }


def child_id(value: Mapping[str, object]) -> str:
    return raw_digest(analysis_key_bytes(value))


def plain_record(value: IdentityObject) -> dict[str, object]:
    selected = _plain(value)
    if not isinstance(selected, dict):
        raise TypeError("analysis record must project as an object")
    return selected


__all__ = (
    "ANALYSIS_AGGREGATE_KIND",
    "ANALYSIS_CONTRACT_VERSION",
    "ANALYSIS_IDENTITY_DOMAIN",
    "ANALYSIS_STATE_FIELDS",
    "AnalysisState",
    "ProjectedRevisionMaterialRef",
    "ProposedMaterialRef",
    "SnapshotMaterialRef",
    "analysis_handle",
    "child_handle",
    "child_id",
    "plain_record",
)
