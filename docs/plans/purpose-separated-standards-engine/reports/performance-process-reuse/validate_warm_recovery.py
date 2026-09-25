"""Run the unchanged real recovery scenario with a new cache per Engine owner."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.source.resolve()))
from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.tests.test_coverage_publication import EngineAuditPublicationTest

original = StandardsEngine.open_repository
caches = []
def opened(root, **kwargs):
    cache = CompiledSnapshotCache(Path(root), kwargs['purpose'])
    caches.append(cache)
    return original(root, compiled_cache=cache, **kwargs)

start = time.perf_counter()
try:
    with patch.object(StandardsEngine, 'open_repository', side_effect=opened):
        case = EngineAuditPublicationTest('test_review_verify_apply_recover_and_read_without_original_database')
        case.test_review_verify_apply_recover_and_read_without_original_database()
    assert len(caches) == 2, len(caches)
    assert caches[0].statistics['hits'] > 0, caches[0].statistics
    result = {'outcome': 'passed', 'seconds': time.perf_counter() - start,
              'scenario': case.id(), 'caches_before_close': [cache.statistics for cache in caches],
              'scope': 'Original assertions unchanged; first Engine warms through review, live-evidence rejection, interrupted apply and recovery. Second Engine uses a fresh cache and independent database.'}
finally:
    for cache in caches:
        cache.close()
result['caches_after_close'] = [cache.statistics for cache in caches]
args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
