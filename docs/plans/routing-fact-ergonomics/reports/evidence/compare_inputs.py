"""Planning-only projection experiment; never edits source or publishes standards.

Run from the exact baseline checkout, with PYTHONPATH set to that checkout. This
prototype proposes a wire grammar and exercises existing binders/evaluators. It
is not a candidate implementation or actual model/host qualification.
"""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
import json, sys, tomllib
from jsonschema import Draft202012Validator
from tools.standards_contracts.standards_contracts import compile_contracts, schema_closure
from tools.standards_applicability.standards_applicability import ApplicabilityError, ApplicabilityFailure, compile_fact_schema
from tools.standards_applicability.tests.test_applicability import declaration
from tools.standards_engine.standards_engine import StandardsEngine, AgentToolFacade
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog

ROOT=Path.cwd(); OUT=Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
base=AgentToolFacade.load_interface(ROOT)
assert base.interface.interface_schema_version==44
value_schema={'oneOf':[
 {'type':'boolean'}, {'type':'null'}, {'type':'string'},
 {'type':'array','items':{'type':'string'},'uniqueItems':True},
 {'type':'object','additionalProperties':False,'required':['state'],
  'properties':{'state':{'enum':['known-absent','unknown']}}},
]}
assertions_schema={'type':'object','additionalProperties':deepcopy(value_schema)}
validator=Draft202012Validator(assertions_schema)
canonical_validator=Draft202012Validator(schema_closure(base.schema['$defs']['FactSet'],base.schema['$defs']))

# A planning-only type completion. The implementation plan requires shared
# authoritative lookup/error ownership instead of copying this error construction.
def lower(schema, values):
 validator.validate(values)
 expanded={}
 for name, value in values.items():
  definition=schema.resolve(name)
  if definition is None:
   raise ApplicabilityError(ApplicabilityFailure('APPLICABILITY.INVALID','invalid',
       'fact is not declared by the applicability schema',field=name))
  expanded[name]=({'type':definition.type, **deepcopy(value)} if isinstance(value,dict)
                  else {'type':definition.type,'state':'known','value':deepcopy(value)})
 return expanded

def compact(typed):
 return {name: deepcopy(v['value']) if v['state']=='known' else {'state':v['state']}
         for name,v in typed.items()}

def bound_json(bound): return {k:v.as_contract() for k,v in bound.canonical_values.items()}

def observe(schema, values):
 try: return {'status':'bound','values':bound_json(schema.bind(values))}
 except ApplicabilityError as error: return {'status':'rejected','failure':asdict(error.failure)}

specs=[
 {'id':'enabled','type':'boolean','nullable':False,'aliases':['on']},
 {'id':'mode','type':'enum','nullable':False,'values':['x','y'],'aliases':['m']},
 {'id':'text','type':'string','nullable':True,'aliases':[]},
 {'id':'names','type':'string-set','nullable':False,'aliases':[]},
 {'id':'tags','type':'enum-set','nullable':True,'values':['x','y'],'aliases':[]},
 {'id':'artifact','type':'canonical-id','nullable':False,'aliases':[]},
]
schema=compile_fact_schema(declaration(specs))
cases=[]
for definition in specs:
 for raw in (True,False,None,'','x','unknown','known-absent','x.y',[],['x'],['y','x'],['x','x'],[''],0,1,1.5,{}, {'state':'known-absent'}, {'state':'unknown'}, {'state':'known'}, {'state':'unknown','value':None}):
  name=definition['id']; new={name:raw}
  old={name: {'type':definition['type'], **raw} if isinstance(raw,dict)
               else {'type':definition['type'],'state':'known','value':raw}}
  static_new=validator.is_valid(new);static_old=canonical_validator.is_valid(old)
  # Validity must agree after snapshot type completion; generic raw shapes can
  # pass the new static stage before their registered type is known.
  old_valid=static_old and observe(schema,old)['status']=='bound'
  new_result=observe(schema,lower(schema,new)) if static_new else {'status':'static-rejected'}
  new_valid=new_result['status']=='bound'
  assert old_valid==new_valid,(new,old,old_valid,new_result)
  if new_valid:
   assert new_result==observe(schema,old),(new,old)
   assert compact(new_result['values'])==compact(observe(schema,old)['values'])
  cases.append({'case':new,'old_static':static_old,'new_static':static_new,
                'equivalent_final_validity':True,'final_status':new_result['status']})
# Literal expected states, not only converter roundtrips.
expected={
 'omitted': ({},'unknown'),
 'false': ({'enabled':False},'true'),
 'empty': ({'names':[]},'true'),
 'null': ({'text':None},'true'),
 'absent': ({'text':{'state':'known-absent'}},'false'),
 'unknown': ({'text':{'state':'unknown'}},'unknown'),
}
state_cases=[]
for label,(data,truth) in expected.items():
 target=next(iter(data),'text');bound=schema.bind(lower(schema,data))
 result=schema.compile({'operator':'exists','fact':target}).evaluate(bound)
 assert result.truth.value==truth,(label,result)
 state_cases.append({'case':label,'input':data,'exists':truth,'canonical':bound_json(bound)})
# Alias collisions stay collisions, never last-writer-wins.
aliases=[]
for data in ({'on':True},{'enabled':True,'on':True},{'enabled':True,'on':{'state':'unknown'}}):
 observed=observe(schema,lower(schema,data));aliases.append({'input':data,'result':observed})
assert aliases[0]['result']['values']=={'enabled':{'type':'boolean','state':'known','value':True}}
assert all(x['result']['status']=='rejected' for x in aliases[1:])
# The same shorthand is bound against the actual selected schema, not Python types.
s2=compile_fact_schema(declaration([{'id':'mode','type':'boolean','nullable':False,'aliases':[]}]))
assert observe(schema,lower(schema,{'mode':'x'}))['status']=='bound'
assert observe(s2,lower(s2,{'mode':'x'}))['status']=='rejected'
assert schema.digest!=s2.digest

