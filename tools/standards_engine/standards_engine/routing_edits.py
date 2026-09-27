"""Immutable authored routing values; semantic interpretation belongs to applicability.

These declarations are not bound FactContracts or evaluated programs. Keeping their
exact fields/order, including semantically invalid values, preserves when the
existing projection checks reject an edit against its co-edited context.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Literal


def _freeze(value: object) -> object:
    """Retain JSON-shaped authored data, not a second applicability grammar."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in sorted(value.items())})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if value is None or type(value) in (str, int, float, bool):
        return value
    raise TypeError('Authored routing values must be JSON data.')


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _same_value(left: object, right: object) -> bool:
    """Authored equality preserves JSON scalar types, not Python's True == 1."""
    if type(left) is not type(right):
        return False
    if isinstance(left, Mapping):
        return left.keys() == right.keys() and all(_same_value(left[key], right[key]) for key in left)
    if isinstance(left, tuple):
        return len(left) == len(right) and all(_same_value(a, b) for a, b in zip(left, right))
    return left == right


@dataclass(frozen=True, slots=True, eq=False)
class RoutingFactDeclaration:
    id: str
    semantic_revision: int
    # These authored values are interpreted by the fact-schema owner at the
    # existing projection boundary, not by this storage representation.
    type: object
    nullable: object
    values: object
    aliases: object
    meaning: str
    prompt: str

    def __post_init__(self) -> None:
        for name in ('type', 'nullable', 'values', 'aliases'):
            object.__setattr__(self, name, _freeze(getattr(self, name)))

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return all(_same_value(getattr(self, name), getattr(other, name)) for name in
                   ('id', 'semantic_revision', 'type', 'nullable', 'values', 'aliases', 'meaning', 'prompt'))

    def as_declaration(self) -> dict[str, object]:
        # Preserve the map ordering produced by the former canonical JSON round
        # trip: the TOML writer intentionally observes this declaration order.
        return {'aliases': _thaw(self.aliases), 'id': self.id, 'meaning': self.meaning,
                'nullable': _thaw(self.nullable), 'prompt': self.prompt,
                'semantic_revision': self.semantic_revision, 'type': _thaw(self.type),
                'values': _thaw(self.values)}


@dataclass(frozen=True, slots=True, eq=False)
class RoutingRuleDeclaration:
    id: str
    target: str
    when: Mapping[str, object]
    condition: str

    def __post_init__(self) -> None:
        object.__setattr__(self, 'when', _freeze(self.when))

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return all(_same_value(getattr(self, name), getattr(other, name))
                   for name in ('id', 'target', 'when', 'condition'))

    def as_declaration(self) -> dict[str, object]:
        return {'condition': self.condition, 'id': self.id, 'target': self.target,
                'when': _thaw(self.when)}


@dataclass(frozen=True, slots=True)
class PutRoutingFact:
    fact: RoutingFactDeclaration
    rationale: str
    kind: ClassVar[Literal['put-routing-fact']] = 'put-routing-fact'

    @property
    def facet(self) -> tuple[str, ...]:
        return ('routing-fact', self.fact.id)

    def as_contract(self) -> dict[str, object]:
        return {'fact': self.fact.as_declaration(), 'kind': self.kind, 'rationale': self.rationale}


@dataclass(frozen=True, slots=True)
class RemoveRoutingFact:
    fact: str
    rationale: str
    kind: ClassVar[Literal['remove-routing-fact']] = 'remove-routing-fact'

    @property
    def facet(self) -> tuple[str, ...]:
        return ('routing-fact', self.fact)

    def as_contract(self) -> dict[str, object]:
        return {'fact': self.fact, 'kind': self.kind, 'rationale': self.rationale}


@dataclass(frozen=True, slots=True)
class PutRoutingRule:
    rule: RoutingRuleDeclaration
    rationale: str
    kind: ClassVar[Literal['put-routing-rule']] = 'put-routing-rule'

    @property
    def facet(self) -> tuple[str, ...]:
        return ('routing-rule', self.rule.id)

    def as_contract(self) -> dict[str, object]:
        return {'kind': self.kind, 'rationale': self.rationale, 'rule': self.rule.as_declaration()}


@dataclass(frozen=True, slots=True)
class RemoveRoutingRule:
    rule: str
    rationale: str
    kind: ClassVar[Literal['remove-routing-rule']] = 'remove-routing-rule'

    @property
    def facet(self) -> tuple[str, ...]:
        return ('routing-rule', self.rule)

    def as_contract(self) -> dict[str, object]:
        return {'kind': self.kind, 'rationale': self.rationale, 'rule': self.rule}


RoutingEdit = PutRoutingFact | RemoveRoutingFact | PutRoutingRule | RemoveRoutingRule
ROUTING_EDIT_KINDS = frozenset(
    cls.kind for cls in (PutRoutingFact, RemoveRoutingFact, PutRoutingRule, RemoveRoutingRule)
)
