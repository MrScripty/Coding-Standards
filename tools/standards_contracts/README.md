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
application variant, while authoring uses the base operation. Transport code
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
