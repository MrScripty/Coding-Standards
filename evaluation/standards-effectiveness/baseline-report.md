# Standards Effectiveness Baseline

## Source

- Baseline commit:
  `6b4df85f042898374e9d23d265f4ecd25b0a7ba7`
- Captured: 2026-07-28
- Scope: all 40 Markdown guidance, template, reference, and plan artifacts
  present in the working standards library.
- Local-only exception: three ignored prompt files are represented by immutable
  baseline snapshots and hashes.

## Corpus Metrics

| Metric | Value |
| --- | ---: |
| Markdown artifacts | 40 |
| All Markdown lines | 12,088 |
| All headings | 1,015 |
| Strong imperative occurrences | 352 |
| Normative or operationally derived artifacts | 36 |
| Normative or operationally derived lines | 11,066 |
| Normative or operationally derived headings | 916 |
| Normative or operationally derived imperatives | 321 |
| Inventoried normative/derived sections | 916 |

The imperative metric counts lines containing `must`, `required`, `shall`,
`never`, `always`, `mandatory`, or `do not` outside alphabetic word
continuations. It is a stable comparison signal, not a complete semantic rule
count.

## Routing Baseline

The root quick start directs adopters to copy the complete library and read
every document. No applicability contract identifies exclusions, prerequisites,
specializations, or precedence.

Consequently:

- every fixture begins with 100% of normative and derived guidance;
- median baseline routing load is 100%;
- generic plus Rust guidance is additive without deterministic rule
  supersession; and
- the reader must infer whether examples, recommendations, and mandatory rules
  bind the task.

## Planning And Process Baseline

- The active plan is treated as execution scope and status history.
- Milestone status is limited to not started, in progress, and complete.
- There is no distinct `Implemented`, `Verifying`, `Accepted`, `Deferred`, or
  `Superseded` state.
- Re-planning requires more plan content but no replacement or rollover
  contract.
- Full-path testing is required for cross-layer features, but plan completion
  does not bind objective status to a named acceptance level.
- Every source directory requires a README and changed source must update a
  README or ADR regardless of decision impact.
- Unpushed history inspection/rewrite is mandatory before every commit without
  an explicit authority boundary.

## Reproducibility

Run `generate-baseline.sh` against a clone containing the baseline commit.
Expected outputs are recorded in `generated/`. The generator:

1. reads tracked artifacts from the baseline Git tree;
2. reads ignored prompts only from committed baseline snapshots;
3. verifies each artifact with a SHA-256 digest;
4. regenerates file metrics and all 916 section identifiers; and
5. emits the summary values above.

The frozen outputs must not be regenerated against later standards content.
After restructuring, use a separate comparison output and preserve this
baseline.

## Known Baseline Limitations

- Strong imperative counts cannot identify indirect normative language.
- Heading inventory is finer than semantic rule ownership: one section may
  contain multiple rules or examples.
- Semantic duplicate clusters require reviewed source references and are
  maintained in `findings.md`.
- Local-only prompts were not part of the versioned repository contract. Their
  snapshots preserve evidence but do not make them canonical.

These limitations are explicit so later comparison does not claim more
precision than the baseline supports.
