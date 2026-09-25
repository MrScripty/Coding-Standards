"""Measure real nested authoring operations against one explicit fixture source.

Run baseline and candidate serially, with separate ``--source`` checkouts and
one common ``--fixture-source`` checkout. The source repositories remain
unchanged; all proposal and snapshot writes use disposable Git/SQLite fixtures.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import time
from typing import Callable, TextIO
from unittest.mock import patch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--fixture-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    arguments = parser.parse_args()
    if arguments.repeats < 1:
        parser.error("--repeats must be positive")
    source = arguments.source.resolve(strict=True)
    fixture_source = arguments.fixture_source.resolve(strict=True)
    sys.path.insert(0, str(source))

    from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
    from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
    from tools.standards_engine.standards_engine import _generated_contract as contract
    from tools.standards_engine.standards_engine.logical_authoring import LogicalAuthoringCompiler
    from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer, _contracts
    from tools.standards_engine.tests import test_agent_workflow as fixtures
    from tools.standards_snapshots.standards_snapshots import SnapshotModule

    # Only fixture preparation uses this location. The imported implementation
    # remains the separately selected --source revision.
    fixtures.ROOT = fixture_source

    def run_trial(trial: int, stream: TextIO) -> None:
        with tempfile.TemporaryDirectory(prefix="nested-operation-timing-") as temporary:
            root = Path(temporary) / "repository"
            fixtures.prepare_repository(root)
            with StandardsEngine.open_repository(
                root, purpose="authoring",
                execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(root)),
            ) as engine:
                facade = AgentToolFacade(engine, _contracts(root))
                created = facade.create_snapshot({"kind": "create-snapshot"})
                if created["kind"] != "create-snapshot-result":
                    raise AssertionError(created)
                snapshot = created["snapshot"]["snapshot"]
                identity = engine._snapshot_id(contract.SnapshotHandle.from_value(snapshot))
                capture = engine._snapshots.load_content(identity)
                dimensions = {
                    "files": len(capture.files),
                    "source_bytes": sum(len(item.content) for item in capture.files),
                    "content_id": str(engine._snapshots._content_id(capture)),
                    "source_revision": capture.source_revision,
                }

                def measure(
                    name: str, expected: str, invoke: Callable[[], dict],
                ) -> dict:
                    counts: Counter[str] = Counter()
                    spans: Counter[str] = Counter()
                    with ExitStack() as patches:
                        for owner, method in (
                            (StandardsEngine, "_compiled_snapshot"),
                            (StandardsEngine, "_proposal_projection"),
                            (StandardsEngine, "_evaluate"),
                            (LogicalAuthoringCompiler, "compile"),
                            (SnapshotModule, "load_content"),
                        ):
                            original = getattr(owner, method)
                            key = owner.__name__ + "." + method

                            def timed(self, *args, _original=original, _key=key, **kwargs):
                                counts[_key] += 1
                                started = time.perf_counter()
                                try:
                                    return _original(self, *args, **kwargs)
                                finally:
                                    spans[_key] += time.perf_counter() - started

                            patches.enter_context(patch.object(owner, method, timed))

                        original_compile = StandardsEngine._compile

                        def timed_compile(content):
                            key = "StandardsEngine._compile"
                            counts[key] += 1
                            started = time.perf_counter()
                            try:
                                return original_compile(content)
                            finally:
                                spans[key] += time.perf_counter() - started

                        patches.enter_context(patch.object(
                            StandardsEngine, "_compile", staticmethod(timed_compile),
                        ))
                        # The logical compiler captured its callback at construction;
                        # instrument that callback as well as direct Engine compiles.
                        patches.enter_context(patch.object(
                            engine._logical_authoring, "_compile_authorities", timed_compile,
                        ))
                        started = time.perf_counter()
                        cpu = time.process_time()
                        result = invoke()
                        elapsed_cpu = time.process_time() - cpu
                        elapsed = time.perf_counter() - started
                    observed = result.get("status", result["kind"])
                    if observed != expected:
                        raise AssertionError((name, expected, result))
                    record = {
                        "corpus": dimensions, "trial": trial, "operation": name,
                        "seconds": elapsed, "cpu_seconds": elapsed_cpu,
                        "status": observed, "counts": dict(counts),
                        "inclusive_seconds": dict(spans),
                    }
                    encoded = json.dumps(record)
                    stream.write(encoded + "\n")
                    stream.flush()
                    print(encoded, flush=True)
                    return result

                reference = measure("propose_reference", "complete", lambda: facade.propose({
                    "snapshot": snapshot,
                    "change_set": fixtures.reference_change(root, "nestedref"),
                }))
                measure("analyze_context", "complete", lambda: facade.analyze({
                    "context": reference["revision"],
                }))
                measure("analyze_proposal", "complete", lambda: facade.analyze_proposal({
                    "revision": reference["revision"],
                }))
                measure("workflow_status", "complete", lambda: facade.workflow_status({
                    "context": reference["context"],
                }))
                measure("query_proposal", "proposal-read-result", lambda: facade.query_proposal({
                    "revision": reference["revision"],
                    "request": {"kind": "read", "target": "reference.testing.nestedref"},
                }))
                measure("revise_reference", "complete", lambda: facade.revise({
                    "context": reference["context"],
                    "change_set": fixtures.reference_change(root, "nestedref", revision=True),
                }))
                change = fixtures.reference_change(root, "nestednorm")
                change["edits"][0]["standard"].update(
                    id="topic.nested-normative-fixture", role="topic", level="MUST",
                    body="Resolve this isolated semantic impact explicitly.\n",
                )
                normative = measure("propose_normative", "needs-action", lambda: facade.propose({
                    "snapshot": snapshot, "change_set": change,
                }))
                obligation = normative["outcome"]["obligations"][0]
                submission = {
                    "kind": "impact-disposition", "obligation": obligation["handle"],
                    "result": "confirmed",
                    "rationale": "The isolated scope is explicitly acknowledged.",
                    "evidence": [fixtures.evidence(root)],
                    "fingerprint": obligation["fingerprint"],
                }
                measure("resolve_workflow", "complete", lambda: facade.resolve_workflow({
                    "context": normative["context"], "submission": submission,
                }))

    # Exclusive creation protects an earlier measurement from accidental overwrite.
    with arguments.output.open("x", encoding="utf-8") as stream:
        for trial in range(arguments.repeats):
            run_trial(trial, stream)


if __name__ == "__main__":
    main()
