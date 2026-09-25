"""Focused navigation composition over exact Engine snapshot queries."""

from __future__ import annotations

import json

from . import _generated_contract as contract


# This is a serialized result bound, not a total interpreter-memory promise.
READ_MANY_RESULT_BYTES = 2 * 1024 * 1024


def focused_continuations(value):
    """Project native query hints onto the corresponding focused operations."""
    return {
        **value,
        "next_operations": [
            {**item, "operation": item["request_kind"]}
            if item["operation"] == "query"
            else item
            for item in value["next_operations"]
        ],
    }


def navigate(engine, operation: str, call):
    arguments = call.as_contract()
    snapshot = arguments.pop("snapshot", None)
    detail = arguments.pop("detail", "compact")
    if snapshot is None:
        created = engine.create_snapshot(
            contract.CreateSnapshotCall(kind="create-snapshot")
        )
        if isinstance(created, contract.RejectedResult):
            return created
        snapshot = created.as_contract()["snapshot"]["snapshot"]
    if operation == "route":
        from .engine import _QueryProjection

        try:
            handle = contract.SnapshotHandle.from_value(snapshot)
            compiled = engine._compiled_snapshot(engine._snapshot_id(handle))
            return contract.AgentRouteResult.from_value(
                focused_continuations(
                    engine._route_value(
                        _QueryProjection.snapshot(handle),
                        compiled,
                        contract.RouteRequest.from_value(
                            {"kind": "route", **arguments}
                        ),
                        explain=True,
                    )
                )
            )
        except engine._domain_errors() as error:
            return engine._domain_rejection(error)
    result = engine.query(
        contract.QueryCall.from_value(
            {
                "snapshot": snapshot,
                "request": {"kind": operation, **arguments},
            }
        )
    )
    return present_read(result, detail)


def present_read(result, detail):
    """One single-item presentation for independent and grouped reads."""
    value = focused_continuations(result.as_contract())
    if isinstance(result, contract.ReadResult) and detail == "compact":
        del value["related"]
        value.update(kind="compact-read-result", detail="compact")
        return contract.CompactReadResult.from_value(value)
    return type(result).from_value(value)


def read_many(engine, call, compiled, *, application_view=None):
    """Read a bounded requested set from one already-verified immutable input.

    Lifecycle observations remain current throughout the operation. Results stay
    private until the complete ordered set and final lifecycle check succeed.
    The existing domain projection owns each item's content and purpose.
    """
    snapshot_id = engine._snapshot_id(call.snapshot)
    application = application_view is not None
    value = {
        "kind": "application-read-many-result" if application else "read-many-result",
        "snapshot": call.snapshot.as_contract(),
        "items": [],
    }
    if application:
        value["purpose"] = "application"
    # Default JSON separators/escaping match the current MCP text encoding. The
    # fixed envelope's empty array is replaced by these item encodings.
    size = len(json.dumps(value).encode("utf-8"))
    for item in call.items:
        engine._snapshots.snapshot(snapshot_id)
        arguments = item.as_contract()
        detail = arguments.pop("detail", "compact")
        if application:
            result = application_view.read(arguments["target"], detail)
        else:
            result = engine._read(
                call.snapshot, compiled,
                contract.ReadRequest.from_value({"kind": "read", **arguments}),
            )
            if isinstance(result, contract.RejectedResult):
                return result
            result = present_read(result, detail)
        output = result.as_contract()
        size += len(json.dumps(output).encode("utf-8")) + (2 if value["items"] else 0)
        if size > READ_MANY_RESULT_BYTES:
            if application:
                from .context_projection import application_rejection
                return application_rejection("APPLICATION.RESULT_LIMIT", "unsupported")
            return engine._reject(
                "READ_MANY.RESULT_LIMIT", "unsupported",
                "Select fewer items or narrower policy scopes; the complete JSON result is limited to 2 MiB.",
            )
        value["items"].append(output)
    engine._snapshots.snapshot(snapshot_id)
    model = contract.ApplicationReadManyResult if application else contract.ReadManyResult
    return model.from_value(value)


def fact_definitions(router):
    fields = (
        "id",
        "semantic_revision",
        "type",
        "nullable",
        "values",
        "aliases",
        "meaning",
        "prompt",
    )
    result = []
    for fact in router.facts:
        value = {**fact.as_contract(), "values": list(fact.values)}
        result.append({key: value[key] for key in fields})
    return result


def routing_facts(engine, call):
    snapshot = call.as_contract().get("snapshot")
    if snapshot is None:
        created = engine.create_snapshot(
            contract.CreateSnapshotCall(kind="create-snapshot")
        )
        if isinstance(created, contract.RejectedResult):
            return created
        snapshot = created.as_contract()["snapshot"]["snapshot"]
    try:
        handle = contract.SnapshotHandle.from_value(snapshot)
        compiled = engine._compiled_snapshot(engine._snapshot_id(handle))
        return contract.RoutingFactsResult.from_value(
            {
                "kind": "routing-facts-result",
                "snapshot": snapshot,
                "facts": fact_definitions(compiled.router),
            }
        )
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)
