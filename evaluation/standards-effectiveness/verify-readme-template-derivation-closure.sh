#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-47-owner-validation.tsv"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
MAP="$S/generated/rule-owner-map.tsv"
GAPS="$S/fixtures/migration/undisposed-source-gaps.tsv"
AUDIT="$S/milestone-7-undisposed-source-audit.md"
TEMPLATE="$R/templates/README-TEMPLATE.md"
WORKFLOW="$R/workflows/documentation.md"
CORPUS="$S/corpus.tsv"
SOURCE="templates/README-TEMPLATE.md"
OWNER="workflows/documentation.md"

mapfile -t expected < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
mapfile -t actual < <(
  awk -F '\t' -v source="$SOURCE" '$2 == source { print $1 }' "$DISPOSITIONS"
)
[[ "${#expected[@]}" -eq 18 && "${actual[*]}" == "${expected[*]}" ]]

while IFS=$'\t' read -r id expected_owner expected_disposition _treatment _reason; do
  [[ "$id" == id ]] && continue
  row="$(awk -F '\t' -v id="$id" '$1 == id { print $2 FS $3 FS $4 FS $5 }' "$DISPOSITIONS")"
  IFS=$'\t' read -r source owner disposition rationale <<< "$row"
  [[ "$source" == "$SOURCE" && "$owner" == "$expected_owner" ]]
  [[ "$owner" == "$OWNER" && "$disposition" == "$expected_disposition" ]]
  [[ "$disposition" == split && -n "$rationale" ]]
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]
done < "$V"

remaining="$(
  awk -F '\t' -v source="$SOURCE" '
    NR == FNR { if ($1 != "id") disposed[$1] = 1; next }
    $2 == source && !($1 in disposed) { n++ }
    END { print n+0 }
  ' "$DISPOSITIONS" "$MAP"
)"
[[ "$remaining" -eq 0 ]]
[[ "$(cat "$GAPS")" == $'id\tclassification\treason' ]]

[[ "$(awk -F '\t' '$1 == "templates/README-TEMPLATE.md" { print $2 FS $3 FS $4 FS $5 FS $6 }' "$CORPUS")" == $'template\tderived\treference\tsplit\tgit' ]]
for metadata in 'ID: `workflow.documentation`' 'Requires: `core`' \
  'Canonical owner: `workflows/documentation.md`'; do
  rg -F -q "$metadata" "$WORKFLOW"
done
for text in 'If the impact cannot be classified' 'Contradictory trigger' \
  '`unavailable`' '`unsupported`' \
  'Do not default to a `src/` directory, README per directory, fixed headings'; do
  rg -F -q "$text" "$WORKFLOW"
done

for text in 'selects a' '`boundary-readme` or `contract-readme`' \
  'Delete instructions and optional' 'sections that do not apply' \
  '## Purpose' '## Responsibility' '## Invariants' '## Entry Points' \
  '## Decision Links' '## Consumer Contract' '## Produced Contract'; do
  rg -F -q "$text" "$TEMPLATE"
done
for heading in '## Contents' '## Problem' '## Constraints' '## Decision' \
  '## Alternatives Rejected' '## Revisit Triggers' '## Dependencies' \
  '### Internal' '### External' '## Related ADRs' '## Usage Examples' \
  '## API Consumer Contract' '## Structured Producer Contract' \
  '## Testing' '## Notes'; do
  ! rg -F -x -q "$heading" "$TEMPLATE"
done

for text in 'observes zero undisposed source gaps' \
  'Restoring the universal README' 'template is not an admissible option'; do
  rg -F -q "$text" "$AUDIT"
done

"$S/verify-undisposed-source-gaps.sh"
"$S/verify-documentation-decisions.sh"
"$S/verify-documentation-policy-consolidation.sh"
printf 'README template derivation closure passed: 18 exact split dispositions, 0 source gaps, P39 closed\n'
