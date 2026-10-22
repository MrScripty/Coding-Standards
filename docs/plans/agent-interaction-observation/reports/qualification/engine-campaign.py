import json, os, subprocess, time
from pathlib import Path
root=Path('/tmp/coding-standards-observation-o1')
python='/home/jeremy/.local/share/standards-engine/venv/bin/python'
packages=['standards_engine']
results=json.loads(Path('/tmp/observation-ci-results.json').read_text())[:12]
for package in packages:
 start=time.monotonic()
 log=Path('/tmp/observation-ci-'+package+'.log')
 print('START',package,flush=True)
 env={**os.environ,'PYTHONPATH':'.:tools/standards_verifier' if package=='standards_verifier' else '.', 'PYTHONDONTWRITEBYTECODE':'1'}
 with log.open('w') as output:
  code=subprocess.run([python,'-m','unittest','discover','-s',f'tools/{package}/tests','-v'],cwd=root,env=env,stdout=output,stderr=subprocess.STDOUT).returncode
 row={'package':package,'exit_code':code,'seconds':round(time.monotonic()-start,3),'log':str(log)}
 results.append(row)
 Path('/tmp/observation-ci-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print('END',json.dumps(row),flush=True)
print('START complete-verifier',flush=True)
with Path('/tmp/observation-ci-complete.log').open('w') as output:
 code=subprocess.run([python,'tools/standards_verifier/verify.py','--complete'],cwd=root,env={**os.environ,'PYTHONPATH':'.:tools/standards_verifier','PYTHONDONTWRITEBYTECODE':'1'},stdout=output,stderr=subprocess.STDOUT).returncode
results.append({'package':'complete-verifier','exit_code':code,'log':'/tmp/observation-ci-complete.log'})
Path('/tmp/observation-ci-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('END complete-verifier',code,flush=True)
raise SystemExit(any(row['exit_code'] for row in results))
