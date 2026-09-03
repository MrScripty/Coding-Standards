from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace

from tools.standards_contracts.standards_contracts import (
    compile_contracts,
    render_repository_projections,
)
from tools.standards_engine.standards_engine import AgentToolFacade
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
    def test_interface_operations_bind_generated_calls_results_and_facade(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        facade = AgentToolFacade(object(), contracts)
        expected_inputs = {
            "create_snapshot": generated.CreateSnapshotCall,
            "find_snapshots": generated.FindSnapshotsCall,
            "delete_snapshot": generated.DeleteSnapshotCall,
            "undelete_snapshot": generated.UndeleteSnapshotCall,
            "query": generated.QueryCall,
            "prepare": generated.PrepareCall,
            "resolve": generated.ResolveCall,
            "inspect": generated.InspectCall,
            "create_proposal": generated.CreateProposalCall,
            "find_proposals": generated.FindProposalsCall,
            "revise_proposal": generated.ReviseProposalCall,
            "query_proposal": generated.QueryProposalCall,
            "analyze_proposal": generated.AnalyzeProposalCall,
            "review_proposal": generated.ReviewProposalCall,
            "apply_proposal": generated.ApplyProposalCall,
            "recover_application": generated.RecoverApplicationCall,
        }

        for operation in contracts.interface.operations:
            with self.subTest(operation=operation.id):
                self.assertIs(
                    getattr(generated, operation.input_definition),
                    expected_inputs[operation.id],
                )
                self.assertTrue(callable(getattr(facade, operation.id)))
                self.assertEqual(facade._operation(operation.id), operation)
                for definition in operation.result_definitions:
                    self.assertIn(definition, generated.DEFINITION_METADATA)

        class WrongQueryResult:
            __definition__ = "CompleteResult"

            @staticmethod
            def as_contract() -> dict[str, object]:
                return {"kind": "complete-result"}

        with self.assertRaisesRegex(RuntimeError, "outside the query result algebra"):
            facade._result("query", WrongQueryResult())

    def test_prepare_facade_passes_the_complete_generated_call(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        observed: list[object] = []
        rejected = generated.RejectedResult(
            "rejected-result",
            "ANALYSIS.TEST",
            "unavailable",
            "test result",
            {},
            (),
        )
        engine = SimpleNamespace(
            prepare=lambda call: observed.append(call) or rejected,
        )
        facade = AgentToolFacade(engine, contracts)
        examples = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text(encoding="utf-8")
        )["examples"]
        arguments = next(
            item["value"] for item in examples if item["definition"] == "PrepareCall"
        )

        result = facade.prepare(arguments)

        self.assertEqual(result["code"], "ANALYSIS.TEST")
        self.assertEqual(len(observed), 1)
        self.assertIsInstance(observed[0], generated.PrepareCall)

    def test_generated_contract_projections_are_current(self) -> None:
        completed = subprocess.run(
            (
                sys.executable,
                "-P",
                "-m",
                "tools.standards_contracts.standards_contracts.projection",
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
        projections = render_repository_projections()
        for path, projection in projections.items():
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertEqual(path.read_text(encoding="utf-8"), projection)

    def test_generated_native_models_decode_complete_v20_values(self) -> None:
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

        recovery_value = {
            "kind": "recover-application",
            "readiness": {
                "kind": "readiness-handle",
                "id": "readiness:sha256:" + "d" * 64,
                "schema_version": 1,
            },
        }
        recovery = generated.RecoverApplicationCall.from_value(recovery_value)
        self.assertEqual(recovery.as_contract(), recovery_value)
        with self.assertRaises(ValueError):
            generated.RecoverApplicationCall.from_value(
                {**recovery_value, "application": "caller-selected"}
            )

    def test_review_call_requires_exactly_three_decisions(self) -> None:
        examples = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text(encoding="utf-8")
        )["examples"]
        call = next(
            item["value"]
            for item in examples
            if item["definition"] == "ReviewProposalCall"
        )

        generated.ReviewProposalCall.from_value(call)
        with self.assertRaises(ValueError):
            generated.ReviewProposalCall.from_value(
                {
                    **call,
                    "decisions": [
                        *call["decisions"],
                        {
                            **call["decisions"][0],
                            "rationale": "A duplicate owner cannot add a fourth decision.",
                        },
                    ],
                }
            )

    def test_agent_tools_are_the_exact_compiler_projection(self) -> None:
        tools_path = (
            REPO_ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"
        )
        projected = render_repository_projections()[tools_path]
        self.assertEqual(tools_path.read_text(encoding="utf-8"), projected)

    def test_authored_v20_examples_satisfy_the_public_contract(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(contracts.interface.interface_schema_version, 20)
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

    def test_identity_fixtures_use_valid_public_handle_versions(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/identity-fixtures.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(corpus["identity_encoding_version"], 2)
        handles = corpus["public_handles"]
        self.assertEqual(
            {fixture["definition"] for fixture in handles},
            {
                "SnapshotHandle",
                "AnalysisHandle",
                "SnapshotChildHandle",
                "AnalysisChildHandle",
                "ProposalHandle",
                "ProposalRevisionHandle",
                "ReadinessHandle",
                "ApplicationHandle",
            },
        )
        for fixture in handles:
            with self.subTest(handle=fixture["name"]):
                contracts.validate(fixture["definition"], fixture["value"])


if __name__ == "__main__":
    unittest.main()
