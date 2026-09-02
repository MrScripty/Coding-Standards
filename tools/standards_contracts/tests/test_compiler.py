from __future__ import annotations

import copy
import unittest

from tools.standards_contracts.standards_contracts import (
    ContractError,
    compile_contracts,
)

from support import canonical_inputs


class ContractCompilerTest(unittest.TestCase):
    def test_canonical_schema_and_interface_have_one_exact_public_closure(self) -> None:
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)

        self.assertEqual(set(compiled.reachable_definitions), set(schema["$defs"]))
        self.assertEqual(
            tuple(operation.id for operation in compiled.interface.operations),
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
        self.assertEqual(
            set(compiled.interface.operations[6].capability_by_submission),
            {
                "provide-fact",
                "consumer-disposition",
                "impact-disposition",
                "coverage-attestation",
            },
        )

    def test_unreachable_missing_and_remote_references_have_typed_outcomes(
        self,
    ) -> None:
        schema, interface = canonical_inputs()
        schema["$defs"]["Unused"] = {"type": "string"}
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNREACHABLE_DEFINITION"
        )

        schema, interface = canonical_inputs()
        schema["$defs"]["QueryCall"]["properties"]["snapshot"] = {
            "$ref": "#/$defs/Missing"
        }
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNRESOLVABLE_REFERENCE"
        )

        schema, interface = canonical_inputs()
        schema["$defs"]["QueryCall"]["properties"]["snapshot"] = {
            "$ref": "https://example.invalid/remote-schema"
        }
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNSUPPORTED_REFERENCE"
        )
        self.assertEqual(caught.exception.failure.outcome, "unsupported")

    def test_dialect_keyword_pattern_and_alias_profile_is_closed(self) -> None:
        schema, interface = canonical_inputs()
        schema["$schema"] = "https://json-schema.org/draft/2019-09/schema"
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.UNSUPPORTED_DIALECT")

        schema, interface = canonical_inputs()
        schema["$defs"]["NonEmptyString"]["format"] = "email"
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PROJECTION"
        )

        for unsupported_keyword, value in (
            ("$vocabulary", {"https://example.invalid/vocab": True}),
            ("$dynamicRef", "#node"),
            ("allOf", [{"type": "string"}]),
            ("anyOf", [{"type": "string"}]),
            ("not", {"type": "null"}),
            ("if", {"type": "string"}),
            ("contains", {"type": "string"}),
            ("maxItems", 2),
            ("maxLength", 2),
            ("exclusiveMinimum", 0),
            ("examples", ["example"]),
            ("x-project-extension", True),
        ):
            schema, interface = canonical_inputs()
            schema["$defs"]["NonEmptyString"][unsupported_keyword] = value
            with (
                self.subTest(keyword=unsupported_keyword),
                self.assertRaises(ContractError) as caught,
            ):
                compile_contracts(schema, interface)
            self.assertEqual(
                caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PROJECTION"
            )

        schema, interface = canonical_inputs()
        schema["$defs"]["QueryCall"]["additionalProperties"] = True
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PROJECTION"
        )

        schema, interface = canonical_inputs()
        schema["$defs"]["CanonicalId"]["pattern"] = "(?i)^[a-z]+$"
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PATTERN")

        schema, interface = canonical_inputs()
        schema["$defs"]["CanonicalId"]["pattern"] = r"^a\.b$"
        compiled = compile_contracts(schema, interface)
        compiled.validate("CanonicalId", "a.b")
        with self.assertRaises(ContractError):
            compiled.validate("CanonicalId", "axb")

        schema, interface = canonical_inputs()
        schema["$defs"]["NonEmptyString"] = {"$ref": "#/$defs/CanonicalId"}
        schema["$defs"]["CanonicalId"] = {"$ref": "#/$defs/NonEmptyString"}
        compiled = compile_contracts(schema, interface)
        with self.assertRaises(ContractError) as caught:
            compiled.project()
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PROJECTION"
        )

    def test_interface_and_schema_roots_must_agree_exactly(self) -> None:
        schema, interface = canonical_inputs()
        interface["operations"][0]["extra"] = True
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

        schema, interface = canonical_inputs()
        del interface["operations"][6]["capability_by_submission"]["provide-fact"]
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

        schema, interface = canonical_inputs()
        schema["oneOf"].pop()
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(
            caught.exception.failure.code, "CONTRACT.ROOT_CLOSURE_MISMATCH"
        )

    def test_operation_sequence_is_exact_and_resolve_is_selected_by_identity(
        self,
    ) -> None:
        for mutation in ("missing", "duplicate", "reordered", "unknown"):
            schema, interface = canonical_inputs()
            operations = interface["operations"]
            if mutation == "missing":
                operations.pop(0)
            elif mutation == "duplicate":
                operations.insert(1, copy.deepcopy(operations[0]))
            elif mutation == "reordered":
                operations[0], operations[1] = operations[1], operations[0]
            else:
                operations[0]["id"] = "unknown"
            with (
                self.subTest(mutation=mutation),
                self.assertRaises(ContractError) as caught,
            ):
                compile_contracts(schema, interface)
            self.assertEqual(
                caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE"
            )

        schema, interface = canonical_inputs()
        resolve = next(
            operation
            for operation in interface["operations"]
            if operation["id"] == "resolve"
        )
        del resolve["capability_by_submission"]["provide-fact"]
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

    def test_inputs_are_copied_before_compilation(self) -> None:
        schema, interface = canonical_inputs()
        expected_schema = copy.deepcopy(schema)
        compiled = compile_contracts(schema, interface)
        schema["title"] = "mutated after compile"
        interface["operations"].clear()

        self.assertEqual(compiled.schema["title"], expected_schema["title"])
        self.assertEqual(len(compiled.interface.operations), 10)


if __name__ == "__main__":
    unittest.main()
