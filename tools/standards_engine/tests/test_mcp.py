from __future__ import annotations

from contextlib import redirect_stderr
import io
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.mcp import (
    MCPServer,
    serve,
    tool_catalog,
    input_schema,
)
from tools.standards_engine.standards_engine.tools import _contracts


ROOT = Path(__file__).resolve().parents[3]


def request(method, params=None, identifier=1):
    return {
        "jsonrpc": "2.0",
        "id": identifier,
        "method": method,
        "params": params or {},
    }


def initialize(server):
    response = server.dispatch(
        request(
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1"},
            },
        )
    )
    server.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
    return response


class MCPTest(unittest.TestCase):
    def test_catalog_schemas_validate_authored_examples_and_resolve_refs(self):
        catalog = {tool["name"]: tool for tool in tool_catalog(ROOT, advanced=True)}
        contract = json.loads(
            (
                ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"
            ).read_text()
        )
        self.assertEqual(set(catalog), {op["id"] for op in contract["operations"]})
        examples = json.loads(
            (
                ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text()
        )["examples"]
        for operation in contract["operations"]:
            tool = catalog[operation["id"]]
            for key in ("inputSchema", "outputSchema"):
                schema = tool[key]
                Draft202012Validator.check_schema(schema)

                def check_refs(value):
                    if isinstance(value, dict):
                        if "$ref" in value:
                            self.assertIn(
                                value["$ref"].removeprefix("#/$defs/"), schema["$defs"]
                            )
                        for child in value.values():
                            check_refs(child)
                    elif isinstance(value, list):
                        for child in value:
                            check_refs(child)

                check_refs(schema)
            for example in examples:
                if example["definition"] == operation["input_definition"]:
                    Draft202012Validator(tool["inputSchema"]).validate(example["value"])

    def test_default_catalog_focuses_navigation_and_workflows(self):
        catalog = {t["name"] for t in tool_catalog(ROOT)}
        self.assertTrue(
            {
                "route",
                "routing_facts",
                "propose",
                "review",
                "apply",
                "recover",
            }.issubset(catalog)
        )
        self.assertNotIn("query", catalog)
        self.assertNotIn("apply_proposal", catalog)
        server = MCPServer(ROOT)
        initialize(server)
        self.assertEqual(
            server.dispatch(request("tools/call", {"name": "query"}))["error"]["code"],
            -32602,
        )

    def test_authoring_inputs_expose_structure_and_preserve_recursive_validation(self):
        catalog = {tool["name"]: tool for tool in tool_catalog(ROOT)}
        generated = json.loads(
            (
                ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"
            ).read_text()
        )
        definitions = generated["$defs"]
        examples = json.loads(
            (
                ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text()
        )["examples"]
        change = deepcopy(
            next(
                x["value"]["change_set"]
                for x in examples
                if x["definition"] == "ProposeCall"
            )
        )
        rule = deepcopy(
            next(
                x["value"] for x in examples if x["definition"] == "PutRoutingRuleEdit"
            )
        )
        expression = rule["rule"]["when"]
        for _ in range(12):
            expression = {"operator": "not", "expression": expression}
        rule["rule"]["when"] = expression
        change["edits"] = [rule]
        original = {**definitions["ProposeCall"], "$defs": definitions}
        projected = catalog["propose"]["inputSchema"]
        for name in ("propose", "revise"):
            shape = catalog[name]["inputSchema"]["properties"]["change_set"]
            self.assertEqual(shape["type"], "object")
            self.assertEqual(set(shape["required"]), {"purpose", "edits"})
            self.assertEqual(shape["properties"]["purpose"]["type"], "object")
            edits = shape["properties"]["edits"]["items"]["oneOf"]
            self.assertEqual(len(edits), len(definitions["StandardEdit"]["oneOf"]))
            self.assertTrue(all(edit["type"] == "object" for edit in edits))
        self.assertEqual(
            catalog["propose"]["inputSchema"]["properties"]["snapshot"]["type"],
            "object",
        )
        for validator in (
            Draft202012Validator(original),
            Draft202012Validator(projected),
        ):
            validator.validate({"change_set": change})
            invalid = deepcopy(change)
            invalid["edits"][0]["rule"]["when"]["expression"]["expression"] = {
                "operator": "invented"
            }
            self.assertFalse(validator.is_valid({"change_set": invalid}))
            self.assertFalse(
                validator.is_valid({"change_set": {**change, "extra": True}})
            )
            self.assertFalse(
                validator.is_valid({"change_set": {**change, "edits": []}})
            )

    def test_input_projection_preserves_reference_siblings(self):
        schema = input_schema(
            {"$ref": "#/$defs/Name", "minLength": 3},
            {"Name": {"type": "string", "maxLength": 5}},
        )
        validator = Draft202012Validator(schema)
        self.assertTrue(validator.is_valid("name"))
        for invalid in ("a", "too long", 12):
            self.assertFalse(validator.is_valid(invalid))

    def test_default_guidance_uses_available_recovery_tools(self):
        server = MCPServer(ROOT)
        instructions = initialize(server)["result"]["instructions"]
        self.assertNotIn("recover_application", instructions)
        self.assertIn("recover", instructions)
        with (
            patch.object(AgentToolFacade, "open_repository") as opened,
            redirect_stderr(io.StringIO()),
        ):
            facade = opened.return_value.__enter__.return_value
            facade.apply.side_effect = RuntimeError("failure")
            response = server.dispatch(
                request(
                    "tools/call",
                    {"name": "apply", "arguments": {"context": {"opaque": "identity"}}},
                )
            )["result"]
            self.assertTrue(response["isError"])
            self.assertIn("workflow_status", response["content"][0]["text"])
            self.assertNotIn("recover_application", response["content"][0]["text"])
            facade.apply.assert_called_once()
            facade.recover.assert_not_called()

    def test_lifecycle_and_protocol_errors_never_open_engine(self):
        server = MCPServer(ROOT, advanced=True)
        with patch.object(AgentToolFacade, "open_repository") as opened:
            self.assertEqual(
                server.dispatch(request("tools/list"))["error"]["code"], -32000
            )
            self.assertIn("tools", initialize(server)["result"]["capabilities"])
            self.assertEqual(server.dispatch(request("ping"))["result"], {})
            self.assertEqual(
                len(server.dispatch(request("tools/list"))["result"]["tools"]),
                len(server.names),
            )
            for method, params, code in [
                ("tools/list", {"cursor": "bad"}, -32602),
                ("tools/call", {"name": "close"}, -32602),
                ("tools/call", {"name": "query", "arguments": []}, -32602),
                ("unknown", {}, -32601),
            ]:
                self.assertEqual(
                    server.dispatch(request(method, params))["error"]["code"], code
                )
            self.assertEqual(server.dispatch([])["error"]["code"], -32600)
            opened.assert_not_called()

    def test_preserves_typed_outcomes_and_never_retries(self):
        server = MCPServer(ROOT, advanced=True)
        initialize(server)
        for kind in (
            "pending-result",
            "complete-result",
            "rejected-result",
            "application-recovery-required-result",
        ):
            value = {"kind": kind, "next_operations": ["recover_application"]}
            with patch.object(AgentToolFacade, "open_repository") as opened:
                facade = opened.return_value.__enter__.return_value
                facade.apply_proposal.return_value = value
                response = server.dispatch(
                    request(
                        "tools/call",
                        {
                            "name": "apply_proposal",
                            "arguments": {"readiness": {"opaque": "identity"}},
                        },
                    )
                )["result"]
                self.assertEqual(response["structuredContent"], value)
                self.assertEqual(json.loads(response["content"][0]["text"]), value)
                self.assertEqual(response["isError"], kind == "rejected-result")
                facade.apply_proposal.assert_called_once_with(
                    {"readiness": {"opaque": "identity"}}
                )
                facade.recover_application.assert_not_called()
                opened.return_value.__exit__.assert_called_once()

    def test_internal_failure_is_tool_error_without_retry(self):
        server = MCPServer(ROOT, advanced=True)
        initialize(server)
        with (
            patch.object(AgentToolFacade, "open_repository") as opened,
            redirect_stderr(io.StringIO()),
        ):
            facade = opened.return_value.__enter__.return_value
            facade.apply_proposal.side_effect = RuntimeError("private diagnostic")
            response = server.dispatch(
                request("tools/call", {"name": "apply_proposal"})
            )["result"]
            self.assertTrue(response["isError"])
            self.assertNotIn("private diagnostic", json.dumps(response))
            facade.apply_proposal.assert_called_once()
            facade.recover_application.assert_not_called()

    def test_real_snapshot_read_and_validation_through_server(self):
        server = MCPServer(ROOT, advanced=True)
        initialize(server)
        with StandardsEngine.open_repository(ROOT, durable=False) as engine:
            facade = AgentToolFacade(engine, _contracts(ROOT))
            # The context manager normally owns a durable store per request.
            # Keep this test's in-memory store open across both calls.
            with patch.object(AgentToolFacade, "open_repository") as opened:
                opened.return_value.__enter__.return_value = facade
                created = server.dispatch(
                    request(
                        "tools/call",
                        {
                            "name": "create_snapshot",
                            "arguments": {"kind": "create-snapshot"},
                        },
                    )
                )["result"]["structuredContent"]
                self.assertEqual(created["kind"], "create-snapshot-result", created)
                snapshot = created["snapshot"]["snapshot"]
                read = server.dispatch(
                    request(
                        "tools/call",
                        {
                            "name": "query",
                            "arguments": {
                                "snapshot": snapshot,
                                "request": {
                                    "kind": "read",
                                    "target": "router",
                                    "include_routing": True,
                                },
                            },
                        },
                    )
                )["result"]["structuredContent"]
                self.assertEqual(read["kind"], "read-result", read)
                self.assertIn("routing", read)
                schema = next(
                    t["outputSchema"] for t in server.tools if t["name"] == "query"
                )
                Draft202012Validator(schema).validate(read)
                rejected = server.dispatch(
                    request(
                        "tools/call",
                        {
                            "name": "query",
                            "arguments": {"snapshot": snapshot, "invented": True},
                        },
                    )
                )["result"]
                self.assertTrue(rejected["isError"])
                self.assertEqual(
                    rejected["structuredContent"]["code"], "INTERFACE.INVALID_ARGUMENTS"
                )
                Draft202012Validator(schema).validate(rejected["structuredContent"])

    def test_parse_errors_and_notifications_keep_stream_synchronized(self):
        output = io.StringIO()
        serve(
            MCPServer(ROOT, advanced=True),
            io.StringIO(
                "bad json\n"
                + json.dumps({"jsonrpc": "2.0", "method": "notifications/cancelled"})
                + "\n"
                + json.dumps(request("ping", identifier=9))
                + "\n"
            ),
            output,
        )
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(responses), 2)
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1]["id"], 9)

    def test_module_stdio_launch_from_unrelated_working_directory(self):
        messages = [
            request(
                "initialize",
                {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1"},
                },
            ),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            request("tools/list", identifier=2),
        ]
        result = subprocess.run(
            [
                sys.executable,
                "-P",
                "-m",
                "tools.standards_engine.standards_engine.mcp",
                "--repo-root",
                str(ROOT),
            ],
            input="".join(json.dumps(message) + "\n" for message in messages),
            text=True,
            capture_output=True,
            cwd="/tmp",
            env={**os.environ, "PYTHONPATH": str(ROOT)},
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([r["id"] for r in responses], [1, 2])
        self.assertIn("route", {t["name"] for t in responses[1]["result"]["tools"]})


if __name__ == "__main__":
    unittest.main()
