"""Measure complete authority compilation against one fixed corpus.

Run this script with separate baseline/candidate --source checkouts and the same
--corpus directory, in the supported locked environment. It reads but never
changes the corpus. Compare input/output digests before comparing observations.
Capture, warm-up, structural counters and result comparisons are outside timings.
This measures compilation, not complete revision admission or MCP latency.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time
from unittest.mock import patch


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def coverage_material(compiled, coverage):
    index = compiled.coverage
    horizon = index.horizon
    return {
        "horizon": {"id": horizon.id, "provider": horizon.provider, "version": horizon.version,
                    "members": [member.as_projection() for member in horizon.members],
                    "digest": horizon.digest, "input_sources": list(horizon.input_sources),
                    "consumer_members": {key: value.as_projection() for key, value in horizon.consumer_members.items()}},
        "suite_inputs": horizon.suite_inputs.as_projection(),
        "dependencies": {suite.id: asdict(horizon.suite_inputs.dependency(suite.id))
                         for suite in horizon.suite_inputs.suites},
        "views": {key: value.as_projection() for key, value in index.views.items()},
        "requirements": {key: value.as_projection() for key, value in index.requirements.items()},
        "requirement_ids": {key: coverage.coverage_requirement_id(index.requirements[key], view)
                            for key, view in index.views.items()},
        "input_sources": list(index.input_sources),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    if args.output.exists():
        parser.error("--output must be a new evidence file")
    args.source = args.source.resolve()
    args.corpus = args.corpus.resolve()
    sys.path.insert(0, str(args.source))
    from tools.standards_engine.standards_engine.engine import StandardsEngine
    from tools.standards_engine.standards_engine.compiled_cache import _retained_size
    from tools.standards_metadata.standards_metadata.source import DirectoryContentSource, RecordingContentSource
    from tools.standards_metadata.standards_metadata import suite_inputs
    from tools.standards_analysis.standards_analysis import coverage

    recording = RecordingContentSource(DirectoryContentSource(args.corpus))
    StandardsEngine._compile(recording)
    frozen = recording.freeze()
    input_digest = hashlib.sha256()
    for path, content in frozen.files:
        path_bytes = path.encode()
        input_digest.update(len(path_bytes).to_bytes(8, "big"))
        input_digest.update(path_bytes)
        input_digest.update(len(content).to_bytes(8, "big"))
        input_digest.update(content)
    # Untimed structural observation keeps instrumentation out of measurements.
    with patch.object(suite_inputs, "_identity_digest", wraps=suite_inputs._identity_digest) as fingerprints:
        reference = StandardsEngine._compile(frozen)
    material = coverage_material(reference, coverage)
    expected_signature = reference.semantic_signature()
    observations = []
    for iteration in range(args.repeats + 1):
        cpu_start = time.process_time()
        start = time.perf_counter()
        result = StandardsEngine._compile(frozen)
        wall = time.perf_counter() - start
        cpu = time.process_time() - cpu_start
        if result.semantic_signature() != expected_signature or coverage_material(result, coverage) != material:
            raise RuntimeError("Compilation changed semantic or coverage material during measurement")
        observations.append({"warmup": iteration == 0, "wall_seconds": wall, "cpu_seconds": cpu})
    times = [row["wall_seconds"] for row in observations if not row["warmup"]]
    versions = {}
    for package in ("attrs", "jsonschema", "jsonschema-specifications", "referencing", "rpds-py", "typing-extensions"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    source_files = ("tools/standards_analysis/standards_analysis/coverage.py",
                    "tools/standards_metadata/standards_metadata/suite_inputs.py",
                    "tools/standards_engine/standards_engine/engine.py")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.source, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=args.source, capture_output=True, text=True)
    evidence = {
        "scope": "complete frozen authority compilation; excludes capture, revision admission and transport",
        "source": str(args.source), "corpus": str(args.corpus),
        "head": head.stdout.strip() if head.returncode == 0 else None,
        "status": status.stdout if status.returncode == 0 else None,
        "input_sha256": input_digest.hexdigest(), "coverage_output_sha256": digest_json(material),
        "captured_files": len(frozen.files), "captured_bytes": sum(len(content) for _, content in frozen.files),
        "policies": len(reference.corpus.policy_units), "relationships": len(reference.policy_impact.semantics),
        "suites": len(reference.coverage.horizon.suite_inputs.suites),
        "dependency_fingerprints_per_compile": fingerprints.call_count,
        "accounted_compile_bytes": _retained_size(reference, 32 * 1024 * 1024),
        "python": sys.version, "platform": platform.platform(), "packages": versions,
        "source_sha256": {name: hashlib.sha256((args.source / name).read_bytes()).hexdigest() for name in source_files},
        "median_seconds": statistics.median(times), "min_seconds": min(times), "max_seconds": max(times),
        "observations": observations,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(evidence, stream, indent=2)
        stream.write("\n")
    print(json.dumps({key: evidence[key] for key in ("median_seconds", "min_seconds", "max_seconds",
                     "dependency_fingerprints_per_compile", "input_sha256", "coverage_output_sha256")}))


if __name__ == "__main__":
    main()
