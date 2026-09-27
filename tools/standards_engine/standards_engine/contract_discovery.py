"""Bounded contract observation for one installed, purpose-qualified catalog.

Schema documents are data. Canonical validation and shared structural traversal
own their semantics; this observer owns selection, whole-record paging and
catalog binding, independently of standards state and transport sessions.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Collection
import hashlib
import json
from typing import Literal

from tools.standards_contracts.standards_contracts import (
    CompiledContracts, ContractError, direct_schema_references,
    local_definition_name, schema_closure,
)

from . import _generated_contract as c
from .context_projection import Purpose, qualified_operations


DISCOVERY_DEFAULT_RECORDS = 8
DISCOVERY_RESULT_BYTES = 16 * 1024
OUTPUT_SCHEMA_DIGEST_KEY = "standards-engine/output-schema-digest"


def output_schema_root(result_definitions: Collection[str]) -> dict:
    """The complete operation result algebra, excluding its local definitions."""
    return {"type": "object", "oneOf": [
        {"$ref": f"#/$defs/{name}"} for name in result_definitions
    ]}


def operation_output_schema(operation: dict, definitions: dict) -> dict:
    """One exact schema for eager advertisement and on-demand reconstruction."""
    return schema_closure(output_schema_root(operation["result_definitions"]), definitions)


def output_schema_digest(schema: dict) -> str:
    """Bind the full schema even when its bytes are absent from a catalog."""
    content = json.dumps(schema, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


class ContractDiscovery:
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
        self._operations = {
            operation["id"]: operation
            for operation in qualified_operations(projection, self._purpose)
            if operation["id"] in published
        }

    def _ordered_definitions(self, roots: Collection[str]) -> list[str]:
        """Visit containing shapes first; recursive definition graphs terminate."""
        pending = deque(roots)
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

    def invoke(self, arguments: object, *, direction: Literal["input", "output"] = "input") -> dict:
        # This selector is owned by the named public operation, not caller data.
        if direction == "input":
            call_type, result_type = c.DescribeInputCall, c.InputContractResult
        elif direction == "output":
            call_type, result_type = c.DescribeOutputCall, c.OutputContractResult
        else:
            raise ValueError("Unknown contract direction.")
        try:
            value = call_type.from_value(arguments).as_contract()
        except (ContractError, ValueError, TypeError) as error:
            from .input_feedback import feedback_value
            result = self._reject(direction, "INVALID_ARGUMENTS", "invalid",
                                  f"Use describe_{direction} with a published operation and its returned selection fields.")
            result["input_feedback"] = feedback_value(f"describe_{direction}", getattr(error, "failure", None))
            rejected = c.InputContractRejectedResult if direction == "input" else c.OutputContractRejectedResult
            return rejected.from_value(result).as_contract()
        operation = self._operations.get(value["operation"])
        if operation is None:
            return self._reject(direction, "OPERATION_UNAVAILABLE", "unavailable",
                                "Select an operation published in this running catalog.")
        offset = int(value.get("offset", 0))
        expected = value.get("expected_catalog")
        if ("selector" in value or offset != 0) and expected is None:
            return self._reject(direction, "SELECTION_INVALID", "invalid",
                                "Selected and continued reads require expected_catalog from the first discovery result.")
        if expected is not None and expected != self._catalog_digest:
            return self._reject(direction, "CATALOG_CHANGED", "unavailable",
                                "Refresh tools and begin discovery against the running catalog; earlier selections are not reused.")
        roots = ([operation["input_definition"]] if direction == "input"
                 else operation["result_definitions"])
        selection = value.get("selector", roots[0] if direction == "input" else None)
        if selection is not None and selection not in self._ordered_definitions(roots):
            return self._reject(direction, "SELECTION_INVALID", "invalid",
                                f"Select only a definition returned or referenced by this operation's {direction} contract.")
        names = self._ordered_definitions([selection] if selection is not None else roots)
        if offset > len(names):
            return self._reject(direction, "SELECTION_INVALID", "invalid",
                                f"The offset exceeds the selected {direction}-definition closure.")
        limit = int(value.get("limit", DISCOVERY_DEFAULT_RECORDS))
        result = {
            "kind": f"{direction}-contract-result", "purpose": self._purpose.value,
            "interface_version": self._version, "catalog_digest": self._catalog_digest,
            "operation": value["operation"], "dialect": self._dialect,
            "offset": offset, "total": len(names), "records": [],
        }
        if selection is not None:
            result["selector"] = selection
        if direction == "input":
            result["root"] = roots[0]
        else:
            result.update(roots=list(roots),
                          root_schema_json=json.dumps(output_schema_root(roots), sort_keys=True, separators=(",", ":")),
                          schema_digest=output_schema_digest(operation_output_schema(operation, self._definitions)))

        def continuation() -> None:
            end = offset + len(result["records"])
            if end < len(names):
                result["next"] = {
                    "operation": value["operation"], "expected_catalog": self._catalog_digest,
                    "offset": end, "limit": limit,
                    **({"selector": selection} if selection is not None else {}),
                }
            else:
                result.pop("next", None)

        for name in names[offset:offset + limit]:
            result["records"].append({
                "name": name,
                "schema_json": json.dumps(self._definitions[name], sort_keys=True, separators=(",", ":")),
            })
            continuation()
            if len(json.dumps(result).encode("utf-8")) > DISCOVERY_RESULT_BYTES:
                result["records"].pop()
                if not result["records"]:
                    return self._reject(direction, "RESULT_LIMIT", "unsupported",
                                        "One schema record exceeds the 16 KiB discovery bound. Report this contract as unavailable to this discovery path; no partial schema was returned.")
                break
        continuation()
        if len(json.dumps(result).encode("utf-8")) > DISCOVERY_RESULT_BYTES:
            return self._reject(direction, "RESULT_LIMIT", "unsupported",
                                "The selected discovery result exceeds the 16 KiB bound; no partial schema was returned.")
        return result_type.from_value(result).as_contract()

    def _reject(self, direction: str, code: str, outcome: str, message: str) -> dict:
        model = c.InputContractRejectedResult if direction == "input" else c.OutputContractRejectedResult
        return model.from_value({
            "kind": f"{direction}-contract-rejected-result", "purpose": self._purpose.value,
            "code": direction.upper() + "_DISCOVERY." + code, "outcome": outcome, "message": message,
        }).as_contract()
