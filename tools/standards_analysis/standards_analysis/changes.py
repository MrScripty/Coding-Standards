from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .errors import AnalysisError, AnalysisFailure
from .policy_units import PolicyUnit, PolicyUnitCorpus, PolicyUnitTombstone


POLICY_IMPACT = "policy-impact"
STANDARDS_REQUIRES = "standards-requires"
STANDARDS_SPECIALIZES = "standards-specializes"


class ChangeKind(str, Enum):
    MODIFICATION = "modification"
    ADDITION = "addition"
    REMOVAL = "removal"
    MOVE = "move"
    SPLIT = "split"
    MERGE = "merge"


CHANGE_GRAPH_GROUPS = {
    ChangeKind.MODIFICATION: ((POLICY_IMPACT,), (POLICY_IMPACT,)),
    ChangeKind.ADDITION: (
        (),
        (POLICY_IMPACT, STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
    ),
    ChangeKind.REMOVAL: ((POLICY_IMPACT,), ()),
}


class ChangeClassification(str, Enum):
    UNCHANGED = "unchanged"
    REPRESENTATION_ONLY_CANDIDATE = "representation-only-candidate"
    POSSIBLY_SEMANTICALLY_CHANGED = "possibly-semantically-changed"
    SEMANTICALLY_CHANGED = "semantically-changed"


class SemanticState(str, Enum):
    ACCEPTED_UNCHANGED = "accepted-unchanged"
    PROPOSED = "proposed"
    REMOVED = "removed"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class ReviewScope:
    kind: str
    heading_path: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        valid = self.kind == "whole-artifact" or (
            self.kind == "structured"
            and bool(self.heading_path)
            and all(self.heading_path)
        )
        if not valid or (self.kind == "whole-artifact" and self.heading_path):
            raise _error("CHANGE.SCOPE", "review scope is invalid", field="scope")

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {"kind": self.kind}
        if self.heading_path:
            value["heading_path"] = list(self.heading_path)
        return value


@dataclass(frozen=True, slots=True)
class ChangeDescriptor:
    kind: ChangeKind
    accepted_ids: tuple[str, ...]
    proposed_ids: tuple[str, ...]
    scope: ReviewScope
    accepted_module: str | None = None
    proposed_module: str | None = None


@dataclass(frozen=True, slots=True)
class SemanticProposal:
    policy: str
    accepted_semantic_revision: int | None
    proposed_semantic_revision: int
    intent: str
    structural_digest: str


@dataclass(frozen=True, slots=True)
class ChangedPolicyUnit:
    policy: str
    change_kind: ChangeKind
    classification: ChangeClassification
    accepted_representation_digest: str | None
    proposed_representation_digest: str | None
    accepted_structural_digest: str | None
    proposed_structural_digest: str | None
    accepted_semantic_revision: int | None
    proposed_semantic_revision: int | None
    semantic_state: SemanticState
    scope: ReviewScope

    def as_contract(self) -> dict[str, object]:
        return {
            "policy": self.policy,
            "change_kind": self.change_kind.value,
            "classification": self.classification.value,
            "accepted_representation_digest": self.accepted_representation_digest,
            "proposed_representation_digest": self.proposed_representation_digest,
            "accepted_structural_digest": self.accepted_structural_digest,
            "proposed_structural_digest": self.proposed_structural_digest,
            "accepted_semantic_revision": self.accepted_semantic_revision,
            "proposed_semantic_revision": self.proposed_semantic_revision,
            "semantic_state": self.semantic_state.value,
            "scope": self.scope.as_contract(),
        }


@dataclass(frozen=True, slots=True)
class GraphSeedSelection:
    accepted_seeds: tuple[str, ...]
    accepted_groups: tuple[str, ...]
    proposed_seeds: tuple[str, ...]
    proposed_groups: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClassifiedChange:
    descriptor: ChangeDescriptor
    changed_units: tuple[ChangedPolicyUnit, ...]
    graph: GraphSeedSelection


def _error(code: str, message: str, *, field: str | None = None, observed: str | None = None) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(code, "invalid", message, field=field, observed=observed)
    )


