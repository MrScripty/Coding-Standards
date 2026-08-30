from __future__ import annotations

import copy
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "tools" / "standards_engine" / "contracts"


def canonical_inputs() -> tuple[dict[str, object], dict[str, object]]:
    schema = json.loads((CONTRACTS / "a1-contract.schema.json").read_text())
    with (CONTRACTS / "a1-interface.toml").open("rb") as selected:
        interface = tomllib.load(selected)
    return schema, interface


def mutated_definition(
    name: str, replacement: dict[str, object]
) -> tuple[dict[str, object], dict[str, object]]:
    schema, interface = canonical_inputs()
    schema["$defs"][name] = copy.deepcopy(replacement)
    return schema, interface
