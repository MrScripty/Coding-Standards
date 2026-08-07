#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly INDEX="$REPO_ROOT/CODING-STANDARDS.md"
readonly ROUTES="$SCRIPT_DIR/fixtures/source-closure/coding-index-routes.tsv"
readonly CORPUS="$SCRIPT_DIR/corpus.tsv"
readonly MANIFEST="$SCRIPT_DIR/milestone-7-final-source-closure.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A seen_routes seen_targets
route_count=0
while IFS=$'\t' read -r route target extra; do
  [[ "$route" == route ]] && continue
  [[ -n "$route" && -z "${seen_routes[$route]:-}" ]]
  [[ -n "$target" && -z "${seen_targets[$target]:-}" ]]
  [[ -z "${extra:-}" ]]
  target_path="${target%%#*}"
  [[ -f "$REPO_ROOT/$target_path" ]]
  rg -F -q "($target)" "$INDEX"
  seen_routes["$route"]=1
  seen_targets["$target"]=1
  ((route_count += 1))
done < "$ROUTES"
[[ "$route_count" -eq 17 ]]

expected_headings=(
  '# Coding Standards Legacy Index'
  '## Universal Coding Routes'
  '## Error Handling Legacy Route'
  '## Boundary Validation Legacy Route'
  '## Dependency Management Legacy Route'
  '## Invariants And Safety Legacy Route'
  '## Disabled Features Legacy Route'
  '## Build Behavior Route'
  '## License Attribution Legacy Route'
  '## Language-Specific Guidelines Legacy Route'
  '## Frontend Standards Legacy Route'
  '## Performance Legacy Route'
)
mapfile -t observed_headings < <(rg '^#{1,6} ' "$INDEX")
[[ "${observed_headings[*]}" == "${expected_headings[*]}" ]]
[[ "$(wc -l < "$INDEX")" -le 64 ]]

for text in 'non-normative navigation' 'This file owns no coding rule' \
  'fallback authority' "Router's typed" 'instead of using prior wording'; do
  rg -F -q "$text" "$INDEX"
done
for prohibited in 'Migration authority' 'remains canonical only' \
  'This file remains canonical' 'Conflicts for moved rules' \
  'not yet moved' '### '; do
  if rg -F -q "$prohibited" "$INDEX"; then
    printf 'invalid: coding index retains legacy authority: %s\n' \
      "$prohibited" >&2
    exit 1
  fi
done

[[ "$(awk -F '\t' '$1 == "CODING-STANDARDS.md" { print $2 FS $3 FS $4 FS $5 FS $6 }' "$CORPUS")" == \
  $'standard\tderived\tcore\tsplit\tgit' ]]
[[ "$(awk -F '\t' '$2 == "CODING-STANDARDS.md" { n += 1 } END { print n + 0 }' "$OWNER_MAP")" -eq 60 ]]
[[ "$(awk -F '\t' 'NR > 1 && $2 == "CODING-STANDARDS.md" { n += 1 } END { print n + 0 }' "$DISPOSITIONS")" -eq 60 ]]
[[ "$(awk -F '\t' '$2 == "CODING-STANDARDS.md" && $5 != "rewrite-index" { n += 1 } END { print n + 0 }' "$MANIFEST")" -eq 0 ]]
[[ "$(awk -F '\t' '$2 == "CODING-STANDARDS.md" { print $3 FS $4 FS $5 }' "$MANIFEST")" == \
  $'CORE-STANDARDS.md\texpanded\trewrite-index' ]]
rg -F -q '`7.4c3.1` (`Accepted`)' "$PLAN"

"$SCRIPT_DIR/verify-core-simplicity.sh"
"$SCRIPT_DIR/verify-contract-boundary-proof.sh"
"$SCRIPT_DIR/verify-contract-invariants.sh"
"$SCRIPT_DIR/verify-language-profile-routing.sh"
"$SCRIPT_DIR/verify-router-legacy-route-closure.sh"

printf 'Coding index source closure passed: %s routes, 60 frozen IDs, derived corpus state\n' \
  "$route_count"
