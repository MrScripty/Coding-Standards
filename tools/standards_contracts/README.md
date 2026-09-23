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
