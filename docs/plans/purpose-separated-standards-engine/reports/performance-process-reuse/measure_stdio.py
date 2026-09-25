"""Observe startup and explicit retained-snapshot reads through real MCP stdio."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from statistics import median

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--fixture',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--repeats',type=int,default=3)
a=p.parse_args();source=a.source.resolve();sys.path.insert(0,str(source))
from tools.standards_engine.standards_engine import AgentToolFacade

def rss(pid):
 try:
  rows=Path(f'/proc/{pid}/status').read_text().splitlines()
  return int(next(row.split()[1] for row in rows if row.startswith('VmRSS:')))*1024
 except (OSError,StopIteration,ValueError):return None

rows=[]
with tempfile.TemporaryDirectory(prefix='mcp-process-measurement-') as tmp:
 root=Path(tmp)/'repository'
 subprocess.run(['git','clone','--quiet','--no-hardlinks',str(a.fixture.resolve()),str(root)],check=True)
 subprocess.run(['git','-C',str(root),'checkout','--quiet','-B','main','b81a5aae'],check=True)
 with AgentToolFacade.open_repository(root,purpose='authoring') as f:
  created=f.create_snapshot({'kind':'create-snapshot'})
  assert created['kind']=='create-snapshot-result',created
  snapshot=created['snapshot']['snapshot']
 for repeat in range(a.repeats):
  startup=time.perf_counter()
  with tempfile.TemporaryFile(mode='w+t') as errors:
   process=subprocess.Popen([sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp','--repo-root',str(root),'--purpose','authoring'],cwd=tmp,env={**os.environ,'PYTHONPATH':str(source)},stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True)
   def send(method,params=None,number=1):
    process.stdin.write(json.dumps({'jsonrpc':'2.0','id':number,'method':method,'params':params or {}})+'\n');process.stdin.flush()
    line=process.stdout.readline()
    if not line:
     errors.seek(0);raise RuntimeError('MCP closed without a response: '+errors.read())
    response=json.loads(line)
    assert 'result' in response,response
    return response['result']
   try:
    send('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'performance-measurement','version':'1'}})
    rows.append({'repeat':repeat,'operation':'process_initialize','seconds':time.perf_counter()-startup,'rss_bytes':rss(process.pid)})
    process.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');process.stdin.flush()
    for label,target in [('read_cold','core'),('read_warm','core'),('read_other','workflow.planning'),('read_warm_again','core')]:
     start=time.perf_counter();value=send('tools/call',{'name':'read','arguments':{'snapshot':snapshot,'target':target}})
     assert not value['isError'],value
     assert value['structuredContent']['snapshot']==snapshot
     rows.append({'repeat':repeat,'operation':label,'seconds':time.perf_counter()-start,'rss_bytes':rss(process.pid)})
    process.stdin.close();process.wait(timeout=30)
    assert process.returncode==0,process.returncode
   finally:
    if process.poll() is None:process.terminate();process.wait(timeout=30)
    process.stdout.close()
a.output.write_text(json.dumps({'source':str(source),'python':sys.version,'observations':rows},indent=2)+'\n')
for label in dict.fromkeys(row['operation'] for row in rows):
 values=[row for row in rows if row['operation']==label]
 print(label,round(median(x['seconds'] for x in values),5), 'RSS',median(x['rss_bytes'] for x in values))
