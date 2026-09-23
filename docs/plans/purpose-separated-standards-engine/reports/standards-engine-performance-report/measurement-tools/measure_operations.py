"""Observe existing Engine operations without changing their semantics or source."""
from __future__ import annotations
import argparse,collections,contextlib,cProfile,functools,gc,hashlib,json,os,platform,pstats,resource,sys,time,tracemalloc
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--output',required=True);p.add_argument('--samples',type=int,default=3);p.add_argument('--profile',action='store_true');a=p.parse_args()
r=Path(a.repo).resolve();os.chdir(r);sys.path[:0]=[str(r),str(r/'tools/standards_verifier')];os.environ['PYTHONPATH']=str(r);os.environ['PYTHONDONTWRITEBYTECODE']='1'
from tools.standards_engine.standards_engine import StandardsEngine,AgentToolFacade
from tools.standards_engine.standards_engine import engine as em
from tools.standards_engine.standards_engine import supporting as sm,navigation_indexes as nm
from tools.standards_engine.standards_engine import tools as tm
from tools.standards_engine.tests.platform_harness import HarnessAuthorizer,_disposition
from tools.standards_analysis.standards_analysis import AnalysisExecutionContext
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_snapshots.standards_snapshots.module import SnapshotModule
from tools.standards_snapshots.standards_snapshots.store import SQLiteSnapshotStore
from tools.repository_git.repository_git import repository as gm
out=Path(a.output);out.mkdir(parents=True,exist_ok=True);log=(out/'operations.jsonl').open('w',buffering=1)
stats={};stack=[];reads=collections.Counter();objects=collections.Counter();commands=collections.Counter();phase=None;current=None;unwrap=[]
def record(label,fn,args,kwargs):
 global stack
 t=time.perf_counter();frame=[0.0];stack.append(frame)
 try:return fn(*args,**kwargs)
 finally:
  elapsed=time.perf_counter()-t;stack.pop();s=stats.setdefault(label,{'calls':0,'wall_s':0.,'self_s':0.});s['calls']+=1;s['wall_s']+=elapsed;s['self_s']+=elapsed-frame[0]
  if stack:stack[-1][0]+=elapsed

def patch(owner,name,label=None,static=False):
 original=getattr(owner,name);label=label or name
 @functools.wraps(original)
 def wrapped(*args,**kwargs):
  tag=label
  if name=='_compile':
   src=args[0];tag='_compile/'+type(getattr(src,'_source',src)).__name__
  if label=='git.read_bytes':reads[args[1]]+=1
  if label=='git.object':objects[(str(args[1]),args[2],args[3])]+=1
  if label=='git.command':commands[' '.join(args[1][:2])]+=1
  return record(tag,original,args,kwargs)
 setattr(owner,name,staticmethod(wrapped) if static else wrapped);unwrap.append((owner,name,original,static))
for name in ['_compiled_snapshot','_proposal_projection','_evaluate','_evaluate_compiled','_validate_projected_inputs','_load_analysis']:
 patch(StandardsEngine,name,'engine.'+name)
patch(StandardsEngine,'_compile',static=True)
for name in ['load_canonical_standards_corpus','compile_policy_impact','load_supporting_content','standards_navigation_registry','load_router_projection','compile_coverage_definitions','load_coverage_horizon','load_repository_coverage_decisions','evaluate_analysis']:
 patch(em,name,'compile.'+name)
patch(sm,'build_materials','compile.build_materials');patch(nm,'load_indexes','compile.load_indexes')
patch(em._GitRevisionSource,'read_bytes','git.read_bytes');patch(gm.GitRepository,'read_file','git.read_file');patch(gm.GitRepository,'_object','git.object');patch(gm,'git_output','git.command')
for name in ['load_content','maintain','publish_aggregate']:
 patch(SnapshotModule,name,'snapshot.'+name)
for name in ['__init__','_verify_integrity','load_content','snapshot']:
 patch(SQLiteSnapshotStore,name,'sqlite.'+name)
patch(tm,'_contracts','facade.contracts')
def op(label,fn):
 global stats,reads,objects,commands,current
 stats={};reads=collections.Counter();objects=collections.Counter();commands=collections.Counter();current=label
 print('START',label,flush=True);t=time.perf_counter();cpu=time.process_time();status='ok'
 try:
  value=fn()
  if isinstance(value,dict) and 'reject' in str(value.get('kind')):status=value.get('code','rejected')
  return value
 except Exception as e:status=type(e).__name__+': '+str(e);raise
 finally:
  row={'operation':label,'wall_s':time.perf_counter()-t,'cpu_s':time.process_time()-cpu,'status':status,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'spans':stats,'git_reads':{'count':sum(reads.values()),'unique':len(reads),'top':reads.most_common(10)},'git_objects':{'count':sum(objects.values()),'unique':len(objects)},'git_commands':dict(commands)}
  log.write(json.dumps(row)+'\n');print('END',label,row['wall_s'],status,flush=True)

