from __future__ import annotations

import copy
import unittest

from tools.standards_contracts.standards_contracts import (
    ContractError,
    compile_contracts,
)
from tools.standards_contracts.standards_contracts.compiler import schema_digest

from support import canonical_inputs, metaschema_checks


class ContractCompilerTest(unittest.TestCase):
    def test_operation_variants_preserve_submission_capability_coverage(self):
        schema, interface = canonical_inputs()
        resolve = next(operation for operation in interface["operations"] if operation["id"] == "resolve")
        resolve["variants"] = {"mismatched": {"input_definition": "CreateSnapshotCall",
                                              "result_definitions": ["RejectedResult"]}}
        with self.assertRaises(ContractError) as rejected:
            compile_contracts(schema, interface)
        self.assertEqual(rejected.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

    def test_canonical_schema_and_interface_have_one_exact_public_closure(self) -> None:
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)

        self.assertEqual(set(compiled.reachable_definitions), set(schema["$defs"]))
        self.assertEqual(
            tuple(operation.id for operation in compiled.interface.operations),
            tuple(operation["id"] for operation in interface["operations"]),
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

    def test_operation_catalog_is_authoritative_and_duplicate_dispatch_is_rejected(
        self,
    ) -> None:
        schema, interface = canonical_inputs()
        interface["operations"].reverse()
        compiled = compile_contracts(schema, interface)
        self.assertEqual(
            tuple(o.id for o in compiled.interface.operations),
            tuple(o["id"] for o in interface["operations"]),
        )
        interface["operations"].append(copy.deepcopy(interface["operations"][0]))
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

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
        expected_operations = tuple(item["id"] for item in interface["operations"])
        compiled = compile_contracts(schema, interface)
        schema["title"] = "mutated after compile"
        interface["operations"].clear()

        self.assertEqual(compiled.schema["title"], expected_schema["title"])
        self.assertEqual(
            tuple(item.id for item in compiled.interface.operations),
            expected_operations,
        )


if __name__ == "__main__":
    unittest.main()


class OperationVariantTest(unittest.TestCase):
    def test_variant_has_its_own_closed_roots_and_immutable_selection(self):
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)
        read = next(op for op in compiled.interface.operations if op.id == "read")
        selected = read.select_variant("application")
        self.assertEqual(selected.input_definition, "ApplicationReadCall")
        self.assertIn("ApplicationReadResult", selected.result_definitions)
        self.assertNotIn("ReadResult", selected.result_definitions)
        self.assertEqual(selected.capability, read.capability)
        with self.assertRaises(TypeError):
            read.variants["other"] = read.variants["application"]
        with self.assertRaises(KeyError):
            read.select_variant("missing")
        projected = compiled.project().agent_tools
        projected_read = next(op for op in projected["operations"] if op["id"] == "read")
        self.assertEqual(projected_read["variants"]["application"]["input_definition"], selected.input_definition)

    def test_variant_rejects_unknown_definitions_fields_and_duplicate_results(self):
        for replacement in (
            {"input_definition": "Missing", "result_definitions": ["ApplicationReadResult"]},
            {"input_definition": "ApplicationReadCall", "result_definitions": ["ApplicationReadResult"] * 2},
            {"input_definition": "ApplicationReadCall", "result_definitions": []},
            {"input_definition": "ApplicationReadCall", "result_definitions": ["ApplicationReadResult"], "capability": "extra"},
        ):
            schema, interface = canonical_inputs()
            read = next(op for op in interface["operations"] if op["id"] == "read")
            read["variants"]["application"] = replacement
            with self.subTest(replacement=replacement), self.assertRaises(ContractError) as caught:
                compile_contracts(schema, interface)
            self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")


