# Schema-directed post-validation decoding

**Status:** implemented; focused and canonical contract tests pass in the recorded
local environment. Supported-runtime, installed Engine, and complete repository
qualification remain pending.

**Base:** `MrScripty/Coding-Standards`, branch
`implementation/purpose-separated-standards-engine`, commit
`bf1358c81a0fa1c59019a4b30682c39c62126d7f`, tree
`5c07a26bde3a4dd48973d52c88ad057e80b00caf`.

## Outcome and write scope

Reduce repeated `oneOf` branch validation while constructing generated models
from a root value that has already passed the canonical validator. This is the
schema-directed decoder increment selected after successor construction; it
contains no snapshot-identity, suite-manifest incrementality, or general compiler
optimization.

The production write set is `standards_contracts/runtime.py` and the new internal
`standards_contracts/union_selection.py`. The package README, two focused test
modules, this report, and the measurement runner complete the seven-file update.
Canonical schemas, interface declarations, generated models/tool definitions,
dependency locks, public exports, persisted formats, and version domains are
unchanged. No remote branch, accepted main, user store, or installed client was
modified by this delivery.

## Design and deciding correctness argument

`ContractRuntime` still calls its existing root validator before decoding, and
`normalize_model` still validates the complete generated-model wire value before
normalizing its fields. Strict JSON checks, reference resolution, diagnostics,
optional-field omission, schema-default annotations, and model construction keep
their existing implementation owners.

On runtime construction, the selector planner reads the runtime's private copied
schema. It admits a table only when every alternative is explicitly an object
and all alternatives share a required property whose direct string `const` or
all-string `enum` values are pairwise disjoint. The table maps those values to
the original alternative nodes, rather than flattening or replacing `$ref`
branches. Bare same-resource definition aliases can be followed during planning;
cycles terminate planning without selecting a table.

After successful root validation, an instance satisfying that union must have
exactly one valid alternative. Its required string tag excludes every other
alternative, so the table identifies the construction branch. The root proof
still establishes all remaining constraints and `oneOf` exclusivity. The planner
is not an instance validator and does not create a second JSON Schema semantics
implementation.

Overlapping tags, optional or missing tags, scalar unions, mixed/non-string tag
values, reference siblings, property references, and other unrecognized shapes
retain the original `is_valid` selection loop. A missing tag at lookup also uses
that loop. The planner follows schema positions only, not objects inside
`const`, `enum`, or annotation values. A nested resource `$id` disables tables
for that runtime, preserving the existing reference path. These are optimization
eligibility restrictions, not new schema support or rejection rules.

Tables are created once per runtime and indexed by the identity of nodes in its
retained schema copy. Their size and lifetime follow that schema. They retain no
request values, introduce no process-global cache, and require no persistence or
invalidation service. The current canonical schema produces 26 tables. Runtime
initialization costs and retained table state are the corresponding tradeoff.

## Verification results

All existing package tests were restored unchanged and checked against their
pushed Git blob identities before running the package test campaign.

| Check | Observed result | Evidence boundary |
| --- | --- | --- |
| Candidate contract package | 52 tests: 51 passed, 1 existing skip | All 23 original tests plus 29 added tests |
| Baseline original package | 23 tests: 22 passed, same skip | Unmodified decoder on the same interpreter/dependencies |
| Focused union tests | 23 passed in the candidate campaign | Eligibility, fallback, mutation isolation, root validation and diagnostics |
| Canonical generated-model tests | 6 passed in the candidate campaign | 42 canonical examples, recursive variants, constructor/from-value and required-field mutations |
| Canonical generation | Both generated outputs byte-identical | Actual schema/interface -> compiler -> Python and agent-tool artifacts |
| Syntax | All five changed/new Python files compile and parse with the 3.11 grammar | Syntax only, not supported-interpreter execution |

The skipped test is the existing exact-dependency runtime qualification test,
which admits CPython 3.11 and 3.12 only. It was neither changed nor bypassed by a
new skip. Test logs retain the actual result and skip reason.

Tests distinguish construction-time `is_valid` calls from calls made inside the
canonical root validator. Rejections compare complete structured failure values,
including nested pointers and causes, against the original branch-selection path.
Cases include a valid tag with an invalid payload, absent required fields, invalid
operators, multiple matching alternatives, strings with distinct Unicode spelling,
empty-string tags, and JSON boolean/numeric equality cases. Generated model types,
wire values, immutability, and omitted optional fields are observable assertions.

The test-only general decoder reproduces the prior branch-selection strategy and
shares unchanged validation/construction owners. Its comparisons establish
consistency of the optimization, not independent completeness for arbitrary JSON
Schema. Existing package semantics tests continue comparing the admitted behavior
with the selected `Draft202012Validator`; unsupported constructs remain owned by
the existing compiler profile.

## Measured decoding effect

The [runner](performance-schema-decoding/measure_decoding.py) measured seven
alternating baseline/candidate pairs, using a fresh worker process for each sample.
Each worker uses the same canonical schema and real compiler-generated models.
One warm-up decode per workload is excluded; the measured operation includes
complete root validation plus generated-model construction. Imports, generation,
initialization, serialization, and separate instrumented observations are outside
that timer. Every run checks input/output digests, generated source identity,
schema identity, Python, and dependency versions.

