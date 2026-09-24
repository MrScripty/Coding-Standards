from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import json
import sys
import types
import unittest
from unittest.mock import patch

from tools.standards_contracts.standards_contracts import (
    ContractError, ContractRuntime, compile_contracts, model_as_contract,
)
from tools.standards_contracts.standards_contracts.runtime import _wire
from tools.standards_contracts.tests.support import CONTRACTS, canonical_inputs
from tools.standards_contracts.tests.test_union_decoding import construction_observations


class GeneralUnionRuntime(ContractRuntime):
    """The pre-optimization branch-selection oracle, without selector tables.

    Validation and construction keep their existing owners. Only branch choice
    is independent of the optimized lookup, so comparisons exercise its effect.
    """
    def _decode_node(self, node, value, definition=None):
        variants = node.get("oneOf")
        if "$ref" not in node and isinstance(variants, list):
            selected = [variant for variant in variants
                        if self._validator.evolve(schema=variant).is_valid(_wire(value))]
            if len(selected) != 1:
                raise AssertionError("validated oneOf did not select exactly one branch")
            return self._decode_node(selected[0], value)
        return super()._decode_node(node, value, definition)


class CanonicalUnionProjectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema, interface = canonical_inputs()
        cls.artifacts = compile_contracts(cls.schema, interface).project()
        cls.generated = types.ModuleType("union_projection_fixture")
        sys.modules[cls.generated.__name__] = cls.generated
        cls.addClassCleanup(sys.modules.pop, cls.generated.__name__, None)
        exec(compile(cls.artifacts.python_source, "<canonical union models>", "exec"),
             cls.generated.__dict__)
        cls.examples = json.loads((CONTRACTS / "examples/a1-examples.json").read_text())["examples"]

    def setUp(self):
        self.candidate = ContractRuntime(self.schema, self.generated.MODEL_TYPES)
        self.general = GeneralUnionRuntime(self.schema, self.generated.MODEL_TYPES)

    def test_all_canonical_examples_keep_generated_types_values_and_omissions(self):
        for example in self.examples:
            with self.subTest(example=example["name"]):
                value = deepcopy(example["value"])
                actual = self.candidate.decode(example["definition"], value)
                expected = self.general.decode(example["definition"], value)
                self.assertEqual(actual, expected)
                self.assertIs(type(actual), type(expected))
                self.assertEqual(model_as_contract(actual), example["value"])
                self.assertEqual(value, example["value"])

    def test_recursive_expression_and_scalar_variants_match_the_general_decoder(self):
        leaves = [
            {"operator": "always"}, {"operator": "exists", "fact": "task.kind"},
            *({"operator": "equals", "fact": "task.kind", "value": value}
              for value in (None, True, 1, 1.0, "text")),
            {"operator": "in", "fact": "task.kind", "values": [None, True, 1, "text"]},
            {"operator": "contains", "fact": "task.tags", "value": "text"},
        ]
        values = [*leaves, {"operator": "all", "expressions": leaves},
                  {"operator": "any", "expressions": leaves},
                  {"operator": "not", "expression": {"operator": "all", "expressions": leaves}}]
        for value in values:
            with self.subTest(value=value):
                actual = self.candidate.decode("ApplicabilityExpression", value)
                expected = self.general.decode("ApplicabilityExpression", value)
                self.assertEqual(actual, expected)
                self.assertEqual(model_as_contract(actual), value)

    def test_recursive_tagged_construction_eliminates_branch_checks_not_root_validation(self):
        value = {"operator": "always"}
        for _ in range(8):
            value = {"operator": "not", "expression": value}
        with construction_observations(self.candidate) as optimized:
            actual = self.candidate.decode("ApplicabilityExpression", value)
        with construction_observations(self.general) as original:
            expected = self.general.decode("ApplicabilityExpression", value)
        self.assertEqual(actual, expected)
        self.assertEqual(optimized, {"roots": 1, "branches": 0})
        self.assertEqual(original["roots"], 1)
        self.assertGreater(original["branches"], 0)

    def test_all_example_required_field_rejections_keep_complete_diagnostics(self):
        for example in self.examples:
            definition = example["definition"]
            required = self.schema["$defs"][definition].get("required", [])
            for name in required:
                value = deepcopy(example["value"])
                del value[name]
                with self.subTest(example=example["name"], missing=name):
                    failures = []
                    for runtime in (self.general, self.candidate):
                        with self.assertRaises(ContractError) as caught:
                            runtime.decode(definition, value)
                        failures.append(asdict(caught.exception.failure))
                    self.assertEqual(*failures)

    def test_generated_constructor_and_from_value_use_the_shared_runtime(self):
        value = {"operator": "all", "expressions": [{"operator": "always"}]}
        with construction_observations(self.generated._RUNTIME) as observed:
            from_value = self.generated.AllExpression.from_value(deepcopy(value))
            direct = self.generated.AllExpression(**deepcopy(value))
        self.assertEqual(from_value, direct)
        self.assertEqual(direct.as_contract(), value)
        self.assertEqual(observed, {"roots": 2, "branches": 0})

    def test_selector_compilation_does_not_repeat_for_each_request(self):
        from tools.standards_contracts.standards_contracts import runtime
        with patch.object(runtime, "compile_union_selectors", side_effect=AssertionError("replanned")):
            for _ in range(5):
                self.candidate.decode("ApplicabilityExpression", {"operator": "always"})


if __name__ == "__main__":
    unittest.main()
