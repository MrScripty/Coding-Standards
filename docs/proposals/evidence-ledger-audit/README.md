# Evidence and ledger audit refinements

## Source and limits

[Source audit](source-audit.pdf), supplied by the maintainer on 22 October 2026,
is preserved byte for byte (SHA-256
`c701c6c6d38767d5a765521068fa57fb395f2c3bd44ebabf4da1ef5fc2c3a04d`).
The report inspected pinned Rheon and Tuldok records against standards revision
`73bd032b`; it did not reproduce their runtime results. Those observations are
reported evidence, not independently reproduced results of this refinement.

The accepted standards were read through the authoring MCP at `2e3ef047`.
The five wording targets still exist. Existing Core and Verification rules
already support adequate evidence, material environment qualification, owned
gates and truthful completion. The proposed changes clarify their application.
They do not establish that standards wording caused the historical incidents.

## Bounded change

1. Documentation: replace the broad tests-and-review sentence with a reference
   to applicable verification and change review.
2. Verification: bind a result or finding to the stable subject actually
   inspected, with intervening changes detected before attribution.
3. Verification: explicitly include the verification client's lifecycle,
   dependency and environment preconditions in reviewable test design.
4. Router and Development Proportionality: include sufficient acceptance
   decisions in the applicability of additional investigation, evidence and
   review; align the executable routing fact's meaning and condition.
5. Commit: confirm that selected evidence remains valid for the staged slice;
   rerun for relevant changes or an owned fresh-execution gate.

Historical measurements, current project release thresholds and pending draft
proposals remain governed by their actual owners. The older CodeRabbit drafts
overlap evidence attribution, but are neither accepted guidance nor a reason to
add their larger proposed protocols here.

## Semantic review cases

These are reasoning cases for the proposed clauses, not rerun downstream tests
or evidence of improved agent behavior:

| Case | Required interpretation |
| --- | --- |
| Evidence-only commit; relevant source, inputs, environment and gates unchanged | Confirm existing evidence covers the staged slice; no automatic repeated execution. Review the actual staged diff. |
| V1 is inspected while V2 is written | Attribute findings to retained V1, or detect the intervening change and reconcile; V2's later hash cannot identify the observation of V1. |
| A test client receives acknowledgement before semantic readiness | Respect the actual readiness transition before making dependent observations. |
| A worker runs with optional dependencies absent | Establish the verification client's selected dependency/environment contract before relying on its evidence. |
| A filter selects no required observations | A successful command alone cannot satisfy the unobserved claim. Existing claim/observation rules continue to apply. |
| Local and hosted results prove the same claim in adequate environments | Evaluate reuse before another evidence cycle; distinct environment obligations can still justify both. |
| A confidence interval is inconclusive under an owned release rule | Preserve the result and the failed gate; proportionality does not relax its acceptance threshold. |
| An owned gate requires fresh execution | Execute it even if other unchanged evidence can be reused. |

## Publication status

This is supporting audit evidence and change intent. It is not normative
guidance or a claim that the proposed standards are accepted. Engine workflow
records and accepted MCP readback determine publication.
