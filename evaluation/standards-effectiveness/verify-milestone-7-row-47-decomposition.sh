#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
V="$S/milestone-7-row-47-owner-validation.tsv"
D="$S/milestone-7-row-47-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
TRAIN="$S/milestone-7-execution-train.tsv"
PACKAGES="$S/milestone-7-accelerated-packages.tsv"
MAP="$S/generated/rule-owner-map.tsv"
INVENTORY="$S/generated/section-inventory.tsv"
TEMPLATE="$R/templates/README-TEMPLATE.md"
WORKFLOW="$R/workflows/documentation.md"
CORPUS="$S/corpus.tsv"

row="$(awk -F '\t' '$1 == 47 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 }' "$TRAIN")"
IFS=$'\t' read -r wave start_id end_id source owner owner_state activation checkpoint <<< "$row"
[[ "$wave" == reference-index-closure ]]
[[ "$start_id" == STD-0899 && "$end_id" == STD-0916 ]]
[[ "$source" == templates/README-TEMPLATE.md ]]
[[ "$owner" == workflows/documentation.md ]]
[[ "$owner_state" == exists && "$activation" == pre-slice-review && "$checkpoint" == full-suite ]]

package="$(awk -F '\t' '$1 == 47 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $9 FS $10 }' "$PACKAGES")"
IFS=$'\t' read -r package_id risk package_owner owner_action semantics concurrency gate outcome dependencies <<< "$package"
[[ "$package_id" == P39 && "$risk" == consolidation && "$package_owner" == "$owner" ]]
[[ "$owner_action" == existing-review && "$semantics" == migration-structure ]]
[[ "$concurrency" == serial-only && "$gate" == full-suite ]]
[[ "$outcome" == readme-template-derivation && "$dependencies" == core ]]

mapfile -t expected < <(
  awk -F '\t' -v source="$source" '
    $2 == source {
      number = substr($1, 5) + 0
      if (number >= 899 && number <= 916) print $1
    }
  ' "$INVENTORY"
)
mapfile -t actual < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
[[ "${#expected[@]}" -eq 18 && "${actual[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' -v owner="$owner" 'NR > 1 && ($2 != owner || $3 != "split" || $4 == "" || $5 == "") { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 { seen[$4] = 1 } END { print length(seen) }' "$V")" -eq 11 ]]

while IFS=$'\t' read -r id map_source line map_owner action heading extra; do
  [[ "$id" == id ]] && continue
  number="${id#STD-}"
  number="$((10#$number))"
  (( number >= 899 && number <= 916 )) || continue
  [[ "$map_source" == "$source" && "$line" =~ ^[0-9]+$ && "$map_owner" == "$owner" ]]
  [[ "$action" == align-derived-template && -n "$heading" && -z "${extra:-}" ]]
done < "$MAP"

for text in '## Review Finding' 'one coherent Documentation-owned' \
  '## Owner Contract' '## Exact Outcomes' 'All eighteen identifiers' \
  '## Ordered Child' '`47.1`' '## Bounded Write Sets' \
  '## Verification Gates' '## Typed Outcomes And No Fallback' \
  '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

[[ "$(awk -F '\t' '$1 == "templates/README-TEMPLATE.md" { print $2 FS $3 FS $4 FS $5 FS $6 }' "$CORPUS")" == $'template\tderived\treference\tsplit\tgit' ]]
for metadata in 'ID: `workflow.documentation`' 'Requires: `core`' \
  'Canonical owner: `workflows/documentation.md`'; do
  rg -F -q "$metadata" "$WORKFLOW"
done
for text in '## Documentation Profiles' '## Boundary README' \
  '## Contract Documentation' '## Decision Traceability' \
  'If the impact cannot be classified' 'Contradictory trigger' \
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

rg -F -q '`7.4b37a` (`Accepted`)' "$P"
rg -F -q '`7.4b37b` (`Accepted`)' "$P"
"$S/verify-readme-template-derivation-closure.sh"
"$S/verify-documentation-decisions.sh"
"$S/verify-documentation-policy-consolidation.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-47 closure passed: 18 split dispositions, P39 closed, final source closure active\n'
