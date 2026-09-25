"""Measure exact-revision consumer operations on a fixed disposable workload."""
from __future__ import annotations
import argparse
from contextlib import ExitStack
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

p=argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--fixture', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--prepare', action='store_true')
p.add_argument('--repeats', type=int, default=3)
a=p.parse_args()
sys.path.insert(0,str(a.source.resolve()))
from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_engine.tests.test_agent_workflow import reference_change
from tools.standards_engine.standards_engine import logical_authoring as logical
from tools.standards_engine.standards_engine import engine as engine_module
from tools.standards_snapshots.standards_snapshots import SnapshotModule

manifest=a.fixture.parent/'workload.json'
if a.prepare:
    if a.fixture.exists(): raise RuntimeError('fixture must be new')
    a.fixture.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['git','clone','--quiet','--no-hardlinks',str(a.source),str(a.fixture)],check=True)
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=a.fixture,text=True).strip()
    if branch!='main': subprocess.run(['git','branch','-M','main'],cwd=a.fixture,check=True)
    with AgentToolFacade.open_repository(a.fixture,purpose='authoring') as f:
        result=f.create_snapshot({'kind':'create-snapshot'})
        assert result['kind']=='create-snapshot-result',result
        snapshot=result['snapshot']['snapshot']; selected={}
        for n in range(1,13):
            change=reference_change(a.fixture,'projection-latency',revision=n>1)
            change['edits'][0]['standard']['body']+=f'Revision {n}.\n'
            args={'change_set':change}
            if n==1:
                args['snapshot']=snapshot; out=f.propose(args)
            else:
                args['context']=out['context']; out=f.revise(args)
            assert out['status']=='complete',out
            if n in (1,4,12): selected[str(n)]=deepcopy(out)
        data={'snapshot':snapshot,'selected':selected,'target':'reference.testing.projection-latency'}
        manifest.write_text(json.dumps(data,indent=2)+'\n')
    a.output.write_text(json.dumps({'fixture':str(a.fixture),'prepared':True})+'\n')
    sys.exit(0)

work=json.loads(manifest.read_text()); rows=[]; counts=Counter()
def instrument(owner,name,label):
    original=getattr(owner,name)
    def measured(*args,**kwargs):
        counts[label]+=1
        return original(*args,**kwargs)
    return patch.object(owner,name,measured)
with ExitStack() as stack:
    stack.enter_context(instrument(logical,'_refresh_suite_input_projection','manifest_refreshes'))
    stack.enter_context(instrument(engine_module,'compile_policy_impact','full_compiles'))
    stack.enter_context(instrument(SnapshotModule,'load_content','durable_loads'))
    stack.enter_context(instrument(engine_module,'evaluate_analysis','decision_evaluations'))
    for length, result in work['selected'].items():
        server=MCPServer(a.fixture,purpose='authoring'); initialize(server)
        operations=[('query_proposal',{'revision':result['revision'],'request':{'kind':'read','target':work['target']}}),
                    ('workflow_status',{'context':result['context']})]
        for iteration in range(a.repeats+1):
            for op,args in operations:
                counts.clear(); start=time.perf_counter(); cpu=time.process_time()
                out=server.dispatch(request('tools/call',{'name':op,'arguments':args}))
                elapsed=time.perf_counter()-start; cpu=time.process_time()-cpu
                value=out['result']['structuredContent']
                assert not out['result']['isError'],out
                if op=='query_proposal': assert f'Revision {length}.' in value['content']
                else: assert value['status']==('complete' if length=='12' else 'stale'),value
                encoded=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
                rows.append({'history':int(length),'iteration':iteration,'operation':op,
                             'wall_seconds':elapsed,'cpu_seconds':cpu,'counts':dict(counts),
                             'result_sha256':hashlib.sha256(encoded).hexdigest(),
                             'cache':server._compiled_cache.statistics})
        server.close()
info={'source':str(a.source),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip(),
      'python':sys.version,'executable_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
      'packages':{n:importlib.metadata.version(n) for n in ('jsonschema','rpds-py')},'observations':rows}
a.output.write_text(json.dumps(info,indent=2)+'\n')
