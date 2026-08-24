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
from tools.standards_engine.contracts import validate_contracts
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

        expected_definitions = {
            name: schema["$defs"][name]
            for name in generate_contract._public_definitions(schema)
        }
        self.assertEqual(
            dict(generated.DEFINITION_SCHEMAS),
            expected_definitions,
        )
        for name, contract_names in generated.FIELD_NAMES.items():
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
            ("minimum", lambda value: value["$defs"]["SemanticProposal"]["properties"]["proposed_semantic_revision"].update(minimum=2)),
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

        result_mutations = (
            (
                "result-type",
                lambda value: value["$defs"]["RouteResult"]["properties"][
                    "summary"
                ].update(type="integer"),
            ),
            (
                "result-required",
                lambda value: value["$defs"]["RouteResult"]["required"].append(
                    "summary"
                ),
            ),
        )
        for label, mutate in result_mutations:
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

    def test_generated_models_enforce_schema_constraints_and_result_shape(self) -> None:
        with self.assertRaises(ValueError):
            generated.CoverageRequirementHandle(
                id="coverage-requirement:sha256:" + "a" * 64,
                schema_version=True,
            )

        self.assertEqual(
            generated._decode_node(
                {"type": "string", "pattern": "required-fragment"},
                "prefix-required-fragment-suffix",
            ),
            "prefix-required-fragment-suffix",
        )

        with self.assertRaises(ValueError):
            generated.SemanticProposal(
                policy="workflow.planning.written-plan-applicability",
                accepted_semantic_revision=1,
                proposed_semantic_revision=0,
                intent="Exercise the generated minimum constraint.",
                structural_digest="sha256:" + "a" * 64,
            )

        with self.assertRaises(ValueError):
            generated.RouteResult.from_value({"kind": "route-result"})

    def test_generated_unique_items_matches_canonical_serialization(self) -> None:
        schema = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
            ).read_text(encoding="utf-8")
        )
        node = schema["$defs"]["InExpression"]
        mixed_numeric_values = {
            "operator": "in",
            "fact": "change.requires-review",
            "values": [1, True],
        }
        validate_contracts.validate(schema, node, mixed_numeric_values, "$")
        self.assertEqual(
            generated.InExpression.from_value(mixed_numeric_values).values,
            (1, True),
        )

        canonically_duplicate_unicode = {
            "operator": "in",
            "fact": "change.requires-review",
            "values": ["é", "e\u0301"],
        }
        with self.assertRaises(validate_contracts.ContractError):
            validate_contracts.validate(schema, node, canonically_duplicate_unicode, "$")
        with self.assertRaises(ValueError):
            generated.InExpression.from_value(canonically_duplicate_unicode)

    def test_generated_const_and_enum_use_canonical_serialization(self) -> None:
        schema = {"$defs": {}}
        for node in ({"const": "é"}, {"enum": ["é"]}):
            with self.subTest(node=node):
                validate_contracts.validate(schema, node, "e\u0301", "$")
                self.assertEqual(
                    generated._decode_node(node, "e\u0301"),
                    "e\u0301",
                )

        for node, value in (
            ({"const": 1}, True),
            ({"const": True}, 1),
            ({"enum": [1]}, True),
            ({"enum": [True]}, 1),
        ):
            with self.subTest(node=node, value=value):
                with self.assertRaises(validate_contracts.ContractError):
                    validate_contracts.validate(schema, node, value, "$")
                with self.assertRaises(ValueError):
                    generated._decode_node(node, value)

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
