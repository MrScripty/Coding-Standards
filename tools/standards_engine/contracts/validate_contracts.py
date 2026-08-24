#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "a1-contract.schema.json"
EXAMPLES_PATH = ROOT / "examples" / "a1-examples.json"
IDENTITIES_PATH = ROOT / "identity-fixtures.json"

SCHEMA_KEYS = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "title",
    "description",
    "type",
    "const",
    "enum",
    "oneOf",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minItems",
    "uniqueItems",
    "minLength",
    "pattern",
    "minimum",
}

IDENTITY_PREFIX = {
    "coding-standards:snapshot:v1": "snapshot",
    "coding-standards:navigation:v1": "navigation",
    "coding-standards:packet:v2": "packet",
    "coding-standards:obligation:v2": "obligation",
    "coding-standards:analysis-report:v1": "analysis-report",
    "coding-standards:coverage-authority-view:v1": "coverage-view",
    "coding-standards:coverage-audit-requirement:v1": "coverage-requirement",
    "coding-standards:coverage-attestation:v1": "coverage-attestation",
    "coding-standards:consumer-coverage-certificate:v1": "certificate",
}


class ContractError(ValueError):
    pass


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object)
    except (OSError, json.JSONDecodeError, ContractError) as error:
        raise ContractError(f"{path}: {error}") from error


def check_schema_node(node: dict[str, Any], path: str) -> None:
    for key in node:
        if key not in SCHEMA_KEYS and not key.startswith("x-standards-engine-"):
            raise ContractError(f"{path}: unsupported schema keyword {key!r}")

    for name, definition in node.get("$defs", {}).items():
        if not isinstance(definition, dict):
            raise ContractError(f"{path}/$defs/{name}: definition must be an object")
        check_schema_node(definition, f"{path}/$defs/{name}")
    for name, definition in node.get("properties", {}).items():
        if not isinstance(definition, dict):
            raise ContractError(f"{path}/properties/{name}: property schema must be an object")
        check_schema_node(definition, f"{path}/properties/{name}")
    for index, definition in enumerate(node.get("oneOf", [])):
        if not isinstance(definition, dict):
            raise ContractError(f"{path}/oneOf/{index}: variant must be an object")
        check_schema_node(definition, f"{path}/oneOf/{index}")
    items = node.get("items")
    if isinstance(items, dict):
        check_schema_node(items, f"{path}/items")
    additional = node.get("additionalProperties")
    if isinstance(additional, dict):
        check_schema_node(additional, f"{path}/additionalProperties")


