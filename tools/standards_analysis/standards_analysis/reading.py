from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Iterable, Mapping, Protocol

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    PolicyUnit,
)

from .changes import ReviewScope
from .errors import AnalysisError, AnalysisFailure
from .obligations import Obligation
from .keys import analysis_key_bytes


READING_STATES = frozenset({"selected", "unresolved", "conditional"})
READING_AUTHORITIES = frozenset(
    {"normative", "projection", "contextual", "evidence"}
)
STATE_RANK = {"selected": 0, "unresolved": 1, "conditional": 2}


def _error(code: str, message: str, *, observed: str | None = None) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(code, "invalid", message, observed=observed)
    )


class ReadingCause(Protocol):
    def as_contract(self) -> dict[str, object]: ...


@dataclass(frozen=True, slots=True)
class ConsumerReviewObligationCause:
    obligation: str

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "consumer-review-obligation",
            "obligation": self.obligation,
        }


@dataclass(frozen=True, slots=True)
class RoutingBaseCause:
    projection: str

    def as_contract(self) -> dict[str, object]:
        return {"kind": "routing-base", "projection": self.projection}


@dataclass(frozen=True, slots=True)
class RoutingRuleCause:
    rule: str
    facts: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "facts", tuple(sorted(set(self.facts))))

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "routing-rule",
            "rule": self.rule,
            "facts": list(self.facts),
        }


@dataclass(frozen=True, slots=True)
class DependencyCause:
    kind: str
    edge: str
    source: str

    def __post_init__(self) -> None:
        if self.kind not in {"requires", "specializes"}:
            raise _error(
                "READING_PLAN.DEPENDENCY_KIND",
                "dependency causes must be requires or specializes",
                observed=self.kind,
            )

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "edge": self.edge,
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class ReadingSelection:
    target: str
    scope: ReviewScope
    cause: ReadingCause
    state: str
    order_class: int
    order_rank: int = 0

    def __post_init__(self) -> None:
        if not self.target:
            raise _error(
                "READING_PLAN.TARGET",
                "reading selections require a canonical target",
            )
        if self.state not in READING_STATES:
            raise _error(
                "READING_PLAN.STATE",
                "reading selection state is invalid",
                observed=self.state,
            )
        if self.order_class < 0 or self.order_rank < 0:
            raise _error(
                "READING_PLAN.ORDER",
                "reading selection ordering values must be nonnegative",
                observed=self.target,
            )


@dataclass(frozen=True, slots=True)
class ReadingPlanEntry:
    target: str
    scope: ReviewScope
    authority: str
    reasons: tuple[Mapping[str, object], ...]
    state: str

    def __post_init__(self) -> None:
        projected = tuple(reason for reason in self.reasons)
        keys = tuple(analysis_key_bytes(reason) for reason in projected)
        if not keys or keys != tuple(sorted(set(keys))):
            raise _error(
                "READING_PLAN.REASONS",
                "reading-plan reasons must be nonempty, unique, and canonical",
                observed=self.target,
            )
        object.__setattr__(
            self,
            "reasons",
            tuple(_freeze(reason) for reason in projected),
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "target": self.target,
            "scope": self.scope.as_contract(),
            "authority": self.authority,
            "reasons": [_thaw(reason) for reason in self.reasons],
            "state": self.state,
        }


AuthorityResolver = Callable[[str], str]


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def compile_reading_plan(
    selections: Iterable[ReadingSelection],
    authority_for: AuthorityResolver,
) -> tuple[ReadingPlanEntry, ...]:
    grouped: dict[tuple[str, bytes], list[ReadingSelection]] = {}
    for selection in selections:
        key = (
            selection.target,
            analysis_key_bytes(selection.scope.as_contract()),
        )
        grouped.setdefault(key, []).append(selection)

    compiled: list[tuple[int, int, ReadingPlanEntry]] = []
    for key in sorted(grouped, key=lambda item: (item[0], item[1])):
        selected = grouped[key]
        target = key[0]
        authority = authority_for(target)
        if authority not in READING_AUTHORITIES:
            raise _error(
                "READING_PLAN.AUTHORITY",
                "reading target has no canonical authority classification",
                observed=target,
            )
        reasons_by_content = {
            analysis_key_bytes(item.cause.as_contract()): item.cause.as_contract()
            for item in selected
        }
        reasons = tuple(
            reasons_by_content[value] for value in sorted(reasons_by_content)
        )
        state = min(
            {item.state for item in selected},
            key=lambda value: STATE_RANK[value],
        )
        order_class = min(item.order_class for item in selected)
        order_rank = min(
            item.order_rank
            for item in selected
            if item.order_class == order_class
        )
        compiled.append(
            (
                order_class,
                order_rank,
                ReadingPlanEntry(
                    target,
                    selected[0].scope,
                    authority,
                    reasons,
                    state,
                ),
            )
        )
    return tuple(
        entry
        for _class, _rank, entry in sorted(
            compiled,
            key=lambda item: (
                item[0],
                item[1],
                item[2].target,
                analysis_key_bytes(item[2].scope.as_contract()),
            ),
        )
    )


def consumer_reading_selections(
    obligations: Iterable[Obligation],
) -> tuple[ReadingSelection, ...]:
    return tuple(
        ReadingSelection(
            obligation.target,
            obligation.scope,
            ConsumerReviewObligationCause(obligation.id),
            "selected",
            3,
        )
        for obligation in obligations
        if obligation.kind == "consumer-review"
    )


def canonical_target_authority(
    target: str,
    corpus: CanonicalStandardsCorpus,
    graph: EdgeRegistry,
) -> str:
    module = corpus.resolve_module(target)
    if module is not None and module.module_id == target:
        return "contextual" if module.role == "reference" else "normative"
    policy = corpus.resolve_policy_unit(target)
    if isinstance(policy, PolicyUnit) and policy.id == target:
        owner = corpus.resolve_module(policy.module)
        if owner is None:
            raise _error(
                "READING_PLAN.AUTHORITY",
                "policy-unit owner cannot be resolved",
                observed=target,
            )
        return "contextual" if owner.role == "reference" else "normative"
    node = graph.nodes.get(target)
    authority = None if node is None else node.metadata.get("authority")
    if authority not in READING_AUTHORITIES:
        raise _error(
            "READING_PLAN.AUTHORITY",
            "registered reading target must declare canonical authority metadata",
            observed=target,
        )
    return authority


__all__ = (
    "ConsumerReviewObligationCause",
    "DependencyCause",
    "ReadingPlanEntry",
    "ReadingSelection",
    "RoutingBaseCause",
    "RoutingRuleCause",
    "canonical_target_authority",
    "compile_reading_plan",
    "consumer_reading_selections",
)
