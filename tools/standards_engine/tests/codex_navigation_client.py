"""Check configured MCP schemas/navigation through Codex without a model turn.

Run with the locked Engine Python from the repository root. Requires the Codex
CLI and an authoring-purpose MCP configuration pointing at this checkout. Creates
an ephemeral client thread, captures a standards snapshot, and reads policy.
"""

import argparse
import asyncio
import json
import sys
import tempfile
from pathlib import Path
from jsonschema import Draft202012Validator
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.codex_discovery_client import result_contracts

ROOT = Path(__file__).resolve().parents[3]


async def main(server_name, output_schemas="eager"):
    with tempfile.TemporaryFile(mode="w+") as log:
        process = await asyncio.create_subprocess_exec(
            "codex",
            "app-server",
            "--stdio",
            "-c",
            "analytics.enabled=false",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=log,
            limit=8 * 1024 * 1024,
        )
        counter = 0

        async def request(method, params):
            nonlocal counter
            counter += 1
            process.stdin.write(
                (
                    json.dumps({"id": counter, "method": method, "params": params})
                    + "\n"
                ).encode()
            )
            await process.stdin.drain()
            while True:
                line = await asyncio.wait_for(process.stdout.readline(), timeout=600)
                assert line, "Codex app server closed"
                item = json.loads(line)
                if item.get("id") == counter:
                    assert "error" not in item, item
                    return item["result"]
                if "id" in item and "method" in item:
                    raise AssertionError("Unexpected client request: " + item["method"])

        try:
            await request(
                "initialize",
                {
                    "clientInfo": {"name": "standards-client-check", "version": "1"},
                    "capabilities": {"experimentalApi": True},
                },
            )
            process.stdin.write(b'{"method":"initialized","params":{}}\n')
            thread = await request(
                "thread/start", {"cwd": str(ROOT), "ephemeral": True}
            )
            tid = thread["thread"]["id"]
            inventory = await request("mcpServerStatus/list", {"threadId": tid})
            server = next(
                s for s in inventory["data"] if s["name"] == server_name
            )
            toolmap = server["tools"]
            print("Codex tools:", sorted(toolmap), flush=True)
            from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
            interface = AgentToolFacade.load_interface(ROOT)
            expected = tool_catalog(interface, purpose='authoring', output_schemas=output_schemas)
            examples = json.loads((ROOT / "tools/standards_engine/contracts/examples/a1-examples.json").read_text())["examples"]
            validation = result_contracts(interface, {tool['name']: tool for tool in expected})
            for tool in expected:
                observed = toolmap[tool["name"]]
                for field in ("inputSchema", "outputSchema", "description"):
                    assert (field in observed) == (field in tool) and observed.get(field) == tool.get(field), (tool["name"], field)
                Draft202012Validator.check_schema(observed["inputSchema"])
                if "outputSchema" in observed:
                    Draft202012Validator.check_schema(observed["outputSchema"])
            for name, definition in (("propose", "AgentProposeCall"),
                                     ("revise", "AgentReviseCall"),
                                     ("review", "AgentReviewCall"),
                                     ("resolve_many", "AgentResolveManyCall"),
                                     ("resolve_workflow", "AgentResolveWorkflowCall")):
                validator = Draft202012Validator(toolmap[name]["inputSchema"])
                for fixture in (e["value"] for e in examples if e["definition"] == definition):
                    validator.validate(fixture)
            print(f"Codex catalog: exact native input/output schemas and descriptions preserved", flush=True)

            async def call(name, arguments):
                r = await request(
                    "mcpServer/tool/call",
                    {
                        "threadId": tid,
                        "server": server_name,
                        "tool": name,
                        "arguments": arguments,
                    },
                )
                assert not r.get("isError"), r
                value = r["structuredContent"]
                schema = validation[name]
                Draft202012Validator(schema).validate(value)
                return value

            # Scripted discovery conformance is independent of catalog transport;
            # the separate codex_discovery_client runs the model-visible scenario.
            for name in ("propose", "revise", "resolve_workflow", "resolve_many", "review"):
                arguments = {"operation": name, "limit": 16}
                records = {}
                while True:
                    page = await call("describe_input", arguments)
                    assert page["kind"] == "input-contract-result", page
                    records.update({item["name"]: json.loads(item["schema_json"]) for item in page["records"]})
                    if "next" not in page:
                        break
                    arguments = page["next"]
                validator = Draft202012Validator({"$schema": page["dialect"],
                    "$ref": "#/$defs/" + page["selector"], "$defs": records})
                for fixture in (e["value"] for e in examples if e["definition"] == page["root"]):
                    validator.validate(fixture)
            print("Codex scripted discovery: five complete authoring input closures preserved (not a model qualification)", flush=True)

            groups = await call("relationship_groups", {})
            assert groups["kind"] == "relationship-groups-result", groups
            assert all(item["id"] and item["traversal_directions"] for item in groups["items"])

            output_args, documents = {"operation": "read", "limit": 16}, {}
            while True:
                page = await call("describe_output", output_args)
                documents.update({r["name"]: json.loads(r["schema_json"]) for r in page["records"]})
                if "next" not in page:
                    break
                output_args = page["next"]
            reconstructed = {**json.loads(page["root_schema_json"]), "$defs": documents}
            assert reconstructed == validation["read"]
            print(f"Codex {output_schemas} output delivery: exact read contract rediscovered", flush=True)
            # No model turn here: verify the actual host accepts the current
            # grammar and reuses returned facts/authority, not observer-injected types.
            vocabulary = await call("routing_facts", {})
            actual_facts = {item["id"]: item for item in vocabulary["facts"]}
            category = actual_facts["routing.activities"]
            assert "implementation" in category["values"]
            assertions = {"routing.activities": ["implementation"]}
            focused = await call("route", {"snapshot": vocabulary["snapshot"], "facts": assertions,
                                          "content": {"limit": 1}})
            assert focused["facts"] == assertions and focused["unresolved_questions"]
            explained = await call("route", focused["explanation"])
            assert explained["facts"] == focused["facts"]
            if "next" in focused["content"]:
                continuation = await call("route", focused["content"]["next"])
                assert continuation["snapshot"] == focused["snapshot"]
                assert continuation["facts"] == focused["facts"]
            uncertain = await call("route", {"snapshot": vocabulary["snapshot"],
                "facts": {"routing.activities": {"state": "unknown"}}})
            assert uncertain["facts"] == {"routing.activities": {"state": "unknown"}}
            print("Focused routing assertions and cold-independent continuations: host path checked; no model qualification", flush=True)
            routed = await call("route", {"facts": {}})
            assert routed["kind"] == "compact-route-result", routed
            assert all(i["operation"] in toolmap for i in routed["next_operations"])
            op = next(i for i in routed["next_operations"] if i["operation"] == "read")
            read = await call(
                "read", {"snapshot": op["snapshot"], "target": op["target"]}
            )
            assert read["kind"] == "compact-read-result", read
            assert read["snapshot"] == routed["snapshot"]
            assert all(i["operation"] in toolmap for i in read["next_operations"])
            grouped = await call("read_many", {
                "snapshot": routed["snapshot"],
                "items": [{"target": op["target"]}, {"target": op["target"], "detail": "full"}],
            })
            assert grouped["kind"] == "read-many-result", grouped
            composed = await call("route", {"facts": {}, "snapshot": routed["snapshot"], "content": {"limit": 32}})
            assert composed["reading_plan"] == routed["reading_plan"]
            assert composed["unresolved_questions"] == routed["unresolved_questions"]
            assert read in composed["content"]["items"]
            assert grouped["items"][0] == read
            assert all(item["snapshot"] == routed["snapshot"] for item in grouped["items"])
            print(
                "Codex route -> read: available continuations, same snapshot, exact content returned",
                flush=True,
            )
        except BaseException:
            log.seek(0)
            sys.stderr.write(log.read())
            raise
        finally:
            process.stdin.close()
            try:
                await asyncio.wait_for(process.wait(), 10)
            except asyncio.TimeoutError:
                process.terminate()
                await process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", default="standards-authoring", help="Configured authoring-purpose MCP registration")
    parser.add_argument("--output-schemas", choices=("eager", "on-demand"), default="eager",
                        help="Expected delivery of the configured server; does not reconfigure it")
    arguments = parser.parse_args()
    asyncio.run(main(arguments.server, arguments.output_schemas))
