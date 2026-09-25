"""Paired fixed-corpus measurements; only disposable repositories/stores are written."""
from __future__ import annotations
import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import tracemalloc
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--fixture-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=3)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
    from tools.standards_engine.standards_engine import _generated_contract as c
    from tools.standards_engine.standards_engine import logical_authoring as logical
    from tools.standards_engine.standards_engine.tools import LocalAlwaysAllowAuthorizer, _contracts
    from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
    from tools.standards_engine.tests import test_agent_workflow as fixtures
    from tools.standards_identity.standards_identity import encode_identity_value, frame_path_byte_set
    fixtures.ROOT = args.fixture_source.resolve()
    records = []
    with tempfile.TemporaryDirectory(prefix='performance-paired-') as tmp:
        root = Path(tmp) / 'repository'
        fixtures.prepare_repository(root)
        with StandardsEngine.open_repository(root, purpose='authoring',
                execution_context=AnalysisExecutionContext(LocalAlwaysAllowAuthorizer(root))) as engine:
            facade = AgentToolFacade(engine, _contracts(root))
            snap = facade.create_snapshot({'kind':'create-snapshot'})
            assert snap['kind'] == 'create-snapshot-result', snap
            snapshot = snap['snapshot']['snapshot']
            capture = engine._snapshots.load_content(engine._snapshot_id(c.SnapshotHandle.from_value(snapshot)))
            dims = {'files':len(capture.files), 'source_bytes':sum(len(x.content) for x in capture.files),
                    'content_id':engine._snapshots._content_id(capture)}
            entries = tuple((x.path.components,x.content) for x in capture.files)
            encoded = encode_identity_value(frame_path_byte_set(entries))
            dims.update(preimage_bytes=len(encoded),preimage_sha256=hashlib.sha256(encoded).hexdigest())
            del encoded
            for trial in range(args.repeats):
                for op, action in [('content_identity',lambda:engine._snapshots._content_id(capture)),
                                   ('read',lambda:facade.read({'snapshot':snapshot,'target':'core'})),
                                   ('propose',lambda:facade.propose({'snapshot':snapshot,'change_set':fixtures.reference_change(root,f'bytebench{trial}')}))]:
                    spans = []; original = logical._refresh_suite_input_projection
                    def refresh(*a, **k):
                        t=time.perf_counter()
                        try:return original(*a,**k)
                        finally:spans.append(time.perf_counter()-t)
                    with patch.object(logical,'_refresh_suite_input_projection',refresh):
                        t=time.perf_counter(); cpu=time.process_time(); result=action()
                        elapsed=time.perf_counter()-t; used=time.process_time()-cpu
                    if op == 'content_identity': assert result == dims['content_id']
                    elif op == 'read': assert result['kind'] in ('read-result','compact-read-result'),result
                    else: assert result.get('status') == 'complete',result
                    records.append({'operation':op,'trial':trial,'seconds':elapsed,'cpu_seconds':used,
                                    'manifest_refresh_seconds':sum(spans),'manifest_refresh_calls':len(spans),**dims})
            gc.collect(); tracemalloc.start(); t=time.perf_counter()
            identity=engine._snapshots._content_id(capture)
            retained,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            assert identity==dims['content_id']
            records.append({'operation':'identity_memory','retained_bytes':retained,'peak_bytes':peak,
                            'instrumented_seconds':time.perf_counter()-t,**dims})
    args.output.write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__': main()
