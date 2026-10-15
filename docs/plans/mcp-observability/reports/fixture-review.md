# Independent fixture repair review

Date: 2026-10-14. Parent baseline:
`4887b7aff0ba84acd257da081135b7849cc9c79f`.
Disposition: **satisfied for this bounded fixture change**. No source, privacy or
oracle-weakening findings. Overall acceptance remains with the owner's final
frozen-source analysis/full Engine and generated-input verification gates.

## Exact scope

The only test behavior change is in
`tools/standards_engine/tests/test_analysis.py:2191`, method
`test_proposal_analysis_uses_one_projection_and_one_verified_base`:

- Resolve `POLICY` through the compiled corpus of the same `self.snapshot` used
  as the proposal's `base_snapshot` and source of its body.
- Assert the policy exists, then use its semantic revision as the accepted
  revision and that revision plus one as the proposed revision.
- Perform this setup before installing the two counting mocks.

The diff is seven added lines and one removed line. The actual analysis call,
`PendingResult` assertion and both exact `call_count == 1` assertions are
unchanged. No production validator, normative content, telemetry code or public
contract changes. The coordinated generated `suite-inputs.json` refresh is an
allowed fixture-repair artifact: it records the changed registered test input and
review-file membership; it does not alter the validator or weaken its decision.

## Authority and oracle assessment

`StandardsEngine._compiled_snapshot` at `engine.py:2122` loads captured content for
the explicit snapshot ID and compiles a `FrozenContentSource`; it does not select
the current live policy implicitly. Snapshot `load_content` at
`standards_snapshots/module.py:123` verifies captured content identity after its
durable read. The fixture's `open_repository` call supplies no compiled cache, so
the extra setup lookup does not introduce a warm-cache substitute for the observed
analysis path.

The repair follows the existing nearby convention in
`test_analysis.py:335–351`: obtain the policy's accepted semantic revision from the
captured corpus and advance it explicitly. This is correct fixture authority,
rather than a new expected-result oracle derived from the subject under test.
The test's independent expected behavior remains one verified-base load and one
proposal projection during the analysis operation. Real proposal construction
and revision validation still run and `CreateProposalResult` remains required.

## Independent evidence and binding

Command, from `/workspace/Coding-Standards` on CPython 3.12.14:

```sh
PYTHONPATH=. python -m unittest tools.standards_engine.tests.test_analysis.AnalysisWorkflowTest.test_proposal_analysis_uses_one_projection_and_one_verified_base
```

Result: **one test passed in 3.676 seconds**. `git diff --check` passed.

Reviewed test-file SHA256:
`7f51e403f03f5c57be8b1ca5736a79bcf139c87dd9eb4703ce3f7e59f1ba3d01`.

The prior accepted observer, MCP, observer-test and operating-guide hashes were
rechecked unchanged. The reviewer wrote only this report and performed no
publication or installation action. No model calls or private logs were used.

The owner's first broader runs were interrupted because the registered test input
had changed before its generated verifier digest was refreshed; their partial
results are not acceptance evidence. The owner is refreshing through the public
Engine verification path and will rerun the analysis module and full serial
Engine suite from frozen source. Those final results and generated-manifest
freshness are outside this independently executed targeted check.
