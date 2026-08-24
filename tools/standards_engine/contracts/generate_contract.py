from __future__ import annotations

import argparse
import json
import keyword
import pprint
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
PYTHON_PATH = REPO_ROOT / "tools/standards_engine/standards_engine/_generated_contract.py"
TOOLS_PATH = REPO_ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _refs(schema: dict[str, Any], definition: str) -> tuple[str, ...]:
    return tuple(
        item["$ref"].rsplit("/", 1)[1]
        for item in schema["$defs"][definition].get("oneOf", ())
    )


def _result_definitions(schema: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    selected = []
    for name, node in schema["$defs"].items():
        kind = node.get("properties", {}).get("kind", {}).get("const")
        if isinstance(kind, str) and (kind.endswith("-result") or kind == "analysis-state"):
            selected.append((name, kind))
    return tuple(selected)


def _definition_references(node: object) -> set[str]:
    references: set[str] = set()
    if isinstance(node, dict):
        reference = node.get("$ref")
        if isinstance(reference, str) and reference.startswith("#/$defs/"):
            references.add(reference.rsplit("/", 1)[1])
        for value in node.values():
            references.update(_definition_references(value))
    elif isinstance(node, list):
        for value in node:
            references.update(_definition_references(value))
    return references


def _public_definitions(schema: dict[str, Any]) -> tuple[str, ...]:
    operations = schema["x-standards-engine-contract"]["public_operations"].values()
    pending = [contract["input"] for contract in operations]
    pending.extend(
        result
        for contract in schema["x-standards-engine-contract"][
            "public_operations"
        ].values()
        for result in contract["results"]
    )
    selected: set[str] = set()
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        selected.add(name)
        pending.extend(_definition_references(schema["$defs"][name]) - selected)
    return tuple(sorted(selected))


def _structured_object(node: dict[str, Any]) -> bool:
    return node.get("type") == "object" and bool(node.get("properties"))


def _python_name(value: str) -> str:
    selected = value.replace("-", "_")
    return selected + "_" if keyword.iskeyword(selected) else selected


def _annotation(node: dict[str, Any]) -> str:
    reference = node.get("$ref")
    if isinstance(reference, str):
        return reference.rsplit("/", 1)[1]
    if "oneOf" in node:
        return " | ".join(dict.fromkeys(_annotation(item) for item in node["oneOf"]))
    if "const" in node:
        value = node["const"]
        if isinstance(value, (str, int, bool)):
            return f"Literal[{value!r}]"
        if value is None:
            return "None"
        if isinstance(value, list):
            return "tuple[()]" if not value else f"tuple[{_annotation({'enum': value})}, ...]"
        return "object"
    if "enum" in node:
        return "Literal[" + ", ".join(repr(item) for item in node["enum"]) + "]"
    value_type = node.get("type")
    primitives = {"string": "str", "integer": "int", "boolean": "bool", "null": "None"}
    if value_type in primitives:
        return primitives[value_type]
    if value_type == "array":
        return f"tuple[{_annotation(node.get('items', {}))}, ...]"
    if value_type == "object":
        additional = node.get("additionalProperties")
        item = "object" if not isinstance(additional, dict) else _annotation(additional)
        return f"Mapping[str, {item}]"
    return "object"


def _field_default(node: dict[str, Any], required: bool) -> str | None:
    if "default" in node:
        return repr(node["default"])
    if "const" in node:
        value = node["const"]
        if isinstance(value, (list, dict)):
            frozen = tuple(value) if isinstance(value, list) else value
            return f"field(default_factory=lambda: {frozen!r})"
        return repr(value)
    return None if required else "None"


def _class_projection(
    name: str,
    node: dict[str, Any],
    *,
    result: bool,
) -> list[str]:
    required = set(node.get("required", ()))
    selected = [
        (
            contract_name,
            _python_name(contract_name),
            _annotation(field_node),
            _field_default(field_node, contract_name in required),
        )
        for contract_name, field_node in node["properties"].items()
    ]
    ordered = [item for item in selected if item[3] is None]
    ordered += [item for item in selected if item[3] is not None and item[0] != "kind"]
    ordered += [item for item in selected if item[3] is not None and item[0] == "kind"]
    lines = [
        "@dataclass(frozen=True, slots=True)",
        f"class {name}({'ContractResult' if result else 'ContractObject'}):",
        f"    __definition__: ClassVar[str] = {name!r}",
    ]
    for _, python_name, annotation, default in ordered:
        if default is None:
            lines.append(f"    {python_name}: {annotation}")
        else:
            if default == "None" and "None" not in annotation.split(" | "):
                annotation += " | None"
            lines.append(f"    {python_name}: {annotation} = {default}")
    lines += ["", "    def __post_init__(self) -> None:", "        _coerce_object(self)"]
    return lines


def _alias_order(aliases: tuple[str, ...], schemas: dict[str, dict[str, Any]]) -> tuple[str, ...]:
    alias_set = set(aliases)
    ordered: list[str] = []
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in ordered:
            return
        if name in visiting:
            raise ValueError(f"generated input aliases contain a cycle at {name}")
        visiting.add(name)
        for dependency in sorted(_definition_references(schemas[name]) & alias_set):
            visit(dependency)
        visiting.remove(name)
        ordered.append(name)

    for name in aliases:
        visit(name)
    return tuple(ordered)


RUNTIME = """
class ContractObject(Mapping[str, object]):
    __definition__: ClassVar[str]

    @classmethod
    def from_value(cls, value: Mapping[str, object]):
        selected = decode_contract(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError(f"{cls.__definition__} decoded to the wrong type")
        return selected

    def as_contract(self) -> dict[str, object]:
        required = set(DEFINITION_SCHEMAS[self.__definition__].get("required", ()))
        result = {}
        for contract_name, python_name in FIELD_NAMES[self.__definition__].items():
            value = getattr(self, python_name)
            if value is None and contract_name not in required:
                continue
            result[contract_name] = _encode(value)
        return result

    def __getitem__(self, key: str) -> object:
        return self.as_contract()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.as_contract())

    def __len__(self) -> int:
        return len(self.as_contract())


class ContractResult(ContractObject):
    pass


def _encode(value: object) -> object:
    if isinstance(value, ContractObject):
        return value.as_contract()
    if isinstance(value, Mapping):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    return value


def _schema_equal(left: object, right: object) -> bool:
    return canonical_json_bytes(_encode(left)) == canonical_json_bytes(_encode(right))


def _decode_node(node: Mapping[str, object], value: object) -> object:
    reference = node.get("$ref")
    if isinstance(reference, str):
        return decode_contract(reference.rsplit("/", 1)[1], value)
    variants = node.get("oneOf")
    if isinstance(variants, list):
        failures = []
        matches = []
        for variant in variants:
            try:
                matches.append(_decode_node(variant, value))
            except (TypeError, ValueError) as error:
                failures.append(str(error))
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise TypeError("value matches no generated union variant: " + "; ".join(failures))
        raise ValueError("value matches more than one generated union variant")
    if "const" in node and not _schema_equal(_encode(value), node["const"]):
        raise ValueError(f"expected constant {node['const']!r}")
    if "enum" in node and not any(
        _schema_equal(_encode(value), item) for item in node["enum"]
    ):
        raise ValueError(f"value {value!r} is outside the generated enum")
    value_type = node.get("type")
    if value_type == "string" and not isinstance(value, str):
        raise TypeError("expected string")
    if value_type == "string" and len(value) < int(node.get("minLength", 0)):
        raise ValueError("string is shorter than the generated minimum")
    if value_type == "string" and "pattern" in node and re.search(node["pattern"], value) is None:
        raise ValueError("string does not match the generated pattern")
    if value_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        raise TypeError("expected integer")
    if value_type == "integer" and "minimum" in node and value < node["minimum"]:
        raise ValueError("integer is below the generated minimum")
    if value_type == "boolean" and not isinstance(value, bool):
        raise TypeError("expected boolean")
    if value_type == "null" and value is not None:
        raise TypeError("expected null")
    if value_type == "array":
        if not isinstance(value, (list, tuple)):
            raise TypeError("expected array")
        result = tuple(_decode_node(node.get("items", {}), item) for item in value)
        if len(result) < int(node.get("minItems", 0)):
            raise ValueError("array is shorter than the generated minimum")
        if node.get("uniqueItems"):
            encoded = [canonical_json_bytes(_encode(item)) for item in result]
            if len(set(encoded)) != len(encoded):
                raise ValueError("array items must be unique")
        return result
    if value_type == "object":
        if isinstance(value, ContractObject) or hasattr(value, "as_contract"):
            value = value.as_contract()
        if not isinstance(value, Mapping):
            raise TypeError("expected object")
        properties = node.get("properties", {})
        required = set(node.get("required", ()))
        missing = required - set(value)
        if missing:
            raise ValueError(f"object is missing {sorted(missing)!r}")
        additional = node.get("additionalProperties")
        extra = set(value) - set(properties)
        if additional is False and extra:
            raise ValueError(f"object has unexpected fields {sorted(extra)!r}")
        result = {}
        for key, item in value.items():
            property_node = properties.get(key)
            if isinstance(property_node, Mapping):
                result[str(key)] = _decode_node(property_node, item)
            elif isinstance(additional, Mapping):
                result[str(key)] = _decode_node(additional, item)
            else:
                result[str(key)] = _freeze(item)
        return MappingProxyType(result)
    return value


def decode_contract(definition: str, value: object) -> object:
    node = DEFINITION_SCHEMAS.get(definition)
    if node is None:
        raise ValueError(f"unknown generated input definition {definition!r}")
    selected = _CLASS_BY_DEFINITION.get(definition)
    if selected is None:
        return _decode_node(node, value)
    if isinstance(value, selected):
        return value
    if hasattr(value, "as_contract"):
        value = value.as_contract()
    if not isinstance(value, Mapping):
        raise TypeError(f"{definition} must be an object")
    required = set(node.get("required", ()))
    properties = node.get("properties", {})
    missing = required - set(value)
    extra = set(value) - set(properties)
    if missing:
        raise ValueError(f"{definition} is missing {sorted(missing)!r}")
    if extra:
        raise ValueError(f"{definition} has unexpected fields {sorted(extra)!r}")
    arguments = {}
    for contract_name, python_name in FIELD_NAMES[definition].items():
        if contract_name in value:
            arguments[python_name] = _decode_node(properties[contract_name], value[contract_name])
    return selected(**arguments)


def _coerce_object(value: ContractObject) -> None:
    node = DEFINITION_SCHEMAS[value.__definition__]
    required = set(node.get("required", ()))
    for contract_name, python_name in FIELD_NAMES[value.__definition__].items():
        selected = getattr(value, python_name)
        if selected is None and contract_name not in required:
            continue
        object.__setattr__(value, python_name, _decode_node(node["properties"][contract_name], selected))
""".strip().splitlines()


def _python_projection(schema: dict[str, Any]) -> str:
    metadata = schema["x-standards-engine-contract"]
    results = _result_definitions(schema)
    result_map = {kind: name for name, kind in results}
    definition_names = _public_definitions(schema)
    definition_schemas = {
        name: schema["$defs"][name] for name in definition_names
    }
    class_names = {
        name for name, node in definition_schemas.items() if _structured_object(node)
    }
    aliases = _alias_order(
        tuple(name for name in definition_names if name not in class_names),
        definition_schemas,
    )
    field_names = {
        name: {
            field: _python_name(field)
            for field in definition_schemas[name].get("properties", {})
        }
        for name in sorted(class_names)
    }
    uses_default_factory = any(
        _field_default(field_node, field_name in set(node.get("required", ())))
        not in {None, "None"}
        and str(
            _field_default(
                field_node,
                field_name in set(node.get("required", ())),
            )
        ).startswith("field(")
        for node in definition_schemas.values()
        for field_name, field_node in node.get("properties", {}).items()
    )
    lines = [
        "# Generated by tools/standards_engine/contracts/generate_contract.py.",
        "# Do not edit this file directly.",
        "from __future__ import annotations",
        "",
        "import re",
        "",
        "from dataclasses import dataclass" + (", field" if uses_default_factory else ""),
        "from types import MappingProxyType",
        "from typing import Any, ClassVar, Iterator, Literal, Mapping, TypeAlias",
        "",
        "from tools.standards_metadata.standards_metadata import canonical_json_bytes",
        "",
        f"INTERFACE_SCHEMA_VERSION = {metadata['schema_version']}",
        "PUBLIC_OPERATIONS = MappingProxyType(",
        pprint.pformat(metadata["public_operations"], sort_dicts=True, width=88),
        ")",
        "DEFINITION_SCHEMAS = MappingProxyType(",
        pprint.pformat(definition_schemas, sort_dicts=True, width=88),
        ")",
        "FIELD_NAMES = MappingProxyType(",
        pprint.pformat(field_names, sort_dicts=True, width=88),
        ")",
        "RESULT_KIND_TO_DEFINITION = MappingProxyType(",
        pprint.pformat(result_map, sort_dicts=True, width=88),
        ")",
        f"INSPECTABLE_HANDLE_DEFINITIONS = {_refs(schema, 'InspectableHandle')!r}",
        "",
        "",
        "def _freeze(value: Any) -> Any:",
        "    if isinstance(value, Mapping):",
        "        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})",
        "    if isinstance(value, (list, tuple)):",
        "        return tuple(_freeze(item) for item in value)",
        "    return value",
        "",
        "",
        "def _thaw(value: Any) -> Any:",
        "    if isinstance(value, Mapping):",
        "        return {key: _thaw(item) for key, item in value.items()}",
        "    if isinstance(value, tuple):",
        "        return [_thaw(item) for item in value]",
        "    return value",
        "",
        "",
        *RUNTIME,
        "",
        "",
    ]
    for name in sorted(class_names):
        lines += _class_projection(
            name,
            definition_schemas[name],
            result=name in result_map.values(),
        ) + ["", ""]
    lines += ["_CLASS_BY_DEFINITION = MappingProxyType({"]
    lines += [f"    {name!r}: {name}," for name in sorted(class_names)]
    lines += ["})", "", ""]
    lines += [
        f"{name}: TypeAlias = {_annotation(definition_schemas[name])}"
        for name in aliases
    ]
    navigation = " | ".join(_refs(schema, "NavigationResult") + ("RejectedResult",))
    inspections = " | ".join(_refs(schema, "InspectionResult"))
    lines += ["", "", f"QueryResult: TypeAlias = {navigation}", f"ContractInspectionResult: TypeAlias = {inspections} | RejectedResult", ""]
    exported = sorted(
        {
            *definition_names,
            "ContractInspectionResult",
            "ContractObject",
            "ContractResult",
            "QueryResult",
            "decode_contract",
        }
    )
    lines += ["__all__ = (", *(f"    {name!r}," for name in exported), ")", ""]
    return "\n".join(lines)


def _agent_tools_projection(schema: dict[str, Any]) -> str:
    metadata = schema["x-standards-engine-contract"]
    descriptions = {
        "query": "Route, read, or navigate relationships in one exact standards snapshot.",
        "prepare": "Prepare immutable read-only analysis for exact base and proposed snapshots.",
        "resolve": "Advance one immutable analysis with an authorized typed submission.",
        "inspect": "Inspect an exact Standards Engine handle and its provenance.",
    }
    tools = [
        {
            "name": f"standards_{operation}",
            "description": descriptions[operation],
            "input_definition": contract["input"],
            "input_schema": {"$ref": f"#/$defs/{contract['input']}"},
            "result_definitions": contract["results"],
        }
        for operation, contract in metadata["public_operations"].items()
    ]
    value = {"schema_version": metadata["schema_version"], "canonical_schema": "../a1-contract.schema.json", "tools": tools, "$defs": schema["$defs"]}
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_projections() -> dict[Path, str]:
    schema = _load_schema()
    return {PYTHON_PATH: _python_projection(schema), TOOLS_PATH: _agent_tools_projection(schema)}


def check_projections() -> tuple[str, ...]:
    return tuple(
        path.relative_to(REPO_ROOT).as_posix()
        for path, expected in render_projections().items()
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Standards Engine projections")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    projections = render_projections()
    if args.check:
        stale = check_projections()
        if stale:
            print("stale generated contract projections: " + ", ".join(stale), file=sys.stderr)
            return 1
        return 0
    for path, content in projections.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
