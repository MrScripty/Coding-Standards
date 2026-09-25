"""External read-only baseline instrumentation; no candidate implementation."""
from __future__ import annotations
import argparse,cProfile,concurrent.futures,gc,hashlib,json,os,pstats,shutil,subprocess,sys,tempfile,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--evidence',required=True);p.add_argument('--wait-pid',type=int);a=p.parse_args()
if a.wait_pid:
    while Path(f'/proc/{a.wait_pid}/stat').exists() and Path(f'/proc/{a.wait_pid}/stat').read_text().split()[2]!='Z': time.sleep(3)
r=Path(a.repo).resolve();E=Path(a.evidence).resolve();O=E/'followup';O.mkdir(exist_ok=True)
for controller in ('qualified.pid','qualified-navigation.pid'):
    if (E/controller).exists():
        qualified_pid=int((E/controller).read_text())
        while Path(f'/proc/{qualified_pid}/stat').exists() and Path(f'/proc/{qualified_pid}/stat').read_text().split()[2]!='Z': time.sleep(3)
os.chdir(r);sys.path[:0]=[str(r),str(r/'tools/standards_verifier')]
from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_identity.standards_identity import frame_path_byte_set,hash_identity,encode_identity_value
from tools.standards_snapshots.standards_snapshots.module import SnapshotModule
S=json.loads((E/'operations/snapshot-0.json').read_text());engine=StandardsEngine.open_repository(r,store_path=E/'operations/store-0.sqlite3',purpose='authoring')
identity,capture=engine._snapshots._store.load_content(engine._snapshot_id(c.SnapshotHandle.from_value(S)))
rows=[]
def observe(label,fn):
    t=time.perf_counter();cpu=time.process_time();v=fn();dt=time.perf_counter()-t
    rows.append({'operation':label,'wall_s':dt,'cpu_s':time.process_time()-cpu}); print(label,dt,flush=True);return v
entries=tuple((f.path.components,f.content) for f in capture.files)
for i in range(3):
    material=observe(f'identity_frame_{i}',lambda:frame_path_byte_set(entries))
    encoded=observe(f'identity_encode_{i}',lambda:encode_identity_value(material))
    observed=observe(f'identity_complete_hash_{i}',lambda:SnapshotModule._content_id(capture))
    assert observed==identity
    # This micro-observation isolates SHA-256 cost. It is NOT a substitute identity.
    observe(f'sha256_encoded_bytes_only_{i}',lambda:hashlib.sha256(encoded).digest())
    del material,encoded;gc.collect()
profile=cProfile.Profile();profile.enable();observed=SnapshotModule._content_id(capture);profile.disable();assert observed==identity
profile.dump_stats(str(O/'identity.pstats'))
with (O/'identity-profile.txt').open('w') as f:pstats.Stats(profile,stream=f).strip_dirs().sort_stats('cumulative').print_stats(50)
engine.close()
with tempfile.TemporaryDirectory(prefix='transport-baseline-',dir=O) as td:
    root=Path(td)/'repo'
    subprocess.run(['git','clone','--local','--quiet','--branch','implementation/purpose-separated-standards-engine',str(r),str(root)],check=True)
    subprocess.run(['git','-C',str(root),'branch','main','HEAD'],check=True)
    dest=root/'.standards-engine/snapshots-v1.sqlite3';dest.parent.mkdir(exist_ok=True)
    # Original producer and all operation readers closed before this quiesced copy.
    shutil.copy2(E/'operations/store-0.sqlite3',dest)
    env={**os.environ,'PYTHONPATH':str(root),'PYTHONDONTWRITEBYTECODE':'1'}
    payload={'snapshot':S,'request':{'kind':'read','target':'workflow.planning'}}
    cli=[sys.executable,'-P',str(root/'.agents/skills/standards-engine/scripts/invoke.py'),'--purpose','authoring','--repo-root',str(root),'query']
    for i in range(3):
        result=observe(f'fresh_python_cli_read_{i}',lambda:subprocess.run(cli,input=json.dumps(payload),text=True,capture_output=True,cwd=root,env=env))
        assert result.returncode==0,(result.returncode,result.stderr)
        assert json.loads(result.stdout)['kind']=='read-result'
    def simultaneous_read(index):
        t=time.perf_counter(); result=subprocess.run(cli,input=json.dumps(payload),text=True,capture_output=True,cwd=root,env=env)
        assert result.returncode==0,result.stderr
        assert json.loads(result.stdout)['kind']=='read-result'
        return {'reader':index,'wall_s':time.perf_counter()-t}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        concurrent_rows=observe('two_concurrent_process_reads_same_store',lambda:list(pool.map(simultaneous_read,range(2))))
    (O/'concurrent-readers.json').write_text(json.dumps(concurrent_rows,indent=2))
    for session in range(2):
        stderr=(O/f'mcp-{session}.stderr').open('w');t=time.perf_counter()
        proc=subprocess.Popen([sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp','--purpose','authoring','--repo-root',str(root)],cwd=root,env=env,text=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr,bufsize=1)
        def rpc(message):
            proc.stdin.write(json.dumps(message)+'\n');proc.stdin.flush()
            value=json.loads(proc.stdout.readline());assert 'error' not in value,value;return value['result']
        init=rpc({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'performance-observer','version':'1'}}})
        rows.append({'operation':f'fresh_mcp_initialize_{session}','wall_s':time.perf_counter()-t,'cpu_s':None})
        proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');proc.stdin.flush()
        catalog=observe(f'mcp_tools_list_{session}',lambda:rpc({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}}))
        assert len(catalog['tools'])==15,len(catalog['tools'])
        for i in range(3):
            result=observe(f'mcp_{session}_read_{i}',lambda:rpc({'jsonrpc':'2.0','id':i+3,'method':'tools/call','params':{'name':'read','arguments':{'snapshot':S,'target':'workflow.planning'}}}))
            assert not result.get('isError',False),result
            assert result['structuredContent']['kind']=='compact-read-result'
        if session==0:
            implicit=observe('mcp_read_with_implicit_new_capture',lambda:rpc({'jsonrpc':'2.0','id':20,'method':'tools/call','params':{'name':'read','arguments':{'target':'workflow.planning'}}}))
            assert not implicit.get('isError',False),implicit
        proc.stdin.close();proc.wait();assert proc.returncode==0;proc.stdout.close();stderr.close()
(O/'measurements.json').write_text(json.dumps(rows,indent=2));(O/'source-size.json').write_text(json.dumps({'files':len(capture.files),'raw_bytes':sum(len(f.content) for f in capture.files),'identity':identity}))
print('FOLLOWUP COMPLETE',flush=True)