class ValidatedSchemaDigestTest(unittest.TestCase):
    """Only the schema named by a recorded digest skips the metaschema check."""

    def test_schema_with_the_recorded_digest_is_not_validated_again(self) -> None:
        schema, interface = canonical_inputs()
        with metaschema_checks() as checked:
            validated = compile_contracts(schema, interface)
            self.assertEqual(checked.call_count, 1)
            reused = compile_contracts(
                schema, interface, validated_schema_digest=schema_digest(schema)
            )
            self.assertEqual(checked.call_count, 1)

        self.assertEqual(reused.schema, validated.schema)
        self.assertEqual(reused.interface, validated.interface)
        self.assertEqual(reused.reachable_definitions, validated.reachable_definitions)
        self.assertEqual(reused.project(), validated.project())

    def test_schema_that_differs_from_the_digest_is_fully_validated(self) -> None:
        schema, interface = canonical_inputs()
        recorded = schema_digest(schema)
        schema["$defs"]["NonEmptyString"]["minLength"] = 2
        with metaschema_checks() as checked:
            compiled = compile_contracts(schema, interface, validated_schema_digest=recorded)
        self.assertEqual(checked.call_count, 1)
        with self.assertRaises(ContractError):
            compiled.validate("NonEmptyString", "a")

    def test_invalid_schema_is_rejected_with_and_without_a_recorded_digest(self) -> None:
        canonical, _ = canonical_inputs()
        # -1 fails the metaschema only. true equals the canonical 1 in Python,
        # so comparing parsed schemas instead of digests would accept it.
        for value, keyword in ((-1, "minimum"), (True, "type")):
            for recorded in (None, schema_digest(canonical)):
                schema, interface = canonical_inputs()
                schema["$defs"]["NonEmptyString"]["minLength"] = value
                self.assertEqual(schema == canonical, value is True)
                with self.subTest(value=value, recorded=recorded):
                    with self.assertRaises(ContractError) as caught:
                        compile_contracts(schema, interface, validated_schema_digest=recorded)
                    self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_SCHEMA")
                    self.assertEqual(caught.exception.failure.outcome, "invalid")
                    self.assertEqual(caught.exception.failure.keyword, keyword)

    def test_every_other_check_still_runs_for_a_matching_digest(self) -> None:
        def another_dialect(schema: dict[str, object]) -> None:
            schema["$schema"] = "https://json-schema.org/draft/2019-09/schema"

        def unsupported_keyword(schema: dict[str, object]) -> None:
            schema["$defs"]["NonEmptyString"]["format"] = "email"

        def unreachable_definition(schema: dict[str, object]) -> None:
            schema["$defs"]["Unused"] = {"type": "string"}

        def missing_root(schema: dict[str, object]) -> None:
            schema["oneOf"].pop()

        for change, code in (
            (another_dialect, "CONTRACT.UNSUPPORTED_DIALECT"),
            (unsupported_keyword, "CONTRACT.UNSUPPORTED_PROJECTION"),
            (unreachable_definition, "CONTRACT.UNREACHABLE_DEFINITION"),
            (missing_root, "CONTRACT.ROOT_CLOSURE_MISMATCH"),
        ):
            schema, interface = canonical_inputs()
            change(schema)
            with self.subTest(code=code):
                with self.assertRaises(ContractError) as caught:
                    compile_contracts(
                        schema, interface, validated_schema_digest=schema_digest(schema)
                    )
                self.assertEqual(caught.exception.failure.code, code)

        schema, interface = canonical_inputs()
        interface["operations"][0]["extra"] = True
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface, validated_schema_digest=schema_digest(schema))
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_INTERFACE")

    def test_digest_names_the_json_value_not_its_key_order(self) -> None:
        schema, _ = canonical_inputs()
        reordered = dict(reversed(schema.items()))
        self.assertNotEqual(list(reordered), list(schema))
        self.assertEqual(schema_digest(reordered), schema_digest(schema))
        self.assertRegex(schema_digest(schema), r"\Asha256:[0-9a-f]{64}\Z")
        digests = {
            schema_digest({"minLength": value}) for value in (1, 1.0, True, "1", [1], None)
        }
        self.assertEqual(len(digests), 6)

    def test_python_value_that_only_serializes_like_the_schema_is_validated(self) -> None:
        canonical, interface = canonical_inputs()
        recorded = schema_digest(canonical)
        # json.dumps writes this tuple as the same array, but it is not a JSON array
        # and the metaschema rejects it.
        schema, _ = canonical_inputs()
        required = schema["$defs"]["QueryCall"]["required"]
        schema["$defs"]["QueryCall"]["required"] = tuple(required)
        self.assertIsNone(schema_digest(schema))
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface, validated_schema_digest=recorded)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.INVALID_SCHEMA")

        # An integer key reads back as a string; mixed keys and a set cannot be written.
        for not_json in ({1: "key"}, {1: "key", "a": "key"}, {"const": {1, 2}}):
            with self.subTest(not_json=not_json):
                self.assertIsNone(schema_digest(not_json))
