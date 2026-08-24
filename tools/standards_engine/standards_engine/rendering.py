from __future__ import annotations

from typing import Mapping, Protocol


class ContractValue(Protocol):
    def as_contract(self) -> dict[str, object]: ...


def render_text(value: ContractValue | Mapping[str, object]) -> str:
    """Render a deterministic human projection of one typed engine result."""
    contract = value.as_contract() if hasattr(value, "as_contract") else dict(value)
    kind = str(contract.get("kind", "unknown"))
    if kind == "pending-result":
        return _pending(contract)
    if kind == "complete-result":
        return _complete(contract)
    if kind == "analysis-state":
        return _state(contract)
    if kind == "fact-observation":
        return _observation(contract)
    if kind in {"route-result", "read-result", "related-result"}:
        return _navigation(contract)
    if kind == "rejected-result":
        return _rejection(contract)
    return f"RESULT {kind}\n"


def _pending(value: Mapping[str, object]) -> str:
    lines = [f"ANALYSIS {_handle_id(value)}", "STATE needs-action"]
    requirements = _items(value, "fact_requirements")
    obligations = _items(value, "obligations")
    if requirements:
        lines.append("FACT REQUIREMENTS")
        lines.extend(
            f"  {item['handle']['id']} {item['fact']}" for item in requirements
        )
    if obligations:
        lines.append("REVIEWS")
        lines.extend(
            f"  {item['id']} {item['target']} [{item['state']}]" for item in obligations
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
                f"COVERAGE DECISIONS {len(_items(value, 'coverage_decisions'))}",
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
    lines = [f"NAVIGATION {_handle_id(value)}"]
    for item in _items(value, "reading_plan"):
        lines.append(f"  READ {item['target']} [{item['state']}]")
    return "\n".join(lines) + "\n"


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


def _handle_id(value: Mapping[str, object]) -> str:
    return str(_mapping(value.get("handle")).get("id", ""))


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


__all__ = ("render_text",)
