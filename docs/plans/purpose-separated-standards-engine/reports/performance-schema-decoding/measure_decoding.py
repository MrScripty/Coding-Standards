"""Compare root validation plus generated-model decoding, not Engine execution.

Each sample uses an isolated process. Imports, schema compilation, warm-up,
serialization and instrumentation are outside the decode timer. Built-in cases
are synthetic instances of the canonical schema. --workloads accepts an array
of recorded {name, definition, value} instances for a consumer-specific check.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time
import tomllib
import types
from unittest.mock import patch


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def workloads():
    snapshot = {"kind": "snapshot-handle", "id": "snapshot:v1:00000000-0000-4000-8000-000000000001", "schema_version": 5}
    expressions = [{"operator": "all", "expressions": [
        {"operator": "exists", "fact": f"task.fact{i}"},
        {"operator": "not", "expression": {"operator": "equals", "fact": f"task.fact{i}", "value": True}},
        {"operator": "any", "expressions": [{"operator": "contains", "fact": "task.tags", "value": "example"},
                                              {"operator": "always"}]},
    ]} for i in range(32)]
    return [
        {"name": "compact-query", "definition": "QueryCall", "value": {
            "snapshot": snapshot, "request": {"kind": "route", "facts": {}}}},
        {"name": "recursive-expression", "definition": "ApplicabilityExpression", "value": {
            "operator": "all", "expressions": expressions}},
        {"name": "synthetic-route-result", "definition": "AgentRouteResult", "value": {
            "kind": "agent-route-result", "snapshot": snapshot, "reading_plan": [],
            "unresolved_questions": [], "next_operations": [],
            "facts": {f"task.fact{i}": {"type": "boolean", "state": "unknown"} for i in range(32)},
            "rules": [{"id": f"rule.example{i}", "target": "core", "when": expression,
                       "state": "unresolved"} for i, expression in enumerate(expressions)]}},
    ]


def worker(source, cases):
    sys.path.insert(0, str(source))
    from jsonschema import Draft202012Validator
    from tools.standards_contracts.standards_contracts import ContractRuntime, compile_contracts, model_as_contract
    root = source / "tools/standards_engine/contracts"
    schema = json.loads((root / "a1-contract.schema.json").read_text())
    interface = tomllib.loads((root / "a1-interface.toml").read_text())
    generated = types.ModuleType("measured_contracts")
    sys.modules[generated.__name__] = generated
    artifacts = compile_contracts(schema, interface).project()
    exec(compile(artifacts.python_source, "<canonical models>", "exec"), generated.__dict__)
    started = time.perf_counter()
    runtime = ContractRuntime(schema, generated.MODEL_TYPES)
    initialization = time.perf_counter() - started
    observations = []
    for case in cases:
        runtime.decode(case["definition"], case["value"])
        started, cpu = time.perf_counter(), time.process_time()
        decoded = runtime.decode(case["definition"], case["value"])
        elapsed, cpu_elapsed = time.perf_counter() - started, time.process_time() - cpu
        wire = model_as_contract(decoded)
        if digest(wire) != digest(case["value"]):
            raise AssertionError(f"Changed decoded value: {case['name']}")
        counts = {"root_validations": 0, "construction_is_valid_calls": 0}
        validating = False
        original_validate, original_is_valid = runtime.validate, Draft202012Validator.is_valid

        def validate(*args, **kwargs):
            nonlocal validating
            counts["root_validations"] += 1
            validating = True
            try:
                return original_validate(*args, **kwargs)
            finally:
                validating = False

        def is_valid(validator, *args, **kwargs):
            if not validating:
                counts["construction_is_valid_calls"] += 1
            return original_is_valid(validator, *args, **kwargs)

        with patch.object(runtime, "validate", validate), patch.object(Draft202012Validator, "is_valid", is_valid):
            observed = runtime.decode(case["definition"], case["value"])
        if model_as_contract(observed) != wire or counts["root_validations"] != 1:
            raise AssertionError("Instrumentation changed output or root validation")
        observations.append({"name": case["name"], "wall_seconds": elapsed, "cpu_seconds": cpu_elapsed,
                             "input_sha256": digest(case), "output_sha256": digest(wire), **counts})
    package = source / "tools/standards_contracts/standards_contracts"
    return {"python": sys.version, "platform": platform.platform(),
            "dependencies": {name: importlib.metadata.version(name) for name in (
                "jsonschema", "referencing", "attrs", "jsonschema-specifications", "rpds-py", "typing-extensions")},
            "source_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.glob("*.py"))},
            "schema_sha256": digest(schema), "generated_source_sha256": hashlib.sha256(artifacts.python_source.encode()).hexdigest(),
            "runtime_initialization_seconds": initialization,
            "selector_count": len(getattr(runtime, "_union_selectors", {})), "observations": observations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workloads", type=Path)
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker.resolve(), json.load(sys.stdin))))
        return
    if not args.baseline or not args.candidate or not args.output or args.repeats < 1:
        parser.error("Provide baseline, candidate, new output and positive repeats")
    if args.output.exists():
        parser.error("Output must be a new evidence file")
    cases = json.loads(args.workloads.read_text()) if args.workloads else workloads()
    runs = []
    for repeat in range(args.repeats):
        order = [("baseline", args.baseline), ("candidate", args.candidate)]
        if repeat % 2:
            order.reverse()
        for variant, source in order:
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", str(source)],
                                       input=json.dumps(cases), text=True, capture_output=True, check=True)
            run = json.loads(completed.stdout)
            run.update({"variant": variant, "repeat": repeat})
            runs.append(run)
            print(f"{repeat + 1}/{args.repeats} {variant}", file=sys.stderr, flush=True)
    reference = runs[0]
    for run in runs:
        for key in ("schema_sha256", "generated_source_sha256", "dependencies", "python"):
            if run[key] != reference[key]:
                raise AssertionError(f"Inputs or environments differ: {key}")
        if len(run["observations"]) != len(reference["observations"]):
            raise AssertionError("Different workload lengths")
        for original, observed in zip(reference["observations"], run["observations"]):
            for key in ("name", "input_sha256", "output_sha256"):
                if original[key] != observed[key]:
                    raise AssertionError(f"Differential mismatch: {key}")
    summary = []
    for case in cases:
        row = {"name": case["name"], "definition": case["definition"],
               "input_bytes": len(json.dumps(case["value"]).encode())}
        for variant in ("baseline", "candidate"):
            observations = [o for r in runs if r["variant"] == variant for o in r["observations"] if o["name"] == case["name"]]
            values = [o["wall_seconds"] for o in observations]
            row[variant] = {"median_seconds": statistics.median(values), "min_seconds": min(values), "max_seconds": max(values),
                            "construction_is_valid_calls": sorted({o["construction_is_valid_calls"] for o in observations})}
        row["latency_reduction_percent"] = 100 * (1 - row["candidate"]["median_seconds"] / row["baseline"]["median_seconds"])
        summary.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"scope": "decoder only; synthetic canonical-schema workloads unless supplied",
                                      "workloads_sha256": digest(cases), "workloads": cases,
                                      "summary": summary, "runs": runs}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
