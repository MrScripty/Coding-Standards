from __future__ import annotations

import copy
import math
from collections.abc import Iterator, Mapping
from dataclasses import MISSING as DATACLASS_MISSING
from dataclasses import fields, replace
from itertools import chain
from typing import Protocol

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .errors import ContractError, ContractFailure
from .union_selection import compile_union_selectors
from .validation_feedback import validation_feedback


class GeneratedModel(Protocol):
    __definition__: str
    __contract_fields__: Mapping[str, str]


class MissingValue:
    __slots__ = ()

    def __repr__(self) -> str:
        return "MISSING"


MISSING = MissingValue()


class FrozenMap(Mapping[str, object]):
    __slots__ = ("_items",)

    def __init__(
        self, items: Iterator[tuple[str, object]] | tuple[tuple[str, object], ...]
    ):
        self._items = tuple(items)

    def __getitem__(self, key: str) -> object:
        for selected, value in self._items:
            if selected == key:
                return value
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"FrozenMap({self._items!r})"


class ContractRuntime:
    def __init__(
        self,
        schema: Mapping[str, object],
        model_types: Mapping[str, type[GeneratedModel]],
    ) -> None:
        selected_schema = copy.deepcopy(dict(schema))
        schema_id = selected_schema["$id"]
        registry = Registry().with_resource(
            schema_id, Resource.from_contents(selected_schema)
        )
        self._validator = Draft202012Validator(selected_schema, registry=registry)
        self._definitions = selected_schema["$defs"]
        self._models = dict(model_types)
        self._union_selectors = compile_union_selectors(selected_schema)

    def validate(self, definition: str, value: object) -> None:
        node = self._definitions[definition]
        validator = self._validator.evolve(schema=node)
        wire_value = _wire(value)
        _ensure_json_value(wire_value)
        errors = validator.iter_errors(wire_value)
        error = next(errors, None)
        if error is not None:
            issues, truncated = validation_feedback(chain((error,), errors), self._union_selectors)
            raise ContractError(replace(
                _adapt_validation_error(definition, error),
                input_issues=issues, issues_truncated=truncated,
            ))

    def decode(self, definition: str, value: object) -> object:
        self.validate(definition, value)
        return self._decode_node(self._definitions[definition], value, definition)

    def normalize_model(self, model: GeneratedModel) -> None:
        definition = model.__definition__
        wire_value = model_as_contract(model)
        self.validate(definition, wire_value)
        properties = self._definitions[definition]["properties"]
        for contract_name, python_name in model.__contract_fields__.items():
            if contract_name in wire_value:
                object.__setattr__(
                    model,
                    python_name,
                    self._decode_node(
                        properties[contract_name], wire_value[contract_name]
                    ),
                )

    def _decode_node(
        self,
        node: Mapping[str, object] | bool,
        value: object,
        definition: str | None = None,
    ) -> object:
        if isinstance(node, bool):
            return value  # A validated boolean schema declares no representation.
        # Root validation already established the JSON value and constraints.
        # Only a schema-constrained integer acquires Python's integral form;
        # number/untyped/literal data retain their supplied representation.
        value_type = node.get("type")
        integer_only = value_type == "integer" or (
            isinstance(value_type, list)
            and "integer" in value_type and "number" not in value_type
        )
        if integer_only and type(value) is float:
            value = int(value)

        reference = node.get("$ref")
        variants = node.get("oneOf")
        if (isinstance(reference, str) or isinstance(variants, list)) and (
            "properties" in node or "items" in node
            or isinstance(node.get("additionalProperties"), dict)
        ):
            # Sibling shape constraints apply as well as a reference/union. They
            # normalize only their declared children before named construction;
            # root validation already established all constraints and branches.
            value = _wire(self._decode_container(node, value))
        if isinstance(reference, str):
            if isinstance(variants, list):
                # Both clauses were validated. Preserve the union's numeric
                # representation before constructing the referenced model.
                siblings = {key: item for key, item in node.items() if key != "$ref"}
                value = _wire(self._decode_node(siblings, value))
            selected = reference.rsplit("/", 1)[1]
            return self._decode_node(self._definitions[selected], value, selected)

        if isinstance(variants, list):
            selector = self._union_selectors.get(id(node))
            branch = selector.select(value) if selector is not None else None
            if branch is not None:
                return self._decode_node(branch, value)
            selected = [
                variant
                for variant in variants
                if self._validator.evolve(schema=variant).is_valid(_wire(value))
            ]
            if len(selected) != 1:
                raise AssertionError(
                    "validated oneOf did not select exactly one branch"
                )
            return self._decode_node(selected[0], value)

        return self._decode_container(node, value, definition)

    def _decode_container(
        self, node: Mapping[str, object], value: object, definition: str | None = None,
    ) -> object:
        """Construct validated containers, including nullable/implicit shapes."""
        value_type = node.get("type")
        types = value_type if isinstance(value_type, list) else [value_type]
        if isinstance(value, (list, tuple)) and ("array" in types or "items" in node):
            item_schema = node.get("items", {})
            return tuple(self._decode_node(item_schema, item) for item in value)
        if isinstance(value, Mapping) and (
            "object" in types or "properties" in node or "additionalProperties" in node
        ):
            properties = node.get("properties")
            if isinstance(properties, dict) and definition in self._models:
                model_type = self._models[definition]
                field_names = model_type.__contract_fields__
                arguments = {
                    field_names[name]: self._decode_node(properties[name], item)
                    for name, item in value.items()
                }
                return self._construct_validated_model(model_type, arguments)
            additional = node.get("additionalProperties")
            item_schema = additional if isinstance(additional, dict) else {}
            # Anonymous object variants have the same property semantics as
            # generated records. Only map entries use additionalProperties.
            property_schemas = properties if isinstance(properties, dict) else {}
            return FrozenMap(
                (key, self._decode_node(property_schemas.get(key, item_schema), item))
                for key, item in value.items()
            )
        return value

    @staticmethod
    def _construct_validated_model(
        model_type: type[GeneratedModel], arguments: Mapping[str, object]
    ) -> GeneratedModel:
        """Retain the root schema proof without revalidating nested models."""
        model = object.__new__(model_type)
        for field in fields(model_type):
            if field.name in arguments:
                selected = arguments[field.name]
            elif field.default is not DATACLASS_MISSING:
                selected = field.default
            elif field.default_factory is not DATACLASS_MISSING:
                selected = field.default_factory()
            else:
                raise AssertionError(
                    f"validated {model_type.__name__} omitted required field "
                    f"{field.name}"
                )
            object.__setattr__(model, field.name, selected)
        return model


