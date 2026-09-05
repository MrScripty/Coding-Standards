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
