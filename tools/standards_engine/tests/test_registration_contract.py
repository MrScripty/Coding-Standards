"""Public contract regression for explicit existing-standard registration."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import types
import unittest

from tools.standards_contracts.standards_contracts import ContractError, compile_contracts


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "tools/standards_engine/contracts"


def registration() -> dict[str, object]:
    return {
        "kind": "register-policy-unit",
        "standard": "topic.registration-fixture",
        "policy_unit": {
            "id": "topic.registration-fixture.policy",
            "heading_chain": ["Registered Scope"],
            "semantic_revision": 1,
            "intent": "Identify the selected existing scope for explicit review.",
            "aliases": [],
            "predecessors": [],
            "successors": [],
        },
    }


class RegistrationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((CONTRACTS / "a1-contract.schema.json").read_text())
        cls.interface = tomllib.loads((CONTRACTS / "a1-interface.toml").read_text())
        cls.contracts = compile_contracts(cls.schema, cls.interface)
        cls.artifacts = cls.contracts.project()
        cls.generated = types.ModuleType("registration_generated_contract_test")
        sys.modules[cls.generated.__name__] = cls.generated
        exec(compile(cls.artifacts.python_source, "generated_registration.py", "exec"), cls.generated.__dict__)

    @classmethod
    def tearDownClass(cls) -> None:
        sys.modules.pop(cls.generated.__name__, None)

    def test_registration_is_reachable_from_the_real_proposal_contract(self) -> None:
        edit = registration()
        self.contracts.validate("RegisterPolicyUnitEdit", edit)
        self.contracts.validate("StandardEdit", edit)
        self.contracts.validate("ProposeCall", {
            "change_set": {
                "purpose": {
                    "summary": "Register an existing scope.",
                    "rationale": "Make consumer maintenance possible.",
                    "evidence": [{"id": "evidence:registration-fixture",
                                  "digest": "sha256:" + "1" * 64,
                                  "provider_contract": "repository-content",
                                  "provider_contract_version": "1"}],
                },
                "edits": [edit],
            },
        })

    def test_generated_model_roundtrips_and_owns_nested_values(self) -> None:
        edit = registration()
        expected = copy.deepcopy(edit)
        value = self.generated.RegisterPolicyUnitEdit.from_value(edit)
        edit["policy_unit"]["heading_chain"].append("Changed by caller")
        self.assertEqual(value.as_contract(), expected)
        returned = value.as_contract()
        returned["policy_unit"]["aliases"].append("caller.alias")
        self.assertEqual(value.as_contract(), expected)
        self.assertEqual(value.policy_unit.semantic_revision, 1)

    def test_closed_fields_and_required_members(self) -> None:
        for member in ("standard", "policy_unit", "kind"):
            edit = registration()
            del edit[member]
            with self.subTest(missing=member), self.assertRaises(ContractError):
                self.contracts.validate("StandardEdit", edit)
        for target in ("edit", "unit"):
            edit = registration()
            (edit if target == "edit" else edit["policy_unit"])["path"] = "../registry.toml"
            with self.subTest(target=target), self.assertRaises(ContractError):
                self.contracts.validate("RegisterPolicyUnitEdit", edit)

    def test_new_identity_has_revision_one_and_an_explicit_scope(self) -> None:
        mutations = [
            ("semantic_revision", 0), ("semantic_revision", 2),
            ("semantic_revision", True), ("heading_chain", []),
            ("heading_chain", [""]), ("heading_chain", "Heading"),
            ("intent", ""), ("aliases", ["same.alias", "same.alias"]),
            ("id", ""),
        ]
        for field, value in mutations:
            edit = registration()
            edit["policy_unit"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ContractError):
                self.generated.RegisterPolicyUnitEdit.from_value(edit)

    def test_registration_has_no_body_or_storage_mutation_fields(self) -> None:
        self.assertEqual(
            set(self.schema["$defs"]["RegisterPolicyUnitEdit"]["properties"]),
            {"kind", "standard", "policy_unit"},
        )
        self.assertEqual(
            self.schema["$defs"]["RegisterPolicyUnitEdit"]["properties"]["policy_unit"],
            {"$ref": "#/$defs/NewPolicyUnit"},
        )

    def test_earlier_edit_contracts_keep_their_existing_meaning(self) -> None:
        for name in ("CreateStandardEdit", "ReviseStandardEdit", "RevisePolicyUnitEdit"):
            self.assertIn(name, self.schema["$defs"])
        values = self.schema["$defs"]["StandardEdit"]["oneOf"]
        references = [entry["$ref"] for entry in values]
        self.assertEqual(references.count("#/$defs/RegisterPolicyUnitEdit"), 1)
        self.assertEqual(len(references), len(set(references)))

    def test_checked_in_contract_projections_are_current(self) -> None:
        generated_python = ROOT / "tools/standards_engine/standards_engine/_generated_contract.py"
        generated_tools = CONTRACTS / "generated/agent-tools.json"
        self.assertEqual(generated_python.read_text(), self.artifacts.python_source)
        self.assertEqual(generated_tools.read_text(), self.artifacts.agent_tools_json)
        self.assertEqual(self.artifacts.agent_tools["interface_schema_version"], self.interface["interface_schema_version"])
        self.assertEqual(self.interface["request_contract_version"], 6)
        self.assertEqual(self.interface["result_projection_version"], 7)

    def test_authored_contract_examples_match_the_current_interface(self) -> None:
        examples = json.loads((CONTRACTS / "examples/a1-examples.json").read_text())
        self.assertEqual(examples["interface_schema_version"], self.interface["interface_schema_version"])
        self.assertTrue(any(item["definition"] == "RegisterPolicyUnitEdit" for item in examples["examples"]))
        for example in examples["examples"]:
            with self.subTest(example=example["name"]):
                self.contracts.validate(example["definition"], example["value"])


if __name__ == "__main__":
    unittest.main()
