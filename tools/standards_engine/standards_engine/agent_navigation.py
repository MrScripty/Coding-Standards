"""Focused navigation composition over exact Engine snapshot queries."""

from __future__ import annotations

import json

from . import _generated_contract as contract


# This is a serialized result bound, not a total interpreter-memory promise.
READ_MANY_RESULT_BYTES = 2 * 1024 * 1024
# A composed route response includes its reading plan, questions and continuation.
ROUTE_CONTENT_RESULT_BYTES = 2 * 1024 * 1024
ROUTE_CONTENT_DEFAULT_ITEMS = 8


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
    if operation == "route":
        rejection = validate_route_content(engine, arguments)
        if rejection is not None:
            return rejection
        arguments.pop("content", None)
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
            routed = contract.AgentRouteResult.from_value(
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
            return with_route_content(engine, call, handle, compiled, routed)
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
        result = read_selected_item(engine, call.snapshot, compiled, item.as_contract(),
                                    application_view=application_view)
        if isinstance(result, contract.RejectedResult):
            return result
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


def read_selected_item(engine, snapshot, compiled, arguments, *, application_view=None):
    """Use the same exact single-read owner for grouped and routed reads."""
    arguments = dict(arguments)
    detail = arguments.pop("detail", "compact")
    if application_view is not None:
        return application_view.read(arguments["target"], detail)
    return present_read(engine._read(
        snapshot, compiled,
        contract.ReadRequest.from_value({"kind": "read", **arguments}),
    ), detail)


def _route_content_rejection(engine, code, outcome, message):
    from .context_projection import Purpose, application_rejection

    if engine.purpose is Purpose.APPLICATION:
        public_code = "APPLICATION.INPUT_INVALID" if outcome == "invalid" else "APPLICATION.RESULT_LIMIT"
        return application_rejection(public_code, outcome)
    return engine._reject(code, outcome, message)


def validate_route_content(engine, arguments):
    """Check the cross-field continuation contract before capturing authority."""
    selection = arguments.get("content", {})
    if selection.get("offset", 0) and "snapshot" not in arguments:
        return _route_content_rejection(
            engine, "ROUTE.CONTENT_SELECTION", "invalid",
            "A nonzero content offset requires the exact snapshot from the route.",
        )
    return None


def with_route_content(engine, call, snapshot, compiled, routed, *, application_view=None):
    """Compose a bounded selected read page without another capture or compile.

    Results remain private through the final lifecycle check. Byte pressure ends
    a page before a whole record; a single oversized record returns a typed limit
    rejection so the caller can explicitly route without content and read it.
    """
    arguments = call.as_contract()
    if "content" not in arguments:
        return routed
    selection = arguments["content"]
    # JSON Schema integers also admit 1.0. Validation has established whole
    # counts; normalize their Python representation before using slice indices.
    offset = int(selection.get("offset", 0))
    limit = int(selection.get("limit", ROUTE_CONTENT_DEFAULT_ITEMS))
    value = routed.as_contract()
    targets = list(dict.fromkeys(
        entry["target"] for entry in value["reading_plan"] if entry["state"] == "selected"
    ))
    if offset > len(targets):
        return _route_content_rejection(engine, "ROUTE.CONTENT_SELECTION", "invalid",
                                        "The content offset exceeds this route's selected targets.")
    snapshot_id = engine._snapshot_id(snapshot)
    page = {"offset": offset, "total": len(targets), "items": []}
    value["content"] = page
    original_hints = value["next_operations"]

    def continuation():
        end = offset + len(page["items"])
        if end < len(targets):
            page["next"] = {
                "snapshot": snapshot.as_contract(), "facts": arguments["facts"],
                "content": {"offset": end, "limit": limit},
            }
        else:
            page.pop("next", None)
        covered = set(targets[:end])
        value["next_operations"] = [
            hint for hint in original_hints
            if not (hint["operation"] == "read" and hint.get("target") in covered)
        ]

    def too_large():
        return len(json.dumps(value).encode("utf-8")) > ROUTE_CONTENT_RESULT_BYTES

    for target in targets[offset:offset + limit]:
        engine._snapshots.snapshot(snapshot_id)
        result = read_selected_item(engine, snapshot, compiled, {"target": target},
                                    application_view=application_view)
        if isinstance(result, contract.RejectedResult):
            return result
        page["items"].append(result.as_contract())
        continuation()
        if too_large():
            page["items"].pop()
            if not page["items"]:
                return _route_content_rejection(
                    engine, "ROUTE.CONTENT_LIMIT", "unsupported",
                    "The complete routed-content result exceeds 2 MiB. Route without content, then explicitly read a selected item.",
                )
            break
    continuation()
    if too_large():
        return _route_content_rejection(engine, "ROUTE.CONTENT_LIMIT", "unsupported",
                                        "Route without content to inspect this selection.")
    engine._snapshots.snapshot(snapshot_id)
    return type(routed).from_value(value)


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
