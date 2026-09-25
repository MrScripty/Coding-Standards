"""Process-owned installed-interface identity and explicit deployment observation.

No repository authority, store, or agent session grants are read or changed here.
A coherent installation is required before process startup. Observation detects
subsequent disk drift; it neither hot-reloads modules nor claims client refresh.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tomllib
import uuid

from tools.standards_contracts.standards_contracts import CompiledContracts, ContractError
from . import _generated_contract as c
from .context_projection import Purpose, application_rejection


INTERFACE_FILES = (
    "tools/standards_engine/contracts/a1-interface.toml",
    "tools/standards_engine/contracts/a1-contract.schema.json",
)


def _digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()
    ).hexdigest()


def _implementation_files(root: Path) -> tuple[Path, ...]:
    # These package roots are the executable installation, not captured standards
    # content. Include new/removed runtime files in the observation as well.
    files = []
    for package in sorted((root / "tools").iterdir()):
        runtime = package / package.name
        if runtime.is_dir():
            files.extend(runtime.rglob("*.py"))
            manifest = package / "pyproject.toml"
            if manifest.is_file():
                files.append(manifest)
    return tuple(sorted(files))


class RuntimeIdentity:
    def __init__(self, root: Path, purpose: Purpose | str,
                 interface: CompiledContracts, catalog: object) -> None:
        self._root = root.resolve()
        self._code_root = Path(__file__).resolve().parents[3]
        self._purpose = Purpose(purpose)
        self._interface = interface
        manifest = self._code_root / "tools/standards_engine/pyproject.toml"
        self._version = tomllib.loads(manifest.read_text())["project"]["version"]
        self._instance = str(uuid.uuid4())
        self._catalog = _digest(catalog)
        self._schema = _digest(interface.schema)
        self._material = self._observe_material()

    def _observe_material(self) -> str:
        records = []
        for path in _implementation_files(self._code_root):
            records.append(("runtime/" + path.relative_to(self._code_root).as_posix(),
                            hashlib.sha256(path.read_bytes()).hexdigest()))
        for relative in INTERFACE_FILES:
            records.append(("interface/" + relative,
                            hashlib.sha256((self._root / relative).read_bytes()).hexdigest()))
        return _digest(records)

    @property
    def implementation_version(self) -> str:
        return self._version

    def metadata(self) -> dict[str, object]:
        return {"instance_id": self._instance,
                "interface_version": self._interface.interface.interface_schema_version,
                "purpose": self._purpose.value, "catalog_digest": self._catalog,
                "schema_digest": self._schema, "implementation_digest": self._material}

    def invoke(self, arguments: object) -> dict[str, object]:
        """Decode through the installed contract, including unknown-field checks."""
        try:
            call = c.RuntimeInfoCall.from_value(arguments)
        except (ContractError, ValueError, TypeError):
            if self._purpose is Purpose.APPLICATION:
                return application_rejection("APPLICATION.INPUT_INVALID", "invalid").as_contract()
            return c.RejectedResult.from_value({
                "kind": "rejected-result", "code": "RUNTIME.INPUT_INVALID", "outcome": "invalid",
                "message": "Supply runtime_info arguments from the installed contract.",
                "details": {}, "next_operations": [],
            }).as_contract()
        expected = call.as_contract().get("expected_catalog")
        client = "unspecified" if expected is None else "matches" if expected == self._catalog else "differs"
        try:
            installation = "current" if self._observe_material() == self._material else "restart-required"
        except OSError:
            installation = "unavailable"
        action = ("check-installation" if installation == "unavailable" else
                  "restart-and-reconnect" if installation == "restart-required" else
                  "refresh-tools" if client == "differs" else "reuse")
        return c.RuntimeInfoResult.from_value({
            "kind": "runtime-info-result", **self.metadata(),
            "implementation_version": self._version,
            "installation_state": installation, "client_catalog_state": client,
            "action": action,
        }).as_contract()
