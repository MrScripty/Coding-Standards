"""Schema-owned construction selectors, used only after root validation.

A required string property with disjoint const/enum values excludes every other
branch. The root proof supplies existence and exclusivity; these tables neither
validate instances nor interpret arbitrary JSON Schema constraints.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
import re
from types import MappingProxyType


_LOCAL_DEFINITION = re.compile(r"#/\$defs/([A-Za-z][A-Za-z0-9]*)\Z")


@dataclass(frozen=True, slots=True)
class StringDiscriminant:
    property_name: str
    variants: Mapping[str, Mapping[str, object]]

    def select(self, value: object) -> Mapping[str, object] | None:
        if not isinstance(value, Mapping):
            return None
        tag = value.get(self.property_name)
        # Keep Python's bool/int equality and non-string enum semantics with
        # the canonical validator. No request data is retained by this selector.
        return self.variants.get(tag) if type(tag) is str else None


def compile_union_selectors(schema: Mapping[str, object]) -> dict[int, StringDiscriminant]:
    """Index the runtime's private schema copy; size/lifetime follow that schema.

    Walk only schema positions, never annotation/const/enum instance data. A
    nested resource scope stays entirely on the existing reference path.
    """
    definitions = schema.get("$defs", {})
    nodes = list(_schema_nodes(schema))
    if not isinstance(definitions, Mapping) or any(
        node is not schema and "$id" in node for node in nodes
    ):
        return {}
    selectors = {}
    for node in nodes:
        variants = node.get("oneOf")
        if isinstance(variants, list):
            selector = _string_discriminant(variants, definitions)
            if selector is not None:
                selectors[id(node)] = selector
    return selectors


def _schema_nodes(schema: Mapping[str, object]) -> Iterator[Mapping[str, object]]:
    pending = [schema]
    seen: set[int] = set()
    while pending:
        node = pending.pop()
        if not isinstance(node, Mapping) or id(node) in seen:
            continue
        seen.add(id(node))
        yield node
        for keyword in ("$defs", "properties"):
            children = node.get(keyword)
            if isinstance(children, Mapping):
                pending.extend(children.values())
        variants = node.get("oneOf")
        if isinstance(variants, list):
            pending.extend(variants)
        pending.extend(node.get(keyword) for keyword in ("items", "additionalProperties"))


def _local_object(
    node: object, definitions: Mapping[str, object],
) -> Mapping[str, object] | None:
    seen: set[str] = set()
    while isinstance(node, Mapping) and "$ref" in node:
        reference = node["$ref"]
        match = _LOCAL_DEFINITION.fullmatch(reference) if type(reference) is str else None
        # Reference siblings and other reference forms keep their existing
        # interpretation; the planner follows only bare same-resource aliases.
        if set(node) != {"$ref"} or match is None or reference in seen:
            return None
        seen.add(reference)
        node = definitions.get(match[1])
    if isinstance(node, Mapping) and node.get("type") == "object":
        return node
    return None


def _required_tags(node: Mapping[str, object]) -> dict[str, frozenset[str]]:
    properties, required = node.get("properties"), node.get("required")
    if not isinstance(properties, Mapping) or not isinstance(required, list):
        return {}
    tags = {}
    for name in required:
        if type(name) is not str:
            continue
        declaration = properties.get(name)
        if not isinstance(declaration, Mapping) or "$ref" in declaration:
            continue
        const = declaration.get("const")
        enum = declaration.get("enum")
        if type(const) is str:
            tags[name] = frozenset((const,))
        elif isinstance(enum, list) and enum and all(type(item) is str for item in enum):
            tags[name] = frozenset(enum)
    return tags


def _string_discriminant(
    variants: list[object], definitions: Mapping[str, object],
) -> StringDiscriminant | None:
    constraints = []
    branches: list[Mapping[str, object]] = []
    for variant in variants:
        if not isinstance(variant, Mapping):
            return None
        branches.append(variant)
        node = _local_object(variant, definitions)
        if node is None:
            return None
        constraints.append(_required_tags(node))
    if not constraints:
        return None
    common = set(constraints[0]).intersection(*(set(item) for item in constraints[1:]))
    for name in sorted(common):
        choices = {}
        for variant, tags in zip(branches, constraints):
            values = tags[name]
            if choices.keys() & values:
                break
            choices.update((value, variant) for value in values)
        else:
            return StringDiscriminant(name, MappingProxyType(choices))
    return None
