from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .errors import ApplicabilityError, ApplicabilityFailure


LANGUAGE_VERSION = 1
SCHEMA_DIGEST_DOMAIN = "coding-standards:applicability-fact-schema:v1"
PROGRAM_DIGEST_DOMAIN = "coding-standards:applicability-program:v1"
FACT_CONTRACT_DIGEST_DOMAIN = "coding-standards:fact-contract:v1"
PROGRAM_INDEX_DIGEST_DOMAIN = "coding-standards:applicability-program-index:v1"
SUPPORTED_FACT_TYPES = frozenset(
    {"boolean", "enum", "string", "string-set", "enum-set", "canonical-id"}
)
SUPPORTED_FACT_STATES = frozenset({"known", "known-absent", "unknown"})
SUPPORTED_OPERATORS = frozenset(
    {"always", "all", "any", "not", "equals", "in", "contains", "exists"}
)


class Truth(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    truth: Truth
    unresolved_facts: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FactContract:
    id: str
    semantic_revision: int
    type: str
    nullable: bool
    values: tuple[str, ...]
    aliases: tuple[str, ...]
    meaning: str
    context_kind: str
    answer_contract: str
    evidence_contract: str
    authorization_capability: str
    prompt: str
    digest: str

    def semantic_projection(self) -> dict[str, object]:
        value: dict[str, object] = {
            "id": self.id,
            "semantic_revision": self.semantic_revision,
            "type": self.type,
            "nullable": self.nullable,
            "meaning": self.meaning,
            "context_kind": self.context_kind,
            "answer_contract": self.answer_contract,
            "evidence_contract": self.evidence_contract,
            "authorization_capability": self.authorization_capability,
        }
        if self.values:
            value["values"] = list(self.values)
        return value

    def as_contract(self) -> dict[str, object]:
        value = self.semantic_projection()
        value["aliases"] = list(self.aliases)
        value["prompt"] = self.prompt
        value["digest"] = self.digest
        return value

    def bind(self, value: Mapping[str, object]) -> FactValue:
        return _bind_value(self, value)


@dataclass(frozen=True, slots=True)
class FactValue:
    type: str
    state: str
    value: object = None

    def as_contract(self) -> dict[str, object]:
        result: dict[str, object] = {"type": self.type, "state": self.state}
        if self.state == "known":
            result["value"] = list(self.value) if isinstance(self.value, tuple) else self.value
        return result


@dataclass(frozen=True, slots=True)
class FactSet:
    schema_digest: str
    canonical_values: Mapping[str, FactValue]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "canonical_values",
            MappingProxyType(dict(sorted(self.canonical_values.items()))),
        )


@dataclass(frozen=True, slots=True)
class _Expression:
    operator: str
    fact: str | None = None
    value: object = None
    children: tuple[_Expression, ...] = ()


@dataclass(frozen=True, slots=True)
class ApplicabilityProgram:
    normalized_expression: Mapping[str, object]
    referenced_facts: tuple[str, ...]
    language_version: int
    schema_digest: str
    dependency_digest: str
    _root: _Expression = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "normalized_expression",
            _freeze(self.normalized_expression),
        )

    def evaluate(self, facts: FactSet) -> EvaluationResult:
        if facts.schema_digest != self.schema_digest:
            raise _invalid(
                "fact set belongs to a different fact schema",
                field="schema_digest",
                observed=facts.schema_digest,
            )
        return _evaluate(self._root, facts.canonical_values)

    def as_expression(self) -> dict[str, object]:
        return _thaw(self.normalized_expression)

    def as_projection(self) -> dict[str, object]:
        return {
            "normalized_expression": self.as_expression(),
            "referenced_facts": list(self.referenced_facts),
            "language_version": self.language_version,
            "schema_digest": self.schema_digest,
            "dependency_digest": self.dependency_digest,
        }


