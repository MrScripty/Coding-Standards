"""Compare an unchanged explicit-snapshot MCP sequence in isolated Git fixtures."""
from __future__ import annotations
import argparse, json, subprocess, sys, tempfile, time
from pathlib import Path
from statistics import median
from unittest.mock import patch
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--repeats',type=int,default=3)
a=p.parse_args();sys.path.insert(0,str(a.source.resolve()))
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.standards_engine import tools as facade_tools
from tools.standards_snapshots.standards_snapshots import SnapshotModule
observations=[]; active=[]
original_compile = StandardsEngine._compile
def timed_compile(source):
 t=time.perf_counter()
 try:return original_compile(source)
 finally:active.append({'name':'compile','seconds':time.perf_counter()-t})
def wrap(name, fn):
 def called(*args,**kwargs):
  t=time.perf_counter()
  try:return fn(*args,**kwargs)
  finally: active.append({'name':name,'seconds':time.perf_counter()-t})
 return called
def call(server, method, params=None, number=1):
 return server.dispatch({'jsonrpc':'2.0','id':number,'method':method,'params':params or {}})
def init(server):
 r=call(server,'initialize',{'protocolVersion':'2025-11-25','clientInfo':{'name':'performance-observer','version':'1'},'capabilities':{}})
 assert 'result' in r,r
 server.dispatch({'jsonrpc':'2.0','method':'notifications/initialized'})
with tempfile.TemporaryDirectory(prefix='engine-interface-benchmark-') as tmp:
 root=Path(tmp)/'repo'
 subprocess.run(['git','clone','--quiet','--no-hardlinks',str(a.fixture.resolve()),str(root)],check=True)
 subprocess.run(['git','-C',str(root),'checkout','--quiet','-B','main','b81a5aae'],check=True)
 with AgentToolFacade.open_repository(root,purpose='authoring') as facade:
  c=facade.create_snapshot({'kind':'create-snapshot'})
  assert c['kind']=='create-snapshot-result',c
  snap=c['snapshot']['snapshot']
  from tools.standards_snapshots.standards_snapshots import SnapshotId
  capture=facade._engine._snapshots.load_content(SnapshotId(snap['id']))
  corpus={'files':len(capture.files),'bytes':sum(len(x.content) for x in capture.files),'content_id':SnapshotModule._content_id(capture),'source_revision':capture.source_revision}
 with patch.object(facade_tools,'_contracts',wrap('interface',facade_tools._contracts)),patch.object(StandardsEngine,'_compile',staticmethod(timed_compile)),patch.object(SnapshotModule,'load_content',wrap('load_content',SnapshotModule.load_content)):
  for repeat in range(a.repeats):
   active.clear();t=time.perf_counter();server=MCPServer(root,purpose='authoring');init(server)
   observations.append({'repeat':repeat,'operation':'initialize','seconds':time.perf_counter()-t,'spans':active.copy()})
   for label,args in [('read_first',{'target':'core','snapshot':snap}),('read_repeat',{'target':'core','snapshot':snap}),('read_other',{'target':'workflow.planning','snapshot':snap}),('read_full',{'target':'core','snapshot':snap,'detail':'full'})]:
    active.clear();t=time.perf_counter();cpu=time.process_time();r=call(server,'tools/call',{'name':'read','arguments':args})
    assert 'result' in r and not r['result']['isError'],r
    result=r['result']['structuredContent'];assert result['snapshot']==snap
    observations.append({'repeat':repeat,'operation':label,'seconds':time.perf_counter()-t,'cpu':time.process_time()-cpu,'spans':active.copy(),'content_size':len(result['content'])})
   active.clear();t=time.perf_counter();r=call(server,'tools/call',{'name':'route','arguments':{'facts':{},'snapshot':snap}})
   assert not r['result']['isError'],r
   observations.append({'repeat':repeat,'operation':'route','seconds':time.perf_counter()-t,'spans':active.copy()})
   if hasattr(server,'_compiled_cache'):
    observations.append({'repeat':repeat,'operation':'cache_statistics','seconds':0,'stats':server._compiled_cache.statistics})
   if hasattr(server,'close'):server.close()
a.output.write_text(json.dumps({'source':str(a.source),'python':sys.version,'corpus':corpus,'observations':observations},indent=2)+'\n')
for name in dict.fromkeys(x['operation'] for x in observations):
 xs=[x['seconds'] for x in observations if x['operation']==name]
 print(name,round(median(xs),5),flush=True)
