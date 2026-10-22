import json, os, subprocess, time
from pathlib import Path
root=Path('/tmp/coding-standards-observation-o1')
python='/home/jeremy/.local/share/standards-engine/venv/bin/python'
packages=['standards_identity','standards_applicability','graph_engine','standards_graph','standards_snapshots','repository_git','review_evidence','standards_metadata','standards_policy_impact','standards_contracts','standards_analysis','standards_verifier']
results=[]
for package in packages:
 start=time.monotonic()
 log=Path('/tmp/observation-final-'+package+'.log')
 print('START',package,flush=True)
 env={**os.environ,'PYTHONPATH':'.:tools/standards_verifier' if package=='standards_verifier' else '.', 'PYTHONDONTWRITEBYTECODE':'1'}
 with log.open('w') as output:
  code=subprocess.run([python,'-m','unittest','discover','-s',f'tools/{package}/tests'],cwd=root,env=env,stdout=output,stderr=subprocess.STDOUT).returncode
 row={'package':package,'exit_code':code,'seconds':round(time.monotonic()-start,3),'log':str(log)}
 results.append(row)
 Path('/tmp/observation-final-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print('END',json.dumps(row),flush=True)
raise SystemExit(any(row["exit_code"] for row in results))
