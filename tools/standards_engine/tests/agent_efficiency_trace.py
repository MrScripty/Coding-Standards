"""Measure cold MCP calls and exact outcomes in disposable repositories.

This controlled same-build comparison separates wire presentation from policy and
state identity. Catalog bytes are comparable with an archived baseline catalog;
request/result bytes are not model tokens or billing measurements. No publication
or model turn is performed. Run with PYTHONPATH=. and the selected Engine Python.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_agent_workflow import decisions
from tools.standards_engine.tests.test_request_evidence import shared
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change
from tools.standards_engine.standards_engine.tools import AgentToolFacade

ROOT = Path(__file__).resolve().parents[3]


def encoded_bytes(value: object) -> int:
    return len(json.dumps(value).encode("utf-8"))


class ColdClient:
    """Only protocol transport and measurement; decisions remain fixture-owned."""

    def __init__(self, root: Path, purpose: str):
        self.root, self.purpose = root, purpose
        self.calls: list[dict] = []

    def call(self, name: str, arguments: dict, *, rejected: bool = False) -> dict:
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-11-25", "capabilities": {},
                "clientInfo": {"name": "agent-efficiency-trace", "version": "1"},
            }},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                "name": name, "arguments": arguments,
            }},
        ]
        response = subprocess.run(
            [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
             "--repo-root", str(self.root), "--purpose", self.purpose],
            input="".join(json.dumps(item) + "\n" for item in messages),
            text=True, capture_output=True, check=True, env=os.environ.copy(),
        )
        replies = [json.loads(line) for line in response.stdout.splitlines()]
        selected = next(item for item in replies if item.get("id") == 2)
        if "error" in selected:
            raise AssertionError(selected)
        wire = selected["result"]
        value = wire["structuredContent"]
        assert json.loads(wire["content"][0]["text"]) == value
        assert bool(wire["isError"]) == rejected, value
        self.calls.append({"operation": name, "argument_bytes": encoded_bytes(arguments),
                           "result_bytes": encoded_bytes(value)})
        return value


def totals(calls: list[dict]) -> dict:
    return {"call_count": len(calls), "calls": calls,
            "argument_bytes": sum(item["argument_bytes"] for item in calls),
            "result_bytes": sum(item["result_bytes"] for item in calls)}


def route_trace(root: Path, snapshot: dict, purpose: str) -> dict:
    client = ColdClient(root, purpose)
    arguments = {"facts": {}, "snapshot": snapshot}
    selected = client.call("route", arguments)
    targets = list(dict.fromkeys(item["target"] for item in selected["reading_plan"]
                                 if item["state"] == "selected"))
    assert 1 <= len(targets) <= 32
    grouped = client.call("read_many", {"snapshot": snapshot, "items": [{"target": t} for t in targets]})
    split_calls = list(client.calls)
    client.calls.clear()
    composed = client.call("route", {**arguments, "content": {"limit": 32}})
    assert composed["reading_plan"] == selected["reading_plan"]
    assert composed["unresolved_questions"] == selected["unresolved_questions"]
    assert composed["content"]["items"] == grouped["items"]
    assert "next" not in composed["content"]
    assert composed["content"]["total"] == len(targets)
    return {"purpose": purpose, "schema_mode": "native", "policy_count": len(targets),
            "unresolved_questions": len(selected["unresolved_questions"]),
            "separate": totals(split_calls), "composed": totals(client.calls), "exact_content_equal": True}


def evidence_trace(root: Path) -> dict:
    client = ColdClient(root, "authoring")
    pending = client.call("propose", {"change_set": topic_change(root, "evidence-trace-native", 4)})
    arguments = {"context": pending["context"],
                 "submissions": [decision(root, item["obligation"]) for item in pending["work"]["items"]]}
    client.calls.clear()
    ordinary = client.call("resolve_many", arguments)
    assert ordinary["status"] == "complete", ordinary
    review_args = {"context": ordinary["context"], "decisions": decisions(root)}
    ready = client.call("review", review_args)
    assert ready["status"] == "ready", ready
    inline_calls = list(client.calls)
    client.calls.clear()
    equivalent = client.call("resolve_many", shared(arguments))
    assert equivalent == ordinary
    shared_ready = client.call("review", shared(review_args))
    assert shared_ready == ready
    shared_calls = list(client.calls)
    forgotten = shared(arguments)
    del forgotten["evidence"]
    client.call("resolve_many", forgotten, rejected=True)
    reconstructed = client.call("workflow_status", {"context": ready["context"]})
    assert reconstructed["status"] == "ready"
    assert reconstructed["context"] == ready["context"]
    return {"schema_mode": "native", "inline": totals(inline_calls), "shared": totals(shared_calls),
            "exact_analysis_and_readiness_equal": True, "cold_readback": True,
            "previous_request_alias_rejected": True, "final_status": "ready", "published": False}


def measure() -> dict:
    # This qualified captured fixture is deliberately separate from the real
    # corpus's evolving review status. Both purposes observe the exact same bytes.
    from tools.standards_engine.tests.test_purpose_projection import PurposeProjectionTest
    from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotPath

    reports, evidence_reports = [], []
    with tempfile.TemporaryDirectory(prefix="agent-efficiency-") as temporary:
        root = Path(temporary) / "repository"
        _clone_tracked_worktree(root)
        PurposeProjectionTest.setUpClass()
        try:
            with StandardsEngine.open_repository(root, purpose="authoring") as engine:
                captured = engine._snapshots.create_snapshot(CapturedContent("efficiency-fixture", (
                    SnapshotFile(SnapshotPath.parse(path), content)
                    for path, content in PurposeProjectionTest.files.items())))
                snapshot = engine._snapshot_handle(captured.snapshot)
            reports.extend(route_trace(root, snapshot, purpose)
                           for purpose in ("application", "authoring"))
            evidence_reports.append(evidence_trace(root))
        finally:
            PurposeProjectionTest.tearDownClass()
    catalogs = []
    for purpose in ("application", "authoring"):
        catalog = tool_catalog(AgentToolFacade.load_interface(ROOT), purpose=purpose)
        catalogs.append({"purpose": purpose, "schema_mode": "native",
                         "catalog_bytes": encoded_bytes(catalog), "tool_count": len(catalog),
                         "description_bytes": sum(len(t["description"].encode()) for t in catalog),
                         "input_schema_bytes": sum(encoded_bytes(t["inputSchema"]) for t in catalog),
                         "output_schema_bytes": sum(encoded_bytes(t["outputSchema"]) for t in catalog)})
    return {"python": sys.version, "transport": "cold-mcp-stdio", "model_turns": 0,
            "comparison": "same-build, same-snapshot and exact immutable analysis/readiness",
            "routing": reports, "evidence": evidence_reports, "catalogs": catalogs}


if __name__ == "__main__":
    print(json.dumps(measure(), indent=2))
