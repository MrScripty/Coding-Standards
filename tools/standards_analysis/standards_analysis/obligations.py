from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping

from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    PolicyUnit,
    PolicyUnitTombstone,
    canonical_json_bytes,
    digest_bytes,
    project_unmapped_module,
)

from .changes import ClassifiedChange, ReviewScope
from .serialization import identity


OBLIGATION_DOMAIN = "coding-standards:obligation:v1"
ABSENT_DIGEST = digest_bytes(canonical_json_bytes({"state": "absent"}))


@dataclass(frozen=True, slots=True)
class DecisionDependency:
    dependency_class: str
    identity: str
    digest: str

    def as_contract(self) -> dict[str, str]:
        return {
            "class": self.dependency_class,
            "identity": self.identity,
            "digest": self.digest,
        }


@dataclass(frozen=True, slots=True)
class DecisionContract:
    id: str
    version: int
    dependency_classes: tuple[str, ...]

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "decision-contract",
            "id": self.id,
            "version": self.version,
            "dependency_classes": list(self.dependency_classes),
        }


UNMAPPED_DECISION_CONTRACT = DecisionContract(
    "decision-contract.unmapped-normative-change.v1",
    1,
    (
        "analysis-contract",
        "module-locator",
        "policy-unit",
        "representation",
    ),
)
ANALYSIS_CONTRACT_DIGEST = digest_bytes(
    canonical_json_bytes(UNMAPPED_DECISION_CONTRACT.as_contract())
)


@dataclass(frozen=True, slots=True)
class DecisionFingerprint:
    decision_kind: str
    decision_contract: str
    dependencies: tuple[DecisionDependency, ...]
    schema_version: int = 1

    def as_contract(self) -> dict[str, object]:
        return {
            "decision_kind": self.decision_kind,
            "decision_contract": self.decision_contract,
            "schema_version": self.schema_version,
            "dependencies": [item.as_contract() for item in self.dependencies],
        }


@dataclass(frozen=True, slots=True)
class Obligation:
    id: str
    kind: str
    source: str
    target: str
    scope: ReviewScope
    reason: Mapping[str, str]
    state: str
    permitted_submissions: tuple[str, ...]
    fingerprint: DecisionFingerprint
    applicability: str = "not-declared"

    def __post_init__(self) -> None:
        object.__setattr__(self, "reason", MappingProxyType(dict(self.reason)))

    def as_contract(self) -> dict[str, object]:
        return {
            "id": self.id,
            "kind": self.kind,
            "source": self.source,
            "target": self.target,
            "scope": self.scope.as_contract(),
            "reason": dict(self.reason),
            "state": self.state,
            "applicability": self.applicability,
            "permitted_submissions": list(self.permitted_submissions),
            "fingerprint": self.fingerprint.as_contract(),
        }


def _authority_digest(value: PolicyUnit | PolicyUnitTombstone | None) -> str:
    if value is None:
        return ABSENT_DIGEST
    if isinstance(value, PolicyUnitTombstone):
        projection: dict[str, object] = {
            "state": "retired",
            "id": value.id,
            "retired_semantic_revision": value.retired_semantic_revision,
            "successors": list(value.successors),
            "evidence": value.evidence,
        }
    else:
        projection = {
            "state": "active",
            "id": value.id,
            "module": value.module,
            "heading_path": list(value.heading_path),
            "semantic_revision": value.semantic_revision,
            "aliases": list(value.aliases),
            "predecessors": list(value.predecessors),
            "successors": list(value.successors),
            "representation_digest": value.representation_digest,
            "structural_digest": value.structural_digest,
        }
    return digest_bytes(canonical_json_bytes(projection))


def _module_policy_ids(
    accepted: CanonicalStandardsCorpus,
    proposed: CanonicalStandardsCorpus,
    module_id: str,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                unit.id
                for corpus in (accepted, proposed)
                for unit in corpus.policy_unit_corpus.for_module(module_id)
            }
        )
    )