def require(value,kind):
 if value.get('kind')!=kind:raise RuntimeError(f'Expected {kind}: {value}')
 return value

for sample in range(a.samples):
 prefix=f's{sample}.';store=out/f'store-{sample}.sqlite3'
 engine=op(prefix+'engine_open_new',lambda:StandardsEngine.open_repository(r,store_path=store,purpose='authoring',execution_context=AnalysisExecutionContext(HarnessAuthorizer())))
 facade=op(prefix+'facade_construct',lambda:AgentToolFacade(engine,tm._contracts(r)))
 created=op(prefix+'create_snapshot',lambda:require(facade.create_snapshot({'kind':'create-snapshot'}),'create-snapshot-result'))
 snapshot=created['snapshot']['snapshot'];(out/f'snapshot-{sample}.json').write_text(json.dumps(snapshot))
 for i in range(3):
  read=op(prefix+f'query_read_{i}',lambda:require(facade.query({'snapshot':snapshot,'request':{'kind':'read','target':'workflow.planning'}}),'read-result'))
 policy=read['policy']['handle']
 op(prefix+'inspect_policy',lambda:facade.inspect({'handle':policy}))
 op(prefix+'route_explicit',lambda:facade.route({'snapshot':snapshot,'facts':{}}))
 request={'kind':'analysis-request','base_snapshot':snapshot,'proposed_snapshot':snapshot,'changes':[{'kind':'modification','accepted_ids':['workflow.planning.written-plan-applicability'],'proposed_ids':['workflow.planning.written-plan-applicability'],'scope':{'kind':'whole-artifact'}}],'semantic_proposals':[],'contract_version':6}
 prepared=op(prefix+'prepare_same_snapshot',lambda:require(facade.prepare({'request':request}),'pending-result'))
 submission=_disposition(c.PendingResult.from_value(prepared)).as_contract()
 resolved=op(prefix+'resolve',lambda:require(facade.resolve(submission),'pending-result'))
 op(prefix+'inspect_analysis',lambda:facade.inspect({'handle':resolved['handle']}))
 op(prefix+'inspect_snapshot',lambda:facade.inspect({'handle':snapshot}))
 capture=engine._snapshots.load_content(engine._snapshot_id(c.SnapshotHandle.from_value(snapshot)))
 (out/f'capture-size-{sample}.json').write_text(json.dumps({'store_bytes':store.stat().st_size,'files':len(capture.files),'content_bytes':sum(len(f.content) for f in capture.files)}))
 op(prefix+'engine_close',engine.close)
 for i in range(2):
  fresh=op(prefix+f'reopen_{i}',lambda:StandardsEngine.open_repository(r,store_path=store,purpose='authoring'))
  fresh_facade=op(prefix+f'reopen_facade_{i}',lambda:AgentToolFacade(fresh,tm._contracts(r)))
  op(prefix+f'reopened_query_{i}',lambda:require(fresh_facade.query({'snapshot':snapshot,'request':{'kind':'read','target':'workflow.planning'}}),'read-result'))
  fresh.close()
if a.profile:
 for owner,name,original,static in reversed(unwrap):setattr(owner,name,staticmethod(original) if static else original)
 src=FrozenContentSource((str(f.path),f.content) for f in capture.files)
 prof=cProfile.Profile();prof.enable();compiled=StandardsEngine._compile(src);prof.disable();prof.dump_stats(str(out/'compile.pstats'))
 with (out/'compile-profile.txt').open('w') as f:pstats.Stats(prof,stream=f).strip_dirs().sort_stats('cumulative').print_stats(70)
 del compiled;gc.collect();tracemalloc.start();before=tracemalloc.get_traced_memory();compiled=StandardsEngine._compile(FrozenContentSource((str(f.path),f.content) for f in capture.files));cur,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 (out/'compiled-memory.json').write_text(json.dumps({'retained_tracemalloc_bytes':cur-before[0],'peak_tracemalloc_bytes':peak-before[0],'capture_bytes':sum(len(f.content) for f in capture.files),'note':'single compilation allocation increment; excludes prior imports and existing captured byte objects; not process RSS cap'},indent=2))
print('DONE',flush=True)
