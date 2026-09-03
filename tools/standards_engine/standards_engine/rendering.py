from __future__ import annotations

from typing import Callable, Mapping, Protocol


class ContractValue(Protocol):
    def as_contract(self) -> dict[str, object]: ...


def render_text(value: ContractValue | Mapping[str, object]) -> str:
    """Render a deterministic human projection of one typed engine result."""
    contract = value.as_contract() if hasattr(value, "as_contract") else dict(value)
    kind = str(contract.get("kind", "unknown"))
    if kind == "fact-observation":
        return _observation(contract)
    if kind.endswith("-inspection-result"):
        return _inspection(contract)
    renderer = _RESULT_RENDERERS.get(kind)
    if renderer is None:
        raise ValueError(f"unsupported Standards Engine result kind {kind!r}")
    return renderer(contract)


def _pending(value: Mapping[str, object]) -> str:
    lines = [f"ANALYSIS {_handle_id(value)}", "STATE needs-action"]
    requirements = _items(value, "fact_requirements")
    obligations = _items(value, "obligations")
    if requirements:
        lines.append("FACT REQUIREMENTS")
        for item in requirements:
            requirement = _mapping(item.get("requirement"))
            handle = _mapping(requirement.get("handle"))
            lines.append(f"  {handle.get('child_id', '')} {requirement.get('fact', '')}")
    if obligations:
        lines.append("REVIEWS")
        for item in obligations:
            handle = _mapping(item.get("handle"))
            lines.append(
                f"  {handle.get('child_id', '')} {item['target']} [{item['state']}]"
            )
    operations = _items(value, "next_operations")
    if operations:
        lines.append("NEXT")
        lines.extend(
            f"  {item['operation']} {item['request_kind']}" + _operation_target(item)
            for item in operations
        )
    return "\n".join(lines) + "\n"


def _complete(value: Mapping[str, object]) -> str:
    completion = _mapping(value.get("completion"))
    return (
        "\n".join(
            (
                f"ANALYSIS {_handle_id(value)}",
                f"STATE {value['status']}",
                "CONSUMER REVIEWS "
                f"{len(completion.get('reached_consumer_obligations', []))}",
                "FACT OBSERVATIONS "
                f"{len(completion.get('observed_fact_requirements', []))}",
            )
        )
        + "\n"
    )


def _state(value: Mapping[str, object]) -> str:
    return (
        "\n".join(
            (
                f"ANALYSIS STATE {_handle_id(value)}",
                f"OBSERVATIONS {len(_items(value, 'fact_observations'))}",
                f"DISPOSITIONS {len(_items(value, 'dispositions'))}",
                f"COVERAGE ATTESTATIONS {len(_items(value, 'coverage_attestations'))}",
            )
        )
        + "\n"
    )


def _observation(value: Mapping[str, object]) -> str:
    requirement = _mapping(value.get("requirement"))
    fact_value = _mapping(value.get("value"))
    return (
        "\n".join(
            (
                f"FACT OBSERVATION {_handle_id(value)}",
                f"REQUIREMENT {requirement.get('id', '')}",
                f"VALUE {fact_value.get('state', '')}",
            )
        )
        + "\n"
    )


def _navigation(value: Mapping[str, object]) -> str:
    authority = _snapshot_id(value) or _revision_id(value.get("revision"))
    lines = [f"NAVIGATION {authority}"]
    for item in _items(value, "reading_plan"):
        lines.append(f"  READ {item['target']} [{item['state']}]")
    policy = _mapping(value.get("policy"))
    if policy:
        identity = _mapping(policy.get("handle")).get("child_id") or policy.get("id", "")
        lines.append(f"  POLICY {identity}")
    relationships = _items(value, "relationships")
    if relationships:
        lines.append(f"  RELATIONSHIPS {len(relationships)}")
    return "\n".join(lines) + "\n"


def _snapshot_lifecycle(value: Mapping[str, object]) -> str:
    kind = str(value["kind"])
    summaries = _items(value, "snapshots")
    if summaries:
        lines = [f"SNAPSHOTS {len(summaries)}"]
        lines.extend(f"  {_snapshot_id(item)}" for item in summaries)
        return "\n".join(lines) + "\n"
    snapshot = _mapping(value.get("snapshot"))
    return f"{kind.upper()} {_snapshot_id(snapshot or value)}\n"


def _proposal_lifecycle(value: Mapping[str, object]) -> str:
    kind = str(value["kind"])
    proposals = _items(value, "proposals")
    if kind == "find-proposals-result":
        lines = [f"PROPOSALS {len(proposals)}"]
        lines.extend(
            f"  {_proposal_id(item)} {_revision_id(item.get('head_revision'))}"
            for item in proposals
        )
        return "\n".join(lines) + "\n"
    return (
        f"{kind.upper()} {_proposal_id(value)} "
        f"{_revision_id(value.get('revision'))}\n"
    )


def _rejection(value: Mapping[str, object]) -> str:
    return (
        "\n".join(
            (
                f"REJECTED {value.get('code', '')}",
                f"OUTCOME {value.get('outcome', '')}",
                f"MESSAGE {value.get('message', '')}",
            )
        )
        + "\n"
    )


def _inspection(value: Mapping[str, object]) -> str:
    kind = str(value["kind"])
    artifact_fields = tuple(key for key in value if key != "kind")
    return f"INSPECTION {kind} {' '.join(artifact_fields)}\n"


def _handle_id(value: Mapping[str, object]) -> str:
    return str(_mapping(value.get("handle")).get("id", ""))


def _snapshot_id(value: Mapping[str, object]) -> str:
    snapshot = _mapping(value.get("snapshot"))
    if snapshot.get("kind") == "snapshot-handle":
        return str(snapshot.get("id", ""))
    nested = _mapping(snapshot.get("snapshot"))
    return str(nested.get("id", ""))


def _proposal_id(value: Mapping[str, object]) -> str:
    return str(_mapping(value.get("proposal")).get("id", ""))


def _revision_id(value: object) -> str:
    return str(_mapping(value).get("id", ""))


def _items(
    value: Mapping[str, object],
    key: str,
) -> tuple[Mapping[str, object], ...]:
    selected = value.get(key, ())
    if not isinstance(selected, (list, tuple)):
        return ()
    return tuple(_mapping(item) for item in selected)


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _operation_target(value: Mapping[str, object]) -> str:
    target = value.get("target")
    return "" if target is None else f" {target}"


_RESULT_RENDERERS: dict[
    str,
    Callable[[Mapping[str, object]], str],
] = {
    "pending-result": _pending,
    "complete-result": _complete,
    "analysis-state": _state,
    "create-snapshot-result": _snapshot_lifecycle,
    "find-snapshots-result": _snapshot_lifecycle,
    "delete-snapshot-result": _snapshot_lifecycle,
    "undelete-snapshot-result": _snapshot_lifecycle,
    "create-proposal-result": _proposal_lifecycle,
    "find-proposals-result": _proposal_lifecycle,
    "revise-proposal-result": _proposal_lifecycle,
    "route-result": _navigation,
    "read-result": _navigation,
    "related-result": _navigation,
    "proposal-route-result": _navigation,
    "proposal-read-result": _navigation,
    "proposal-related-result": _navigation,
    "rejected-result": _rejection,
}


__all__ = ("render_text",)
