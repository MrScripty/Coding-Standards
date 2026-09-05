from __future__ import annotations

import copy
import json
import keyword
import re
from collections.abc import Mapping

from jsonschema import Draft202012Validator, SchemaError
from referencing import Registry, Resource

from .errors import ContractError, ContractFailure, failure
from .model import (
    DefinitionProjection,
    FieldProjection,
    InterfaceContract,
    OperationContract,
    ProjectionArtifacts,
)
from .runtime import ContractRuntime

_DIALECT = "https://json-schema.org/draft/2020-12/schema"
_SCHEMA_KEYS = frozenset(
    {
        "$schema",
        "$id",
        "$ref",
        "$defs",
        "title",
        "description",
        "default",
        "type",
        "const",
        "enum",
        "oneOf",
        "required",
        "properties",
        "additionalProperties",
        "items",
        "minItems",
        "maxItems",
        "uniqueItems",
        "minLength",
        "pattern",
        "minimum",
    }
)
_INTERFACE_KEYS = frozenset(
    {
        "schema_version",
        "interface_schema_version",
        "request_contract_version",
        "result_projection_version",
        "operations",
    }
)
_OPERATION_KEYS = frozenset(
    {
        "id",
        "input_definition",
        "result_definitions",
        "capability",
        "capability_by_submission",
    }
)
_OPERATIONS = (
    "create_snapshot",
    "find_snapshots",
    "delete_snapshot",
    "undelete_snapshot",
    "query",
    "prepare",
    "resolve",
    "inspect",
    "create_proposal",
    "find_proposals",
    "revise_proposal",
    "query_proposal",
    "analyze_proposal",
    "review_proposal",
    "apply_proposal",
    "recover_application",
)
_ASCII_PATTERN = re.compile(r"\A[\x20-\x7e]*\Z")


