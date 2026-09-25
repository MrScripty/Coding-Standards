"""External observation only. Repository assertions and production behavior remain intact."""
from __future__ import annotations
import argparse,collections,functools,json,os,sys,threading,time,traceback,unittest
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--output',required=True);p.add_argument('--pattern',default='test*.py');p.add_argument('--test');p.add_argument('--exclude');a=p.parse_args()
r=Path(a.repo).resolve();os.chdir(r);sys.path[:0]=[str(r),str(r/'tools/standards_engine/tests'),str(r/'tools/standards_verifier')];os.environ['PYTHONPATH']=os.pathsep.join(sys.path[:3]);os.environ['PYTHONDONTWRITEBYTECODE']='1'
f=Path(a.output).open('w',buffering=1);start=time.perf_counter();phase={};counts={};main_thread=threading.get_ident();active={'test':'collection/fixture','start':time.perf_counter()};finished=threading.Event()
def emit(value):f.write(json.dumps(value)+'\n')
def monitor():
 while not finished.wait(45):
  frame=sys._current_frames().get(main_thread)
  emit({'event':'observation','test':active['test'],'elapsed_s':time.perf_counter()-active['start'],'stack':traceback.format_stack(frame) if frame else []})
threading.Thread(target=monitor,daemon=True).start()
from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine import engine as em
from tools.standards_engine.standards_engine.authoring import AuthoringModule
from tools.standards_snapshots.standards_snapshots.module import SnapshotModule
from tools.standards_engine.standards_engine import tools as tm

def patch(owner,name,static=False):
 original=getattr(owner,name);label=owner.__name__+'.'+name
 @functools.wraps(original)
 def observe(*args,**kwargs):
  t=time.perf_counter()
  try:return original(*args,**kwargs)
  finally:
   s=counts.setdefault(label,{'calls':0,'inclusive_s':0.});s['calls']+=1;s['inclusive_s']+=time.perf_counter()-t
 setattr(owner,name,staticmethod(observe) if static else observe)
for n in ['_compiled_snapshot','_proposal_projection','_validate_projected_inputs','_evaluate','prepare','resolve','propose','revise','analyze_proposal','query_proposal','review_proposal','apply_proposal','verify_proposal']:
 patch(StandardsEngine,n)
patch(StandardsEngine,'_compile',True);patch(SnapshotModule,'_content_id',True);patch(SnapshotModule,'load_content');patch(AuthoringModule,'read_revision');patch(tm,'_contracts')
for method,label in [('_callSetUp','setup_s'),('_callTestMethod','body_s'),('_callTearDown','teardown_s')]:
 original=getattr(unittest.TestCase,method)
 def timed(self,*args,_fn=original,_label=label,**kwargs):
  t=time.perf_counter()
  try:return _fn(self,*args,**kwargs)
  finally:phase.setdefault(self.id(),{})[_label]=time.perf_counter()-t
 setattr(unittest.TestCase,method,timed)
class Result(unittest.TextTestResult):
 def startTest(self,test):
  global counts
  counts={};super().startTest(test);self.started=time.perf_counter();self.cpu=time.process_time();self.result='pass';active.update(test=test.id(),start=self.started)
  emit({'event':'start','test':test.id(),'at':time.time()});print('START',test.id(),flush=True)
 def addError(self,*args):self.result='error';super().addError(*args)
 def addFailure(self,*args):self.result='failure';super().addFailure(*args)
 def addSkip(self,*args):self.result='skip';super().addSkip(*args)
 def stopTest(self,test):
  row={'event':'end','test':test.id(),'wall_s':time.perf_counter()-self.started,'cpu_s':time.process_time()-self.cpu,'status':self.result,'spans':counts,**phase.get(test.id(),{})}
  emit(row);print('END',test.id(),round(row['wall_s'],3),self.result,flush=True);super().stopTest(test);active.update(test='between-test/fixture',start=time.perf_counter())
excluded=set(json.loads(Path(a.exclude).read_text())) if a.exclude else set()
def leaves(suite):
 for v in suite:
  if isinstance(v,unittest.TestSuite):yield from leaves(v)
  else:yield v
suite=unittest.defaultTestLoader.loadTestsFromName(a.test) if a.test else unittest.defaultTestLoader.discover(str(r/'tools/standards_engine/tests'),pattern=a.pattern)
suite=unittest.TestSuite(v for v in leaves(suite) if v.id() not in excluded)
try:
 result=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(suite)
 emit({'event':'summary','total_s':time.perf_counter()-start,'run':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'skips':len(result.skipped)})
 code=int(not result.wasSuccessful())
except BaseException:
 emit({'event':'runner-exception','traceback':traceback.format_exc()});code=2
finally:finished.set()
sys.exit(code)
