import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
W=Path('/mnt/data/engine-performance'); E=W/'evidence'; H=W/'harness';root=W/'benchmark-checkout';env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
pid=int((E/'operations.pid').read_text())
while Path(f'/proc/{pid}/stat').exists() and Path(f'/proc/{pid}/stat').read_text().split()[2]!='Z':time.sleep(2)
slow='test_agent_workflow.AgentWorkflowTest.test_normative_proposal_stops_at_real_pending_work'
def run(label,args,repo):
 t=time.time()
 with (E/f'{label}.stdout').open('w') as out,(E/f'{label}.stderr').open('w') as err:
  code=subprocess.call([sys.executable,'-u',str(H/'run_timed_suite.py'),'--repo',str(repo),'--output',str(E/f'{label}.jsonl'),*args],stdout=out,stderr=err,env=env)
 (E/f'{label}.exit.json').write_text(json.dumps({'returncode':code,'elapsed_s':time.time()-t,'args':args}))
 return code
run('slow-case-isolated',['--test',slow],root)
excluded=json.loads((E/'completed-original.json').read_text());excluded.append(slow);(E/'completed-for-parallel.json').write_text(json.dumps(excluded))
patterns=[p.name for p in (root/'tools/standards_engine/tests').glob('test*.py') if p.name!='test_agent_navigation.py']
patterns.sort(key=lambda v:({'test_analysis.py':0,'test_navigation_indexes.py':1,'test_logical_authoring.py':2,'test_supporting_workflow.py':3}.get(v,4),v))
def module(pattern):
 label=pattern[:-3];repo=W/'module-checkouts'/label
 repo.parent.mkdir(exist_ok=True)
 subprocess.run(['git','clone','--local','--quiet','--branch','implementation/purpose-separated-standards-engine',str(root),str(repo)],check=True)
 subprocess.run(['git','-C',str(repo),'branch','main','HEAD'],check=True)
 return run(label,['--pattern',pattern,'--exclude',str(E/'completed-for-parallel.json')],repo)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=dict(zip(patterns,ex.map(module,patterns)))
(E/'parallel-summary.json').write_text(json.dumps(results,indent=2))
