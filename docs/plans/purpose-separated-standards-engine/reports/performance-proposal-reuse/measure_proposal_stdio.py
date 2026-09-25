"""Alternating real-MCP draft reads on the same immutable twelve-edit workload."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import time

p=argparse.ArgumentParser()
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--candidate',type=Path,required=True)
p.add_argument('--fixture',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--repeats',type=int,default=3)
a=p.parse_args()
work=json.loads((a.fixture.parent/'workload.json').read_text())
selection=work['selected']['12']; rows=[]; expected={}

def sequence(label,source,sample):
    env={**os.environ,'PYTHONPATH':str(source.resolve())}
    command=[sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp','--repo-root',str(a.fixture.resolve()),'--purpose','authoring']
    with tempfile.TemporaryFile(mode='w+') as errors:
        start=time.perf_counter()
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True,bufsize=1,env=env,start_new_session=True)
        def send(method,params,identifier):
            process.stdin.write(json.dumps({'jsonrpc':'2.0','id':identifier,'method':method,'params':params})+'\n');process.stdin.flush()
            ready,_,_=select.select([process.stdout],[],[],90)
            if not ready: raise TimeoutError('MCP benchmark response unavailable')
            line=process.stdout.readline()
            if not line:
                errors.seek(0);raise RuntimeError(errors.read())
            value=json.loads(line)
            assert value.get('id')==identifier,value
            assert 'error' not in value,value
            return value['result']
        try:
            send('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'projection-measurement','version':'1'}},1)
            rows.append({'implementation':label,'sample':sample,'operation':'initialization','wall_seconds':time.perf_counter()-start})
            process.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');process.stdin.flush()
            operations=[('query_proposal',{'revision':selection['revision'],'request':{'kind':'read','target':work['target']}}),('workflow_status',{'context':selection['context']})]
            identifier=2
            for iteration in range(3):
                for op,arguments in operations:
                    start=time.perf_counter()
                    out=send('tools/call',{'name':op,'arguments':arguments},identifier);identifier+=1
                    elapsed=time.perf_counter()-start
                    assert not out['isError'],out
                    value=out['structuredContent']; assert json.loads(out['content'][0]['text'])==value
                    if op=='query_proposal':assert 'Revision 12.' in value['content']
                    else:assert value['status']=='complete',value
                    digest=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                    if op in expected:assert expected[op]==digest,(op,expected[op],digest)
                    else:expected[op]=digest
                    rows.append({'implementation':label,'sample':sample,'iteration':iteration,'operation':op,'wall_seconds':elapsed,'result_sha256':digest})
            process.stdin.close()
            assert process.wait(timeout=10)==0
        finally:
            if process.poll() is None:
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL);process.wait()
            process.stdout.close()
            if not process.stdin.closed:process.stdin.close()

for sample in range(a.repeats):
    order=[('baseline',a.baseline),('candidate',a.candidate)]
    if sample%2:order.reverse()
    for label,source in order:sequence(label,source,sample)
    a.output.write_text(json.dumps({'python':sys.version,'executable_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'observations':rows},indent=2)+'\n')