@dataclass(frozen=True, slots=True)
class FactSchema:
    id: str
    version: int
    definitions: tuple[FactContract, ...]
    aliases: Mapping[str, str]
    digest: str
    _index: Mapping[str, FactContract] = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "aliases", MappingProxyType(dict(self.aliases)))
        object.__setattr__(self, "_index", MappingProxyType(dict(self._index)))

    def compile(
        self,
        expression: Mapping[str, object],
        *,
        language_version: int = LANGUAGE_VERSION,
    ) -> ApplicabilityProgram:
        if language_version != LANGUAGE_VERSION:
            raise _unsupported(
                "applicability language version is unsupported",
                observed=str(language_version),
            )
        root, normalized = _compile_expression(expression, self._index)
        referenced = tuple(sorted(_referenced(root)))
        dependencies = [
            _definition_projection(self._index[fact_id]) for fact_id in referenced
        ]
        dependency_digest = _digest(
            PROGRAM_DIGEST_DOMAIN,
            {
                "language_version": language_version,
                "expression": normalized,
                "referenced_fact_definitions": dependencies,
            },
        )
        return ApplicabilityProgram(
            normalized,
            referenced,
            language_version,
            self.digest,
            dependency_digest,
            root,
        )

    def as_declaration(self) -> dict[str, object]:
        return {
            "kind": "applicability-fact-schema",
            "id": self.id,
            "version": self.version,
            "facts": [
                {
                    **item.semantic_projection(),
                    "aliases": list(item.aliases),
                    "prompt": item.prompt,
                }
                for item in self.definitions
            ],
        }

    def resolve(self, fact_id: str) -> FactContract | None:
        return self._index.get(fact_id)

    def bind(self, values: Mapping[str, object]) -> FactSet:
        selected: dict[str, FactValue] = {}
        for supplied_id, raw in values.items():
            definition = self._index.get(supplied_id)
            if definition is None:
                raise _invalid(
                    "fact is not declared by the applicability schema",
                    field=supplied_id,
                )
            if definition.id in selected:
                raise _invalid(
                    "a fact and its alias cannot both be supplied",
                    field=definition.id,
                )
            selected[definition.id] = _bind_value(definition, raw)
        return FactSet(self.digest, selected)


@dataclass(frozen=True, slots=True)
class ApplicabilityProgramIndex:
    programs: Mapping[str, ApplicabilityProgram]
    by_fact: Mapping[str, tuple[str, ...]]
    digest: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "programs",
            MappingProxyType(dict(sorted(self.programs.items()))),
        )
        object.__setattr__(
            self,
            "by_fact",
            MappingProxyType(dict(sorted(self.by_fact.items()))),
        )

    def dependents(self, fact_id: str) -> tuple[str, ...]:
        return self.by_fact.get(fact_id, ())


def index_programs(
    programs: Mapping[str, ApplicabilityProgram],
) -> ApplicabilityProgramIndex:
    selected = dict(sorted(programs.items()))
    if any(not program_id for program_id in selected):
        raise _invalid("program index IDs must be non-empty")
    by_fact: dict[str, list[str]] = {}
    for program_id, program in selected.items():
        for fact_id in program.referenced_facts:
            by_fact.setdefault(fact_id, []).append(program_id)
    normalized = {
        fact_id: tuple(sorted(program_ids))
        for fact_id, program_ids in by_fact.items()
    }
    digest = _digest(
        PROGRAM_INDEX_DIGEST_DOMAIN,
        {
            "programs": [
                {
                    "id": program_id,
                    "dependency_digest": program.dependency_digest,
                }
                for program_id, program in selected.items()
            ]
        },
    )
    return ApplicabilityProgramIndex(selected, normalized, digest)


def compile_fact_schema(declaration: Mapping[str, object]) -> FactSchema:
    expected = {"kind", "id", "version", "facts"}
    if set(declaration) != expected or declaration.get("kind") != "applicability-fact-schema":
        raise _invalid("fact schema shape is invalid")
    schema_id = declaration.get("id")
    version = declaration.get("version")
    raw_definitions = declaration.get("facts")
    if not isinstance(schema_id, str) or not schema_id:
        raise _invalid("fact schema id must be a non-empty string", field="id")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise _invalid("fact schema version must be a positive integer", field="version")
    if not isinstance(raw_definitions, list):
        raise _invalid("fact schema facts must be an array", field="facts")

    definitions: list[FactContract] = []
    names: dict[str, FactContract] = {}
    aliases: dict[str, str] = {}
    for index, raw in enumerate(raw_definitions):
        definition = _compile_definition(raw, index)
        for name in (definition.id, *definition.aliases):
            if name in names:
                raise _invalid(
                    "fact identities and aliases must be globally unique",
                    field=name,
                )
            names[name] = definition
        for alias in definition.aliases:
            aliases[alias] = definition.id
        definitions.append(definition)
    definitions.sort(key=lambda item: item.id)
    projection = {
        "kind": "applicability-fact-schema",
        "id": _text(schema_id),
        "version": version,
        "facts": [item.semantic_projection() for item in definitions],
    }
    return FactSchema(
        str(projection["id"]),
        version,
        tuple(definitions),
        dict(sorted(aliases.items())),
        _digest(SCHEMA_DIGEST_DOMAIN, projection),
        names,
    )


