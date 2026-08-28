from __future__ import annotations

import json
import tomllib
from pathlib import Path

from tools.standards_contracts.standards_contracts import compile_contracts


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-interface.toml"

with INTERFACE_PATH.open("rb") as source:
    _CONTRACTS = compile_contracts(
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        tomllib.load(source),
    )


def validate_contract(definition: str, value: object) -> None:
    _CONTRACTS.validate(definition, value)


__all__ = ("validate_contract",)
