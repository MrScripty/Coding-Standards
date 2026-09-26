"""Bounded input-contract observation for one installed, purpose-qualified catalog.

Schema documents are data here. The canonical validator owns their semantics;
shared structural traversal owns references. Discovery owns only selection,
whole-record paging and catalog binding, independently of standards state.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Collection
import json

from tools.standards_contracts.standards_contracts import (
    CompiledContracts,
    ContractError,
    direct_schema_references,
    local_definition_name,
)

from . import _generated_contract as c
from .context_projection import Purpose, qualified_operations


INPUT_DISCOVERY_DEFAULT_RECORDS = 8
INPUT_DISCOVERY_RESULT_BYTES = 16 * 1024


class InputContractDiscovery:
    """Own an immutable view; no repository access, session state or new identity."""

    def __init__(self, interface: CompiledContracts, *, purpose: Purpose | str,
                 operation_names: Collection[str], catalog_digest: str) -> None:
        self._purpose = Purpose(purpose)
        self._version = interface.interface.interface_schema_version
        self._catalog_digest = catalog_digest
        projection = interface.project().agent_tools
        self._definitions = projection["$defs"]
        self._dialect = interface.schema["$schema"]
        published = frozenset(operation_names)
        self._roots = {
            operation["id"]: operation["input_definition"]
            for operation in qualified_operations(projection, self._purpose)
            if operation["id"] in published
        }

    def _ordered_definitions(self, root: str) -> list[str]:
        """Visit containing shapes before descendants; recursive graphs terminate."""
        pending = deque([root])
        seen: set[str] = set()
        ordered = []
        while pending:
            name = pending.popleft()
            if name in seen:
                continue
            seen.add(name)
            ordered.append(name)
            pending.extend(sorted({local_definition_name(reference) for reference in
                                   direct_schema_references(self._definitions[name])}))
        return ordered

    def invoke(self, arguments: object) -> dict:
        try:
            value = c.DescribeInputCall.from_value(arguments).as_contract()
        except (ContractError, ValueError, TypeError):
            return self._reject("INVALID_ARGUMENTS", "invalid",
                                "Use describe_input with a published operation and its returned selection fields.")
        operation = value["operation"]
        root = self._roots.get(operation)
        if root is None:
            return self._reject("OPERATION_UNAVAILABLE", "unavailable",
                                "Select an operation published in this running catalog.")
        offset = int(value.get("offset", 0))
        expected = value.get("expected_catalog")
        if ("selector" in value or offset != 0) and expected is None:
            return self._reject("SELECTION_INVALID", "invalid",
                                "Selected and continued reads require expected_catalog from the first discovery result.")
        if expected is not None and expected != self._catalog_digest:
            return self._reject("CATALOG_CHANGED", "unavailable",
                                "Refresh tools and begin discovery against the running catalog; earlier selections are not reused.")
        selection = value.get("selector", root)
        if selection not in self._ordered_definitions(root):
            return self._reject("SELECTION_INVALID", "invalid",
                                "Select only a definition returned or referenced by this operation's input contract.")
        names = self._ordered_definitions(selection)
        if offset > len(names):
            return self._reject("SELECTION_INVALID", "invalid",
                                "The offset exceeds the selected input-definition closure.")
        limit = int(value.get("limit", INPUT_DISCOVERY_DEFAULT_RECORDS))
        result = {
            "kind": "input-contract-result", "purpose": self._purpose.value,
            "interface_version": self._version, "catalog_digest": self._catalog_digest,
            "operation": operation, "root": root, "selector": selection,
            "dialect": self._dialect, "offset": offset, "total": len(names), "records": [],
        }

        def continuation() -> None:
            end = offset + len(result["records"])
            if end < len(names):
                result["next"] = {
                    "operation": operation, "selector": selection,
                    "expected_catalog": self._catalog_digest, "offset": end, "limit": limit,
                }
            else:
                result.pop("next", None)

        for name in names[offset:offset + limit]:
            result["records"].append({
                "name": name,
                "schema_json": json.dumps(self._definitions[name], sort_keys=True, separators=(",", ":")),
            })
            continuation()
            if len(json.dumps(result).encode("utf-8")) > INPUT_DISCOVERY_RESULT_BYTES:
                result["records"].pop()
                if not result["records"]:
                    return self._reject("RESULT_LIMIT", "unsupported",
                                        "One schema record exceeds the 16 KiB discovery bound. Report this contract as unavailable to this discovery path; no partial schema was returned.")
                break
        continuation()
        if len(json.dumps(result).encode("utf-8")) > INPUT_DISCOVERY_RESULT_BYTES:
            return self._reject("RESULT_LIMIT", "unsupported",
                                "The selected discovery result exceeds the 16 KiB bound; no partial schema was returned.")
        return c.InputContractResult.from_value(result).as_contract()

    def _reject(self, code: str, outcome: str, message: str) -> dict:
        return c.InputContractRejectedResult.from_value({
            "kind": "input-contract-rejected-result", "purpose": self._purpose.value,
            "code": "INPUT_DISCOVERY." + code, "outcome": outcome, "message": message,
        }).as_contract()