def classify_changes(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptors: Iterable[ChangeDescriptor],
    semantic_proposals: Iterable[SemanticProposal] = (),
) -> tuple[ClassifiedChange, ...]:
    selected = tuple(descriptors)
    proposals = tuple(semantic_proposals)
    if not selected:
        raise _error("CHANGE.EMPTY", "analysis requires at least one change")
    by_policy: dict[str, SemanticProposal] = {}
    for proposal in proposals:
        if proposal.policy in by_policy:
            raise _error(
                "CHANGE.DUPLICATE_SEMANTIC_PROPOSAL",
                "a policy may have only one semantic proposal",
                field="semantic_proposals",
                observed=proposal.policy,
            )
        if not proposal.intent or proposal.proposed_semantic_revision < 1:
            raise _error(
                "CHANGE.SEMANTIC_PROPOSAL",
                "semantic proposal intent and revision are invalid",
                field="semantic_proposals",
                observed=proposal.policy,
            )
        by_policy[proposal.policy] = proposal

    claimed: set[str] = set()
    results: list[ClassifiedChange] = []
    for descriptor in selected:
        identities = set((*descriptor.accepted_ids, *descriptor.proposed_ids))
        overlap = claimed.intersection(identities)
        if overlap:
            raise _error(
                "CHANGE.DUPLICATE_POLICY",
                "one policy identity cannot be classified by multiple changes",
                field="changes",
                observed=sorted(overlap)[0],
            )
        claimed.update(identities)
        results.append(
            _classify_change(accepted, proposed, descriptor, by_policy)
        )

    unused = sorted(set(by_policy) - claimed)
    if unused:
        raise _error(
            "CHANGE.ORPHAN_SEMANTIC_PROPOSAL",
            "semantic proposal does not belong to a declared change",
            field="semantic_proposals",
            observed=unused[0],
        )
    return tuple(results)


