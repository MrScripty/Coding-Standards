"""Structural locations in the admitted Draft 2020-12 projection profile.

The compiler owns profile admission; jsonschema/referencing own evaluation. These
helpers only locate schemas and same-resource definitions. Literal const, enum,
default and other annotation payloads are data, even when they contain $ref.
allOf is traversed for the adapter's reference-sibling output; its presence here
neither admits it to the canonical compiler nor adds a constraint evaluator.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from copy import deepcopy
import re
from typing import TypeAlias

from .errors import failure

SchemaNode: TypeAlias = Mapping[str, object] | bool
SchemaPath: TypeAlias = tuple[str | int, ...]

_SCHEMA_MAPS = frozenset({"$defs", "properties"})
_SCHEMA_ARRAYS = frozenset({"oneOf", "allOf"})
_SCHEMA_VALUES = frozenset({"items", "additionalProperties"})
_LOCAL_DEFINITION = re.compile(r"#/\$defs/([A-Za-z][A-Za-z0-9]*)\Z")


def schema_children(node: Mapping[str, object]) -> Iterator[tuple[SchemaPath, SchemaNode]]:
    """Yield immediate schema positions in source order, preserving field names."""
    for keyword, value in node.items():
        if keyword in _SCHEMA_MAPS and isinstance(value, Mapping):
            for name, child in value.items():
                if isinstance(child, (Mapping, bool)):
                    yield (keyword, name), child
        elif keyword in _SCHEMA_ARRAYS and isinstance(value, list):
            for index, child in enumerate(value):
                if isinstance(child, (Mapping, bool)):
                    yield (keyword, index), child
        elif keyword in _SCHEMA_VALUES and isinstance(value, (Mapping, bool)):
            yield (keyword,), value


def schema_nodes(root: SchemaNode) -> Iterator[Mapping[str, object]]:
    """Walk schema objects once without following references or entering data."""
    pending = [root]
    seen: set[int] = set()
    while pending:
        node = pending.pop()
        if not isinstance(node, Mapping) or id(node) in seen:
            continue
        seen.add(id(node))
        yield node
        pending.extend(child for _, child in reversed(list(schema_children(node))))


def map_schema_children(
    node: Mapping[str, object], transform: Callable[[SchemaNode], SchemaNode],
) -> dict[str, object]:
    """Copy one schema, transforming its child schemas and preserving JSON data."""
    result = {}
    for keyword, value in node.items():
        if keyword in _SCHEMA_MAPS and isinstance(value, Mapping):
            result[keyword] = {name: transform(child) for name, child in value.items()}
        elif keyword in _SCHEMA_ARRAYS and isinstance(value, list):
            result[keyword] = [transform(child) for child in value]
        elif keyword in _SCHEMA_VALUES and isinstance(value, (Mapping, bool)):
            result[keyword] = transform(value)
        else:
            result[keyword] = deepcopy(value)
    return result


def direct_schema_references(root: SchemaNode) -> Iterator[str]:
    """Read $ref only from schema objects, including sibling subschemas."""
    for node in schema_nodes(root):
        reference = node.get("$ref")
        if isinstance(reference, str):
            yield reference


def local_definition_name(reference: str) -> str:
    """Parse the profile's local reference form; retrieval is never attempted."""
    match = _LOCAL_DEFINITION.fullmatch(reference)
    if match is None:
        raise failure(
            "CONTRACT.UNSUPPORTED_REFERENCE", "only same-resource $defs references are supported",
            outcome="unsupported",
        )
    return match[1]


def referenced_definitions(
    root: SchemaNode, definitions: Mapping[str, object],
) -> dict[str, object]:
    """Select the transitive closure, borrowing definitions without changing them."""
    selected: dict[str, object] = {}
    pending = list(reversed(list(direct_schema_references(root))))
    while pending:
        name = local_definition_name(pending.pop())
        if name in selected:
            continue
        if name not in definitions:
            raise failure(
                "CONTRACT.UNRESOLVABLE_REFERENCE", f"local definition is missing: {name}",
                schema_pointer="/$defs",
            )
        definition = definitions[name]
        selected[name] = definition
        pending.extend(reversed(list(direct_schema_references(definition))))
    return selected


def schema_closure(root: Mapping[str, object], definitions: Mapping[str, object]) -> dict:
    """Return an independent standalone schema with only reachable definitions."""
    return deepcopy({**root, "$defs": referenced_definitions(root, definitions)})
