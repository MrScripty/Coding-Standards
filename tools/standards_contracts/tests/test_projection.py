from __future__ import annotations

import dataclasses
import copy
import json
import sys
import types
import unittest

from tools.standards_contracts.standards_contracts import (
    ContractError,
    MISSING,
    compile_contracts,
)

from support import canonical_inputs


def load_generated(source: str) -> types.ModuleType:
    module = types.ModuleType("staging_a1_contract")
    sys.modules[module.__name__] = module
    exec(compile(source, "staging_a1_contract.py", "exec"), module.__dict__)
    return module


class ContractProjectionTest(unittest.TestCase):
    @staticmethod
    def accepts(compiled: object, definition: str, value: object) -> bool:
        try:
            compiled.validate(definition, value)
        except ContractError:
            return False
        return True

    def test_generated_models_are_immutable_complete_and_validator_backed(self) -> None:
        schema, interface = canonical_inputs()
        artifacts = compile_contracts(schema, interface).project()
        generated = load_generated(artifacts.python_source)
        value = {
            "snapshot": {
                "kind": "snapshot-handle",
                "id": "snapshot:v1:00000000-0000-4000-8000-000000000000",
                "schema_version": 5,
            },
            "request": {"kind": "route", "facts": {}},
        }

        selected = generated.QueryCall.from_value(value)
        self.assertEqual(selected.as_contract(), value)
        self.assertIsInstance(selected.snapshot, generated.SnapshotHandle)
        self.assertIsInstance(selected.request, generated.RouteRequest)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            selected.snapshot = None
        with self.assertRaises(ContractError):
            generated.QueryCall.from_value({"request": value["request"]})
        with self.assertRaises(ContractError):
            generated.QueryCall(snapshot=selected.snapshot, request={"kind": "route"})

        mutable_value = copy.deepcopy(value)
        direct = generated.QueryCall(
            snapshot=mutable_value["snapshot"], request=mutable_value["request"]
        )
        mutable_value["request"]["facts"]["late"] = {"state": "unknown"}
        self.assertEqual(direct.as_contract(), value)
        self.assertIsInstance(direct.snapshot, generated.SnapshotHandle)
        self.assertIsInstance(direct.request, generated.RouteRequest)

        self.assertEqual(
            set(generated.__all__) - {"DEFINITION_METADATA", "decode_contract"},
            set(schema["$defs"]),
        )
        self.assertNotIn("def _decode_node", artifacts.python_source)
        with self.assertRaises(TypeError):
            generated.DEFINITION_METADATA["QueryCall"] = None

    def test_optional_values_distinguish_omission_from_explicit_values(self) -> None:
        schema, interface = canonical_inputs()
        generated = load_generated(
            compile_contracts(schema, interface).project().python_source
        )
        base = {
            "kind": "rejected-result",
            "code": "EXAMPLE.INVALID",
            "outcome": "invalid",
            "message": "invalid example",
            "details": {},
            "next_operations": [],
        }
        omitted = generated.RejectedResult.from_value(base)
        explicit = generated.RejectedResult.from_value(
            {**base, "target": "target.example"}
        )

        self.assertIs(omitted.target, MISSING)
        self.assertNotIn("target", omitted.as_contract())
        self.assertEqual(explicit.as_contract()["target"], "target.example")

    def test_feature_local_mutations_change_projection_without_default_injection(
        self,
    ) -> None:
        schema, interface = canonical_inputs()
        baseline = compile_contracts(schema, interface).project()
        query = next(item for item in baseline.definitions if item.name == "QueryCall")
        self.assertEqual(
            tuple(item.contract_name for item in query.fields), ("snapshot", "request")
        )

        schema["$defs"]["QueryCall"]["properties"]["label"] = {
            "type": "string",
            "default": "display only",
        }
        changed = compile_contracts(schema, interface).project()
        query = next(item for item in changed.definitions if item.name == "QueryCall")
        self.assertEqual(query.fields[-1].contract_name, "label")
        self.assertEqual(query.fields[-1].default_annotation, "display only")
        generated = load_generated(changed.python_source)
        value = {
            "snapshot": {
                "kind": "snapshot-handle",
                "id": "snapshot:v1:00000000-0000-4000-8000-000000000000",
                "schema_version": 5,
            },
            "request": {"kind": "route", "facts": {}},
        }
        selected = generated.QueryCall.from_value(value)
        self.assertIs(selected.label, MISSING)
        self.assertNotIn("label", selected.as_contract())

    def test_every_admitted_projection_keyword_has_a_feature_local_mutation(
        self,
    ) -> None:
        canonical_schema, interface = canonical_inputs()
        baseline = compile_contracts(canonical_schema, interface)
        baseline_artifacts = baseline.project()

        schema = copy.deepcopy(canonical_schema)
        schema["$id"] = (
            "https://coding-standards.local/contracts/standards-engine/a1/mutated"
        )
        self.assertNotEqual(
            compile_contracts(schema, interface).project().python_source,
            baseline_artifacts.python_source,
        )

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["QueryCall"]["title"] = "Query input"
        schema["$defs"]["QueryCall"]["description"] = "Compiled documentation."
        changed = compile_contracts(schema, interface).project()
        query = next(item for item in changed.definitions if item.name == "QueryCall")
        self.assertEqual(query.title, "Query input")
        self.assertEqual(query.description, "Compiled documentation.")

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["QueryCall"]["properties"]["snapshot"] = {
            "$ref": "#/$defs/AnalysisHandle"
        }
        changed_compiled = compile_contracts(schema, interface)
        query = next(
            item
            for item in changed_compiled.project().definitions
            if item.name == "QueryCall"
        )
        self.assertEqual(query.fields[0].annotation, "AnalysisHandle")

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["CanonicalId"]["type"] = "number"
        changed_compiled = compile_contracts(schema, interface)
        canonical_id = next(
            item
            for item in changed_compiled.project().definitions
            if item.name == "CanonicalId"
        )
        self.assertEqual(canonical_id.annotation, "int | float")
        self.assertFalse(self.accepts(baseline, "CanonicalId", 2))
        self.assertTrue(self.accepts(changed_compiled, "CanonicalId", 2))

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["RouteRequest"]["properties"]["kind"]["const"] = "route-v2"
        changed_compiled = compile_contracts(schema, interface)
        route_v1 = {"kind": "route", "facts": {}}
        route_v2 = {"kind": "route-v2", "facts": {}}
        self.assertTrue(self.accepts(baseline, "RouteRequest", route_v1))
        self.assertFalse(self.accepts(changed_compiled, "RouteRequest", route_v1))
        self.assertTrue(self.accepts(changed_compiled, "RouteRequest", route_v2))

        rejected = {
            "kind": "rejected-result",
            "code": "EXAMPLE.INVALID",
            "outcome": "invalid",
            "message": "invalid example",
            "details": {},
            "next_operations": [],
        }
        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["RejectedResult"]["properties"]["outcome"]["enum"].remove(
            "invalid"
        )
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "RejectedResult", rejected))
        self.assertFalse(self.accepts(changed_compiled, "RejectedResult", rejected))

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["ScalarValue"]["oneOf"] = schema["$defs"]["ScalarValue"][
            "oneOf"
        ][:2]
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "ScalarValue", "text"))
        self.assertFalse(self.accepts(changed_compiled, "ScalarValue", "text"))

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["QueryCall"]["required"].remove("snapshot")
        changed_compiled = compile_contracts(schema, interface)
        query = next(
            item
            for item in changed_compiled.project().definitions
            if item.name == "QueryCall"
        )
        self.assertFalse(query.fields[0].required)
        self.assertTrue(
            self.accepts(
                changed_compiled,
                "QueryCall",
                {"request": {"kind": "route", "facts": {}}},
            )
        )

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["FactSet"]["additionalProperties"] = {"type": "string"}
        changed_compiled = compile_contracts(schema, interface)
        self.assertFalse(self.accepts(baseline, "FactSet", {"fact": "value"}))
        self.assertTrue(self.accepts(changed_compiled, "FactSet", {"fact": "value"}))

        all_expression = {
            "operator": "all",
            "expressions": [{"operator": "always"}],
        }
        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["AllExpression"]["properties"]["expressions"]["items"] = {
            "type": "string"
        }
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "AllExpression", all_expression))
        self.assertFalse(
            self.accepts(changed_compiled, "AllExpression", all_expression)
        )

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["AllExpression"]["properties"]["expressions"]["minItems"] = 2
        changed_compiled = compile_contracts(schema, interface)
        self.assertFalse(
            self.accepts(changed_compiled, "AllExpression", all_expression)
        )

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["AllExpression"]["properties"]["expressions"]["uniqueItems"] = (
            True
        )
        changed_compiled = compile_contracts(schema, interface)
        duplicates = {
            "operator": "all",
            "expressions": [{"operator": "always"}, {"operator": "always"}],
        }
        self.assertTrue(self.accepts(baseline, "AllExpression", duplicates))
        self.assertFalse(self.accepts(changed_compiled, "AllExpression", duplicates))

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["NonEmptyString"]["minLength"] = 2
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "NonEmptyString", "x"))
        self.assertFalse(self.accepts(changed_compiled, "NonEmptyString", "x"))

        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["CanonicalId"]["pattern"] = "^[A-Z]+$"
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "CanonicalId", "lower"))
        self.assertFalse(self.accepts(changed_compiled, "CanonicalId", "lower"))

        proposal = {
            "policy": "policy.example",
            "accepted_semantic_revision": None,
            "proposed_semantic_revision": 1,
            "intent": "Add policy.",
            "structural_digest": "sha256:" + "0" * 64,
        }
        schema = copy.deepcopy(canonical_schema)
        schema["$defs"]["SemanticProposal"]["properties"]["proposed_semantic_revision"][
            "minimum"
        ] = 2
        changed_compiled = compile_contracts(schema, interface)
        self.assertTrue(self.accepts(baseline, "SemanticProposal", proposal))
        self.assertFalse(self.accepts(changed_compiled, "SemanticProposal", proposal))

    def test_agent_tools_derive_every_operation_and_reachable_definition(self) -> None:
        schema, interface = canonical_inputs()
        tools = dict(compile_contracts(schema, interface).project().agent_tools)
        self.assertEqual(
            tuple(operation["id"] for operation in tools["operations"]),
            (
                "create_snapshot",
                "find_snapshots",
                "delete_snapshot",
                "undelete_snapshot",
                "query",
                "prepare",
                "resolve",
                "inspect",
                "create_proposal",
                "find_proposals",
            ),
        )
        self.assertEqual(set(tools["$defs"]), set(schema["$defs"]))
        self.assertEqual(tools["interface_schema_version"], 13)
        self.assertEqual(tools["request_contract_version"], 4)
        self.assertEqual(tools["result_projection_version"], 4)
        json.dumps(tools)


if __name__ == "__main__":
    unittest.main()
