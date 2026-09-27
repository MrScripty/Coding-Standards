# Standards Contracts

`standards_contracts` is the A1b boundary for canonical contract validation and
public projection compilation. Draft 2020-12 behavior is delegated unchanged
to `jsonschema.Draft202012Validator`; immutable same-resource reference
resolution is delegated to `referencing`.

The Module compiles the canonical schema and closed interface together:

```python
compiled = compile_contracts(schema, interface)
compiled.validate("QueryCall", value)
artifacts = compiled.project()
```

Compilation self-checks the Draft schema, builds a retrieval-free local
resource registry, proves exact public-root reachability, admits only the
reviewed projection profile, and verifies capability coverage. Validation
errors are adapted into stable `ContractFailure` values.

`ProjectionArtifacts` contains deterministic staging Python and agent-tool
projections. Generated models are immutable and call the same compiled
validator before construction; they contain no JSON Schema keyword evaluator.
Schema defaults remain annotations and never inject values.

Install the complete admitted dependency closure with:

```sh
python -m pip install \
  --require-hashes \
  --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Runtime retrieval, custom vocabularies, validator keyword overrides, and a
repository implementation of JSON Schema are outside this module.

## Named operation variants

An operation may declare named input/result variants in the canonical interface.
Their roots participate in the same exact reachable schema closure and generated
projection. Variants select wire shape; their names do not grant permissions or
change the operation's capability authority. The Engine host selects the
application variant; the authoring facade selects the agent input variant where
declared and normalizes it to the base domain operation. Transport code
consumes these definitions rather than maintaining a second schema.

## Post-validation union construction

`ContractRuntime` keeps complete root validation as the instance-acceptance
boundary. It derives construction selectors from its private schema copy for
object unions whose branches share a required string property with disjoint
`const` or all-string `enum` values. After the root succeeds, that property
selects the original branch (and its generated type) without repeating branch
validation. Direct generated-model construction uses the same root boundary.

The selector planner follows only bare same-resource definition aliases.
Overlapping or absent tags, optional tags, scalar unions, reference siblings,
and unrecognized forms retain the existing validator-backed selection path.
Nested resource scopes also retain that path. These restrictions limit an
optimization; they neither expand nor narrow the admitted schema profile.

Selectors belong to one runtime and its copied schema, not to a request or
process-global cache. They retain no instance values. Schema changes construct
new selectors; current permission, lifecycle, and publication decisions remain
outside this module. Error adaptation, strict JSON checks, omission, defaults,
and generated serialization keep their existing owners.

## Schema structure and projection ownership

`schema_structure.py` owns structural traversal and same-resource definition
closure for the admitted projection profile. The compiler's profile check,
reachability analysis, post-validation union selectors, MCP schema presentation
and CLI inspection share that owner. Property maps are traversed through their
values; field names such as `$ref` are ordinary names. `const`, `enum` and
`default` payloads are copied as instance data, never dereferenced. The traversal
also recognizes `allOf` as a structural schema position; this neither admits
`allOf` in canonical contracts nor implements its evaluation.
Canonical admission remains closed in the compiler. Validation and reference
semantics remain with jsonschema/referencing, including recursive validation.

`schema_closure` returns an independent standalone schema. The lower-level
`referenced_definitions` selects borrowed definitions without mutating them.
Neither helper loads resources or creates a second validator.

Generated Python preserves wire names through its explicit field mapping. Existing
ordinary Python names retain their spelling; invalid identifiers, names subject
to Python lexical normalization and class-private names use a deterministic
UTF-8 hex escape. Per-object collision checks also apply to escaped names.
Defaults remain annotations and never inject values into decoded requests.


## Safe input feedback

Rejected runtime inputs retain the existing ContractFailure and first-error cause
tree and add bounded InputIssue observations. The canonical jsonschema validator
owns acceptance. `validation_feedback.py` selects relevant causes only through a
proven disjoint tag, otherwise reporting the ambiguous union. It never chooses a
valid branch or accepts input. Declared field pointers/constraints are projected
without instance values or arbitrary map keys. Missing fields are deduplicated;
item, byte and work bounds are explicit. The Engine facade owns its public rejection
and discovery wrapper. No diagnostic work runs for a valid request.


## Native-only catalog consumer

Interface 43 consumes `schema_closure` directly for MCP inputs. The former
`map_schema_children` export and transform-only tests are removed with their sole
production consumer, the recursive input inliner. Structural location/reference
APIs remain retrieval-free and preserve literals, annotations, schema-bearing
property names and recursive closure. Recognizing `allOf` as a structural schema
position does not admit it to the compiler's canonical vocabulary or implement
constraint evaluation; `jsonschema` remains the independent semantics owner.

## Validated numeric representation and digest constraint

After full instance validation, integer-constrained positions normalize integral
floats to Python integers. Named and anonymous properties, map entries, arrays,
references and selected union branches follow their own declared schemas. Integers
already represented as Python integers retain arbitrary precision. Booleans,
fractions and non-finite JSON numbers are rejected where invalid before construction.
Number-only and unconstrained positions remain uncoerced, including numeric values
inside opaque literals with no integer schema. Schema const/enum/default documents
are never modified. Defaults do not inject values and caller-owned inputs remain
unchanged.

`maxLength` is part of the admitted projection profile; its semantics belong to
the existing Draft 2020-12 validator. Interface 44's canonical Digest uses it with
the lowercase SHA-256 pattern to exclude trailing data, including a final newline.
Generated tools/models preserve this constraint without a local keyword evaluator.
