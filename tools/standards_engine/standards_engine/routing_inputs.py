"""Focused wire assertions over the existing snapshot-owned applicability binder.

Generated RouteCall validates the static assertion shape first. This adapter fills
only the registered type; FactSchema owns aliases, states, normalization and domain
constraints. No canonical request, policy fact or stored identity is redefined.
"""
from __future__ import annotations

from collections.abc import Mapping

from tools.standards_applicability.standards_applicability import (
    ApplicabilityError, FactSchema, FactSet,
)
from tools.standards_contracts.standards_contracts import (
    ContractError, ContractFailure, InputIssue, MAX_POINTER_CHARS,
)
from . import _generated_contract as c
from .input_feedback import invalid_input_result


def bind_facts(schema: FactSchema, assertions: Mapping[str, object]) -> FactSet:
    """Complete types from selected authority, then bind once with supplied names.

    Resolution precedes binding: for a multi-error request an undeclared name can
    precede a different value error. The semantic binder retains its own ordering
    after resolution. Never overwrite aliases into canonical keys before binding.
    """
    typed = {}
    for name, value in assertions.items():
        definition = schema.require(name)
        typed[name] = ({"type": definition.type, **value} if isinstance(value, Mapping)
                       else {"type": definition.type, "state": "known", "value": value})
    bound = schema.bind(typed)
    # Canonical normalization can merge distinct Unicode spellings. Keep native
    # binding semantics unchanged, but ensure the focused result/continuation can
    # satisfy its generated grammar before any selection or result construction.
    c.decode_contract("RoutingFactAssertions", fact_assertions(bound))
    return bound


def fact_assertions(facts: FactSet) -> dict[str, object]:
    """Fresh wire values for fact echoes and all focused continuations."""
    return {key: (list(value.value) if isinstance(value.value, tuple) else value.value)
            if value.state == "known" else {"state": value.state}
            for key, value in facts.canonical_values.items()}


def binding_rejection(purpose: str, schema: FactSchema, assertions: Mapping[str, object],
                      error: ApplicabilityError | ContractError) -> c.RejectedResult | c.ApplicationRejectedResult:
    """Expose one safe vocabulary-dependent issue, never caller-controlled keys/data."""
    failure = error.failure
    if isinstance(error, ContractError):
        # The checked projection has canonical, already-authorized keys. Do not
        # echo validator values; the only normalizing shape restriction today is
        # uniqueness of set entries, but keep failure of any declared shape safe.
        field = failure.instance_pointer.lstrip("/").split("/", 1)[0].replace("~1", "/").replace("~0", "~")
        message = "Use normalized routing values that fit the declared shape; set entries must remain distinct after Unicode normalization."
    else:
        field, message = failure.field or "", failure.message
    definition = schema.resolve(field)
    location = "/facts"
    exact = False
    if definition is not None:
        names = [name for name in assertions if schema.resolve(name) == definition]
        if len(names) == 1:
            pointer = "/facts/" + names[0].replace("~", "~0").replace("/", "~1")
            if len(pointer) <= MAX_POINTER_CHARS:
                location, exact = pointer, True
    # FactSchema's value-binding errors are fixed constraint prose. Their field
    # and observed payload are deliberately not copied to the public rejection.
    issue = InputIssue(location, exact, "fact", message)
    value = invalid_input_result(purpose, "route", ContractFailure(
        "invalid", failure.code, message, input_issues=(issue,)), code="ROUTE.INPUT_INVALID")
    model = c.ApplicationRejectedResult if purpose == "application" else c.RejectedResult
    return model.from_value(value)
