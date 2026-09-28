from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=Path('/mnt/data/review-packet-planning/delivery/docs/plans/review-evidence-packaging')
ids=json.loads(Path('/mnt/data/review-packet-planning/evidence/example-source-identities.json').read_text())
record_base='docs/plans/routing-fact-ergonomics/'
example={
 'format_version':1,'repository_label':'MrScripty/Coding-Standards',
 'label':'routing-fact-source-and-closure-material',
 'review_question':'Inspect the selected routing change and its evidence. This is an assembly example, not a request to reopen accepted work or change a plan status.',
 'revisions':{k:ids[k]['commit'] for k in ('baseline','candidate','ci','records')},
 'plan':{'revision':'candidate','path':record_base+'plan.md'},
 'context':['tools/standards_contracts/standards_contracts/runtime.py','tools/standards_contracts/standards_contracts/validation_feedback.py','tools/standards_engine/standards_engine/tools.py','tools/standards_engine/standards_engine/contract_discovery.py','tools/standards_analysis/standards_analysis/routing.py'],
 'comparisons':[{'revision':'ci','scopes':['tools']},{'revision':'records','scopes':['tools']}],
 'artifacts':[
 {'id':'accepted-plan','role':'acceptance-record','subject':'candidate','origin':{'kind':'git-file','revision':'records','path':record_base+'plan.md'}},
 {'id':'verification','role':'verification-report','subject':'candidate','origin':{'kind':'git-file','revision':'records','path':record_base+'reports/verification.md'}},
 {'id':'external-review','role':'review-recommendation','subject':'candidate','origin':{'kind':'git-file','revision':'records','path':record_base+'reports/external-review.md'}},
 {'id':'live-observation','role':'live-observation','subject':'candidate','origin':{'kind':'git-file','revision':'records','path':record_base+'reports/r2-live-agent.md'}},
 {'id':'dispositions','role':'issue-dispositions','subject':'candidate','origin':{'kind':'git-file','revision':'records','path':record_base+'issues.md'}},
 {'id':'ci-log','role':'ci-log','subject':'ci','origin':{'kind':'local-file','path':'ci/36465019273/job.log'}},
 {'id':'ci-run-reference','role':'ci-reference','subject':'ci','origin':{'kind':'reference','label':'Previously reported routing candidate CI; this example includes only its URL','url':'https://github.com/MrScripty/Coding-Standards/actions/runs/36465019273'}}],
 'claims':[{'id':'R-A'+str(n),'artifacts':(['live-observation'] if n==7 else ['external-review','dispositions','accepted-plan'] if n==8 else ['verification','ci-log','ci-run-reference'])} for n in range(1,9)]
}
# Fixed-shape planning schema: it checks syntax only. Cross-reference, Git,
# filesystem, claim ownership and evidence semantics are not implemented here.
def obj(props,required):return {'type':'object','additionalProperties':False,'properties':props,'required':required}
def arr(item):return {'type':'array','items':item,'maxItems':4096}
s={'type':'string','minLength':1}
label={**s,'pattern':'^[a-z][a-z0-9-]*$'}
ref=obj({'revision':label,'path':s},['revision','path'])
origin={'oneOf':[
 obj({'kind':{'const':'git-file'},'revision':label,'path':s},['kind','revision','path']),
 obj({'kind':{'const':'local-file'},'path':s,'expected_sha256':{'type':'string','pattern':'^sha256:[0-9a-f]{64}$'}},['kind','path']),
 obj({'kind':{'const':'reference'},'label':s,'url':s},['kind','label'])]}
schema={'$schema':'https://json-schema.org/draft/2020-12/schema',**obj({
 'format_version':{'const':1},'repository_label':s,'label':s,'review_question':s,
 'revisions':{'type':'object','minProperties':2,'maxProperties':32,'required':['baseline','candidate'],'propertyNames':label,'additionalProperties':{'type':'string','pattern':'^(?:[0-9a-f]{40}|[0-9a-f]{64})$'}},
 'plan':ref,'context':{**arr(s),'uniqueItems':True},
 'comparisons':arr(obj({'revision':label,'scopes':{**arr(s),'minItems':1,'uniqueItems':True}},['revision','scopes'])),
 'artifacts':arr(obj({'id':label,'role':s,'subject':label,'origin':origin},['id','role','origin'])),
 'claims':arr(obj({'id':s,'artifacts':{**arr(label),'uniqueItems':True}},['id','artifacts']))},['format_version','repository_label','label','review_question','revisions','plan','context','comparisons','artifacts','claims'])}
Draft202012Validator.check_schema(schema);v=Draft202012Validator(schema);v.validate(example)
from copy import deepcopy
negative=[]
for name,change in [('old-version',lambda x:x.update(format_version=2)),('branch-in-place-of-oid',lambda x:x['revisions'].update(candidate='main')),('arbitrary-command',lambda x:x.update(run=['pytest'])),('mixed-evidence-origin',lambda x:x['artifacts'][0]['origin'].update(url='https://example.invalid/source')),('extra-top-level-policy',lambda x:x.update(acceptance='Accepted'))]:
 bad=deepcopy(example);change(bad);assert not v.is_valid(bad),name;negative.append(name)
(ROOT/'reports/example-request.json').write_text(json.dumps(example,indent=2)+'\n')
(ROOT/'reports/request-shape.json').write_text(json.dumps(schema,indent=2)+'\n')
(ROOT/'reports/evidence/request-shape-check.json').write_text(json.dumps({'status':'passed','scope':'proposed request shape only; not packet-code or cross-reference validation','example_valid':True,'negative_shapes_rejected':negative},indent=2)+'\n')
print('Example and proposed schema valid; five malformed shapes rejected.')
