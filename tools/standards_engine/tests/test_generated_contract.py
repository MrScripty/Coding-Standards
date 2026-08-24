from __future__ import annotations

import json
import subprocess
import sys
import unittest
from dataclasses import fields
from pathlib import Path

from tools.standards_engine.standards_engine import _generated_contract as generated


REPO_ROOT = Path(__file__).resolve().parents[3]


class GeneratedContractTest(unittest.TestCase):
    def test_generated_contract_projections_are_current(self) -> None:
        completed = subprocess.run(
            (
                sys.executable,
                "tools/standards_engine/contracts/generate_contract.py",
                "--check",
            ),
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)

    def test_generated_python_algebra_exhaustively_matches_schema_variants(
        self,
    ) -> None:
        schema = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected_results = {
            node["properties"]["kind"]["const"]: name
            for name, node in schema["$defs"].items()
            if isinstance(node, dict)
            and isinstance(node.get("properties", {}).get("kind", {}).get("const"), str)
            and (
                node["properties"]["kind"]["const"].endswith("-result")
                or node["properties"]["kind"]["const"] == "analysis-state"
            )
        }
        self.assertEqual(dict(generated.RESULT_KIND_TO_DEFINITION), expected_results)

        for name, contract in generated.REQUEST_FIELDS.items():
            with self.subTest(request=name):
                request_type = getattr(generated, name)
                self.assertEqual(
                    {field.name for field in fields(request_type)},
                    set(contract["properties"]),
                )

    def test_generated_agent_tools_expose_every_public_operation(self) -> None:
        value = json.loads(
            (
                REPO_ROOT
                / "tools/standards_engine/contracts/generated/agent-tools.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            {item["name"] for item in value["tools"]},
            {f"standards_{name}" for name in generated.PUBLIC_OPERATIONS},
        )


if __name__ == "__main__":
    unittest.main()
