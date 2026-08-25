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
| Semantic-version identity | Accepted regression plus the exact temporary mutation matrix under [Semantic-Version Identity Invocation](#semantic-version-identity-invocation) | Every interpretation field in `AnalysisVersions.identity_contract()` changed snapshot identity; analyzer and graph implementation versions did not | Interpretation contracts, not implementation releases, participate in snapshot identity | Complete field-level mutation of the accepted identity projection | This proves the accepted snapshot identity projection, not whether that projection includes every contract that should affect interpretation |
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

The complete script source is retained below under
[Public Cold Reconstruction Source](#public-cold-reconstruction-source), so
the hash and command do not depend on an untracked temporary file.

## Semantic-Version Identity Invocation

The complete temporary source is retained below under
[Semantic-Version Mutation Source](#semantic-version-mutation-source). From the
accepted-tree working directory, it ran as:

```bash
PYTHONPATH=. python3 /tmp/reproduce_a1_version_identity.py \
  /tmp/coding-standards-a1-2359a987
```

Expected and actual exit status was `0`. The result classified all ten fields
returned by `AnalysisVersions.identity_contract()` as `changed` and both
implementation-only provenance fields as `stable`:

```text
analysis_contract_version changed
analysis_schema_version changed
result_schema_version changed
interface_schema_version changed
applicability_version changed
authorization_contract_version changed
metadata_api_version changed
graph_engine_contract_version changed
parser_versions changed
evidence_provider_contract_versions changed
graph_engine_implementation_version stable
analyzer_implementation_version stable
```

## Public Cold Reconstruction Source

Exact source whose digest and invocation are recorded above:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AuthorizationReference,
    ChangeDescriptor,
    ChangeKind,
    ConsumerDispositionSubmission,
    EvidenceReference,
    ProvideFactSubmission,
    ReviewScope,
)
from tools.standards_engine.standards_engine import (
    AnalysisRequest,
    CompleteResult,
    DirectoryAnalysisStateStore,
    InspectCall,
    PendingResult,
    StandardsEngine,
)


SOURCE = Path(sys.argv[1]).resolve()


def authorization(capability: str) -> AuthorizationReference:
    return AuthorizationReference(
        f"authorization.{capability}",
        capability,
        "sha256:" + "a" * 64,
    )


def cold_inspect(repo: Path, store: Path, handles: list[dict[str, object]]) -> dict[str, str]:
    script = r'''
import json
import sys
from pathlib import Path
from tools.standards_engine.standards_engine import DirectoryAnalysisStateStore, InspectCall, StandardsEngine

engine = StandardsEngine.open_repository(
    Path(sys.argv[1]),
    analysis_store=DirectoryAnalysisStateStore(Path(sys.argv[2])),
)
handles = json.loads(sys.argv[3])
print(json.dumps({handle["kind"]: engine.inspect(InspectCall(handle)).as_contract()["kind"] for handle in handles}, sort_keys=True))
'''
    completed = subprocess.run(
        (sys.executable, "-c", script, str(repo), str(store), json.dumps(handles)),
        cwd=SOURCE,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


with tempfile.TemporaryDirectory() as temporary:
    temporary_root = Path(temporary)

    conditional_repo = temporary_root / "conditional-repo"
    shutil.copytree(SOURCE, conditional_repo)
    facts = conditional_repo / "evaluation/standards-effectiveness/policy-impact-facts.toml"
    facts.write_text(
        '''schema_version = 1
id = "policy-impact.applicability"

[[facts]]
id = "change.requires_review"
semantic_revision = 1
type = "boolean"
nullable = false
aliases = []
meaning = "Whether this standards change requires consumer review."
context_kind = "standards-change"
answer_contract = "fact-value.v1"
evidence_contract = "evidence-reference.v1"
authorization_capability = "standards.analyze"
prompt = "Does this standards change require consumer review?"
''',
        encoding="utf-8",
    )
    declarations = conditional_repo / "evaluation/standards-effectiveness/policy-impact/workflow.planning.toml"
    old = '''source = "workflow.planning.projection-completeness"
consumer = "policy-semantic-impact"
relation = "enforcement-suite-projection"
applicability = { operator = "always" }
'''
    new = '''source = "workflow.planning.projection-completeness"
consumer = "policy-semantic-impact"
relation = "enforcement-suite-projection"
applicability = { operator = "equals", fact = "change.requires_review", value = true }
'''
    content = declarations.read_text(encoding="utf-8")
    if content.count(old) != 1:
        raise RuntimeError("conditional relationship source did not match exactly once")
    declarations.write_text(content.replace(old, new), encoding="utf-8")
    empty_attestations = "schema_version = 1\nattestations = []\n"
    for owner in ("workflow.planning", "workflow.commit"):
        attestation = (
            conditional_repo
            / "evaluation/standards-effectiveness/policy-coverage/attestations"
            / f"{owner}.toml"
        )
        attestation.write_text(empty_attestations, encoding="utf-8")

    conditional_store = temporary_root / "conditional-states"
    conditional_engine = StandardsEngine.open_analysis(
        conditional_repo,
        conditional_repo,
        authorizations=(authorization("standards.analyze"),),
        analysis_store=DirectoryAnalysisStateStore(conditional_store),
    )
    policy = "workflow.planning.projection-completeness"
    pending = conditional_engine.prepare(
        AnalysisRequest(
            conditional_engine.snapshot,
            conditional_engine.snapshot,
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (policy,),
                    (policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )
    )
    requirement = pending.fact_requirements[0]
    advanced = conditional_engine.resolve(
        pending.handle,
        ProvideFactSubmission(
            requirement.handle,
            {"type": "boolean", "state": "known", "value": False},
            (
                EvidenceReference(
                    "evidence.cold-public",
                    "sha256:" + "c" * 64,
                    "repository-content",
                    "1",
                ),
            ),
        ),
    )
    state = conditional_engine.inspect(InspectCall(advanced.handle))
    observation = state.fact_observations[0]
    child_results = cold_inspect(
        conditional_repo,
        conditional_store,
        [
            pending.context.handle.as_contract(),
            requirement.handle.as_contract(),
            observation.handle.as_contract(),
        ],
    )

    complete_store = temporary_root / "complete-states"
    capabilities = tuple(
        authorization(capability)
        for capability in (
            "standards.analyze",
            "standards.review.consumer",
            "standards.review.impact",
            "standards.review.audit",
        )
    )
    complete_engine = StandardsEngine.open_analysis(
        SOURCE,
        SOURCE,
        authorizations=capabilities,
        analysis_store=DirectoryAnalysisStateStore(complete_store),
    )
    complete_policy = "workflow.planning.written-plan-applicability"
    result = complete_engine.prepare(
        AnalysisRequest(
            complete_engine.snapshot,
            complete_engine.snapshot,
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (complete_policy,),
                    (complete_policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )
    )
    while isinstance(result, PendingResult):
        obligation = next(item for item in result.obligations if item.state == "required")
        result = complete_engine.resolve(
            result.handle,
            ConsumerDispositionSubmission(
                obligation.id,
                "reviewed-no-change",
                "The accepted consumer remains unchanged for this reproduction.",
                (
                    EvidenceReference(
                        "review.cold-certificate",
                        "sha256:" + "d" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
                obligation.fingerprint,
            ),
        )
    if not isinstance(result, CompleteResult):
        raise RuntimeError("analysis did not complete")
    certificate_results = cold_inspect(
        SOURCE,
        complete_store,
        [item.as_contract() for item in result.coverage_certificates],
    )

    print(
        json.dumps(
            {
                "analysis_children": child_results,
                "certificates": certificate_results,
                "disposition_has_handle": any(
                    hasattr(item, "handle") for item in result.dispositions
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
```

## Semantic-Version Mutation Source

Exact source used by the complete identity-field mutation matrix:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path

from tools.standards_analysis.standards_analysis.snapshots import (
    AnalysisVersions,
    compile_snapshot,
)


ROOT = Path(sys.argv[1]).resolve()
BASE = AnalysisVersions().as_contract()


class VersionProjection:
    def __init__(self, overrides: dict[str, object]) -> None:
        self._value = {**BASE, **overrides}

    def as_contract(self) -> dict[str, object]:
        return dict(self._value)

    def identity_contract(self) -> dict[str, object]:
        value = self.as_contract()
        value.pop("graph_engine_implementation_version")
        value.pop("analyzer_implementation_version")
        return value


def handle(overrides: dict[str, object]) -> dict[str, object]:
    return compile_snapshot(
        ROOT,
        ("CORE-STANDARDS.md",),
        versions=VersionProjection(overrides),  # type: ignore[arg-type]
    ).handle


base = handle({})
semantic_mutations: dict[str, object] = {
    "analysis_contract_version": 6,
    "analysis_schema_version": 3,
    "result_schema_version": 2,
    "interface_schema_version": 10,
    "applicability_version": 4,
    "authorization_contract_version": "authorization-authority.v2",
    "metadata_api_version": "2",
    "graph_engine_contract_version": "2",
    "parser_versions": {"markdown-heading": "2"},
    "evidence_provider_contract_versions": {
        "policy-impact-consumer-horizon": "2",
        "repository-content": "2",
    },
}
implementation_mutations: dict[str, object] = {
    "graph_engine_implementation_version": "2",
    "analyzer_implementation_version": "2",
}

results: dict[str, str] = {}
for field, value in semantic_mutations.items():
    if handle({field: value}) == base:
        raise RuntimeError(f"semantic version did not change identity: {field}")
    results[field] = "changed"
for field, value in implementation_mutations.items():
    if handle({field: value}) != base:
        raise RuntimeError(f"implementation version changed identity: {field}")
    results[field] = "stable"

print(json.dumps(results, indent=2, sort_keys=True))
```
