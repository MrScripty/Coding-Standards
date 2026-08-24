from __future__ import annotations

import json
import copy
import subprocess
import sys
import unittest
from dataclasses import fields
from pathlib import Path
from typing import get_type_hints

from tools.standards_engine.contracts import generate_contract
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

        expected_inputs = {
            name: schema["$defs"][name]
            for name in generate_contract._input_definitions(schema)
        }
        self.assertEqual(
            dict(generated.INPUT_DEFINITION_SCHEMAS),
            expected_inputs,
        )
        for name, contract_names in generated.INPUT_FIELD_NAMES.items():
            with self.subTest(definition=name):
                request_type = getattr(generated, name)
                self.assertEqual(
                    {field.name for field in fields(request_type)},
                    set(contract_names.values()),
                )

        analysis_hints = get_type_hints(generated.AnalysisRequest)
        resolve_hints = get_type_hints(generated.ResolveCall)
        self.assertEqual(
            analysis_hints["changes"],
            tuple[generated.ChangeDescriptor, ...],
        )
        self.assertEqual(
            analysis_hints["semantic_proposals"],
            tuple[generated.SemanticProposal, ...],
        )
        self.assertEqual(resolve_hints["submission"], generated.Submission)
        self.assertFalse(
            generated.RelatedRequest.__dataclass_fields__["transitive"].default
        )
        self.assertEqual(
            generated.AnalysisRequest.__dataclass_fields__["contract_version"].default,
            2,
        )

    def test_schema_semantics_drive_python_projection_and_discriminants(self) -> None:
        schema = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
            ).read_text(encoding="utf-8")
        )
        baseline = generate_contract._python_projection(schema)
        mutations = (
            ("type", lambda value: value["$defs"]["RelatedRequest"]["properties"]["transitive"].update(type="string")),
            ("default", lambda value: value["$defs"]["RelatedRequest"]["properties"]["transitive"].update(default=True)),
            ("const", lambda value: value["$defs"]["ReadRequest"]["properties"]["kind"].update(const="read-v2")),
            ("variant", lambda value: value["$defs"]["Submission"]["oneOf"].pop()),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                candidate = copy.deepcopy(schema)
                mutate(candidate)
                self.assertNotEqual(
                    generate_contract._python_projection(candidate),
                    baseline,
                )

        value = {
            "kind": "provide-fact",
            "requirement": {
                "kind": "fact-requirement-handle",
                "id": "fact-requirement:sha256:" + "a" * 64,
                "schema_version": 1,
            },
            "value": {"type": "boolean", "state": "known", "value": True},
            "evidence": [
                {
                    "id": "evidence.generated-contract",
                    "digest": "sha256:" + "b" * 64,
                    "provider_contract": "repository-content",
                    "provider_contract_version": "1",
                }
            ],
        }
        decoded = generated.decode_contract("Submission", value)
        self.assertIsInstance(decoded, generated.ProvideFactSubmission)
        self.assertEqual(decoded.as_contract(), value)

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
