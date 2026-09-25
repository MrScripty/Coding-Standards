"""Compare six real MCP reads with read_many over one synthetic qualified capture."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

TARGETS = ("core", "workflow.implementation", "workflow.planning", "workflow.verification",
           "topic.contracts", "topic.architecture")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    source, fixture = args.source.resolve(), args.fixture.resolve()
    sys.path.insert(0, str(source))
    from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
    from tools.standards_engine.standards_engine import _generated_contract as contract
    from tools.standards_engine.standards_engine.logical_authoring import _toml_inline
    from tools.standards_engine.standards_engine.mcp import MCPServer
    from tools.standards_engine.tests.test_purpose_projection import refresh
    from tools.standards_metadata.standards_metadata import APPLICATION_CONTENT
    from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotId, SnapshotModule, SnapshotPath
    observations, server_observations = [], []
    with tempfile.TemporaryDirectory(prefix="read-many-pair-") as temporary:
        root = Path(temporary) / "repository"
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(fixture), str(root)], check=True)
        revision = subprocess.check_output(["git", "-C", str(fixture), "rev-parse", "main"], text=True).strip()
        subprocess.run(["git", "-C", str(root), "checkout", "--quiet", "-B", "main", revision], check=True)
        # Installed interface comes from implementation; policy capture stays on
        # the exact common fixture's accepted main, not these working-tree files.
        for path in ("tools/standards_engine/contracts/a1-contract.schema.json",
                     "tools/standards_engine/contracts/a1-interface.toml",
                     "tools/standards_engine/contracts/generated/agent-tools.json"):
            shutil.copyfile(source / path, root / path)
        with AgentToolFacade.open_repository(root, purpose="authoring") as facade:
            value = facade.create_snapshot({"kind": "create-snapshot"})
            assert value["kind"] == "create-snapshot-result", value
            original_snapshot = value["snapshot"]["snapshot"]
            engine = facade._engine
            capture = engine._snapshots.load_content(SnapshotId(original_snapshot["id"]))
            compiled = engine._compiled_snapshot(SnapshotId(original_snapshot["id"]))
            selected, pending = set(TARGETS), list(TARGETS)
            while pending:
                material = compiled.materials[pending.pop()]
                for identity in (*material.requires, *material.specializes):
                    if identity not in selected:
                        selected.add(identity)
                        pending.append(identity)
            files = {str(row.path): row.content for row in capture.files}
            entries = [{"target": identity, "binding": compiled.materials[identity].binding} for identity in sorted(selected)]
            files[APPLICATION_CONTENT] = ("schema_version = 1\nentries = " + _toml_inline(entries) + "\n").encode()
            frozen = refresh(files)
            approved = CapturedContent(capture.source_revision, (
                SnapshotFile(SnapshotPath.parse(path), content) for path, content in frozen.files))
            summary = engine._snapshots.create_snapshot(approved)
            snapshot = engine._snapshot_handle(summary.snapshot)
            corpus = {"files": len(approved.files), "bytes": sum(len(row.content) for row in approved.files),
                      "content_id": SnapshotModule._content_id(approved), "source_revision": capture.source_revision,
                      "synthetic_approvals": sorted(selected)}
        items = [{"target": target} for target in TARGETS]
        for purpose in ("authoring", "application"):
            with tempfile.TemporaryFile(mode="w+t") as stderr:
                started = time.perf_counter()
                process = subprocess.Popen([sys.executable, "-P", "-m", "tools.standards_engine.standards_engine.mcp",
                    "--repo-root", str(root), "--purpose", purpose], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=stderr, text=True, cwd=temporary, env={**os.environ, "PYTHONPATH": str(source)})
                number = 0
                def send(method, params):
                    nonlocal number
                    number += 1
                    process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": number, "method": method, "params": params}) + "\n")
                    process.stdin.flush()
                    line = process.stdout.readline()
                    if not line:
                        stderr.seek(0)
                        raise RuntimeError("MCP closed: " + stderr.read())
                    value = json.loads(line)
                    assert value.get("id") == number and "result" in value, value
                    return value["result"]
                def rpc(operation, arguments):
                    value = send("tools/call", {"name": operation, "arguments": arguments})
                    assert not value.get("isError"), value
                    data = value["structuredContent"]
                    assert data == json.loads(value["content"][0]["text"])
                    return data
                try:
                    send("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                        "clientInfo": {"name": "capture-multiread-measurement", "version": "1"}})
                    server_observations.append({"purpose": purpose, "initialize_seconds": time.perf_counter() - started})
                    process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
                    process.stdin.flush()
                    # Explicit warm-up excludes initial corpus compilation from
                    # both variants; cold behavior remains a separate claim.
                    rpc("read", {"snapshot": snapshot, "target": "core"})
                    for repeat in range(args.repeats):
                        results = {}
                        for operation in (("six_reads", "read_many") if repeat % 2 == 0 else ("read_many", "six_reads")):
                            begin = time.perf_counter()
                            if operation == "six_reads":
                                values = [rpc("read", {"snapshot": snapshot, **item}) for item in items]
                            else:
                                grouped = rpc("read_many", {"snapshot": snapshot, "items": items})
                                assert grouped["snapshot"] == snapshot
                                values = grouped["items"]
                            seconds = time.perf_counter() - begin
                            results[operation] = values
                            observations.append({"purpose": purpose, "repeat": repeat, "operation": operation,
                                "seconds": seconds, "ordered_items_sha256": hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest(),
                                "item_json_bytes": sum(len(json.dumps(value).encode()) for value in values)})
                            print(json.dumps(observations[-1]), flush=True)
                        assert results["six_reads"] == results["read_many"]
                    process.stdin.close()
                    process.wait(timeout=30)
                    assert process.returncode == 0
                finally:
                    if process.poll() is None:
                        process.kill(); process.wait()
                    process.stdout.close()
                    if not process.stdin.closed:
                        process.stdin.close()
        # Separate attribution exercises real MCP dispatch without changing the
        # timed subprocess runs. Complete loads count before the compiler cache.
        counts = []
        for purpose in ("authoring", "application"):
            server = MCPServer(root, purpose=purpose)
            def call(operation, arguments):
                response = server.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                    "params": {"name": operation, "arguments": arguments}})
                assert "result" in response and not response["result"].get("isError"), response
                return response["result"]["structuredContent"]
            try:
                server.dispatch({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
                    "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "attribution", "version": "1"}}})
                server.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
                call("read", {"snapshot": snapshot, "target": "core"})
                for operation in ("six_reads", "read_many"):
                    with patch.object(SnapshotModule, "load_content", autospec=True, side_effect=SnapshotModule.load_content) as load:
                        if operation == "six_reads":
                            values = [call("read", {"snapshot": snapshot, **item}) for item in items]
                        else:
                            values = call("read_many", {"snapshot": snapshot, "items": items})["items"]
                    counts.append({"purpose": purpose, "operation": operation, "complete_loads": load.call_count})
                    assert load.call_count == (6 if operation == "six_reads" else 1)
            finally:
                server.close()
        args.output.write_text(json.dumps({"source_commit": subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip(), "python": sys.version,
            "corpus": corpus, "targets": TARGETS, "observations": observations, "server_startup": server_observations,
            "separate_dispatch_counts": counts}, indent=2) + "\n")

if __name__ == "__main__":
    main()
