from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .errors import AnalysisError, AnalysisFailure
from tools.standards_metadata.standards_metadata import (
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
)


POLICY_IMPACT = "policy-impact"
STANDARDS_REQUIRES = "standards-requires"
STANDARDS_SPECIALIZES = "standards-specializes"


class ChangeKind(str, Enum):
    NAVIGATION_INDEX = "navigation-index"
    MODULE = "module"
    MODIFICATION = "modification"
    ADDITION = "addition"
    REMOVAL = "removal"
    MOVE = "move"
    SPLIT = "split"
    MERGE = "merge"


class ChangedPolicyKind(str, Enum):
    MODIFICATION = "modification"
    ADDITION = "addition"
    REMOVAL = "removal"
    MOVE = "move"
    SPLIT_PREDECESSOR = "split-predecessor"
    SPLIT_SUCCESSOR = "split-successor"
    MERGE_PREDECESSOR = "merge-predecessor"
    MERGE_SUCCESSOR = "merge-successor"


CHANGE_GRAPH_GROUPS = {
    "navigation-index": ((), ()),
    "module": (
        (STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
        (STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
    ),
    "modification": ((POLICY_IMPACT,), (POLICY_IMPACT,)),
    "addition": (
        (),
        (POLICY_IMPACT, STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
    ),
    "removal": ((POLICY_IMPACT,), ()),
    "move-same-module": ((POLICY_IMPACT,), (POLICY_IMPACT,)),
    "move-cross-module": (
        (POLICY_IMPACT, STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
        (POLICY_IMPACT, STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
    ),
    "split": ((POLICY_IMPACT,), (POLICY_IMPACT,)),
    "merge": ((POLICY_IMPACT,), (POLICY_IMPACT,)),
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

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": self.kind.value,
            "accepted_ids": list(self.accepted_ids),
            "proposed_ids": list(self.proposed_ids),
            "scope": self.scope.as_contract(),
        }
        if self.accepted_module is not None:
            value["accepted_module"] = self.accepted_module
        if self.proposed_module is not None:
            value["proposed_module"] = self.proposed_module
        return value


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
    change_kind: ChangedPolicyKind
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


def _error(
    code: str, message: str, *, field: str | None = None, observed: str | None = None
) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(code, "invalid", message, field=field, observed=observed)
    )


def derive_change_descriptors(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    affected_policy_ids: Iterable[str] = (),
) -> tuple[ChangeDescriptor, ...]:
    """Derive the smallest truthful A1c change set from two compiled corpora."""

    affected = set(affected_policy_ids)
    accepted_units = {item.id: item for item in accepted.units}
    proposed_units = {item.id: item for item in proposed.units}
    accepted_only = set(accepted_units) - set(proposed_units)
    proposed_only = set(proposed_units) - set(accepted_units)
    consumed_accepted: set[str] = set()
    consumed_proposed: set[str] = set()
    scope = ReviewScope("whole-artifact")
    descriptors: list[ChangeDescriptor] = []

    for policy_id in sorted(set(accepted_units).intersection(proposed_units)):
        before = accepted_units[policy_id]
        after = proposed_units[policy_id]
        if before == after and policy_id not in affected:
            continue
        kind = (
            ChangeKind.MOVE
            if (before.module, before.heading_path)
            != (after.module, after.heading_path)
            else ChangeKind.MODIFICATION
        )
        descriptors.append(ChangeDescriptor(kind, (policy_id,), (policy_id,), scope))

    for policy_id in sorted(accepted_only):
        retired = proposed.resolve(policy_id)
        if not isinstance(retired, PolicyUnitTombstone) or len(retired.successors) < 2:
            continue
        successors = tuple(sorted(retired.successors))
        descriptors.append(
            ChangeDescriptor(ChangeKind.SPLIT, (policy_id,), successors, scope)
        )
        consumed_accepted.add(policy_id)
        consumed_proposed.update(successors)

    for policy_id in sorted(proposed_only - consumed_proposed):
        successor = proposed_units[policy_id]
        if len(successor.predecessors) < 2:
            continue
        predecessors = tuple(sorted(successor.predecessors))
        descriptors.append(
            ChangeDescriptor(ChangeKind.MERGE, predecessors, (policy_id,), scope)
        )
        consumed_accepted.update(predecessors)
        consumed_proposed.add(policy_id)

    descriptors.extend(
        ChangeDescriptor(ChangeKind.REMOVAL, (policy_id,), (), scope)
        for policy_id in sorted(accepted_only - consumed_accepted)
    )
    descriptors.extend(
        ChangeDescriptor(ChangeKind.ADDITION, (), (policy_id,), scope)
        for policy_id in sorted(proposed_only - consumed_proposed)
    )
    if not descriptors:
        raise _error(
            "CHANGE.EMPTY",
            "projected material does not contain an analyzable policy-unit change",
        )
    return tuple(descriptors)


def classify_changes(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptors: Iterable[ChangeDescriptor],
    semantic_proposals: Iterable[SemanticProposal] = (),
    *,
    accepted_module_ids: Iterable[str] = (),
    proposed_module_ids: Iterable[str] = (),
    changed_navigation_ids: Iterable[str] = (),
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
    claimed_modules: set[str] = set()
    accepted_modules = set(accepted_module_ids)
    proposed_modules = set(proposed_module_ids)
    navigation_ids = set(changed_navigation_ids)
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
        module_identities = {
            item
            for item in (descriptor.accepted_module, descriptor.proposed_module)
            if item is not None
        }
        if descriptor.kind is ChangeKind.MODULE:
            module_overlap = claimed_modules.intersection(module_identities)
            if module_overlap:
                raise _error(
                    "CHANGE.DUPLICATE_MODULE",
                    "one module identity cannot be classified by multiple module changes",
                    field="changes",
                    observed=sorted(module_overlap)[0],
                )
            claimed_modules.update(module_identities)
        results.append(
            _classify_change(
                accepted,
                proposed,
                descriptor,
                by_policy,
                accepted_modules,
                proposed_modules,
                navigation_ids,
            )
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
    accepted_modules: set[str],
    proposed_modules: set[str],
    navigation_ids: set[str],
) -> ClassifiedChange:
    if descriptor.kind is ChangeKind.NAVIGATION_INDEX:
        if (
            len(descriptor.accepted_ids) != 1
            or descriptor.accepted_ids != descriptor.proposed_ids
            or descriptor.accepted_module is not None
            or descriptor.proposed_module is not None
            or descriptor.scope.kind != "whole-artifact"
        ):
            raise _shape_error(ChangeKind.NAVIGATION_INDEX)
        if descriptor.accepted_ids[0] not in navigation_ids:
            raise _error(
                "CHANGE.NAVIGATION_UNAVAILABLE",
                "Navigation change must name an actually changed registered index.",
            )
        return ClassifiedChange(descriptor, (), GraphSeedSelection((), (), (), ()))
    if descriptor.kind is ChangeKind.MODULE:
        return _module_change(
            descriptor,
            accepted_modules,
            proposed_modules,
        )
    if descriptor.kind is ChangeKind.MODIFICATION:
        return _modification(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.ADDITION:
        return _addition(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.REMOVAL:
        return _removal(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.MOVE:
        return _move(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.SPLIT:
        return _split(accepted, proposed, descriptor, proposals)
    if descriptor.kind is ChangeKind.MERGE:
        return _merge(accepted, proposed, descriptor, proposals)
    raise _error(
        "CHANGE.UNSUPPORTED_KIND",
        "change kind is not implemented by the current admitted slice",
        field="kind",
        observed=str(descriptor.kind),
    )


def _module_change(
    descriptor: ChangeDescriptor,
    accepted_modules: set[str],
    proposed_modules: set[str],
) -> ClassifiedChange:
    before = descriptor.accepted_module
    after = descriptor.proposed_module
    if (
        descriptor.accepted_ids
        or descriptor.proposed_ids
        or (before is None and after is None)
        or (before is not None and after is not None and before != after)
        or descriptor.scope.kind != "whole-artifact"
    ):
        raise _shape_error(ChangeKind.MODULE)
    if before is not None and before not in accepted_modules:
        raise _error(
            "CHANGE.MODULE_UNAVAILABLE",
            "accepted module change target is unavailable",
            field="accepted_module",
            observed=before,
        )
    if after is not None and after not in proposed_modules:
        raise _error(
            "CHANGE.MODULE_UNAVAILABLE",
            "proposed module change target is unavailable",
            field="proposed_module",
            observed=after,
        )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
    return ClassifiedChange(
        descriptor,
        (),
        GraphSeedSelection(
            () if before is None else (before,),
            () if before is None else accepted_groups,
            () if after is None else (after,),
            () if after is None else proposed_groups,
        ),
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
        ChangedPolicyKind.MODIFICATION,
        classification,
        before,
        after,
        before.semantic_revision,
        proposed_revision,
        semantic_state,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
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
        ChangedPolicyKind.ADDITION,
        ChangeClassification.SEMANTICALLY_CHANGED,
        None,
        after,
        None,
        1,
        SemanticState.PROPOSED,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
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
        ChangedPolicyKind.REMOVAL,
        ChangeClassification.SEMANTICALLY_CHANGED,
        before,
        None,
        before.semantic_revision,
        None,
        SemanticState.REMOVED,
        descriptor.scope,
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
    return ClassifiedChange(
        descriptor,
        (changed,),
        GraphSeedSelection((policy_id,), accepted_groups, (), proposed_groups),
    )


def _move(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if (
        len(descriptor.accepted_ids) != 1
        or descriptor.accepted_ids != descriptor.proposed_ids
    ):
        raise _shape_error(ChangeKind.MOVE)
    policy_id = descriptor.accepted_ids[0]
    before = _active(accepted, policy_id, "accepted")
    after = _active(proposed, policy_id, "proposed")
    _module(descriptor.accepted_module, before.module, "accepted_module")
    _module(descriptor.proposed_module, after.module, "proposed_module")
    if before.module == after.module and before.heading_path == after.heading_path:
        raise _error(
            "CHANGE.WRONG_KIND",
            "a move must change canonical ownership or locator",
            observed=policy_id,
        )
    if (
        before.aliases != after.aliases
        or before.predecessors != after.predecessors
        or before.successors != after.successors
    ):
        raise _error(
            "CHANGE.WRONG_KIND",
            "a move cannot alter identity aliases or predecessor/successor lifecycle",
            observed=policy_id,
        )
    if before.semantic_revision != after.semantic_revision:
        raise _error(
            "CHANGE.ACCEPTED_REVISION_MUTATED",
            "a proposed move must retain the accepted semantic revision",
            observed=policy_id,
        )
    classification, state, proposed_revision = _classify_existing(
        before,
        after,
        proposals.get(policy_id),
    )
    changed = _changed(
        policy_id,
        ChangedPolicyKind.MOVE,
        classification,
        before,
        after,
        before.semantic_revision,
        proposed_revision,
        state,
        descriptor.scope,
    )
    profile = (
        "move-same-module" if before.module == after.module else "move-cross-module"
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[profile]
    accepted_seeds = (policy_id,)
    proposed_seeds = (policy_id,)
    if before.module != after.module:
        accepted_seeds = tuple(sorted((policy_id, before.module)))
        proposed_seeds = tuple(sorted((policy_id, after.module)))
    return ClassifiedChange(
        descriptor,
        (changed,),
        GraphSeedSelection(
            accepted_seeds,
            accepted_groups,
            proposed_seeds,
            proposed_groups,
        ),
    )


def _split(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if (
        len(descriptor.accepted_ids) != 1
        or len(descriptor.proposed_ids) < 2
        or len(set(descriptor.proposed_ids)) != len(descriptor.proposed_ids)
    ):
        raise _shape_error(ChangeKind.SPLIT)
    predecessor_id = descriptor.accepted_ids[0]
    if predecessor_id in descriptor.proposed_ids:
        raise _shape_error(ChangeKind.SPLIT)
    before = _active(accepted, predecessor_id, "accepted")
    _module(descriptor.accepted_module, before.module, "accepted_module")
    if predecessor_id in proposals:
        raise _error(
            "CHANGE.SEMANTIC_PROPOSAL",
            "a split predecessor cannot have proposed semantic state",
            observed=predecessor_id,
        )
    tombstone = _retired(proposed, predecessor_id, before)
    expected_successors = tuple(sorted(descriptor.proposed_ids))
    if tuple(sorted(tombstone.successors)) != expected_successors:
        raise _error(
            "CHANGE.SUCCESSOR_MISMATCH",
            "split tombstone successors must equal proposed policy identities",
            observed=predecessor_id,
        )
    successors: list[PolicyUnit] = []
    for policy_id in expected_successors:
        if accepted.resolve(policy_id) is not None:
            raise _error(
                "CHANGE.ADDED_ID_EXISTS",
                "a split successor identity must be absent from accepted authority",
                observed=policy_id,
            )
        successor = _active(proposed, policy_id, "proposed")
        _module(descriptor.proposed_module, successor.module, "proposed_module")
        if successor.predecessors != (predecessor_id,):
            raise _error(
                "CHANGE.PREDECESSOR_MISMATCH",
                "each split successor must name exactly its predecessor",
                observed=policy_id,
            )
        _initial_semantic_proposal(successor, proposals.get(policy_id))
        successors.append(successor)

    changed = [
        _changed(
            predecessor_id,
            ChangedPolicyKind.SPLIT_PREDECESSOR,
            ChangeClassification.SEMANTICALLY_CHANGED,
            before,
            None,
            before.semantic_revision,
            None,
            SemanticState.REMOVED,
            descriptor.scope,
        )
    ]
    changed.extend(
        _changed(
            successor.id,
            ChangedPolicyKind.SPLIT_SUCCESSOR,
            ChangeClassification.SEMANTICALLY_CHANGED,
            None,
            successor,
            None,
            1,
            SemanticState.PROPOSED,
            descriptor.scope,
        )
        for successor in successors
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
    return ClassifiedChange(
        descriptor,
        tuple(changed),
        GraphSeedSelection(
            (predecessor_id,),
            accepted_groups,
            expected_successors,
            proposed_groups,
        ),
    )


def _merge(
    accepted: PolicyUnitCorpus,
    proposed: PolicyUnitCorpus,
    descriptor: ChangeDescriptor,
    proposals: dict[str, SemanticProposal],
) -> ClassifiedChange:
    if (
        len(descriptor.accepted_ids) < 2
        or len(set(descriptor.accepted_ids)) != len(descriptor.accepted_ids)
        or len(descriptor.proposed_ids) != 1
    ):
        raise _shape_error(ChangeKind.MERGE)
    successor_id = descriptor.proposed_ids[0]
    if successor_id in descriptor.accepted_ids:
        raise _shape_error(ChangeKind.MERGE)
    predecessor_ids = tuple(sorted(descriptor.accepted_ids))
    predecessors = tuple(
        _active(accepted, policy_id, "accepted") for policy_id in predecessor_ids
    )
    for predecessor in predecessors:
        _module(descriptor.accepted_module, predecessor.module, "accepted_module")
        if predecessor.id in proposals:
            raise _error(
                "CHANGE.SEMANTIC_PROPOSAL",
                "a merge predecessor cannot have proposed semantic state",
                observed=predecessor.id,
            )
        tombstone = _retired(proposed, predecessor.id, predecessor)
        if tombstone.successors != (successor_id,):
            raise _error(
                "CHANGE.SUCCESSOR_MISMATCH",
                "each merge tombstone must name exactly the merged successor",
                observed=predecessor.id,
            )
    if accepted.resolve(successor_id) is not None:
        raise _error(
            "CHANGE.ADDED_ID_EXISTS",
            "a merge successor identity must be absent from accepted authority",
            observed=successor_id,
        )
    successor = _active(proposed, successor_id, "proposed")
    _module(descriptor.proposed_module, successor.module, "proposed_module")
    if tuple(sorted(successor.predecessors)) != predecessor_ids:
        raise _error(
            "CHANGE.PREDECESSOR_MISMATCH",
            "merge successor predecessors must equal accepted policy identities",
            observed=successor_id,
        )
    _initial_semantic_proposal(successor, proposals.get(successor_id))

    changed = [
        _changed(
            predecessor.id,
            ChangedPolicyKind.MERGE_PREDECESSOR,
            ChangeClassification.SEMANTICALLY_CHANGED,
            predecessor,
            None,
            predecessor.semantic_revision,
            None,
            SemanticState.REMOVED,
            descriptor.scope,
        )
        for predecessor in predecessors
    ]
    changed.append(
        _changed(
            successor.id,
            ChangedPolicyKind.MERGE_SUCCESSOR,
            ChangeClassification.SEMANTICALLY_CHANGED,
            None,
            successor,
            None,
            1,
            SemanticState.PROPOSED,
            descriptor.scope,
        )
    )
    accepted_groups, proposed_groups = CHANGE_GRAPH_GROUPS[descriptor.kind.value]
    return ClassifiedChange(
        descriptor,
        tuple(changed),
        GraphSeedSelection(
            predecessor_ids,
            accepted_groups,
            (successor_id,),
            proposed_groups,
        ),
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


def _classify_existing(
    accepted: PolicyUnit,
    proposed: PolicyUnit,
    semantic: SemanticProposal | None,
) -> tuple[ChangeClassification, SemanticState, int | None]:
    if semantic is not None:
        _semantic_overlay(semantic, accepted.semantic_revision, proposed)
        return (
            ChangeClassification.SEMANTICALLY_CHANGED,
            SemanticState.PROPOSED,
            semantic.proposed_semantic_revision,
        )
    if accepted.representation_digest == proposed.representation_digest:
        return (
            ChangeClassification.UNCHANGED,
            SemanticState.ACCEPTED_UNCHANGED,
            accepted.semantic_revision,
        )
    if accepted.structural_digest == proposed.structural_digest:
        return (
            ChangeClassification.REPRESENTATION_ONLY_CANDIDATE,
            SemanticState.ACCEPTED_UNCHANGED,
            accepted.semantic_revision,
        )
    return (
        ChangeClassification.POSSIBLY_SEMANTICALLY_CHANGED,
        SemanticState.UNRESOLVED,
        None,
    )


def _initial_semantic_proposal(
    policy: PolicyUnit,
    proposal: SemanticProposal | None,
) -> None:
    if proposal is None:
        raise _error(
            "CHANGE.SEMANTIC_PROPOSAL_REQUIRED",
            "a split or merge successor requires proposed semantic state",
            observed=policy.id,
        )
    _semantic_overlay(proposal, None, policy)
    if policy.semantic_revision != 1 or proposal.proposed_semantic_revision != 1:
        raise _error(
            "CHANGE.INITIAL_REVISION",
            "a split or merge successor starts at proposed semantic revision 1",
            observed=policy.id,
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


def _retired(
    corpus: PolicyUnitCorpus,
    policy_id: str,
    accepted: PolicyUnit,
) -> PolicyUnitTombstone:
    value = corpus.resolve(policy_id)
    if not isinstance(value, PolicyUnitTombstone):
        raise _error(
            "CHANGE.TOMBSTONE_REQUIRED",
            "a split or merge predecessor requires a permanent proposed tombstone",
            observed=policy_id,
        )
    if value.retired_semantic_revision != accepted.semantic_revision:
        raise _error(
            "CHANGE.RETIRED_REVISION",
            "the tombstone must bind the accepted semantic revision",
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
    kind: ChangedPolicyKind,
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