def resolve(schema_root: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    seen: set[str] = set()
    while "$ref" in node:
        reference = node["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/$defs/"):
            raise ContractError(f"unsupported schema reference: {reference!r}")
        if reference in seen:
            raise ContractError(f"schema reference cycle without a value boundary: {reference}")
        seen.add(reference)
        name = reference.removeprefix("#/$defs/")
        try:
            node = schema_root["$defs"][name]
        except KeyError as error:
            raise ContractError(f"unknown schema definition: {name}") from error
    return node


def _is_type(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def canonical_value(value: Any) -> Any:
    if isinstance(value, float):
        raise ContractError("floating point values are prohibited in canonical identity data")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [canonical_value(item) for item in value]
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for raw_key, item in value.items():
            if not isinstance(raw_key, str):
                raise ContractError("canonical JSON object keys must be strings")
            key = unicodedata.normalize("NFC", raw_key)
            if key in normalized:
                raise ContractError(f"Unicode normalization creates duplicate key {key!r}")
            normalized[key] = canonical_value(item)
        return normalized
    if value is None or isinstance(value, (bool, int)):
        return value
    raise ContractError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_value(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def validate(schema_root: dict[str, Any], node: dict[str, Any], value: Any, path: str) -> None:
    node = resolve(schema_root, node)

    variants = node.get("oneOf")
    if variants is not None:
        accepted = 0
        failures: list[str] = []
        for variant in variants:
            try:
                validate(schema_root, variant, value, path)
            except ContractError as error:
                failures.append(str(error))
            else:
                accepted += 1
        if accepted != 1:
            detail = failures[0] if failures else "multiple variants accepted the value"
            raise ContractError(f"{path}: oneOf matched {accepted} variants; {detail}")

    if "const" in node and canonical_bytes(value) != canonical_bytes(node["const"]):
        raise ContractError(f"{path}: expected constant {node['const']!r}, got {value!r}")
    if "enum" in node and not any(
        canonical_bytes(value) == canonical_bytes(candidate) for candidate in node["enum"]
    ):
        raise ContractError(f"{path}: {value!r} is not in {node['enum']!r}")

    expected_type = node.get("type")
    if expected_type is not None:
        if expected_type not in {"object", "array", "string", "integer", "boolean", "null"}:
            raise ContractError(f"{path}: unsupported type {expected_type!r}")
        if not _is_type(value, expected_type):
            raise ContractError(f"{path}: expected {expected_type}, got {type(value).__name__}")

    if isinstance(value, str):
        if len(value) < node.get("minLength", 0):
            raise ContractError(f"{path}: string is shorter than minLength")
        pattern = node.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            raise ContractError(f"{path}: {value!r} does not match {pattern!r}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in node and value < node["minimum"]:
            raise ContractError(f"{path}: {value} is below minimum {node['minimum']}")

    if isinstance(value, list):
        if len(value) < node.get("minItems", 0):
            raise ContractError(f"{path}: array is shorter than minItems")
        if node.get("uniqueItems"):
            encoded = [canonical_bytes(item) for item in value]
            if len(set(encoded)) != len(encoded):
                raise ContractError(f"{path}: array items are not unique")
        item_schema = node.get("items")
        if item_schema is not None:
            for index, item in enumerate(value):
                validate(schema_root, item_schema, item, f"{path}/{index}")

    if isinstance(value, dict):
        required = node.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise ContractError(f"{path}: missing required fields {missing!r}")
        properties = node.get("properties", {})
        for key, item in value.items():
            if key in properties:
                validate(schema_root, properties[key], item, f"{path}/{key}")
                continue
            additional = node.get("additionalProperties", True)
            if additional is False:
                raise ContractError(f"{path}: unexpected field {key!r}")
            if isinstance(additional, dict):
                validate(schema_root, additional, item, f"{path}/{key}")


def schema_for_path(schema_root: dict[str, Any], definition: str, dotted_path: str) -> dict[str, Any]:
    node = resolve(schema_root, schema_root["$defs"][definition])
    for part in dotted_path.split("."):
        node = resolve(schema_root, node)
        properties = node.get("properties", {})
        if part not in properties:
            raise ContractError(
                f"{definition}: identity path {dotted_path!r} does not resolve at {part!r}"
            )
        node = properties[part]
    return resolve(schema_root, node)


def value_at_path(value: Any, dotted_path: str) -> Any:
    selected = value
    for part in dotted_path.split("."):
        if not isinstance(selected, dict) or part not in selected:
            raise ContractError(f"identity value does not contain path {dotted_path!r}")
        selected = selected[part]
    return selected


def set_at_path(target: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = dotted_path.split(".")
    selected = target
    for part in parts[:-1]:
        selected = selected.setdefault(part, {})
    selected[parts[-1]] = value


def selected_identity_value(value: dict[str, Any], annotation: dict[str, Any]) -> dict[str, Any]:
    selected: dict[str, Any] = {}
    for path in annotation["include"]:
        set_at_path(selected, path, copy.deepcopy(value_at_path(value, path)))
    return selected


def identity(schema_root: dict[str, Any], definition: str, value: dict[str, Any]) -> str:
    node = resolve(schema_root, schema_root["$defs"][definition])
    annotation = node.get("x-standards-engine-identity")
    if not isinstance(annotation, dict):
        raise ContractError(f"{definition}: no identity annotation")
    domain = annotation.get("domain")
    if domain not in IDENTITY_PREFIX:
        raise ContractError(f"{definition}: unknown identity domain {domain!r}")
    digest = hashlib.sha256(
        domain.encode("utf-8") + b"\0" + canonical_bytes(selected_identity_value(value, annotation))
    ).hexdigest()
    return f"{IDENTITY_PREFIX[domain]}:sha256:{digest}"


def pointer(value: Any, raw_pointer: str | None) -> Any:
    if raw_pointer is None:
        return value
    if not raw_pointer.startswith("/"):
        raise ContractError(f"invalid value pointer {raw_pointer!r}")
    selected = value
    for raw_part in raw_pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(selected, list):
            selected = selected[int(part)]
        elif isinstance(selected, dict):
            selected = selected[part]
        else:
            raise ContractError(f"value pointer {raw_pointer!r} crosses a scalar")
    return selected


def changed_value(value: Any) -> Any:
    if isinstance(value, str):
        return value + ":display-change"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, list):
        return value + ["display-change"]
    if isinstance(value, dict):
        changed = copy.deepcopy(value)
        changed["display_change"] = True
        return changed
    if value is None:
        return "display-change"
    raise ContractError(f"cannot mutate excluded value of type {type(value).__name__}")


def mutate_path(value: dict[str, Any], dotted_path: str) -> dict[str, Any]:
    changed = copy.deepcopy(value)
    parts = dotted_path.split(".")
    selected: Any = changed
    for part in parts[:-1]:
        selected = selected[part]
    selected[parts[-1]] = changed_value(selected[parts[-1]])
    return changed


def validate_identity_annotations(schema_root: dict[str, Any]) -> None:
    for name, raw_node in schema_root["$defs"].items():
        node = resolve(schema_root, raw_node)
        annotation = node.get("x-standards-engine-identity")
        if annotation is None:
            continue
        if set(annotation) != {"domain", "include", "exclude"}:
            raise ContractError(f"{name}: identity annotation must contain domain, include, and exclude")
        if annotation["domain"] not in IDENTITY_PREFIX:
            raise ContractError(f"{name}: unsupported identity domain")
        include = annotation["include"]
        exclude = annotation["exclude"]
        if not include or len(set(include)) != len(include) or len(set(exclude)) != len(exclude):
            raise ContractError(f"{name}: identity paths must be non-empty and unique")
        if set(include) & set(exclude):
            raise ContractError(f"{name}: identity include and exclude paths overlap")
        for path in (*include, *exclude):
            schema_for_path(schema_root, name, path)
        if "id" in include or "handle" in include or "handle.id" in include:
            raise ContractError(f"{name}: identity includes its own identity-bearing handle")


def validate_contract_metadata(schema_root: dict[str, Any]) -> None:
    metadata = schema_root.get("x-standards-engine-contract")
    if not isinstance(metadata, dict):
        raise ContractError("root contract metadata is missing")
    definitions = schema_root["$defs"]
    for operation, contract in metadata["public_operations"].items():
        if contract["input"] not in definitions:
            raise ContractError(f"{operation}: unknown input definition {contract['input']}")
        for name in contract["results"]:
            if name not in definitions:
                raise ContractError(f"{operation}: unknown result definition {name}")
    if metadata["authorization_context"]["caller_authored"] is not False:
        raise ContractError("authorization context must not be caller-authored")
    bootstrap = metadata["snapshot_bootstrap"]
    if bootstrap["caller_authored"] is not False or bootstrap["ambient_fallback"] is not False:
        raise ContractError("snapshot bootstrap must be trusted and have no ambient fallback")
    if bootstrap["result"] not in definitions:
        raise ContractError("snapshot bootstrap result definition is unknown")
    submission_kinds = {
        resolve(schema_root, variant)["properties"]["kind"]["const"]
        for variant in definitions["Submission"]["oneOf"]
    }
    mapped_submission_kinds = set(
        metadata["public_operations"]["resolve"]["capability_by_submission"]
    )
    if submission_kinds != mapped_submission_kinds:
        raise ContractError("resolve capability mapping does not cover the exact Submission variants")
    groups = metadata["impact_graph_groups"]
    allowed = {"policy-impact", "standards-requires", "standards-specializes"}
    for change_kind, selections in groups.items():
        for snapshot_kind in ("accepted", "proposed"):
            selected = selections[snapshot_kind]
            if len(set(selected)) != len(selected) or not set(selected).issubset(allowed):
                raise ContractError(f"{change_kind}: invalid graph group selection")


def validate_completion_examples(examples: dict[str, dict[str, Any]]) -> None:
    for name, example in examples.items():
        if example["definition"] != "CompletedAnalysisReport":
            continue
        completion = example["value"]["completion"]
        required_coverage = set(completion["required_coverage_subjects"])
        certificate_subjects = set(completion["certificate_subjects"])
        if required_coverage != certificate_subjects:
            raise ContractError(f"{name}: completion coverage subject sets differ")
        reached = set(completion["reached_consumer_obligations"])
        disposed = set(completion["disposition_obligations"])
        if reached != disposed:
            raise ContractError(f"{name}: completion obligation sets differ")
        records = example["value"]["dispositions"]
        record_ids = [record["obligation_id"] for record in records if record["kind"] == "consumer-disposition"]
        if len(record_ids) != len(set(record_ids)) or set(record_ids) != disposed:
            raise ContractError(f"{name}: disposition records do not prove exact completion")
        if any(record["result"] == "blocked" for record in records):
            raise ContractError(f"{name}: blocked disposition cannot complete")
        certificate_handles = example["value"]["coverage_certificates"]
        if len(certificate_handles) != len(certificate_subjects):
            raise ContractError(f"{name}: certificate handles do not prove exact coverage")


def validate_change(change: dict[str, Any], owner: str) -> None:
    kind = change["kind"]
    accepted = change["accepted_ids"]
    proposed = change["proposed_ids"]
    valid = {
        "modification": len(accepted) == 1 and accepted == proposed,
        "addition": not accepted and len(proposed) == 1,
        "removal": len(accepted) == 1 and not proposed,
        "move": len(accepted) == 1 and accepted == proposed,
        "split": len(accepted) == 1 and len(proposed) >= 2,
        "merge": len(accepted) >= 2 and len(proposed) == 1,
    }[kind]
    if not valid:
        raise ContractError(f"{owner}: {kind} violates its accepted/proposed identity cardinality")
    if kind == "addition" and "accepted_module" in change:
        raise ContractError(f"{owner}: addition cannot claim an accepted module")
    if kind == "removal" and "proposed_module" in change:
        raise ContractError(f"{owner}: removal cannot claim a proposed module")
    if kind not in {"addition"} and "accepted_module" not in change:
        raise ContractError(f"{owner}: {kind} requires accepted_module")
    if kind not in {"removal"} and "proposed_module" not in change:
        raise ContractError(f"{owner}: {kind} requires proposed_module")


def validate_change_examples(examples: dict[str, dict[str, Any]]) -> None:
    observed: set[str] = set()
    for name, example in examples.items():
        definition = example["definition"]
        value = example["value"]
        if definition == "ChangeDescriptor":
            validate_change(value, name)
            observed.add(value["kind"])
        elif definition == "AnalysisRequest":
            for change in value["changes"]:
                validate_change(change, name)
        elif definition in {"PendingPacket", "CompletedAnalysisReport"}:
            for change in value["changes"]:
                validate_change(change, name)
    expected = {"modification", "addition", "removal", "move", "split", "merge"}
    if observed != expected:
        raise ContractError(f"change examples do not cover every variant: {sorted(expected - observed)}")


def validate_operation_calls(schema: dict[str, Any], examples: dict[str, dict[str, Any]]) -> None:
    route_result = examples["route-result"]["value"]
    pending = examples["pending-packet"]["value"]
    calls = {
        "QueryCall": {
            "snapshot": route_result["handle"]["snapshot"],
            "request": examples["route-request"]["value"],
        },
        "PrepareCall": {"request": examples["analysis-request"]["value"]},
        "ResolveCall": {
            "packet": pending["handle"],
            "submission": examples["consumer-disposition"]["value"],
        },
        "InspectCall": {"handle": pending["handle"]},
    }
    for definition, value in calls.items():
        validate(schema, schema["$defs"][definition], value, f"operation:{definition}")


def expect_rejection(action: Any, label: str) -> None:
    try:
        action()
    except ContractError:
        return
    raise ContractError(f"negative self-check unexpectedly accepted {label}")


def run_negative_self_checks(schema: dict[str, Any], examples: dict[str, dict[str, Any]]) -> None:
    expect_rejection(
        lambda: check_schema_node({"type": "string", "unknownKeyword": True}, "negative"),
        "unknown schema keyword",
    )
    expect_rejection(lambda: _object([("key", 1), ("key", 2)]), "duplicate JSON key")

    route = copy.deepcopy(examples["route-request"]["value"])
    del route["kind"]
    expect_rejection(
        lambda: validate(schema, schema["$defs"]["RouteRequest"], route, "negative:route"),
        "missing route discriminator",
    )

    fact = {"type": "boolean", "state": "known", "value": "true"}
    expect_rejection(
        lambda: validate(schema, schema["$defs"]["FactValue"], fact, "negative:fact"),
        "type-incompatible applicability fact",
    )

    handle = {
        "kind": "snapshot-handle",
        "id": "packet:sha256:" + "0" * 64,
        "schema_version": 1,
    }
    expect_rejection(
        lambda: validate(schema, schema["$defs"]["SnapshotHandle"], handle, "negative:handle"),
        "cross-domain handle identity",
    )

    boolean_version = {
        "kind": "snapshot-handle",
        "id": "snapshot:sha256:" + "0" * 64,
        "schema_version": True,
    }
    expect_rejection(
        lambda: validate(
            schema,
            schema["$defs"]["SnapshotHandle"],
            boolean_version,
            "negative:boolean-version",
        ),
        "Boolean accepted as integer constant",
    )

    invalid_change = copy.deepcopy(examples["change-addition"]["value"])
    invalid_change["accepted_ids"] = ["workflow.verification.existing"]
    expect_rejection(
        lambda: validate_change(invalid_change, "negative:change"),
        "invalid change identity cardinality",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Standards Engine A1 contract")
    parser.add_argument("--print-identities", action="store_true")
    args = parser.parse_args()

    try:
        schema = load_json(SCHEMA_PATH)
        check_schema_node(schema, "#")
        validate_identity_annotations(schema)
        validate_contract_metadata(schema)

        example_document = load_json(EXAMPLES_PATH)
        if example_document.get("schema_version") != 1:
            raise ContractError("example schema_version must be 1")
        examples: dict[str, dict[str, Any]] = {}
        for entry in example_document.get("examples", []):
            name = entry.get("name")
            definition = entry.get("definition")
            if not isinstance(name, str) or name in examples:
                raise ContractError(f"invalid or duplicate example name {name!r}")
            if definition not in schema["$defs"]:
                raise ContractError(f"{name}: unknown definition {definition!r}")
            validate(schema, schema["$defs"][definition], entry.get("value"), f"example:{name}")
            examples[name] = entry
        validate_completion_examples(examples)
        validate_change_examples(examples)
        validate_operation_calls(schema, examples)
        run_negative_self_checks(schema, examples)

        identity_document = load_json(IDENTITIES_PATH)
        if identity_document.get("schema_version") != 1:
            raise ContractError("identity fixture schema_version must be 1")
        seen: set[str] = set()
        outputs: list[tuple[str, str]] = []
        for fixture in identity_document.get("fixtures", []):
            name = fixture.get("name")
            if not isinstance(name, str) or name in seen:
                raise ContractError(f"invalid or duplicate identity fixture name {name!r}")
            seen.add(name)
            definition = fixture.get("definition")
            example_name = fixture.get("example")
            if definition not in schema["$defs"] or example_name not in examples:
                raise ContractError(f"{name}: unknown definition or example")
            value = pointer(examples[example_name]["value"], fixture.get("value_pointer"))
            validate(schema, schema["$defs"][definition], value, f"identity:{name}")
            observed = identity(schema, definition, value)
            outputs.append((name, observed))
            if not args.print_identities and observed != fixture.get("expected"):
                raise ContractError(
                    f"{name}: identity mismatch; expected {fixture.get('expected')!r}, got {observed!r}"
                )

            annotation = resolve(schema, schema["$defs"][definition])["x-standards-engine-identity"]
            for excluded in annotation["exclude"]:
                changed = mutate_path(value, excluded)
                if identity(schema, definition, changed) != observed:
                    raise ContractError(f"{name}: excluded field {excluded!r} changes identity")
            for included in annotation["include"]:
                changed = mutate_path(value, included)
                if identity(schema, definition, changed) == observed:
                    raise ContractError(f"{name}: included field {included!r} does not change identity")

        if args.print_identities:
            for name, observed in outputs:
                print(f"{name}\t{observed}")
        else:
            print(
                f"PASS: {len(examples)} examples, {len(outputs)} identity fixtures, "
                f"4 operation envelopes, {len(schema['$defs'])} definitions"
            )
        return 0
    except (ContractError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