def _compile_definition(raw: object, index: int) -> FactContract:
    if not isinstance(raw, dict):
        raise _invalid("fact declaration must be an object", field=f"facts[{index}]")
    allowed = {
        "id",
        "semantic_revision",
        "type",
        "nullable",
        "values",
        "aliases",
        "meaning",
        "context_kind",
        "answer_contract",
        "evidence_contract",
        "authorization_capability",
        "prompt",
    }
    required = allowed - {"values"}
    if set(raw) - allowed or not required <= set(raw):
        raise _invalid("fact declaration shape is invalid", field=f"facts[{index}]")
    fact_id = raw.get("id")
    semantic_revision = raw.get("semantic_revision")
    fact_type = raw.get("type")
    nullable = raw.get("nullable")
    values = raw.get("values", [])
    aliases = raw.get("aliases")
    meaning = raw.get("meaning")
    context_kind = raw.get("context_kind")
    answer_contract = raw.get("answer_contract")
    evidence_contract = raw.get("evidence_contract")
    authorization_capability = raw.get("authorization_capability")
    prompt = raw.get("prompt")
    if not isinstance(fact_id, str) or not fact_id:
        raise _invalid("fact id must be a non-empty string", field=f"facts[{index}].id")
    if fact_type not in SUPPORTED_FACT_TYPES:
        raise _invalid("fact type is unsupported", field=fact_id, observed=str(fact_type))
    if not isinstance(nullable, bool):
        raise _invalid("fact nullable must be Boolean", field=fact_id)
    if not _unique_strings(values) or not _unique_strings(aliases):
        raise _invalid("fact values and aliases must be unique strings", field=fact_id)
    if fact_type in {"enum", "enum-set"}:
        if not values:
            raise _invalid("enum facts require at least one value", field=fact_id)
    elif values:
        raise _invalid("only enum facts may declare values", field=fact_id)
    if not isinstance(semantic_revision, int) or isinstance(semantic_revision, bool) or semantic_revision < 1:
        raise _invalid("fact semantic revision must be positive", field=fact_id)
    semantic_text = (
        meaning,
        context_kind,
        answer_contract,
        evidence_contract,
        authorization_capability,
        prompt,
    )
    if any(not isinstance(item, str) or not item for item in semantic_text):
        raise _invalid("fact semantic and rendering fields must be non-empty", field=fact_id)
    contract_values = tuple(sorted(_text(item) for item in values))
    semantic_projection: dict[str, object] = {
        "id": _text(fact_id),
        "semantic_revision": semantic_revision,
        "type": str(fact_type),
        "nullable": nullable,
        "meaning": _text(str(meaning)),
        "context_kind": _text(str(context_kind)),
        "answer_contract": _text(str(answer_contract)),
        "evidence_contract": _text(str(evidence_contract)),
        "authorization_capability": _text(str(authorization_capability)),
    }
    if contract_values:
        semantic_projection["values"] = list(contract_values)
    return FactContract(
        _text(fact_id),
        semantic_revision,
        str(fact_type),
        nullable,
        contract_values,
        tuple(sorted(_text(item) for item in aliases)),
        _text(str(meaning)),
        _text(str(context_kind)),
        _text(str(answer_contract)),
        _text(str(evidence_contract)),
        _text(str(authorization_capability)),
        _text(str(prompt)),
        _digest(FACT_CONTRACT_DIGEST_DOMAIN, semantic_projection),
    )


