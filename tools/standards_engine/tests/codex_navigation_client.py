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

ROOT = Path(__file__).resolve().parents[3]


async def main(server_name):
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
            propose = toolmap["propose"]
            shape = propose["inputSchema"]
            assert shape["properties"]["change_set"]["type"] == "object"
            assert set(shape["properties"]["change_set"]["required"]) == {
                "purpose",
                "edits",
            }
            canonical = json.loads((ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text())
            variants = canonical["$defs"]["StandardEdit"]["oneOf"]
            assert len(shape["properties"]["change_set"]["properties"]["edits"]["items"]["oneOf"]) == len(variants)
            assert {"PutDecisionProvenanceEdit", "RetireDecisionProvenanceEdit",
                    "ApproveApplicationContentEdit", "WithdrawApplicationContentEdit",
                    "ReviseOperationalArtifactEdit"} <= {item["$ref"].rsplit("/", 1)[-1] for item in variants}
            print(
                f"Codex authoring schema: purpose, edits, {len(variants)} inline edit variants",
                flush=True,
            )
            for name in ("propose", "revise", "resolve_workflow"):
                documented = json.loads(
                    toolmap[name]["description"]
                    .split("```json\n", 1)[1]
                    .split("\n```", 1)[0]
                )
                Draft202012Validator.check_schema(documented)
                assert set(documented["$defs"]["EvidenceReference"]["required"]) == {
                    "id",
                    "digest",
                    "provider_contract",
                    "provider_contract_version",
                }
                if name != "resolve_workflow":
                    assert documented["$defs"]["StandardEdit"]["oneOf"] == variants
            print(
                "Codex descriptions: exact nested edit/evidence contracts preserved",
                flush=True,
            )

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
                schema = toolmap[name]["outputSchema"]
                Draft202012Validator(schema).validate(value)
                return value

            routed = await call("route", {"facts": {}})
            assert routed["kind"] == "agent-route-result", routed
            assert all(i["operation"] in toolmap for i in routed["next_operations"])
            op = next(i for i in routed["next_operations"] if i["operation"] == "read")
            read = await call(
                "read", {"snapshot": op["snapshot"], "target": op["target"]}
            )
            assert read["kind"] == "compact-read-result", read
            assert read["snapshot"] == routed["snapshot"]
            assert all(i["operation"] in toolmap for i in read["next_operations"])
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
    arguments = parser.parse_args()
    asyncio.run(main(arguments.server))
