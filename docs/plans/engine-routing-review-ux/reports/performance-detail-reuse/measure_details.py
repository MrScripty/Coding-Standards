"""Compare exact historical detail reads through real MCP subprocesses.

Prepare one disposable baseline fixture, then use it unchanged for both
implementations. Preparation, imports and capture are outside detail timings.
No modification of a supplied implementation checkout or installed store occurs.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def prepare(source: Path, fixture: Path) -> None:
    if fixture.exists():
        raise ValueError("Preparation requires a new disposable fixture directory.")
    sys.path.insert(0, str(source.resolve()))
    from tools.standards_engine.standards_engine import AgentToolFacade
    from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
    from tools.standards_engine.tests.test_agent_workflow import prepare_repository, reference_change
    from tools.standards_engine.tests.test_review_workflow_ux import topic_change, decision
    from tools.standards_snapshots.standards_snapshots import SnapshotId

    fixture.mkdir(parents=True)
    root = fixture / "repository"
    prepare_repository(root)
    cache = CompiledSnapshotCache(root, "authoring")
    try:
        with AgentToolFacade.open_repository(root, purpose="authoring", compiled_cache=cache) as facade:
            captured = facade.create_snapshot({"kind": "create-snapshot"})
            assert captured["kind"] == "create-snapshot-result", captured
            snapshot = captured["snapshot"]["snapshot"]
            result = facade.propose({
                "snapshot": snapshot, "change_set": topic_change(root, "detail-probe", 4),
                "detail": "full",
            })
            assert result["status"] == "needs-action", result
            for index in range(1, 12):
                change = reference_change(root, "detail-probe-history", revision=index > 1)
                change["edits"][0]["standard"]["body"] += f"History {index}.\n"
                result = facade.revise({
                    "context": result["context"], "change_set": change, "detail": "full",
                })
                assert result["status"] == "needs-action", result
            pending = result
            submitted = [
                {**decision(root, item), "rationale": "x" * 71000 if index == 0 else f"Complete review {index}."}
                for index, item in enumerate(pending["outcome"]["obligations"])
            ]
            complete = facade.resolve_many({
                "context": pending["context"], "submissions": submitted, "detail": "full",
            })
            assert complete["status"] == "complete", complete
            first_request = {"analysis": pending["context"], "section": "pending_obligations", "limit": 2}
            first = facade.workflow_details(first_request)
            assert first["kind"] == "workflow-details-result", first
            dispositions = facade.workflow_details({
                "analysis": complete["context"], "section": "dispositions", "detail": "full",
            })
            large_index = next(index for index, item in enumerate(complete["outcome"]["dispositions"])
                               if len(json.dumps(item).encode()) > 64 * 1024)
            large_request = {"analysis": complete["context"], "section": "dispositions",
                             "offset": large_index, "observation": dispositions["observation"], "limit": 1}
            rejected = facade.workflow_details(large_request)
            assert rejected["code"] == "WORKFLOW.RESULT_LIMIT", rejected
            requests = [
                ("cold_first_page", first_request),
                ("warm_next_page", first["next"]),
                ("warm_first_page", first_request),
                ("oversized_compact_rejection", large_request),
                ("oversized_full_retry", rejected["next_operations"][0]["request"]),
            ]
            expected = {name: facade.workflow_details(request) for name, request in requests}
            content = facade._engine._snapshots.load_content(SnapshotId(snapshot["id"]))
            workload = {
                "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
                "snapshot": snapshot, "change_sets": 12,
                "files": len(content.files), "source_bytes": sum(len(item.content) for item in content.files),
                "content_id": facade._engine._snapshots._content_id(content),
                "requests": requests, "expected": expected,
            }
            (fixture / "workload.json").write_text(json.dumps(workload, indent=2) + "\n")
    finally:
        cache.close()


@contextmanager
def server(source: Path, root: Path):
    with tempfile.TemporaryFile(mode="w+") as errors:
        process = subprocess.Popen(
            [sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
             "--repo-root", str(root), "--purpose", "authoring"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True,
            env={**os.environ, "PYTHONPATH": str(source.resolve()), "PYTHONDONTWRITEBYTECODE": "1"},
        )
        try:
            yield process
            process.stdin.close()
            trailing = process.stdout.read()
            status = process.wait()
            errors.seek(0)
            diagnostics = errors.read()
            if status or trailing or diagnostics:
                raise RuntimeError(f"MCP shutdown failed: {status}; {trailing}; {diagnostics}")
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            process.stdout.close()
            if not process.stdin.closed:
                process.stdin.close()


def exchange(process, method: str, params: dict, identifier: int) -> dict:
    process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": identifier, "method": method, "params": params}) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    if not line:
        raise RuntimeError("MCP process closed before returning the requested response.")
    response = json.loads(line)
    if response.get("id") != identifier or "result" not in response:
        raise RuntimeError(f"Unexpected MCP response: {response}")
    return response["result"]


def measure(baseline: Path, candidate: Path, fixture: Path, repeats: int) -> dict:
    workload = json.loads((fixture / "workload.json").read_text())
    records = []
    for iteration in range(repeats):
        order = (("baseline", baseline), ("candidate", candidate))
        if iteration % 2:
            order = tuple(reversed(order))
        for label, source in order:
            started = time.perf_counter()
            with server(source, fixture / "repository") as process:
                exchange(process, "initialize", {
                    "protocolVersion": "2025-11-25", "capabilities": {},
                    "clientInfo": {"name": "detail-reuse-measurement", "version": "1"},
                }, 1)
                startup = time.perf_counter() - started
                process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
                process.stdin.flush()
                for identifier, (name, request) in enumerate(workload["requests"], 2):
                    t0 = time.perf_counter()
                    response = exchange(process, "tools/call", {"name": "workflow_details", "arguments": request}, identifier)
                    elapsed = time.perf_counter() - t0
                    value = response["structuredContent"]
                    assert json.loads(response["content"][0]["text"]) == value, name
                    assert value == workload["expected"][name], (label, name, value)
                    records.append({"implementation": label, "iteration": iteration, "operation": name,
                                    "seconds": elapsed, "response_sha256": digest(value),
                                    "json_bytes": len(json.dumps(value).encode()),
                                    "startup_seconds": startup})
            print(label, iteration, "passed", flush=True)
    comparison = {}
    for name, _ in workload["requests"]:
        comparison[name] = {}
        for label in ("baseline", "candidate"):
            values = [row["seconds"] for row in records if row["implementation"] == label and row["operation"] == name]
            comparison[name][label] = {"median": statistics.median(values), "min": min(values), "max": max(values), "n": len(values)}
    return {
        "python": sys.version, "executable_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
        "platform": platform.platform(), "cpu_count": os.cpu_count(),
        "dependencies": {name: importlib.metadata.version(name) for name in ("jsonschema", "referencing", "attrs", "rpds-py")},
        "source_commits": {label: subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
                           for label, source in (("baseline", baseline), ("candidate", candidate))},
        "source_production_sha256": {
            label: {path: hashlib.sha256((source / path).read_bytes()).hexdigest()
                    for path in ("tools/standards_engine/standards_engine/engine.py",
                                 "tools/standards_engine/standards_engine/workflow_presentation.py")}
            for label, source in (("baseline", baseline), ("candidate", candidate))
        },
        "source_status": {
            label: subprocess.check_output(["git", "status", "--porcelain"], cwd=source, text=True)
            for label, source in (("baseline", baseline), ("candidate", candidate))
        },
        "workload_sha256": digest(workload),
        "workload": {key: workload[key] for key in ("source_commit", "snapshot", "change_sets", "files", "source_bytes", "content_id")},
        "comparison": comparison, "observations": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.baseline, args.fixture)
    else:
        if args.candidate is None or args.output is None or args.repeats < 1:
            parser.error("Measurement requires candidate, output and positive repeats.")
        result = measure(args.baseline, args.candidate, args.fixture, args.repeats)
        args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