def _compile_expression(
    value: object,
    definitions: Mapping[str, FactContract],
) -> tuple[_Expression, dict[str, object]]:
    if not isinstance(value, dict):
        raise _invalid("applicability expression must be an object")
    operator = value.get("operator")
    if operator == "always":
        _require_fields(value, {"operator"}, operator)
        return _Expression("always"), {"operator": "always"}
    if operator in {"all", "any"}:
        _require_fields(value, {"operator", "expressions"}, str(operator))
        raw_children = value.get("expressions")
        if not isinstance(raw_children, list) or not raw_children:
            raise _invalid(f"{operator} requires a non-empty expressions array")
        compiled = [_compile_expression(child, definitions) for child in raw_children]
        return (
            _Expression(str(operator), children=tuple(item[0] for item in compiled)),
            {"operator": str(operator), "expressions": [item[1] for item in compiled]},
        )
    if operator == "not":
        _require_fields(value, {"operator", "expression"}, "not")
        child, normalized = _compile_expression(value.get("expression"), definitions)
        return _Expression("not", children=(child,)), {
            "operator": "not",
            "expression": normalized,
        }
    fields = {
        "equals": {"operator", "fact", "value"},
        "contains": {"operator", "fact", "value"},
        "in": {"operator", "fact", "values"},
        "exists": {"operator", "fact"},
    }
    if operator not in SUPPORTED_OPERATORS or operator not in fields:
        raise _invalid("applicability operator is unsupported", observed=str(operator))
    _require_fields(value, fields[str(operator)], str(operator))
    supplied_fact = value.get("fact")
    if not isinstance(supplied_fact, str) or supplied_fact not in definitions:
        raise _invalid("expression references an undeclared fact", observed=str(supplied_fact))
    definition = definitions[supplied_fact]
    normalized: dict[str, object] = {"operator": str(operator), "fact": definition.id}
    operand: object = None
    if operator in {"equals", "contains"}:
        operand = value.get("value")
        _validate_operand(definition, operand, str(operator))
        operand = _normalized_value(operand)
        normalized["value"] = operand
    elif operator == "in":
        raw_values = value.get("values")
        if not isinstance(raw_values, list) or not raw_values:
            raise _invalid("in requires a non-empty values array")
        normalized_values = [_normalized_value(item) for item in raw_values]
        if len({_canonical_json(item) for item in normalized_values}) != len(normalized_values):
            raise _invalid("in values must be unique")
        for item in normalized_values:
            _validate_operand(definition, item, "equals")
        operand = tuple(sorted(normalized_values, key=_canonical_json))
        normalized["values"] = list(operand)
    return _Expression(str(operator), definition.id, operand), normalized


def _evaluate(
    expression: _Expression,
    facts: Mapping[str, FactValue],
) -> EvaluationResult:
    operator = expression.operator
    if operator == "always":
        return EvaluationResult(Truth.TRUE)
    if operator in {"all", "any"}:
        results = tuple(_evaluate(child, facts) for child in expression.children)
        if operator == "all":
            if any(item.truth is Truth.FALSE for item in results):
                return EvaluationResult(Truth.FALSE)
            if all(item.truth is Truth.TRUE for item in results):
                return EvaluationResult(Truth.TRUE)
        else:
            if any(item.truth is Truth.TRUE for item in results):
                return EvaluationResult(Truth.TRUE)
            if all(item.truth is Truth.FALSE for item in results):
                return EvaluationResult(Truth.FALSE)
        return EvaluationResult(
            Truth.UNKNOWN,
            tuple(sorted({fact for item in results for fact in item.unresolved_facts})),
        )
    if operator == "not":
        result = _evaluate(expression.children[0], facts)
        if result.truth is Truth.UNKNOWN:
            return result
        return EvaluationResult(
            Truth.FALSE if result.truth is Truth.TRUE else Truth.TRUE
        )
    assert expression.fact is not None
    state = facts.get(expression.fact)
    if state is None or state.state == "unknown":
        return EvaluationResult(Truth.UNKNOWN, (expression.fact,))
    if operator == "exists":
        return EvaluationResult(
            Truth.FALSE if state.state == "known-absent" else Truth.TRUE
        )
    if state.state == "known-absent":
        return EvaluationResult(Truth.FALSE)
    if operator == "equals":
        matched = state.value == expression.value
    elif operator == "contains":
        matched = expression.value in (state.value or ())
    else:
        matched = state.value in expression.value
    return EvaluationResult(Truth.TRUE if matched else Truth.FALSE)