proposed=base.schema
proposed['$defs']['RoutingFactAssertion']=deepcopy(value_schema)
proposed['$defs']['RoutingFactAssertions']={'type':'object','additionalProperties':{'$ref':'#/$defs/RoutingFactAssertion'}}
for name in ('RouteCall','CompactRouteResult','AgentRouteResult'):
 proposed['$defs'][name]['properties']['facts']={'$ref':'#/$defs/RoutingFactAssertions'}
manifest=tomllib.loads((ROOT/'tools/standards_engine/contracts/a1-interface.toml').read_text())
manifest['interface_schema_version']=45
candidate=compile_contracts(proposed,manifest)
# Python projection generation must be available; no generated files are installed.
projection=candidate.project();assert 'RoutingFactAssertions' in projection.python_source
catalog_metrics={}
for purpose in ('authoring','application'):
 for delivery in ('eager','on-demand'):
  old=tool_catalog(base,purpose=purpose,output_schemas=delivery)
  new=tool_catalog(candidate,purpose=purpose,output_schemas=delivery)
  old_route=next(t for t in old if t['name']=='route')
  new_route=next(t for t in new if t['name']=='route')
  catalog_metrics[purpose+'/'+delivery]={
   'old_tool_count':len(old),'new_tool_count':len(new),
   'old_catalog_json_bytes':len(json.dumps(old).encode()),'new_catalog_json_bytes':len(json.dumps(new).encode()),
   'old_route_input_json_bytes':len(json.dumps(old_route['inputSchema']).encode()),
   'new_route_input_json_bytes':len(json.dumps(new_route['inputSchema']).encode()),
  }

with StandardsEngine.open_repository(ROOT,purpose='authoring',durable=False) as engine:
 f=AgentToolFacade(engine,base)
 vocabulary=f.routing_facts({})
 assert vocabulary['kind']=='routing-facts-result',vocabulary
 sid=vocabulary['snapshot']
 # Routing the planning task uses its actual facts, not an all-empty task.
 task={'activities':['planning','verification','documentation','uncertainty-reduction'],
       'applications':['library'],'boundaries':['generated-contract','ipc'],
       'workflow-profiles':[], 'languages':[], 'frameworks':[],
       'topics':['architecture','contracts','diagnostics','performance','security'],
       'details':['topic.code-design','topic.contracts.schemas','topic.contracts.protocols','topic.contracts.evolution','workflow.verification.oracles']}
 task_values={'routing.'+k:{'type':'enum-set','state':'known','value':v} for k,v in task.items()}
 routed=f.route({'snapshot':sid,'facts':task_values})
 assert routed['kind']=='compact-route-result' and not routed['unresolved_questions'],routed
 readback=f.read_many({'snapshot':sid,'items':[{'target':entry['target']} for entry in routed['reading_plan']]})
 assert readback['kind']=='read-many-result',readback
 (OUT/'standards-route.json').write_text(json.dumps(routed,indent=2)+'\n')
 (OUT/'standards-readback.json').write_text(json.dumps(readback,indent=2)+'\n')
 capture=engine._compiled_snapshot(engine._snapshot_id(__import__('tools.standards_engine.standards_engine._generated_contract',fromlist=['SnapshotHandle']).SnapshotHandle.from_value(sid)))
 actual_schema=capture.router.fact_schema
 examples=[]
 empty_all={x['id']:[] for x in vocabulary['facts']}
 observed_tasks=[{}, {'routing.activities':['implementation'],'routing.applications':[]},
                 empty_all,{**empty_all,'routing.activities':['implementation'],'routing.boundaries':['ipc']},
                 {'routing.activities':{'state':'unknown'}}, {'routing.activities':{'state':'known-absent'}}]
 for values in observed_tasks:
  canonical=lower(actual_schema,values)
  out=f.route({'snapshot':sid,'facts':canonical})
  assert out['kind']=='compact-route-result',out
  roundtrip=lower(actual_schema,compact(out['facts']))
  again=f.route({'snapshot':sid,'facts':roundtrip})
  assert out==again
  original_request={'facts':canonical};proposed_request={'facts':values}
  examples.append({'input':values,'old_request_json_bytes':len(json.dumps(original_request).encode()),
   'new_request_json_bytes':len(json.dumps(proposed_request).encode()),
   'selected_targets':[v['target'] for v in out['reading_plan']],
   'questions':len(out['unresolved_questions']),'normalized_facts_preserved':True,
   'same_current_engine_result_on_roundtrip':True})

(OUT/'proposed-schema.json').write_text(json.dumps({'RoutingFactAssertion':value_schema,'RoutingFactAssertions':proposed['$defs']['RoutingFactAssertions']},indent=2)+'\n')
report={'basis_commit':'ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76','prototype_only':True,
 'deployed_candidate_tested':False,'model_or_host_qualification':False,
 'synthetic_binding_cases':len(cases),'valid_cases':sum(x['final_status']=='bound' for x in cases),
 'shape_vs_semantic_stage_changes':sum(x['old_static']!=x['new_static'] for x in cases),
 'state_cases':state_cases,'alias_cases':aliases,'snapshot_specific_type_binding':True,
 'canonical_definitions_unchanged_except_focused_route': ['RouteCall','CompactRouteResult','AgentRouteResult'],
 'catalogs':catalog_metrics,'route_examples':examples,'cases':cases,
 'scope':'A planning prototype delegates to current schema binding/evaluation. It is not an integrated candidate or proof of unchanged transport/error handling.'}
(OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('cases','alias_cases','state_cases')},indent=2))