class CompiledContracts:
    def __init__(
        self,
        schema: Mapping[str, object],
        interface: InterfaceContract,
        reachable_definitions: tuple[str, ...],
    ) -> None:
        self._schema = copy.deepcopy(dict(schema))
        self.interface = interface
        self.reachable_definitions = reachable_definitions
        self._runtime = ContractRuntime(self._schema, {})

    @property
    def schema(self) -> Mapping[str, object]:
        return copy.deepcopy(self._schema)

    def validate(self, definition: str, value: object) -> None:
        if definition not in self.reachable_definitions:
            raise failure(
                "CONTRACT.UNKNOWN_DEFINITION",
                "definition is not in the public operation closure",
                definition=definition,
            )
        self._runtime.validate(definition, value)

    def project(self) -> ProjectionArtifacts:
        definitions = tuple(
            _project_definition(name, self._schema["$defs"][name])
            for name in self.reachable_definitions
        )
        return ProjectionArtifacts(
            python_source=_python_source(self._schema, definitions),
            agent_tools_json=json.dumps(
                _agent_tools(self._schema, self.interface),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            definitions=definitions,
        )


def compile_contracts(
    schema: Mapping[str, object], interface: Mapping[str, object]
) -> CompiledContracts:
    selected_schema = copy.deepcopy(dict(schema))
    if selected_schema.get("$schema") != _DIALECT:
        raise failure(
            "CONTRACT.UNSUPPORTED_DIALECT",
            "the contract must select JSON Schema Draft 2020-12",
            outcome="unsupported",
            schema_pointer="/$schema",
        )
    try:
        Draft202012Validator.check_schema(selected_schema)
    except SchemaError as error:
        raise ContractError(
            ContractFailure(
                outcome="invalid",
                code="CONTRACT.INVALID_SCHEMA",
                message="the canonical schema is not valid Draft 2020-12",
                schema_pointer=_pointer(error.absolute_schema_path),
                keyword=str(error.validator) if error.validator is not None else None,
            )
        ) from None

    _check_projection_profile(selected_schema)
    definitions = selected_schema.get("$defs")
    if not isinstance(definitions, dict):
        raise failure("CONTRACT.INVALID_SCHEMA", "schema must define $defs")
    references = _definition_references(selected_schema)
    missing = sorted(references - definitions.keys())
    if missing:
        raise failure(
            "CONTRACT.UNRESOLVABLE_REFERENCE",
            f"local definition is missing: {missing[0]}",
            schema_pointer="/$defs",
        )

    parsed_interface = _parse_interface(interface, definitions)
    roots = {
        definition
        for operation in parsed_interface.operations
        for definition in (operation.input_definition, *operation.result_definitions)
    }
    reachable = _reachable_definitions(definitions, roots)
    unreachable = sorted(definitions.keys() - reachable)
    if unreachable:
        raise failure(
            "CONTRACT.UNREACHABLE_DEFINITION",
            f"definition is outside the public operation closure: {unreachable[0]}",
            schema_pointer=f"/$defs/{_escape(unreachable[0])}",
        )

    root_refs = {
        reference.rsplit("/", 1)[1]
        for reference in _direct_refs(selected_schema.get("oneOf", []))
    }
    if root_refs != roots:
        raise failure(
            "CONTRACT.ROOT_CLOSURE_MISMATCH",
            "schema root variants must exactly match interface operation roots",
            schema_pointer="/oneOf",
        )

    schema_id = selected_schema.get("$id")
    if not isinstance(schema_id, str):
        raise failure("CONTRACT.INVALID_SCHEMA", "schema must have a string $id")
    Registry().with_resource(schema_id, Resource.from_contents(selected_schema))
    return CompiledContracts(
        selected_schema, parsed_interface, tuple(sorted(reachable))
    )


def _parse_interface(
    value: Mapping[str, object], definitions: Mapping[str, object]
) -> InterfaceContract:
    if set(value) != _INTERFACE_KEYS:
        raise failure(
            "CONTRACT.INVALID_INTERFACE",
            "interface fields do not match the closed contract",
        )
    versions = (
        value["schema_version"],
        value["interface_schema_version"],
        value["request_contract_version"],
        value["result_projection_version"],
    )
    if any(type(item) is not int or item < 1 for item in versions):
        raise failure(
            "CONTRACT.INVALID_INTERFACE",
            "interface versions must be positive exact integers",
        )
    raw_operations = value["operations"]
    if not isinstance(raw_operations, list):
        raise failure("CONTRACT.INVALID_INTERFACE", "operations must be an array")
    operations: list[OperationContract] = []
    for raw in raw_operations:
        if not isinstance(raw, dict) or not set(raw) <= _OPERATION_KEYS:
            raise failure(
                "CONTRACT.INVALID_INTERFACE",
                "operation fields do not match the closed contract",
            )
        operation_id = raw.get("id")
        input_definition = raw.get("input_definition")
        results = raw.get("result_definitions")
        capability = raw.get("capability")
        by_submission = raw.get("capability_by_submission")
        if (
            not isinstance(operation_id, str)
            or not isinstance(input_definition, str)
            or not isinstance(results, list)
            or not results
            or not all(isinstance(item, str) for item in results)
            or input_definition not in definitions
            or any(item not in definitions for item in results)
        ):
            raise failure(
                "CONTRACT.INVALID_INTERFACE",
                "operation roots must name existing definitions",
            )
        has_capability = isinstance(capability, str) and bool(capability)
        has_submission_map = isinstance(by_submission, dict) and bool(by_submission)
        if has_capability == has_submission_map:
            raise failure(
                "CONTRACT.INVALID_INTERFACE",
                "operation must select exactly one capability form",
            )
        selected_map = by_submission if has_submission_map else {}
        if not all(
            isinstance(key, str) and isinstance(item, str) and item
            for key, item in selected_map.items()
        ):
            raise failure(
                "CONTRACT.INVALID_INTERFACE",
                "submission capabilities must be nonempty strings",
            )
        operations.append(
            OperationContract(
                id=operation_id,
                input_definition=input_definition,
                result_definitions=tuple(results),
                capability=capability if has_capability else None,
                capability_by_submission=selected_map,
            )
        )
    expected_operations = (
        _OPERATIONS + ("verify_repository", "verify_proposal")
        if value["interface_schema_version"] >= 21
        else _OPERATIONS
    )
    if tuple(item.id for item in operations) != expected_operations:
        raise failure(
            "CONTRACT.INVALID_INTERFACE",
            "operations must match the registered interface version: "
            + ", ".join(expected_operations),
        )
    resolve = next(operation for operation in operations if operation.id == "resolve")
    submission_definition = definitions[resolve.input_definition]["properties"][
        "submission"
    ]["$ref"].rsplit("/", 1)[1]
    discriminants = _union_discriminants(definitions, submission_definition)
    if set(resolve.capability_by_submission) != discriminants:
        raise failure(
            "CONTRACT.INVALID_INTERFACE",
            "resolve capabilities must exactly cover submission discriminants",
        )
    return InterfaceContract(
        schema_version=versions[0],
        interface_schema_version=versions[1],
        request_contract_version=versions[2],
        result_projection_version=versions[3],
        operations=tuple(operations),
    )


def _union_discriminants(
    definitions: Mapping[str, object], definition: str
) -> set[str]:
    selected: set[str] = set()
    for variant in definitions[definition].get("oneOf", []):
        name = variant["$ref"].rsplit("/", 1)[1]
        kind = definitions[name].get("properties", {}).get("kind", {}).get("const")
        if not isinstance(kind, str):
            raise failure(
                "CONTRACT.INVALID_INTERFACE",
                "submission variants require string kind discriminants",
                definition=name,
            )
        selected.add(kind)
    return selected


def _check_projection_profile(schema: Mapping[str, object]) -> None:
    def visit(node: object, path: tuple[str | int, ...]) -> None:
        if isinstance(node, dict):
            unknown = set(node) - _SCHEMA_KEYS
            if unknown:
                key = sorted(unknown)[0]
                raise failure(
                    "CONTRACT.UNSUPPORTED_PROJECTION",
                    f"reachable schema keyword is unsupported: {key}",
                    outcome="unsupported",
                    schema_pointer=_pointer((*path, key)),
                )
            reference = node.get("$ref")
            if isinstance(reference, str) and not re.fullmatch(
                r"#/\$defs/[A-Za-z][A-Za-z0-9]*", reference
            ):
                raise failure(
                    "CONTRACT.UNSUPPORTED_REFERENCE",
                    "only same-resource $defs references are supported",
                    outcome="unsupported",
                    schema_pointer=_pointer((*path, "$ref")),
                )
            pattern = node.get("pattern")
            if isinstance(pattern, str) and not _supported_pattern(pattern):
                raise failure(
                    "CONTRACT.UNSUPPORTED_PATTERN",
                    "pattern is outside the common projection profile",
                    outcome="unsupported",
                    schema_pointer=_pointer((*path, "pattern")),
                )
            if node.get("type") == "object":
                properties = node.get("properties")
                additional = node.get("additionalProperties")
                if isinstance(properties, dict) and properties:
                    if additional is not False:
                        raise failure(
                            "CONTRACT.UNSUPPORTED_PROJECTION",
                            "structured objects must reject additional properties",
                            outcome="unsupported",
                            schema_pointer=_pointer((*path, "additionalProperties")),
                        )
                    python_names = [_python_name(name) for name in properties]
                    if len(python_names) != len(set(python_names)):
                        raise failure(
                            "CONTRACT.UNSUPPORTED_PROJECTION",
                            "property names collide in the Python projection",
                            outcome="unsupported",
                            schema_pointer=_pointer((*path, "properties")),
                        )
                elif not isinstance(additional, dict):
                    raise failure(
                        "CONTRACT.UNSUPPORTED_PROJECTION",
                        "map objects require one additional-property schema",
                        outcome="unsupported",
                        schema_pointer=_pointer((*path, "additionalProperties")),
                    )
            for key, item in node.items():
                if key in {"$defs", "properties"}:
                    for name, child in item.items():
                        visit(child, (*path, key, name))
                elif key in {"oneOf"}:
                    for index, child in enumerate(item):
                        visit(child, (*path, key, index))
                elif key in {"items", "additionalProperties"} and isinstance(
                    item, dict
                ):
                    visit(item, (*path, key))

    visit(schema, ())


def _supported_pattern(pattern: str) -> bool:
    if _ASCII_PATTERN.fullmatch(pattern) is None or not (
        pattern.startswith("^") and pattern.endswith("$")
    ):
        return False
    body = pattern[1:-1]
    index = 0
    escaped_punctuation = frozenset(r".^$*+?{}[]\|()/:-")
    literal_punctuation = frozenset("._:/-")
    while index < len(body):
        character = body[index]
        if character == "\\":
            if index + 1 >= len(body) or body[index + 1] not in escaped_punctuation:
                return False
            index += 2
        elif character == "[":
            end = index + 1
            escaped = False
            while end < len(body):
                selected = body[end]
                if escaped:
                    if selected not in escaped_punctuation:
                        return False
                    escaped = False
                elif selected == "\\":
                    escaped = True
                elif selected == "]":
                    break
                elif (
                    not (selected.isascii() and selected.isalnum())
                    and selected not in literal_punctuation
                ):
                    return False
                end += 1
            if end == index + 1 or end >= len(body) or escaped:
                return False
            index = end + 1
        elif character.isascii() and (
            character.isalnum() or character in literal_punctuation
        ):
            index += 1
        else:
            return False

        if index < len(body) and body[index] in "*+?":
            index += 1
        elif index < len(body) and body[index] == "{":
            repetition = re.match(r"\{[0-9]+(?:,[0-9]*)?\}", body[index:])
            if repetition is None:
                return False
            index += len(repetition.group(0))
    return True


def _definition_references(node: object) -> set[str]:
    return {reference.rsplit("/", 1)[1] for reference in _direct_refs(node)}


def _direct_refs(node: object) -> set[str]:
    selected: set[str] = set()
    pending = [node]
    while pending:
        current = pending.pop()
        if isinstance(current, dict):
            reference = current.get("$ref")
            if isinstance(reference, str):
                selected.add(reference)
            pending.extend(current.values())
        elif isinstance(current, list):
            pending.extend(current)
    return selected


def _reachable_definitions(
    definitions: Mapping[str, object], roots: set[str]
) -> set[str]:
    selected: set[str] = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        selected.add(name)
        pending.extend(_definition_references(definitions[name]) - selected)
    return selected


def _project_definition(name: str, node: Mapping[str, object]) -> DefinitionProjection:
    properties = node.get("properties")
    if node.get("type") == "object" and isinstance(properties, dict) and properties:
        required = set(node.get("required", []))
        fields = tuple(
            FieldProjection(
                contract_name=contract_name,
                python_name=_python_name(contract_name),
                annotation=_annotation(field_node),
                required=contract_name in required,
                title=field_node.get("title"),
                description=field_node.get("description"),
                has_default="default" in field_node,
                default_annotation=field_node.get("default"),
            )
            for contract_name, field_node in properties.items()
        )
        return DefinitionProjection(
            name=name,
            annotation=name,
            fields=fields,
            title=node.get("title"),
            description=node.get("description"),
            has_default="default" in node,
            default_annotation=node.get("default"),
        )
    return DefinitionProjection(
        name=name,
        annotation=_annotation(node),
        fields=(),
        title=node.get("title"),
        description=node.get("description"),
        has_default="default" in node,
        default_annotation=node.get("default"),
    )


def _annotation(node: Mapping[str, object]) -> str:
    reference = node.get("$ref")
    if isinstance(reference, str):
        return reference.rsplit("/", 1)[1]
    variants = node.get("oneOf")
    if isinstance(variants, list):
        return " | ".join(dict.fromkeys(_annotation(item) for item in variants))
    const = node.get("const", MISSING)
    if const is not MISSING:
        return _literal_annotation((const,))
    enum = node.get("enum")
    if isinstance(enum, list):
        return _literal_annotation(tuple(enum))
    value_type = node.get("type")
    if value_type == "null":
        return "None"
    if value_type == "boolean":
        return "bool"
    if value_type == "integer":
        return "int | float"
    if value_type == "number":
        return "int | float"
    if value_type == "string":
        return "str"
    if value_type == "array":
        return f"tuple[{_annotation(node.get('items', {}))}, ...]"
    if value_type == "object":
        additional = node.get("additionalProperties")
        item = _annotation(additional) if isinstance(additional, dict) else "object"
        return f"FrozenMap[str, {item}]"
    return "object"


MISSING = object()


def _literal_annotation(values: tuple[object, ...]) -> str:
    if all(value is None or type(value) in {str, bool} for value in values):
        return "Literal[" + ", ".join(repr(value) for value in values) + "]"
    if all(type(value) in {int, float} and type(value) is not bool for value in values):
        return "int | float"
    return "object"


def _python_name(value: str) -> str:
    selected = value.replace("-", "_")
    return selected + "_" if keyword.iskeyword(selected) else selected


def _python_source(
    schema: Mapping[str, object], definitions: tuple[DefinitionProjection, ...]
) -> str:
    models = tuple(item for item in definitions if item.is_object_model)
    aliases = _ordered_aliases(
        tuple(item for item in definitions if not item.is_object_model), schema["$defs"]
    )
    lines = [
        "from __future__ import annotations",
        "",
        "import json",
        "from dataclasses import dataclass",
        "from types import MappingProxyType",
        "from typing import ClassVar, Literal, TypeAlias",
        "",
        "from tools.standards_contracts.standards_contracts import (",
        "    ContractRuntime,",
        "    FrozenMap,",
        "    MISSING,",
        "    MissingValue,",
        "    freeze_json,",
        "    model_as_contract,",
        ")",
        "",
        f"_SCHEMA = json.loads({json.dumps(schema, ensure_ascii=False, separators=(',', ':'))!r})",
        f"DEFINITION_METADATA = freeze_json({_definition_metadata(definitions)!r})",
        "",
    ]
    for model in models:
        lines.extend(
            (
                "@dataclass(frozen=True, slots=True)",
                f"class {model.name}:",
                f"    {_model_docstring(model)!r}",
                f"    __definition__: ClassVar[str] = {model.name!r}",
                "    __contract_fields__: ClassVar = MappingProxyType({",
            )
        )
        for item in model.fields:
            lines.append(f"        {item.contract_name!r}: {item.python_name!r},")
        lines.append("    })")
        required = [item for item in model.fields if item.required]
        optional = [item for item in model.fields if not item.required]
        for item in (*required, *optional):
            suffix = "" if item.required else " = MISSING"
            annotation = item.annotation
            if not item.required:
                annotation = f"{annotation} | MissingValue"
            lines.append(f"    {item.python_name}: {annotation}{suffix}")
        lines.extend(
            (
                "",
                "    def __post_init__(self) -> None:",
                "        _RUNTIME.normalize_model(self)",
                "",
                "    @classmethod",
                f"    def from_value(cls, value: object) -> {model.name}:",
                "        selected = _RUNTIME.decode(cls.__definition__, value)",
                "        if not isinstance(selected, cls):",
                "            raise TypeError('decoded value has the wrong generated type')",
                "        return selected",
                "",
                "    def as_contract(self) -> dict[str, object]:",
                "        return model_as_contract(self)",
                "",
            )
        )
    for alias in aliases:
        lines.append(f"{alias.name}: TypeAlias = {alias.annotation}")
    lines.extend(
        (
            "",
            "MODEL_TYPES = MappingProxyType({",
            *(f"    {model.name!r}: {model.name}," for model in models),
            "})",
            "_RUNTIME = ContractRuntime(_SCHEMA, MODEL_TYPES)",
            "",
            "def decode_contract(definition: str, value: object) -> object:",
            "    return _RUNTIME.decode(definition, value)",
            "",
            "__all__ = (",
            *(f"    {item.name!r}," for item in definitions),
            "    'DEFINITION_METADATA',",
            "    'decode_contract',",
            ")",
            "",
        )
    )
    return "\n".join(lines)


def _model_docstring(definition: DefinitionProjection) -> str:
    return "\n\n".join(
        item for item in (definition.title, definition.description) if item
    )


def _definition_metadata(
    definitions: tuple[DefinitionProjection, ...],
) -> dict[str, object]:
    selected: dict[str, object] = {}
    for definition in definitions:
        properties = {
            field.contract_name: {
                "title": field.title,
                "description": field.description,
                "has_default": field.has_default,
                "default": field.default_annotation,
            }
            for field in definition.fields
        }
        selected[definition.name] = {
            "title": definition.title,
            "description": definition.description,
            "has_default": definition.has_default,
            "default": definition.default_annotation,
            "properties": properties,
        }
    return selected


def _ordered_aliases(
    aliases: tuple[DefinitionProjection, ...],
    schemas: Mapping[str, object],
) -> tuple[DefinitionProjection, ...]:
    by_name = {item.name: item for item in aliases}
    selected: list[DefinitionProjection] = []
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if any(item.name == name for item in selected):
            return
        if name in visiting:
            raise failure(
                "CONTRACT.UNSUPPORTED_PROJECTION",
                "recursive aliases without an object boundary are unsupported",
                outcome="unsupported",
                definition=name,
            )
        visiting.add(name)
        for dependency in sorted(
            _definition_references(schemas[name]) & by_name.keys()
        ):
            visit(dependency)
        visiting.remove(name)
        selected.append(by_name[name])

    for alias in aliases:
        visit(alias.name)
    return tuple(selected)


def _agent_tools(
    schema: Mapping[str, object], interface: InterfaceContract
) -> dict[str, object]:
    operations = []
    for operation in interface.operations:
        selected: dict[str, object] = {
            "id": operation.id,
            "input_definition": operation.input_definition,
            "result_definitions": list(operation.result_definitions),
            "input_schema": {"$ref": f"#/$defs/{operation.input_definition}"},
        }
        if operation.capability is not None:
            selected["capability"] = operation.capability
        else:
            selected["capability_by_submission"] = dict(
                operation.capability_by_submission
            )
        operations.append(selected)
    return {
        "schema_version": interface.schema_version,
        "interface_schema_version": interface.interface_schema_version,
        "request_contract_version": interface.request_contract_version,
        "result_projection_version": interface.result_projection_version,
        "operations": operations,
        "$defs": copy.deepcopy(schema["$defs"]),
    }


def _escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _pointer(parts: object) -> str:
    return "".join(f"/{_escape(str(part))}" for part in parts)


__all__ = ("CompiledContracts", "compile_contracts")
