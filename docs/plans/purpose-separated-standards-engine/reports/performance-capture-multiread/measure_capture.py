"""Compare real accepted-revision captures; writes only disposable stores/evidence."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    source, fixture = args.source.resolve(), args.fixture.resolve()
    sys.path.insert(0, str(source))
    from tools.standards_engine.standards_engine import StandardsEngine
    from tools.standards_engine.standards_engine import _generated_contract as contract
    from tools.standards_snapshots.standards_snapshots import SnapshotId, SnapshotModule
    from tools.repository_git.repository_git import repository as rg

    observations = []
    counters = Counter()
    sessions = []
    peak = {"bytes": 0, "entries": 0}
    compiled = StandardsEngine._compile
    popen = subprocess.Popen
    tree_entries = rg._tree_entries
    session_init = rg.RevisionReadSession.__init__
    session_read = rg.RevisionReadSession.read_file
    def compile_count(content):
        counters["full_compiles"] += 1
        return compiled(content)
    def start(command, *arguments, **options):
        counters["git_processes" if command[0] == "git" else "other_processes"] += 1
        if "cat-file" in command:
            counters["git_batch_processes"] += 1
        return popen(command, *arguments, **options)
    def tree(*arguments):
        counters["tree_parses"] += 1
        return tree_entries(*arguments)
    def initialize(session, *arguments, **options):
        session_init(session, *arguments, **options)
        sessions.append(session)
    def read(session, *arguments):
        value = session_read(session, *arguments)
        peak["bytes"] = max(peak["bytes"], session.cached_bytes)
        peak["entries"] = max(peak["entries"], session.cached_objects)
        counters["source_reads"] += 1
        return value
    def measure(root: Path, store: Path, label: str) -> dict:
        with StandardsEngine.open_repository(root, purpose="authoring", store_path=store) as engine:
            begin, cpu = time.perf_counter(), time.process_time()
            value = engine.create_snapshot(contract.CreateSnapshotCall(kind="create-snapshot")).as_contract()
            wall, cpu_elapsed = time.perf_counter()-begin, time.process_time()-cpu
            if value["kind"] != "create-snapshot-result":
                raise AssertionError(value)
            # The independent readback is outside capture's timing and counters.
            captured = engine._snapshots.load_content(SnapshotId(value["snapshot"]["snapshot"]["id"]))
            return {"label": label, "seconds": wall, "parent_cpu_seconds": cpu_elapsed,
                    "content_id": SnapshotModule._content_id(captured),
                    "source_revision": captured.source_revision,
                    "files": len(captured.files),
                    "source_bytes": sum(len(row.content) for row in captured.files),
                    "store_bytes": store.stat().st_size}
    with tempfile.TemporaryDirectory(prefix="capture-pair-") as temporary:
        scratch = Path(temporary)
        root = scratch / "repository"
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(fixture), str(root)], check=True)
        revision = subprocess.check_output(["git", "-C", str(fixture), "rev-parse", "main"], text=True).strip()
        subprocess.run(["git", "-C", str(root), "checkout", "--quiet", "-B", "main", revision], check=True)
        for index in range(args.repeats):
            row = measure(root, scratch / f"store-{index}.sqlite3", f"sample-{index}")
            observations.append(row)
            print(json.dumps(row), flush=True)
        with ExitStack() as instrumentation:
            instrumentation.enter_context(patch.object(StandardsEngine, "_compile", staticmethod(compile_count)))
            instrumentation.enter_context(patch.object(subprocess, "Popen", start))
            instrumentation.enter_context(patch.object(rg, "_tree_entries", tree))
            instrumentation.enter_context(patch.object(rg.RevisionReadSession, "__init__", initialize))
            instrumentation.enter_context(patch.object(rg.RevisionReadSession, "read_file", read))
            attributed = measure(root, scratch / "counted.sqlite3", "attribution-only")
        attributed["counts"] = dict(counters)
        attributed["peak_session_retention"] = peak
        attributed["session_count"] = len(sessions)
        attributed["closed_session_bytes"] = [session.cached_bytes for session in sessions]
        attributed["closed_session_entries"] = [session.cached_objects for session in sessions]
        assert counters["full_compiles"] == 2, counters
        assert all(session.cached_bytes == 0 for session in sessions)
        assert all(session.cached_objects == 0 for session in sessions)
        assert len({row["content_id"] for row in [*observations, attributed]}) == 1
    args.output.write_text(json.dumps({
        "source_commit": subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip(),
        "fixture_revision": revision, "python": sys.version,
        "python_binary_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
        "observations": observations, "attribution": attributed,
    }, indent=2) + "\n")

if __name__ == "__main__":
    main()
