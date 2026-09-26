"""Small complete contract for schema/data boundary tests, independent of the corpus."""
from __future__ import annotations


def inputs() -> tuple[dict, dict]:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://coding-standards.local/tests/schema-locations",
        "oneOf": [{"$ref": "#/$defs/RuntimeInfoCall"},
                  {"$ref": "#/$defs/RuntimeInfoResult"}],
        "$defs": {
            "Text": {"type": "string", "minLength": 1},
            "RuntimeInfoCall": {
                "type": "object", "properties": {"name": {"$ref": "#/$defs/Text"}},
                "additionalProperties": False,
            },
            "RuntimeInfoResult": {
                "type": "object", "required": ["kind"],
                "properties": {"kind": {"const": "result"}}, "additionalProperties": False,
            },
        },
    }
    variant = {"input_definition": "RuntimeInfoCall", "result_definitions": ["RuntimeInfoResult"]}
    interface = {
        "schema_version": 1, "interface_schema_version": 39,
        "request_contract_version": 6, "result_projection_version": 7,
        "operations": [{"id": "runtime_info", **variant, "capability": "standards.read",
                        "variants": {"application": variant.copy()}}],
    }
    return schema, interface