def _classify_change(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if descriptor.kind is ChangeKind.MODIFICATION:
        return _modification(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.ADDITION:
        return _addition(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.REMOVAL:
        return _removal(accepted, proposed, descriptor, proposals)
    raise _error(
        "CHANGE.UNSUPPORTED_KIND",
        "change kind is not implemented by the current admitted slice",
        field="kind",
        observed=str(descriptor.kind),
    )


def _modification(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if (
        len(descriptor.accepted_ids) != 1
        or descriptor.accepted_ids != descriptor.proposed_ids
    ):
        raise _shape_error(ChangeKind.MODIFICATION)
    policy_id = descriptor.accepted_ids[0]
    before = _active(accepted, policy_id, "accepted")
    after = _active(proposed, policy_id, "proposed")
    _module(descriptor.accepted_module, before.module, "accepted_module")
    _module(descriptor.proposed_module, after.module, "proposed_module")
    if (
        before.module != after.module
        or before.heading_path != after.heading_path
        or before.aliases != after.aliases
        or before.predecessors != after.predecessors
        or before.successors != after.successors
    ):
        raise _error(
            "CHANGE.WRONG_KIND",
            "identity, locator, ownership, or lifecycle changes are not modifications",
            observed=policy_id,
        )
    if before.semantic_revision != after.semantic_revision:
        raise _error(
            "CHANGE.ACCEPTED_REVISION_MUTATED",
            "a proposed snapshot must retain the accepted semantic revision",
            observed=policy_id,
        )

    semantic = proposals.get(policy_id)
    if semantic is not None:
        _semantic_overlay(semantic, before.semantic_revision, after)
        classification = ChangeClassification.SEMANTICALLY_CHANGED
        semantic_state = SemanticState.PROPOSED
        proposed_revision = semantic.proposed_semantic_revision
    elif before.representation_digest == after.representation_digest:
        classification = ChangeClassification.UNCHANGED
        semantic_state = SemanticState.ACCEPTED_UNCHANGED
        proposed_revision = before.semantic_revision
    elif before.structural_digest == after.structural_digest:
        classification = ChangeClassification.REPRESENTATION_ONLY_CANDIDATE
        semantic_state = SemanticState.ACCEPTED_UNCHANGED
        proposed_revision = before.semantic_revision
    else:
        classification = ChangeClassification.POSSIBLY_SEMANTICALLY_CHANGED
        semantic_state = SemanticState.UNRESOLVED
        proposed_revision = None

    changed = _changed(
        policy_id,
        ChangeKind.MODIFICATION,
        classification,
        before,
        after,
        before.semantic_revision,
        proposed_revision,
        semantic_state,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind]
    return ClassifiedChange(
        descriptor,
        (changed,),
        GraphSeedSelection(
            (policy_id,),
            accepted_groups,
            (policy_id,),
            proposed_groups,
        ),
    )


def _addition(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if descriptor.accepted_ids or len(descriptor.proposed_ids) != 1:
        raise _shape_error(ChangeKind.ADDITION)
    policy_id = descriptor.proposed_ids[0]
    if accepted.resolve(policy_id) is not None:
        raise _error(
            "CHANGE.ADDED_ID_EXISTS",
            "an added policy identity must be absent from accepted authority",
            observed=policy_id,
        )
    after = _active(proposed, policy_id, "proposed")
    _module(descriptor.proposed_module, after.module, "proposed_module")
    if descriptor.accepted_module is not None:
        raise _error(
            "CHANGE.MODULE",
            "an addition cannot declare an accepted module",
            field="accepted_module",
        )
    if after.predecessors:
        raise _error(
            "CHANGE.WRONG_KIND",
            "a policy with predecessors must be classified as split or merge",
            observed=policy_id,
        )
    semantic = proposals.get(policy_id)
    if semantic is None:
        raise _error(
            "CHANGE.SEMANTIC_PROPOSAL_REQUIRED",
            "an added policy requires proposed semantic state",
            observed=policy_id,
        )
    _semantic_overlay(semantic, None, after)
    if after.semantic_revision != 1 or semantic.proposed_semantic_revision != 1:
        raise _error(
            "CHANGE.INITIAL_REVISION",
            "an added policy starts at proposed semantic revision 1",
            observed=policy_id,
        )
    changed = _changed(
        policy_id,
        ChangeKind.ADDITION,
        ChangeClassification.SEMANTICALLY_CHANGED,
        None,
        after,
        None,
        1,
        SemanticState.PROPOSED,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind]
    return ClassifiedChange(
        descriptor,
        (changed,),
        GraphSeedSelection(
            (),
            accepted_groups,
            tuple(sorted((policy_id, after.module))),
            proposed_groups,
        ),
    )


def _removal(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if len(descriptor.accepted_ids) != 1 or descriptor.proposed_ids:
        raise _shape_error(ChangeKind.REMOVAL)
    policy_id = descriptor.accepted_ids[0]
    before = _active(accepted, policy_id, "accepted")
    _module(descriptor.accepted_module, before.module, "accepted_module")
    if descriptor.proposed_module is not None:
        raise _error(
            "CHANGE.MODULE",
            "a removal cannot declare a proposed module",
            field="proposed_module",
        )
    if policy_id in proposals:
        raise _error(
            "CHANGE.SEMANTIC_PROPOSAL",
            "a removed policy cannot have proposed semantic state",
            observed=policy_id,
        )
    retired = proposed.resolve(policy_id)
    if not isinstance(retired, PolicyUnitTombstone):
        raise _error(
            "CHANGE.TOMBSTONE_REQUIRED",
            "a removed policy requires a permanent proposed tombstone",
            observed=policy_id,
        )
    if retired.retired_semantic_revision != before.semantic_revision:
        raise _error(
            "CHANGE.RETIRED_REVISION",
            "the tombstone must bind the accepted semantic revision",
            observed=policy_id,
        )
    changed = _changed(
        policy_id,
        ChangeKind.REMOVAL,
        ChangeClassification.SEMANTICALLY_CHANGED,
        before,
        None,
        before.semantic_revision,
        None,
        SemanticState.REMOVED,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind]
    return ClassifiedChange(
        descriptor,
        (changed,),
        GraphSeedSelection((policy_id,), accepted_groups, (), proposed_groups),
    )


def _semantic_overlay(
    proposal: SemanticProposal,
    accepted_revision: int | None,
    proposed: PolicyUnit,
) -> None:
    expected = 1 if accepted_revision is None else accepted_revision + 1
    if (
        proposal.accepted_semantic_revision != accepted_revision
        or proposal.proposed_semantic_revision != expected
        or proposal.structural_digest != proposed.structural_digest
    ):
        raise _error(
            "CHANGE.SEMANTIC_PROPOSAL_MISMATCH",
            "semantic proposal must bind exact accepted revision, next revision, and proposed structure",
            observed=proposal.policy,
        )


def _active(corpus: PolicyUnitCorpus, policy_id: str, state: str) -> PolicyUnit:
    value = corpus.resolve(policy_id)
    if not isinstance(value, PolicyUnit) or value.id != policy_id:
        raise _error(
            "CHANGE.POLICY_UNAVAILABLE",
            f"policy must be active in the {state} corpus",
            observed=policy_id,
        )
    return value


def _module(supplied: str | None, derived: str, field: str) -> None:
    if supplied is not None and supplied != derived:
        raise _error(
            "CHANGE.MODULE_MISMATCH",
            "declared module does not match canonical policy ownership",
            field=field,
            observed=supplied,
        )


def _shape_error(kind: ChangeKind) -> AnalysisError:
    return _error(
        "CHANGE.DESCRIPTOR_SHAPE",
        "change descriptor identity cardinality does not match its kind",
        field="kind",
        observed=kind.value,
    )


def _changed(
    policy_id: str,
    kind: ChangeKind,
    classification: ChangeClassification,
    accepted: PolicyUnit | None,
    proposed: PolicyUnit | None,
    accepted_revision: int | None,
    proposed_revision: int | None,
    state: SemanticState,
    scope: ReviewScope,
) -> ChangedPolicyUnit:
    return ChangedPolicyUnit(
        policy_id,
        kind,
        classification,
        accepted.representation_digest if accepted else None,
        proposed.representation_digest if proposed else None,
        accepted.structural_digest if accepted else None,
        proposed.structural_digest if proposed else None,
        accepted_revision,
        proposed_revision,
        state,
        scope,
    )
