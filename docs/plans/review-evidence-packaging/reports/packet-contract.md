# Proposed packet contract

Status: planning design with a 2026-09-28 owner amendment. The builder is now
implemented, but the plan remains pending qualification and acceptance. The owner
removed the standalone ZIP checker. The example JSON is exercised by the builder.

## Invocation

```sh
PYTHONPATH=. /path/to/locked/python -B -m tools.review_evidence.review_evidence build \
  --repo-root /path/to/Coding-Standards \
  --request /private/review-request.json \
  --evidence-root /private/already-retrieved-evidence \
  --output /private/new-routing-review.zip

```

The installed builder is trusted tooling. The source revisions and documents it
packages are data and are never imported/executed. Output directories are not
created implicitly. The proposed request lists all source identities; the CLI
supplies local filesystem locations separately, avoiding machine paths in the
portable recipe. Input roots and the output parent must already exist. A Git
repository may be dirty because neither index nor worktree supplies source bytes.

## Request concepts

- `format_version: 1`, a caller-selected `label` and `review_question` identify the
  request, not a review outcome.
- `revisions` maps `baseline`, `candidate` and optional explicit named roles to full
  local object IDs. The caller may name `ci` and `records`; neither is implicitly
  current or newer. IDs are resolved/checked as commits by the Git owner.
- `plan` identifies one path at a named revision. The exact document is included.
- `context` names literal files to include at both primary revisions when present,
  with absence recorded. These supplement all primary changed files. A context
  path absent from both primary revisions is an invalid selection.
- `comparisons` identifies an additional revision and literal scope paths/subtrees
  for equal-byte/mode comparison with the candidate. The full changed-path metadata
  outside those scopes is retained. This is not CI applicability judgment.
- `artifacts` lists IDs, navigation roles, declared subject revision when known,
  and one origin. `git-file` names a revision/path; `local-file` names a relative
  path below `--evidence-root`, optionally with an expected SHA-256; `reference`
  carries a label and optional URL that is never fetched. Locators are not authority.
- `claims` maps caller-supplied claim IDs to selected artifact IDs. Claim meaning
  remains in `plan`; the association is not independently evaluated by the builder.
  Both an empty mapping and a partial mapping are allowed and labelled as such.

The [example request](example-request.json) binds the actual routing source and
records. It intentionally references a raw CI log that is not present here. Building
against only the planning inputs would therefore report missing/referenced material,
not silently adopt the source report's CI counts.

## Output layout

```text
INDEX.md
manifest.json
source/baseline/<repository paths>
source/candidate/<repository paths>
changes/baseline-candidate.patch
comparisons/<revision-role>.json
records/<artifact-id>/<original basename>
evidence/<artifact-id>/<original basename>
```

Generated fixed paths and request IDs are validated to avoid collisions. Source
paths retain their exact repository spelling; no unsafe filename is repaired by
lossy normalization. Git executable modes are recorded, but ZIP members are regular,
non-executable data. Missing/reference-only artifacts have manifest/index entries
and no invented payload. The manifest lists exactly every file member other than
itself, including the generated index; it is the hash root, not its own child.

The index gives each revision role, the primary change set, selected context scope,
actual included member counts/sizes, all declared claims and evidence associations,
and explicit material gaps. Every generated local link must resolve to a listed
member. Large generated files are linked directly as complete data; viewers may
paginate them, but the packet never strips the middle or tail. No HTML, scripts,
automatic link requests or execution directives are generated from evidence text.

## Availability and integrity examples

| Material | Physical observation | What is not proved |
| --- | --- | --- |
| Exact committed test file | Included; commit/blob/mode and packet SHA-256 recorded | That the test was run, passed, or covers its claim |
| Committed review recommendation | Included verbatim with its revision identity | Independence, validity, or acceptance by the owner |
| Local CI summary with matching expected hash | Included; provided digest matched | Provider authenticity or applicability to a different candidate |
| CI URL only | Referenced; no bytes checked | A completed or successful run |
| Declared local file missing | Missing; gap retained | Any omitted measurement or result |
| CI subject differs, but `tools/` matches | Limited equality plus outside-scope differences observed | That all CI inputs match or that an owner should accept the evidence |
| Manifest and all member hashes match | Packet self-consistent | Authenticity when the manifest came from the same untrusted sender |

Expected-hash mismatch is a failed build, not the `missing` state. The builder preserves recorded gaps in its staged validation and published
manifest. A separately trusted manifest digest can detect a replaced manifest;
it does not add a trust service.

## New durable format versus Engine versions

The packet format version controls only request/manifest/reader agreement. It does
not replace a standards version, advance Engine interface 45, change request 6 or
state projection 7, invalidate snapshots, or grant an acceptance state. Future
incompatible packet readers reject unsupported format versions rather than
silently dropping fields.

## Initial result contract

```json
{
  "status": "built-with-gaps",
  "packet": "/private/new-routing-review.zip",
  "manifest_sha256": "sha256:<digest of manifest bytes>",
  "material_gaps": [
    {"artifact_id": "ci-log", "availability": "missing"},
    {"artifact_id": "ci-run-reference", "availability": "referenced"}
  ]
}
```

This is illustrative, not observed output. Build exit 0 for intact material
with no declared gaps, 1 for an intact packet with gaps, and 2 for failure. Failure
JSON names `invalid`, `unavailable` or `unsupported` with bounded non-sensitive
context. Raw Git stderr, input paths outside approved roots and arbitrary evidence
contents are not echoed in diagnostics. Existing output is never overwritten.
