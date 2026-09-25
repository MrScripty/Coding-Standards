"""Repeat three fixture-branch failures with the documented disposable main checkout."""
import json,os,subprocess,sys,time
from pathlib import Path
W=Path('/mnt/data/engine-performance');E=W/'evidence';root=W/'benchmark-checkout';repo=W/'qualified-main-checkout'
subprocess.run(['git','clone','--local','--quiet','--branch','implementation/purpose-separated-standards-engine',str(root),str(repo)],check=True)
subprocess.run(['git','-C',str(repo),'checkout','-b','main','HEAD'],check=True,stdout=subprocess.DEVNULL)
tests=[
 ('qualified_apply_topology','test_analysis.AnalysisWorkflowTest.test_apply_create_and_retire_owns_topology_and_commit'),
 ('qualified_apply_cold','test_analysis.AnalysisWorkflowTest.test_apply_proposal_composes_real_verification_and_cold_readback'),
 ('qualified_audit','test_coverage_publication.EngineAuditPublicationTest.test_review_verify_apply_recover_and_read_without_original_database')]
for label,test in tests:
 t=time.time()
 with (E/f'{label}.stdout').open('w') as out,(E/f'{label}.stderr').open('w') as err:
  rc=subprocess.call([sys.executable,'-u',str(W/'harness/run_timed_suite.py'),'--repo',str(repo),'--output',str(E/f'{label}.jsonl'),'--test',test],stdout=out,stderr=err,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 (E/f'{label}.exit.json').write_text(json.dumps({'returncode':rc,'elapsed_s':time.time()-t,'test':test,'qualification':'same source SHA; disposable checkout on local main, so nested test clones create main'}))
