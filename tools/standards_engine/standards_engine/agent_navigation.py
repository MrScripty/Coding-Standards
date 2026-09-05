"""Focused navigation composition over exact Engine snapshot queries."""

from __future__ import annotations

from . import _generated_contract as contract


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
                engine._route_value(
                    _QueryProjection.snapshot(handle),
                    compiled,
                    contract.RouteRequest.from_value({"kind": "route", **arguments}),
                    explain=True,
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
    if isinstance(result, contract.ReadResult) and detail == "compact":
        value = result.as_contract()
        del value["related"]
        value.update(kind="compact-read-result", detail="compact")
        return contract.CompactReadResult.from_value(value)
    return result


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
