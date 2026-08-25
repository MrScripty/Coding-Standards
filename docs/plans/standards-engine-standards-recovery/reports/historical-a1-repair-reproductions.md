# Historical A1 Repair Reproductions

**Status:** `complete for Milestone 0 discovery`

**Accepted A1 commit:**
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`

**Accepted A1 tree:**
`97c850ab718287007c1e1daac538f40869f71a1d`

## Boundary And Environment

The accepted commit resolved to the recorded tree and was exported with
`git archive` into `/tmp/coding-standards-a1-2359a987`. All commands below ran
from that extracted tree, with CPython `3.12.3` and Git `2.43.0`. The extraction
contains no later recovery documents or worktree changes.

The focused baseline was:

```bash
python3 -m unittest discover -s tools/standards_engine/tests -v
python3 -m unittest discover -s tools/standards_analysis/tests -v
python3 -m unittest discover -s tools/standards_metadata/tests -v
python3 tools/standards_engine/contracts/validate_contracts.py
python3 tools/standards_engine/contracts/generate_contract.py --check
```

Observed results were 45 engine tests, 82 analysis tests, and 18 metadata tests
passing; contract validation passed 33 examples, 8 identity fixtures, 4
operation envelopes, and 143 definitions; generated freshness passed.

## Reproduction Matrix

| Repair family | Exact accepted inputs and command | Expected and actual outcome | Claimed property | Oracle | Unsupported domain |
| --- | --- | --- | --- | --- | --- |
| Generated public closure | Engine suite, especially `test_generated_contract.py`; mutate schema type, default, minimum, const, request/submission variant, result type, and result requiredness | Each semantic mutation changed `_python_projection`; generated classes enforced minimum, const, pattern, requiredness, result shape, nested submissions, and operation/result variants; freshness also passed | The accepted generator traverses the current public A1 closure and projects the selected assertions | Canonical A1 schema plus behavioral mutation tests | Freshness and sampled mutations do not prove exhaustive dialect semantics or external conformance |
| Public results and package ownership | Engine suite public `prepare`, `resolve`, facade, rendering, and programming-error tests; inspect `standards_engine/__init__.py`, `model.py`, `tools.py`, and generated imports | Native operations returned exported generated `PendingResult`/`CompleteResult`; every result kind had conversion/rendering; engine `ValueError` propagated as a programming error; generated code used the public metadata export | A1's public result algebra is owned by generated models at the facade | Public package API and agent facade | `validate_contracts.py` and `standards_analysis/serialization.py` still import an internal metadata module; complete package-boundary compilation remains A1b work |
| Immutable reads | `test_module_read_uses_immutable_snapshot_content_after_source_mutation` and `test_module_inspection_remains_bound_to_captured_snapshot_content` | Whole-module read and complete policy inspection remained byte-for-byte stable after live source mutation | Issued snapshot reads use captured authority | Public engine query and inspect results before and after mutation | This proves selected module reads and inspection, not every future authority adapter |
| Cold reconstruction | Accepted cold tests plus the temporary public-authority invocation described below | A separate process reproduced and advanced persisted analysis; a temporary repository-authored fact contract produced context, requirement, and observation handles; a fresh public engine with only the repository and directory state store inspected all three plus a certificate | Persisted A1 state and declared immutable repository authority reconstruct every advertised child-handle kind | Fresh process and public `StandardsEngine` constructors without private fields, providers, authorizations, caches, or in-memory stores | `DispositionRecord` has no handle in the accepted algebra and therefore is not an advertised inspectable handle |
| Semantic-version identity | Analysis suite `test_semantic_contract_versions_participate_in_snapshot_identity` | Changing `metadata_api_version` changed snapshot identity; changing analyzer and graph implementation versions did not | Selected interpretation contracts, not implementation releases, participate in identity | Domain-specific snapshot identity assertion | The accepted regression does not independently vary every interpretation-affecting metadata, graph, parser, applicability, authorization, provider, and analysis contract |
| Equality and validation | Engine generated-contract suite plus the temporary matrix recorded in `json-schema-instance-equality-reproduction.md` | Boolean/integer decisions agreed locally and with Draft 2020-12 for selected cases; composed/decomposed Unicode agreed locally but contradicted Draft 2020-12 | Local validator/generated agreement is distinct from external conformance | Official Draft 2020-12 clauses for the selected cases | No claim of full dialect conformance or corrected A1 behavior |
| Acceptance oracles | Exact accepted-tree harness and direct invocations under [Exact Negative Diagnostics](#exact-negative-diagnostics); generated semantic mutation tests; equality matrix | Invalid plans were otherwise valid and produced one exact complete diagnostic; semantic mutations changed generated output; Boolean/integer and Unicode matrices were both exercised | Negative fixtures reach the intended failure and freshness is not the sole semantic check | Exact diagnostics, mutation-derived expectations, and external equality clauses | Existing tests remain sampled; no claim that all historical acceptance assertions have independent external oracles |

## Exact Negative Diagnostics

All commands in this section ran from the accepted-tree working directory
`/tmp/coding-standards-a1-2359a987`.

The exact harness invocation was:

```bash
bash evaluation/standards-effectiveness/verify-plan-fixtures.sh
```

Expected and actual exit status was `0`, standard error was empty, and complete
standard output was:

```text
Plan lifecycle fixtures passed
```

The exact direct invocations were:

```bash
bash evaluation/standards-effectiveness/check-plan-structure.sh \
  evaluation/standards-effectiveness/fixtures/plans/invalid-accepted-satisfied-without-evidence.md
bash evaluation/standards-effectiveness/check-plan-structure.sh \
  evaluation/standards-effectiveness/fixtures/plans/invalid-objective-partial.md
```

For each direct invocation, expected and actual exit status was `1` and
standard output was empty. Complete standard error was, respectively:

```text
evaluation/standards-effectiveness/fixtures/plans/invalid-accepted-satisfied-without-evidence.md: satisfied objective A1 requires evidence
evaluation/standards-effectiveness/fixtures/plans/invalid-objective-partial.md: objective A1 has invalid status partial
```

This is stronger than accepting any nonzero result or matching a substring.

## Historical Family Disposition

All historical families are reproducible from the exact accepted tree. The
results also preserve the boundaries the accepted checks do not prove:

- generated freshness is not semantic correctness;
- two local implementations are not an external oracle;
- identity canonicalization is not schema instance equality;
- in-process inspection is not cold reconstruction; and
- a selected semantic-version test is not exhaustive version closure.

These gaps motivate the standards recovery and later A1b plan. They do not
authorize an A1 runtime edit in this plan.

## Public Cold Child-Handle Invocation

The temporary orchestration script had SHA-256
`5eed9b6e4327e225030a5dd6d76e4362be39354e0930c5386bdab39f7d268f7d` and ran:

```bash
PYTHONPATH=. python3 /tmp/reproduce_a1_cold_public.py \
  /tmp/coding-standards-a1-2359a987
```

It copied the accepted tree to temporary storage, authored one Boolean fact,
changed exactly the `workflow.planning.projection-completeness` relationship to
an `equals` program over that fact, and cleared copied attestations made stale
by the temporary fact-schema change. It then used public engine constructors
and a directory state store to prepare and resolve the fact. A separate Python
process reopened the same temporary repository and store with no execution
authority and returned:

```text
analysis-context-handle     analysis-context-inspection-result
fact-requirement-handle     fact-requirement-inspection-result
fact-observation-handle     fact-observation-inspection-result
certificate-handle          certificate-inspection-result
disposition has handle      false
```

The temporary authority change was not applied to the accepted tree or current
repository. It exists solely to make the public fact-handle path reachable.
