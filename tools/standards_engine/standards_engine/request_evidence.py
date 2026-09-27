"""Expand validated agent evidence uses at the request boundary, without state.

Native inputs, provider checks and persisted evidence remain canonical. Only the
schema-generated EvidenceUse type is substituted; arbitrary maps and authored
text never acquire reference semantics from a matching key or spelling.
"""
from __future__ import annotations

from collections.abc import Mapping

from tools.standards_contracts.standards_contracts import (
    MISSING, MAX_POINTER_CHARS, ContractError, ContractFailure, InputIssue,
)
from . import _generated_contract as c


REQUEST_EVIDENCE_LIMIT = 128


def _invalid_reference(code: str, path: tuple[str | int, ...], message: str) -> ContractError:
    pointer = ''.join('/' + str(part).replace('~', '~0').replace('/', '~1') for part in path)
    exact = len(pointer) <= MAX_POINTER_CHARS and "*" not in path
    issue = InputIssue(pointer if exact else '', exact, 'evidence_ref', message)
    return ContractError(ContractFailure('invalid', code, message, input_issues=(issue,)))


def expand_request_evidence(call: object) -> dict[str, object]:
    """Return native arguments or reject an incomplete/ambiguous local binding.

    The caller has already validated the complete generated agent input. It must
    validate the returned native input before dispatch, including uniqueness and
    the domain's expanded submission limits. Nothing is cached or verified here.
    """
    table = getattr(call, "evidence", MISSING)
    table = {} if table is MISSING else table
    if len(table) > REQUEST_EVIDENCE_LIMIT:
        raise _invalid_reference("REQUEST_EVIDENCE.LIMIT", ("evidence",),
                                 "A request evidence table supports at most 128 entries.")
    used: set[str] = set()

    def expand(value: object, path: tuple[str | int, ...]) -> object:
        if isinstance(value, c.EvidenceUse):
            name = value.evidence_ref
            if name not in table:
                raise _invalid_reference("REQUEST_EVIDENCE.UNBOUND", (*path, "evidence_ref"),
                                         "An evidence_ref does not name an entry in this request.")
            used.add(name)
            return table[name].as_contract()
        fields = getattr(type(value), "__contract_fields__", None)
        if fields is not None:
            return {
                wire: expand(item, (*path, wire))
                for wire, field in fields.items()
                if (item := getattr(value, field)) is not MISSING
            }
        if isinstance(value, Mapping):
            return {key: expand(item, (*path, "*")) for key, item in value.items()}
        if isinstance(value, (tuple, list)):
            return [expand(item, (*path, index)) for index, item in enumerate(value)]
        return value

    arguments = {
        wire: expand(value, (wire,))
        for wire, field in type(call).__contract_fields__.items()
        if field != "evidence" and (value := getattr(call, field)) is not MISSING
    }
    if used != set(table):
        raise _invalid_reference("REQUEST_EVIDENCE.UNUSED", ("evidence",),
                                 "Every request evidence entry must be explicitly used.")
    return arguments
