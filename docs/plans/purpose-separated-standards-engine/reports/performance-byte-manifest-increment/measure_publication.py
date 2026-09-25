"""Observe an unchanged or snapshot-reused workflow against one fixed fixture.

Implementation imports come from --source; only fixture creation and evidence
output write to disk. The selected test is loaded from --test-source independently.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--fixture-source', type=Path, required=True)
    parser.add_argument('--test-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    from tools.standards_engine.tests import test_agent_workflow as fixtures
    from tools.standards_engine.standards_engine import engine as engine_module
    from tools.standards_snapshots.standards_snapshots import SnapshotModule
    fixtures.ROOT = args.fixture_source.resolve()
    test_path = args.test_source / 'tools/standards_engine/tests/test_supporting_workflow.py'
    spec = importlib.util.spec_from_file_location('measured_publication', test_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    counts = {'capture': 0, 'checkpoint': 0}
    checkpoint_seconds = []
    original_capture = SnapshotModule.create_snapshot
    original_checkpoint = engine_module.run_complete_verification
    def capture(self, *a, **k):
        counts['capture'] += 1
        return original_capture(self, *a, **k)
    def checkpoint(*a, **k):
        counts['checkpoint'] += 1
        start = time.perf_counter()
        try:
            return original_checkpoint(*a, **k)
        finally:
            checkpoint_seconds.append(time.perf_counter() - start)
    class Result(unittest.TextTestResult):
        def startTest(self, test):
            self.started = time.perf_counter()
            super().startTest(test)
        def stopTest(self, test):
            self.body_seconds = time.perf_counter() - self.started
            super().stopTest(test)
    with patch.object(SnapshotModule, 'create_snapshot', capture), \
         patch.object(engine_module, 'run_complete_verification', checkpoint):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(module.SupportingWorkflowTest)
        start = time.perf_counter()
        result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
        elapsed = time.perf_counter() - start
    record = {'source': str(args.source.resolve()), 'test_source': str(args.test_source.resolve()),
              'fixture_source': str(args.fixture_source.resolve()), 'tests': result.testsRun,
              'successful': result.wasSuccessful(), 'body_seconds': getattr(result, 'body_seconds', None),
              'total_seconds': elapsed, 'counts': counts, 'checkpoint_seconds': checkpoint_seconds}
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))
    if not result.wasSuccessful():
        raise SystemExit(1)

if __name__ == '__main__':
    main()
