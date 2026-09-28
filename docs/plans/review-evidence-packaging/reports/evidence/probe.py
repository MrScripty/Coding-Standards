"""Read-only planning probe, not a review-packet implementation or verifier."""
from pathlib import Path
import json, subprocess, hashlib, tempfile, os
from tools.repository_git.repository_git import GitRepository, RepositoryRevision, RepositoryPath
ROOT=Path('/mnt/data/review-packet-planning/repo'); OUT=ROOT.parent/'evidence'
REFS=json.loads((OUT/'example-source-identities.json').read_text())
BASE=REFS['baseline']['commit']; CAND=REFS['candidate']['commit']; REC=REFS['records']['commit']; CI=REFS['ci']['commit']
def run(*args,root=ROOT):return subprocess.check_output(['git','-C',str(root),*args])
def tree(rev):
 result={}
 for row in run('ls-tree','-rz','--full-tree',rev).split(b'\0'):
  if not row:continue
  meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();result[path.decode()]=(mode,kind,oid)
 return result
before=tree(BASE);after=tree(CAND)
changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
context=['tools/standards_contracts/standards_contracts/runtime.py','tools/standards_contracts/standards_contracts/validation_feedback.py','tools/standards_engine/standards_engine/tools.py','tools/standards_engine/standards_engine/contract_discovery.py','tools/standards_analysis/standards_analysis/routing.py']
selected=sorted(set(changes+context)); repo=GitRepository(ROOT);rows=[]
for name,rev,entries in [('baseline',BASE,before),('candidate',CAND,after)]:
 with repo.read_session(RepositoryRevision(rev)) as reader:
  for path in selected:
   if path not in entries:continue
   mode,kind,oid=entries[path];assert mode in ('100644','100755')
   b=reader.read_file(RepositoryPath.parse(path))
   assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
   rows.append({'revision_role':name,'path':path,'mode':mode,'oid':oid,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
report={'kind':'planning-source-selection-probe','requested_change_paths':len(changes),'extra_context_paths':len(context),'selected_source_paths':len(selected),'source_objects':len(rows),'selected_uncompressed_bytes':sum(x['bytes'] for x in rows),'largest_blob_bytes':max(x['bytes'] for x in rows),'full_primary_patch_bytes':REFS['baseline..candidate']['patch_bytes'],'rows':rows}
# Scope equivalence is actually computed, not inferred from commit messages.
report['supplemental_revision_comparisons']=[]
for label,rev in [('ci',CI),('records',REC)]:
 all_changes=REFS['candidate..'+label]['changed_paths'];same_tools=run('rev-parse',CAND+':tools')==run('rev-parse',rev+':tools')
 report['supplemental_revision_comparisons'].append({'role':label,'exact_revision_equal':rev==CAND,'tools_subtree_equal':same_tools,'other_changed_paths':all_changes,'claim_acceptance_inferred':False})
# Isolated fixture exposes why git archive cannot be an exact-file oracle.
with tempfile.TemporaryDirectory(prefix='review-packet-probe-') as tmp:
 p=Path(tmp);subprocess.run(['git','init','-q',str(p)],check=True,capture_output=True)
 def g(*args):return run(*args,root=p)
 g('config','user.name','Planning probe');g('config','user.email','planning@example.invalid')
 (p/'source.txt').write_bytes(b'original source\n');(p/'.gitattributes').write_text('source.txt export-ignore\n')
 g('add','--','.gitattributes','source.txt');g('commit','-qm','probe: exact source')
 revision=RepositoryRevision(g('rev-parse','HEAD').decode().strip()); exact=GitRepository(p)
 (p/'source.txt').write_bytes(b'UNRELATED DIRTY WORK\n');(p/'untracked.zip').write_bytes(b'not selected')
 status=g('status','--porcelain=v1','-z'); index_before=(p/'.git/index').read_bytes()
 observed=exact.read_file(revision,RepositoryPath.parse('source.txt'))
 import io,tarfile
 archive_members=tarfile.open(fileobj=io.BytesIO(g('archive','--format=tar',revision.oid))).getnames()
 assert observed==b'original source\n' and 'source.txt' not in archive_members
 assert (p/'source.txt').read_bytes()==b'UNRELATED DIRTY WORK\n' and (p/'untracked.zip').read_bytes()==b'not selected'
 # Status may refresh its index, so take/read hash around the actual exact read, not git status.
 assert (p/'.git/index').read_bytes()==index_before
 report['isolated_fixture']={'exact_read_ignores_worktree':True,'dirty_untracked_preserved':True,'index_unchanged_during_read':True,'archive_omits_export_ignored_source':True,'not_packet_generator_test':True}
(OUT/'design-probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
