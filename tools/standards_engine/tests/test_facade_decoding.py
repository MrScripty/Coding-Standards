"""Operation contracts, rather than caller-supplied types, own request decoding."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine.context_projection import Purpose
from tools.standards_engine.standards_engine.tools import AgentToolFacade, _contracts
from tools.standards_engine.tests.test_request_evidence import shared

ROOT = Path(__file__).resolve().parents[3]


class FacadeDecodingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = _contracts(ROOT)
        examples = json.loads((ROOT / "tools/standards_engine/contracts/examples/a1-examples.json").read_text())["examples"]
        cls.proposal = next(item["value"] for item in examples if item["definition"] == "ProposeCall")

    def facade(self, purpose):
        return AgentToolFacade(SimpleNamespace(purpose=purpose), self.contracts)

    def test_selected_purpose_owns_the_decoded_type(self):
        for purpose, expected in ((Purpose.APPLICATION, c.ApplicationReadCall),
                                  (Purpose.AUTHORING, c.ReadCall)):
            call = self.facade(purpose)._decode_call("read", {"target": "core"})
            self.assertIsInstance(call, expected)
            self.assertEqual(call.as_contract(), {"target": "core"})

    def test_table_less_and_shared_requests_retain_their_validation_paths(self):
        facade = self.facade(Purpose.AUTHORING)
        for value, expected in ((self.proposal, ["ProposeCall"]),
                                (shared(deepcopy(self.proposal)), ["AgentProposeCall", "ProposeCall"])):
            before = deepcopy(value)
            with patch("tools.standards_engine.standards_engine.tools.decode_contract", wraps=c.decode_contract) as decoder:
                call = facade._decode_call("propose", value)
            self.assertEqual([args.args[0] for args in decoder.call_args_list], expected)
            self.assertIsInstance(call, c.ProposeCall)
            self.assertEqual(call.as_contract(), self.proposal)
            self.assertEqual(value, before)

    def test_a_generated_type_mismatch_is_not_silently_dispatched(self):
        with patch("tools.standards_engine.standards_engine.tools.decode_contract", return_value=object()):
            with self.assertRaisesRegex(RuntimeError, "generated ProposeCall decoder returned the wrong type"):
                self.facade(Purpose.AUTHORING)._decode_call("propose", self.proposal)
