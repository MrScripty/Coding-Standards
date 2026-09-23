"""External timing runner; repository tests and assertions stay unchanged."""
import argparse, faulthandler, json, os, sys, time, unittest
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); p.add_argument('--output',required=True); p.add_argument('--pattern',default='test*.py'); p.add_argument('--test'); a=p.parse_args()
r=Path(a.repo).resolve(); os.chdir(r); sys.path[:0]=[str(r),str(r/'tools/standards_engine/tests'),str(r/'tools/standards_verifier')]
os.environ['PYTHONPATH']=os.pathsep.join(sys.path[:3]); os.environ['PYTHONDONTWRITEBYTECODE']='1'
log=Path(a.output).open('w',buffering=1); phases={}
for method,label in [('_callSetUp','setup'),('_callTestMethod','body'),('_callTearDown','teardown')]:
 original=getattr(unittest.TestCase,method)
 def timed(self,*args,_fn=original,_label=label,**kwargs):
  t=time.perf_counter()
  try: return _fn(self,*args,**kwargs)
  finally: phases.setdefault(self.id(),{})[_label]=time.perf_counter()-t
 setattr(unittest.TestCase,method,timed)
class TimingResult(unittest.TextTestResult):
 def startTest(self,test):
  super().startTest(test); self.started=time.perf_counter(); self.cpu=time.process_time(); self.result='pass'
  log.write(json.dumps({'event':'start','test':test.id(),'at':time.time()})+'\n')
  print('START',test.id(),flush=True); faulthandler.dump_traceback_later(60,repeat=True)
 def addError(self,*args): self.result='error'; super().addError(*args)
 def addFailure(self,*args): self.result='failure'; super().addFailure(*args)
 def addSkip(self,*args): self.result='skip'; super().addSkip(*args)
 def stopTest(self,test):
  faulthandler.cancel_dump_traceback_later(); elapsed=time.perf_counter()-self.started
  record={'event':'end','test':test.id(),'wall_s':elapsed,'cpu_s':time.process_time()-self.cpu,'status':self.result,**phases.get(test.id(),{})}
  log.write(json.dumps(record)+'\n'); print('END',test.id(),f'{elapsed:.3f}s',self.result,flush=True); super().stopTest(test)
faulthandler.enable()
t=time.perf_counter(); suite=unittest.defaultTestLoader.loadTestsFromName(a.test) if a.test else unittest.defaultTestLoader.discover(str(r/'tools/standards_engine/tests'),pattern=a.pattern)
result=unittest.TextTestRunner(verbosity=1,resultclass=TimingResult).run(suite)
log.write(json.dumps({'event':'summary','total_s':time.perf_counter()-t,'run':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'skips':len(result.skipped)})+'\n')
sys.exit(not result.wasSuccessful())
