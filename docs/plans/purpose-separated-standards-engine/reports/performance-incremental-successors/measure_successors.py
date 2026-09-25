"""Measure native successor admission with an exact warm predecessor.

Use the same prepared fixture for the baseline and candidate. Every sample gets
an independent SQLite backup; neither measured run advances the seed's heads.
Preparation, warm reads and output equivalence checks are outside the timed call.
This runner requires a full checkout and the repository's locked environment.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import ExitStack, closing
from copy import deepcopy
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require_kind(result: dict, kind: str) -> dict:
    if result.get("kind") != kind:
        raise RuntimeError(f"Expected {kind}: {result!r}")
    return result


def no_continuation(self, successor, *, projected_files, repository_paths) -> int:
    """Select the ordinary replay strategy without changing compiler identity."""
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Installed engine source checkout")
    parser.add_argument("--fixture", type=Path, required=True, help="Fixed accepted-base fixture repository")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prepare", action="store_true", help="Create a new disposable fixture; never overwrite one")
    parser.add_argument("--strategy", choices=("full-replay", "continuation"), default="continuation")
    parser.add_argument("--repeats", type=int, default=3, help="Measured samples plus one excluded warm-up sample")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    args.source = args.source.resolve()
    args.fixture = args.fixture.resolve()
    if args.output.exists():
        parser.error("--output must be a new evidence file")
    sys.path.insert(0, str(args.source))
    from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
    from tools.standards_engine.standards_engine import engine as engine_module
    from tools.standards_engine.standards_engine import logical_authoring as logical
    from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
    from tools.standards_engine.tests.test_agent_workflow import reference_change
    from tools.standards_snapshots.standards_snapshots import SnapshotModule

    workload_path = args.fixture.parent / f"{args.fixture.name}-successor-workload.json"
    if args.prepare:
        if args.fixture.exists() or workload_path.exists():
            parser.error("Preparation requires new fixture and workload paths")
        args.fixture.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(args.source), str(args.fixture)], check=True)
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=args.fixture, text=True).strip()
        if branch != "main":
            subprocess.run(["git", "branch", "-m", "main"], cwd=args.fixture, check=True)
        workload = []
        with AgentToolFacade.open_repository(args.fixture, purpose="authoring") as facade:
            captured = require_kind(facade.create_snapshot({"kind": "create-snapshot"}), "create-snapshot-result")
            snapshot = captured["snapshot"]["snapshot"]
            for length in (1, 4, 12, 32):
                label = f"incremental-benchmark-{length}"
                for index in range(1, length + 1):
                    change = reference_change(args.fixture, label, revision=index > 1)
                    change["edits"][0]["standard"]["body"] += f"Draft revision {index}.\n"
                    if index == 1:
                        result = require_kind(facade.create_proposal({
                            "kind": "create-proposal", "snapshot": snapshot, "change_set": change,
                        }), "create-proposal-result")
                    else:
                        result = require_kind(facade.revise_proposal({
                            "kind": "revise-proposal", "expected_revision": result["revision"], "change_set": change,
                        }), "revise-proposal-result")
                suffix = reference_change(args.fixture, label, revision=True)
                suffix["edits"][0]["standard"]["body"] += f"Draft revision {length + 1}.\n"
                workload.append({"history": length, "target": f"reference.testing.{label}",
                                 "request": {"kind": "revise-proposal", "expected_revision": result["revision"],
                                             "change_set": suffix}})
        workload_path.write_text(json.dumps(workload, indent=2) + "\n")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"fixture": str(args.fixture), "workload": str(workload_path),
                                           "prepared": True}, indent=2) + "\n")
        return

    workload = json.loads(workload_path.read_text())
    seed = args.fixture / ".standards-engine/snapshots-v1.sqlite3"
    if not seed.is_file():
        raise FileNotFoundError(f"Missing prepared fixture store: {seed}")
    interface = AgentToolFacade.load_interface(args.fixture)
    continuation_name = "tools.standards_engine.standards_engine.projection_continuation"
    continuation_spec = importlib.util.find_spec(continuation_name)
    if args.strategy == "continuation" and continuation_spec is None:
        raise RuntimeError("Selected installed source does not implement continuation")

    rows = []
    signatures: dict[int, tuple[str, str]] = {}
    for sample in workload:
        for iteration in range(args.repeats + 1):
            with tempfile.TemporaryDirectory(prefix="successor-measure-") as directory:
                store = Path(directory) / "sample.sqlite3"
                with closing(sqlite3.connect(seed)) as original, closing(sqlite3.connect(store)) as copy:
                    original.backup(copy)
                with ExitStack() as owners:
                    cache = CompiledSnapshotCache(args.fixture, "authoring")
                    owners.callback(cache.close)
                    engine = owners.enter_context(StandardsEngine.open_repository(
                        args.fixture, store_path=store, purpose="authoring", compiled_cache=cache,
                    ))
                    facade = AgentToolFacade(engine, interface)
                    require_kind(facade.query_proposal({
                        "revision": sample["request"]["expected_revision"],
                        "request": {"kind": "read", "target": sample["target"]},
                    }), "proposal-read-result")
                    warm_cache = dict(cache.statistics)
                    counts = Counter()

                    def instrument(owner, name, label):
                        original = getattr(owner, name)
                        def measured(*values, **kwargs):
                            counts[label] += 1
                            return original(*values, **kwargs)
                        return patch.object(owner, name, measured)

                    with ExitStack() as measurement:
                        if args.strategy == "full-replay" and continuation_spec is not None:
                            from tools.standards_engine.standards_engine.projection_continuation import ProjectionContinuation
                            measurement.enter_context(patch.object(ProjectionContinuation, "prefix_length", no_continuation))
                        measurement.enter_context(instrument(logical.LogicalAuthoringCompiler, "_apply_edit", "executed_edits"))
                        measurement.enter_context(instrument(logical, "_refresh_suite_input_projection", "manifest_refreshes"))
                        measurement.enter_context(instrument(engine_module, "compile_policy_impact", "authority_compiles"))
                        measurement.enter_context(instrument(SnapshotModule, "load_content", "verified_base_loads"))
                        request = deepcopy(sample["request"])
                        wall, cpu = time.perf_counter(), time.process_time()
                        result = facade.revise_proposal(request)
                        elapsed, processor = time.perf_counter() - wall, time.process_time() - cpu
                    require_kind(result, "revise-proposal-result")
                    measured_cache = dict(cache.statistics)
                    measured_counts = dict(counts)
                    expected_edits = sample["history"] + 1 if args.strategy == "full-replay" else 1
                    if counts["executed_edits"] != expected_edits or counts["manifest_refreshes"] != expected_edits:
                        raise RuntimeError(f"Expected {expected_edits} suffix/replay edits and refreshes; observed {dict(counts)}")
                    # Compare full material outside timing, through the existing
                    # independent replay boundary, not through an exact cache hit.
                    revision = engine._authoring.read_revision(result["revision"]["id"])
                    replayed = engine._proposal_projection(revision)
                    retained = engine._proposal_projection(revision, reuse=True)
                    for field in ("repository_paths", "semantic_proposals", "analysis_policy_ids", "analysis_module_ids"):
                        if getattr(retained, field) != getattr(replayed, field):
                            raise RuntimeError(f"Continuation disagrees with full replay: {field}")
                    if retained.source.files != replayed.source.files:
                        raise RuntimeError("Continuation disagrees with full replay: exact projected bytes")
                    material = {
                        "files": [(path, hashlib.sha256(content).hexdigest()) for path, content in retained.source.files],
                        "repository_paths": retained.repository_paths,
                        "semantic_proposals": retained.semantic_proposals,
                        "analysis_policy_ids": retained.analysis_policy_ids,
                        "analysis_module_ids": retained.analysis_module_ids,
                    }
                    signature = digest(result), digest(material)
                    if signatures.setdefault(sample["history"], signature) != signature:
                        raise RuntimeError("Repeated identical requests produced different material or handles")
                    rows.append({"history": sample["history"], "iteration": iteration, "warmup": iteration == 0,
                                 "wall_seconds": elapsed, "cpu_seconds": processor, "counts": measured_counts,
                                 "request_sha256": digest(sample["request"]), "result_sha256": signature[0],
                                 "projection_sha256": signature[1], "warm_cache": warm_cache,
                                 "cache_after_admission": measured_cache})
    source_files = ("logical_authoring.py", "compiled_cache.py", "operation_materials.py", "engine.py", "projection_continuation.py")
    source_hashes = {}
    for name in source_files:
        path = args.source / "tools/standards_engine/standards_engine" / name
        if path.exists():
            source_hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    data = {"operation": "AgentToolFacade.revise_proposal", "strategy": args.strategy,
            "source": str(args.source), "fixture": str(args.fixture),
            "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.source, text=True).strip(),
            "source_changes": subprocess.check_output(["git", "status", "--porcelain"], cwd=args.source, text=True),
            "source_sha256": source_hashes, "workload_sha256": digest(workload),
            "environment": {"python": sys.version, "platform": platform.platform(), "machine": platform.machine(),
                            "processor": platform.processor(),
                            "packages": {name: importlib.metadata.version(name) for name in ("jsonschema", "rpds-py")}},
            "observations": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