These are **synthetic, schema-valid decoder workloads**, not calls through the
Engine, MCP dispatcher, repository store, or user interface. In particular, the
route-result fixture contains explanation-shaped data but is not the result of
executing the Router. The comparison must not be presented as an end-to-end
routing or application latency improvement.

| Workload | Baseline median (range), ms | Candidate median (range), ms | Median decrease |
| --- | ---: | ---: | ---: |
| Compact query, 163 input bytes | 0.392 (0.367–0.468) | 0.326 (0.262–0.475) | Small overlapping range; not a meaningful consumer claim |
| Recursive expression, 9,968 input bytes | 444.377 (429.112–496.635) | 118.860 (110.828–158.345) | 73.3% |
| Synthetic route result, 14,347 input bytes | 337.936 (331.067–423.542) | 126.210 (120.675–135.364) | 62.7% |

The expression fixture contains 225 recursive expression nodes. The route-result
fixture has 32 rules and 32 unknown boolean facts. The input-byte column uses the
runner's standard JSON representation. Seven observations describe medians and
ranges, not tail-latency guarantees.

Separate instrumentation, excluded from timing, found:

| Workload | Construction-time `is_valid` calls, before -> after | Root validations, before -> after |
| --- | ---: | ---: |
| Compact query | 3 -> 0 | 1 -> 1 |
| Recursive expression | 5,128 -> 256 | 1 -> 1 |
| Synthetic route result | 3,968 -> 416 | 1 -> 1 |

Remaining calls cover general-path unions and their nested validator work; their
presence is intentional. Every measured response has the identical output digest.
The delivered runtime/helper hashes match those recorded in every candidate run.

Runtime initialization, measured separately, increased from a median 4.882 ms
(range 4.586–6.637) to 9.733 ms (9.423–11.481). This is approximately 4.851 ms
additional setup per runtime, not per decode. It is not a full process-startup
measurement. Peak memory, process RSS, model token cost, and installed consumer
latency were not measured.

## Environment, provenance and limitations

Measurements and tests used Linux on an Intel Xeon Platinum 8272CL host inside a
container with a four-CPU quota and 4 GiB memory limit. The executable was Python
3.13.5. `jsonschema` 4.26.0, `referencing` 0.37.0, `attrs` 26.1.0,
`jsonschema-specifications` 2025.9.1 and `typing-extensions` 4.16.0 match the selected
versions; `rpds-py` is 2026.5.1 instead of the lock's 2026.6.3. The project admits
Python >=3.11,<3.13, so these are local same-environment results, not qualification
of the supported locked deployment. No test campaign ran alongside the final
paired measurement run.

Direct cloning was unavailable. Prior source deliveries supplied relevant files,
and the GitHub connector supplied current source and blob identities. Sixteen
original files/input artifacts, including the changed existing-file bases, were
checked against exact pushed Git blob hashes. The generated Python and agent-tool
artifacts also match real regeneration from the canonical schema. This verifies
the relevant recovered inputs; it does not turn the working subset into a complete
repository checkout.

The full Engine integration suite, actual MCP route measurement, installed-client
qualification, and complete repository verifier were not run. The canonical
`suite-inputs.json` was deliberately not regenerated from the incomplete checkout.
It must be refreshed through the Engine in the complete repository after applying
and staging this write set. Independent review also remains a separate gate.

The ZIP retains raw measurements, full final candidate/baseline test logs,
environment and source identity records, syntax results, generated freshness,
patch-application verification, and file checksums. An initial measurement command
hit the execution tool's limit; it supplies no accepted timing. The complete
subsequent seven-pair run is the sole source of the measurements reported here.

## Reproduction and integration

Apply the patch or replacement files using the delivery's `APPLY.md`; use one
method, preserve unrelated edits, and reconcile if the expected source hashes have
changed. In the complete checkout, use the admitted locked environment and run:

```bash
PYTHONPATH=. python3 -m unittest discover -s tools/standards_contracts/tests -v
```

After reviewing/staging the intended write set, refresh verification inputs using
their canonical owner, inspect `verification.passed` and all diagnostics, then
review the generated diff:

```bash
printf '%s\n' '{"kind":"verify-repository","refresh_verification_inputs":true}' |
  PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py verify_repository
```

Run the affected Engine integration and generated-contract checks, repeat the
verifier without refresh, and obtain the repository's independent review before
claiming integration acceptance. Restart a retained MCP process after updating its
installed code; a running process continues to use its imported runtime.

For a same-schema decoder comparison, retain an unmodified `bf1358c8` checkout
and the candidate checkout. The runner creates a new evidence file and modifies
neither checkout:

```bash
python3 docs/plans/purpose-separated-standards-engine/reports/performance-schema-decoding/measure_decoding.py \
  --baseline /absolute/baseline --candidate /absolute/candidate \
  --output /tmp/schema-decoding-comparison.json --repeats 7
```

The optional `--workloads` file accepts recorded object-model instances with
`name`, `definition`, and `value` fields. That still measures decoding only. A
representative complete route through the actual host must be measured separately
before asserting an installed authoring-workflow speedup.
