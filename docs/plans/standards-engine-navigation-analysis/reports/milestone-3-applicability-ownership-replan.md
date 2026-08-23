# Milestone 3 Applicability Ownership Replan

## Trigger

The compiled policy-impact proposal must validate typed applicability before
it can produce accepted semantics. The existing evaluator is owned by
`standards_analysis`, which now consumes compiled policy impact. Importing it
would create a dependency cycle. Retaining the policy compiler's private
parser would leave two executable meanings for the same language.

## Accepted Design

Introduce one standard-library-only `standards_applicability` Module. Its
Interface compiles one typed fact schema, compiles many immutable expression
programs against that schema, binds one immutable fact set per request, and
evaluates many programs against that fact set.

```python
schema = compile_fact_schema(declaration)
program = schema.compile(expression)
facts = schema.bind(raw_facts)
result = program.evaluate(facts)
```

The Module owns executable operator semantics, normalization, type checking,
three-valued truth tables, unresolved-fact calculation, schema compatibility,
canonical program serialization, dependency digests, and typed applicability
failures. It has no filesystem, TOML, JSON, graph, metadata, analyzer, engine,
or verifier dependency.

The canonical A1 JSON Schema remains authority for serialized expression,
fact, and result shapes. Runtime coverage is mechanically checked against that
schema; Python classes do not generate or redefine it. Repository adapters own
TOML or JSON loading. Router and analysis policy own questions. Downstream
callers translate neutral failures into their diagnostics.

## Interface Contract

- Empty fact schemas are valid. `always` references no facts and evaluates to
  `true` under an empty schema.
- Fact aliases resolve during schema compilation and binding. Supplying an
  alias together with its canonical ID is invalid.
- Missing and explicitly unknown facts remain distinct inputs but produce
  `unknown` when material. Evaluation reports the exact canonical unresolved
  fact IDs that determine an unknown result.
- Known nullable values, known absence, and unknown are distinct states.
- Unknown operators, invalid arity, undeclared facts, type errors, and values
  outside enum domains are invalid. Unsupported language versions are a
  distinct unsupported failure.
- A program accepts only a fact set bound by the exact same schema digest.
- Program identity binds the language version, normalized expression, and
  referenced fact definitions using domain-separated canonical serialization.
- `all`, `any`, and `not` use explicit Kleene three-valued truth tables and
  never coerce unknown to true or false.

## Dependency Direction

```text
standards_applicability
  `-- Python standard library

standards_policy_impact
  |-- standards_applicability
  |-- standards_metadata
  `-- graph_engine

standards_analysis
  |-- standards_applicability
  |-- standards_policy_impact
  |-- standards_metadata
  `-- graph_engine
```

`standards_engine` composes accepted lower Modules. The verifier consumes
compiled policy-impact and applicability results. Neither lower Module depends
on those consumers.

## Replacement Slice

1. Revise the ADR and active plan before code changes.
2. Implement the neutral Interface, typed failures, truth tables, and identity
   contract.
3. Replace the policy fact ID list with a typed, possibly empty schema.
4. Compile Router rules and policy-impact declarations into programs.
5. Bind Router facts once per request and evaluate every route program.
6. Store `ApplicabilityProgram` in `PolicyImpactSemantics`; analysis and
   verifier consume it without reparsing.
7. Delete the policy compiler's private parser and
   `standards_analysis.applicability` with no compatibility re-export.
8. Prove serialized-schema/runtime agreement and prior Router behavior.

## Verification

Evidence must cover every operator; every fact type and state; aliases and
conflicts; enum domains; empty-schema `always`; invalid versus unsupported;
schema mismatch; canonical serialization and digest stability; exact
unresolved facts under nested truth tables; Router parity; conditional
policy-impact compilation and evaluation; analysis obligation generation; and
verifier consumption.

## Replan Triggers

Re-plan if the neutral Module requires repository loading, graph or metadata
knowledge, verifier diagnostics, a second serialized contract, caller-specific
question text, or a compatibility parser; if one accepted JSON shape cannot
represent the required runtime values; or if Router and policy-impact require
incompatible applicability semantics.
