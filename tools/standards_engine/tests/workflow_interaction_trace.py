"""Measure an explicit decision workflow through cold MCP calls, without a model.

Run with the repository's selected Python and PYTHONPATH=. from either the
baseline or candidate checkout. --mode selects the corresponding public client
behavior; it is not a server compatibility switch. All mutations use a disposable
repository and fixture-owned evidence. Output counts JSON bytes, not model tokens.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change


def measure(mode: str) -> dict[str, object]:
    calls = []
    with tempfile.TemporaryDirectory(prefix="workflow-trace-") as temporary:
        root = Path(temporary) / "repository"
        _clone_tracked_worktree(root)

        def call(name: str, arguments: dict) -> dict:
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                    "protocolVersion": "2025-11-25", "capabilities": {},
                    "clientInfo": {"name": "workflow-interaction-trace", "version": "1"},
                }},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                    "name": name, "arguments": arguments,
                }},
            ]
            completed = subprocess.run(
                [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
                 "--repo-root", str(root), "--purpose", "authoring"],
                input="".join(json.dumps(item) + "\n" for item in messages),
                text=True, capture_output=True, check=True, env=os.environ.copy(),
            )
            responses = [json.loads(line) for line in completed.stdout.splitlines()]
            selected = next(item for item in responses if item.get("id") == 2)
            if "error" in selected:
                raise AssertionError(selected)
            wire = selected["result"]
            value = wire["structuredContent"]
            if wire.get("isError") or json.loads(wire["content"][0]["text"]) != value:
                raise AssertionError(wire)
            calls.append({
                "operation": name,
                "argument_bytes": len(json.dumps(arguments).encode("utf-8")),
                "result_bytes": len(json.dumps(value).encode("utf-8")),
            })
            return value

        result = call("propose", {"change_set": topic_change(root, "interaction-trace", 4)})
        for remaining in (2, 0):
            if result["status"] != "needs-action":
                raise AssertionError(result)
            if mode == "explicit-pages":
                page = call("workflow_details", {
                    "analysis": result["context"], "section": "pending_obligations",
                })
            else:
                page = result["work"]
                if page["kind"] != "workflow-work-page":
                    raise AssertionError(page)
            result = call("resolve_many", {
                "context": result["context"],
                "submissions": [decision(root, item["obligation"]) for item in page["items"][:2]],
            })
            if result["outcome"]["required_obligations"] != remaining:
                raise AssertionError(result)
        if result["status"] != "complete" or {item["operation"] for item in result["next_operations"]} != {"review", "revise"}:
            raise AssertionError(result)
    return {
        "mode": mode, "python": sys.version.split()[0], "transport": "cold-mcp-stdio",
        "scenario": "four explicit impact decisions in two batches; stop before review/publication",
        "calls": calls, "call_count": len(calls),
        "argument_bytes": sum(item["argument_bytes"] for item in calls),
        "result_bytes": sum(item["result_bytes"] for item in calls),
        "final_status": result["status"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("explicit-pages", "inline-work"), required=True)
    print(json.dumps(measure(parser.parse_args().mode), indent=2))
