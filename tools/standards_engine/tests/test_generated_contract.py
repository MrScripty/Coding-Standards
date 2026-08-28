from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

from tools.standards_contracts.standards_contracts import compile_contracts
from tools.standards_engine.contracts import generate_contract
from tools.standards_engine.standards_engine import _generated_contract as generated


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-interface.toml"


def _canonical_contracts() -> tuple[dict[str, object], dict[str, object]]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with INTERFACE_PATH.open("rb") as source:
        interface = tomllib.load(source)
    return schema, interface


class GeneratedContractTest(unittest.TestCase):
    def test_generated_contract_projections_are_current(self) -> None:
        completed = subprocess.run(
            (
                sys.executable,
                "-P",
                str(REPO_ROOT / "tools/standards_engine/contracts/generate_contract.py"),
                "--check",
            ),
            cwd=Path("/tmp"),
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPATH": str(REPO_ROOT),
            },
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)

    def test_compiler_owns_the_complete_public_definition_closure(self) -> None:
        schema, interface = _canonical_contracts()
        compiled = compile_contracts(schema, interface)

        self.assertEqual(set(compiled.reachable_definitions), set(schema["$defs"]))
        self.assertEqual(
            set(generated.DEFINITION_METADATA),
            set(compiled.reachable_definitions),
        )
        projections = generate_contract.render_projections()
        for path, projection in projections.items():
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertEqual(path.read_text(encoding="utf-8"), projection)

    def test_generated_native_models_decode_complete_v11_values(self) -> None:
        request_value = {"kind": "read", "target": "workflow.planning"}
        request = generated.decode_contract("QueryRequest", request_value)
        self.assertIsInstance(request, generated.ReadRequest)
        self.assertEqual(request.as_contract(), request_value)

        result_value = {
            "kind": "rejected-result",
            "code": "AUTHORITY.UNAVAILABLE",
            "outcome": "unavailable",
            "message": "The requested immutable authority is unavailable.",
            "details": {},
            "next_operations": [],
        }
        result = generated.decode_contract("RejectedResult", result_value)
        self.assertIsInstance(result, generated.RejectedResult)
        self.assertEqual(result.as_contract(), result_value)

        with self.assertRaises(ValueError):
            generated.ReadRequest.from_value({"kind": "read"})

    def test_agent_tools_are_the_exact_compiler_projection(self) -> None:
        tools_path = (
            REPO_ROOT
            / "tools/standards_engine/contracts/generated/agent-tools.json"
        )
        projected = generate_contract.render_projections()[tools_path]
        self.assertEqual(tools_path.read_text(encoding="utf-8"), projected)

    def test_authored_v11_examples_satisfy_the_public_contract(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(
            corpus["interface_schema_version"],
            contracts.interface.interface_schema_version,
        )
        names = [example["name"] for example in corpus["examples"]]
        self.assertTrue(names)
        self.assertEqual(len(names), len(set(names)))
        for example in corpus["examples"]:
            with self.subTest(example=example["name"]):
                self.assertEqual(set(example), {"name", "definition", "value"})
                contracts.validate(example["definition"], example["value"])

    def test_identity_fixtures_use_valid_public_v11_handles(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/identity-fixtures.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(corpus["identity_encoding_version"], 2)
        for fixture in corpus["domains"]:
            public_handle = fixture.get("public_handle")
            if public_handle is None:
                continue
            with self.subTest(domain=fixture["name"]):
                contracts.validate(
                    public_handle["definition"],
                    {
                        "kind": public_handle["kind"],
                        "id": fixture["expected"],
                        "schema_version": 4,
                    },
                )


if __name__ == "__main__":
    unittest.main()