def generate_unmapped_normative_obligations(
    accepted_root: Path,
    accepted: CanonicalStandardsCorpus,
    proposed_root: Path,
    proposed: CanonicalStandardsCorpus,
    changes: Iterable[ClassifiedChange],
) -> tuple[Obligation, ...]:
    selected = tuple(changes)
    claimed = {
        policy_id
        for change in selected
        for policy_id in (
            *change.descriptor.accepted_ids,
            *change.descriptor.proposed_ids,
        )
    }
    accepted_modules = {module.module_id: module for module in accepted.modules}
    proposed_modules = {module.module_id: module for module in proposed.modules}
    obligations: list[Obligation] = []

    for module_id in sorted(set(accepted_modules) | set(proposed_modules)):
        before_module = accepted_modules.get(module_id)
        after_module = proposed_modules.get(module_id)
        if all(
            module is None or module.role == "reference"
            for module in (before_module, after_module)
        ):
            continue

        before_projection = (
            None
            if before_module is None
            else project_unmapped_module(accepted_root, accepted, module_id)
        )
        after_projection = (
            None
            if after_module is None
            else project_unmapped_module(proposed_root, proposed, module_id)
        )
        dependencies = [
            DecisionDependency(
                "representation",
                f"{module_id}:accepted-unmapped",
                ABSENT_DIGEST if before_projection is None else before_projection.digest,
            ),
            DecisionDependency(
                "representation",
                f"{module_id}:proposed-unmapped",
                ABSENT_DIGEST if after_projection is None else after_projection.digest,
            ),
            DecisionDependency(
                "module-locator",
                f"{module_id}:accepted-module",
                ABSENT_DIGEST
                if before_module is None
                else digest_bytes(canonical_json_bytes({"path": before_module.path})),
            ),
            DecisionDependency(
                "module-locator",
                f"{module_id}:proposed-module",
                ABSENT_DIGEST
                if after_module is None
                else digest_bytes(canonical_json_bytes({"path": after_module.path})),
            ),
        ]
        changed_outside_units = (
            before_projection is None
            or after_projection is None
            or before_projection.digest != after_projection.digest
            or before_module.path != after_module.path
        )
        unclaimed_change = False
        for policy_id in _module_policy_ids(accepted, proposed, module_id):
            before_policy = accepted.resolve_policy_unit(policy_id)
            after_policy = proposed.resolve_policy_unit(policy_id)
            before_digest = _authority_digest(before_policy)
            after_digest = _authority_digest(after_policy)
            if before_digest == after_digest or policy_id in claimed:
                continue
            unclaimed_change = True
            dependencies.extend(
                (
                    DecisionDependency(
                        "policy-unit",
                        f"{policy_id}:accepted",
                        before_digest,
                    ),
                    DecisionDependency(
                        "policy-unit",
                        f"{policy_id}:proposed",
                        after_digest,
                    ),
                )
            )
        if not changed_outside_units and not unclaimed_change:
            continue

        dependencies.append(
            DecisionDependency(
                "analysis-contract",
                UNMAPPED_DECISION_CONTRACT.id,
                ANALYSIS_CONTRACT_DIGEST,
            )
        )
        fingerprint = DecisionFingerprint(
            "unmapped-normative-change",
            UNMAPPED_DECISION_CONTRACT.id,
            tuple(
                sorted(
                    dependencies,
                    key=lambda item: (item.dependency_class, item.identity),
                )
            ),
        )
        reason = {"kind": "unmapped-normative-change", "source": module_id}
        identity_value = {
            "kind": "unmapped-normative-change",
            "source": module_id,
            "target": module_id,
            "scope": {"kind": "whole-artifact"},
            "reason": reason,
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "unmapped-normative-change",
                module_id,
                module_id,
                ReviewScope("whole-artifact"),
                reason,
                "required",
                ("impact-disposition",),
                fingerprint,
            )
        )
    return tuple(obligations)
