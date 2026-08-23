from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .errors import AnalysisError, AnalysisFailure


class Truth(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class FactDefinition:
    id: str
    type: str
    nullable: bool = False
    values: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FactState:
    type: str
    state: str
    value: object = None


def _invalid(message: str, *, field: str | None = None, observed: str | None = None) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(
            "APPLICABILITY.INVALID",
            "invalid",
            message,
            field=field,
            observed=observed,
        )
    )


class ApplicabilityEvaluator:
    """Validate and evaluate the bounded three-valued applicability language."""

    def __init__(self, definitions: tuple[FactDefinition, ...]) -> None:
        if not definitions:
            raise _invalid("applicability schema must declare at least one fact")
        indexed: dict[str, FactDefinition] = {}
        for definition in definitions:
            if definition.id in indexed:
                raise _invalid("fact identities and aliases must be unique", field=definition.id)
            self._validate_definition(definition)
            indexed[definition.id] = definition
            for alias in definition.aliases:
                if alias in indexed:
                    raise _invalid("fact identities and aliases must be unique", field=alias)
                indexed[alias] = definition
        self._definitions = indexed

    @property
    def canonical_definitions(self) -> tuple[FactDefinition, ...]:
        return tuple(
            definition
            for key, definition in self._definitions.items()
            if key == definition.id
        )

    def validate_facts(self, values: Mapping[str, object]) -> dict[str, FactState]:
        selected: dict[str, FactState] = {}
        for supplied_id, raw in values.items():
            definition = self._definitions.get(supplied_id)
            if definition is None:
                raise _invalid("fact is not declared by the applicability schema", field=supplied_id)
            if definition.id in selected:
                raise _invalid(
                    "a fact and its alias cannot both be supplied",
                    field=definition.id,
                )
            selected[definition.id] = self._fact_state(definition, raw)
        return selected

    def evaluate(
        self,
        expression: Mapping[str, object],
        facts: Mapping[str, FactState],
    ) -> Truth:
        operator = expression.get("operator")
        if operator == "always":
            if set(expression) != {"operator"}:
                raise _invalid("always accepts no operands")
            return Truth.TRUE
        if operator == "all" or operator == "any":
            key = "expressions"
            children = expression.get(key)
            if set(expression) != {"operator", key} or not isinstance(children, list) or not children:
                raise _invalid(f"{operator} requires a non-empty expressions list")
            results = [self.evaluate(self._expression(item), facts) for item in children]
            if operator == "all":
                if Truth.FALSE in results:
                    return Truth.FALSE
                return Truth.UNKNOWN if Truth.UNKNOWN in results else Truth.TRUE
            if Truth.TRUE in results:
                return Truth.TRUE
            return Truth.UNKNOWN if Truth.UNKNOWN in results else Truth.FALSE
        if operator == "not":
            if set(expression) != {"operator", "expression"}:
                raise _invalid("not requires exactly one expression")
            result = self.evaluate(self._expression(expression.get("expression")), facts)
            if result is Truth.UNKNOWN:
                return result
            return Truth.FALSE if result is Truth.TRUE else Truth.TRUE
        if operator in {"equals", "contains"}:
            if set(expression) != {"operator", "fact", "value"}:
                raise _invalid(f"{operator} requires fact and value")
            definition, state = self._resolved_fact(expression.get("fact"), facts)
            expected = expression.get("value")
            self._validate_operand(definition, expected, operator)
            if state is None or state.state == "unknown":
                return Truth.UNKNOWN
            if state.state == "known-absent":
                return Truth.FALSE
            if operator == "equals":
                return Truth.TRUE if state.value == expected else Truth.FALSE
            if state.value is None:
                return Truth.FALSE
            assert isinstance(state.value, tuple)
            return Truth.TRUE if expected in state.value else Truth.FALSE
        if operator == "in":
            if set(expression) != {"operator", "fact", "values"}:
                raise _invalid("in requires fact and values")
            definition, state = self._resolved_fact(expression.get("fact"), facts)
            expected = expression.get("values")
            if (
                not isinstance(expected, list)
                or not expected
                or len({repr(item) for item in expected}) != len(expected)
            ):
                raise _invalid("in values must be a non-empty unique list")
            for item in expected:
                self._validate_operand(definition, item, "equals")
            if state is None or state.state == "unknown":
                return Truth.UNKNOWN
            if state.state == "known-absent":
                return Truth.FALSE
            return Truth.TRUE if state.value in expected else Truth.FALSE
        if operator == "exists":
            if set(expression) != {"operator", "fact"}:
                raise _invalid("exists requires exactly one fact")
            _, state = self._resolved_fact(expression.get("fact"), facts)
            if state is None or state.state == "unknown":
                return Truth.UNKNOWN
            return Truth.FALSE if state.state == "known-absent" else Truth.TRUE
        raise _invalid("applicability operator is unsupported", observed=str(operator))

    def referenced_facts(self, expression: Mapping[str, object]) -> tuple[str, ...]:
        operator = expression.get("operator")
        if operator == "always":
            if set(expression) != {"operator"}:
                raise _invalid("always accepts no operands")
            return ()
        if operator in {"all", "any"}:
            children = expression.get("expressions")
            if not isinstance(children, list):
                raise _invalid(f"{operator} requires an expressions list")
            values = {
                fact
                for item in children
                for fact in self.referenced_facts(self._expression(item))
            }
            return tuple(sorted(values))
        if operator == "not":
            return self.referenced_facts(self._expression(expression.get("expression")))
        if operator in {"equals", "in", "contains", "exists"}:
            definition, _ = self._resolved_fact(expression.get("fact"), {})
            return (definition.id,)
        raise _invalid("applicability operator is unsupported", observed=str(operator))

    def _resolved_fact(
        self,
        fact_id: object,
        facts: Mapping[str, FactState],
    ) -> tuple[FactDefinition, FactState | None]:
        if not isinstance(fact_id, str) or fact_id not in self._definitions:
            raise _invalid("expression references an undeclared fact", observed=str(fact_id))
        definition = self._definitions[fact_id]
        return definition, facts.get(definition.id)

    @staticmethod
    def _expression(value: object) -> Mapping[str, object]:
        if not isinstance(value, dict):
            raise _invalid("applicability expression must be an object")
        return value

    @staticmethod
    def _validate_definition(definition: FactDefinition) -> None:
        supported = {"boolean", "enum", "string", "string-set", "enum-set", "canonical-id"}
        if not definition.id or definition.type not in supported:
            raise _invalid("fact declaration is invalid", field=definition.id)
        if definition.type in {"enum", "enum-set"}:
            if not definition.values or len(set(definition.values)) != len(definition.values):
                raise _invalid("enum facts require unique values", field=definition.id)
        elif definition.values:
            raise _invalid("only enum facts may declare values", field=definition.id)
        if len(set(definition.aliases)) != len(definition.aliases):
            raise _invalid("fact aliases must be unique", field=definition.id)

    def _fact_state(self, definition: FactDefinition, raw: object) -> FactState:
        if not isinstance(raw, dict) or set(raw) - {"type", "state", "value"}:
            raise _invalid("fact value must be a typed state object", field=definition.id)
        value_type = raw.get("type")
        state = raw.get("state")
        if value_type != definition.type or state not in {"known", "known-absent", "unknown"}:
            raise _invalid("fact type or state does not match its declaration", field=definition.id)
        if state != "known":
            if "value" in raw:
                raise _invalid("absent and unknown facts cannot contain a value", field=definition.id)
            return FactState(definition.type, str(state))
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
            if definition.type == "enum" and value not in definition.values:
                raise _invalid("enum fact value is outside its domain", field=definition.id)
        else:
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise _invalid("set fact value must be a string list", field=definition.id)
            if len(set(value)) != len(value):
                raise _invalid("set fact values must be unique", field=definition.id)
            if definition.type == "enum-set" and set(value) - set(definition.values):
                raise _invalid("enum-set fact value is outside its domain", field=definition.id)
            value = tuple(value)
        return FactState(definition.type, "known", value)

    @staticmethod
    def _validate_operand(definition: FactDefinition, value: object, operator: str) -> None:
        if value is None:
            if definition.nullable and operator != "contains":
                return
            raise _invalid("expression null operand is not valid for this fact", field=definition.id)
        if operator == "contains" and definition.type not in {"string-set", "enum-set"}:
            raise _invalid("contains requires a set-valued fact", field=definition.id)
        if operator != "contains" and definition.type in {"string-set", "enum-set"}:
            raise _invalid(
                f"{operator} requires a scalar-valued fact",
                field=definition.id,
            )
        scalar_type = definition.type.removesuffix("-set")
        if scalar_type == "boolean":
            valid = isinstance(value, bool)
        else:
            valid = isinstance(value, str)
        if not valid:
            raise _invalid("expression operand has the wrong type", field=definition.id)
        if scalar_type == "enum" and value not in definition.values:
            raise _invalid("expression operand is outside the enum domain", field=definition.id)