def model_as_contract(model: GeneratedModel) -> dict[str, object]:
    reverse = {value: key for key, value in model.__contract_fields__.items()}
    selected: dict[str, object] = {}
    for item in fields(model):
        value = getattr(model, item.name)
        if value is MISSING:
            continue
        selected[reverse[item.name]] = _wire(value)
    return selected


def freeze_json(value: object) -> object:
    value_type = type(value)
    if value_type is dict:
        return FrozenMap((key, freeze_json(item)) for key, item in value.items())
    if value_type is list:
        return tuple(freeze_json(item) for item in value)
    return value


def _wire(value: object) -> object:
    if hasattr(value, "__contract_fields__"):
        return model_as_contract(value)
    if isinstance(value, Mapping):
        return {key: _wire(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_wire(item) for item in value]
    return value


def _ensure_json_value(value: object) -> None:
    value_type = type(value)
    if value is None or value_type in {bool, int, str}:
        return
    if value_type is float:
        if math.isfinite(value):
            return
        raise ContractError(
            ContractFailure(
                outcome="invalid",
                code="CONTRACT.INVALID_JSON_VALUE",
                message="JSON numbers must be finite",
            )
        )
    if value_type is list:
        for item in value:
            _ensure_json_value(item)
        return
    if value_type is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ContractError(
                    ContractFailure(
                        outcome="invalid",
                        code="CONTRACT.INVALID_JSON_VALUE",
                        message="JSON object keys must be exact strings",
                    )
                )
            _ensure_json_value(item)
        return
    raise ContractError(
        ContractFailure(
            outcome="invalid",
            code="CONTRACT.INVALID_JSON_VALUE",
            message="value is not representable in the strict JSON contract",
        )
    )


def _pointer(parts: object) -> str:
    return "".join(
        "/" + str(part).replace("~", "~0").replace("/", "~1") for part in parts
    )


def _adapt_validation_error(definition: str, error: object) -> ContractFailure:
    causes = tuple(_adapt_validation_error(definition, item) for item in error.context)
    keyword = str(error.validator) if error.validator is not None else None
    return ContractFailure(
        outcome="invalid",
        code="CONTRACT.INVALID_INSTANCE",
        message="value does not satisfy the selected public contract",
        definition=definition,
        instance_pointer=_pointer(error.absolute_path),
        schema_pointer=_pointer(error.absolute_schema_path),
        keyword=keyword,
        causes=causes,
    )


__all__ = (
    "ContractRuntime",
    "FrozenMap",
    "MISSING",
    "MissingValue",
    "freeze_json",
    "model_as_contract",
)
