from __future__ import annotations

import copy
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORTS = ROOT / "docs" / "plans" / "standards-engine-a1b" / "reports"


def canonical_inputs() -> tuple[dict[str, object], dict[str, object]]:
    schema = json.loads((REPORTS / "a1-contract-v11.schema.json").read_text())
    with (REPORTS / "a1-interface-v11.toml").open("rb") as selected:
        interface = tomllib.load(selected)
    return schema, interface


def mutated_definition(
    name: str, replacement: dict[str, object]
) -> tuple[dict[str, object], dict[str, object]]:
    schema, interface = canonical_inputs()
    schema["$defs"][name] = copy.deepcopy(replacement)
    return schema, interface