def _bind_value(definition: FactContract, raw: object) -> FactValue:
    if not isinstance(raw, Mapping) or set(raw) - {"type", "state", "value"}:
        raise _invalid("fact value must be a typed state object", field=definition.id)
    value_type = raw.get("type")
    state = raw.get("state")
    if value_type != definition.type or state not in SUPPORTED_FACT_STATES:
        raise _invalid("fact type or state does not match its declaration", field=definition.id)
    if state != "known":
        if "value" in raw:
            raise _invalid("absent and unknown facts cannot contain a value", field=definition.id)
        return FactValue(definition.type, str(state))
    if "value" not in raw:
        raise _invalid("known facts require a value", field=definition.id)
    value = raw["value"]
    if value is None:
        if not definition.nullable:
            raise _invalid("fact is not nullable", field=definition.id)
    elif definition.type == "boolean":
        if not isinstance(value, bool):
            raise _invalid("boolean fact value is invalid", field=definition.id)
    elif definition.type in {"enum", "string", "canonical-id"}:
        if not isinstance(value, str):
            raise _invalid("scalar fact value is invalid", field=definition.id)
        value = _text(value)
        if definition.type == "enum" and value not in definition.values:
            raise _invalid("enum fact value is outside its domain", field=definition.id)
    else:
        if not isinstance(value, (list, tuple)) or not _unique_strings(value):
            raise _invalid("set fact value must contain unique strings", field=definition.id)
        normalized = tuple(sorted(_text(item) for item in value))
        if definition.type == "enum-set" and set(normalized) - set(definition.values):
            raise _invalid("enum-set fact value is outside its domain", field=definition.id)
        value = normalized
    return FactValue(definition.type, "known", value)


def _validate_operand(definition: FactContract, value: object, operator: str) -> None:
    if value is None:
        if definition.nullable and operator != "contains":
            return
        raise _invalid("null operand is invalid for this fact", field=definition.id)
    if operator == "contains" and definition.type not in {"string-set", "enum-set"}:
        raise _invalid("contains requires a set-valued fact", field=definition.id)
    if operator != "contains" and definition.type in {"string-set", "enum-set"}:
        raise _invalid(f"{operator} requires a scalar-valued fact", field=definition.id)
    scalar_type = definition.type.removesuffix("-set")
    valid = isinstance(value, bool) if scalar_type == "boolean" else isinstance(value, str)
    if not valid:
        raise _invalid("expression operand has the wrong type", field=definition.id)
    if scalar_type == "enum" and value not in definition.values:
        raise _invalid("expression operand is outside the enum domain", field=definition.id)


def _definition_projection(definition: FactContract) -> dict[str, object]:
    return definition.semantic_projection()


def _referenced(expression: _Expression) -> set[str]:
    result = {expression.fact} if expression.fact is not None else set()
    for child in expression.children:
        result.update(_referenced(child))
    return result


def _require_fields(value: Mapping[str, object], expected: set[str], operator: str) -> None:
    if set(value) != expected:
        raise _invalid(f"{operator} has invalid operands")


def _unique_strings(value: object) -> bool:
    return (
        isinstance(value, (list, tuple))
        and all(isinstance(item, str) and item for item in value)
        and len(set(value)) == len(value)
    )


def _text(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _normalized_value(value: object) -> object:
    return _text(value) if isinstance(value, str) else value


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _canonical_json(value: object) -> str:
    return json.dumps(
        _thaw(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(domain: str, value: object) -> str:
    payload = domain.encode("utf-8") + b"\0" + _canonical_json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _invalid(
    message: str,
    *,
    field: str | None = None,
    observed: str | None = None,
) -> ApplicabilityError:
    return ApplicabilityError(
        ApplicabilityFailure("APPLICABILITY.INVALID", "invalid", message, field, observed)
    )


def _unsupported(message: str, *, observed: str) -> ApplicabilityError:
    return ApplicabilityError(
        ApplicabilityFailure(
            "APPLICABILITY.UNSUPPORTED_VERSION",
            "unsupported",
            message,
            "language_version",
            observed,
        )
    )
