#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly F="$S/fixtures/rust/dependency-candidate-inspection-decisions.tsv"
readonly OWNER="$R/topics/dependencies.md"
readonly PROFILE="$R/profiles/languages/rust/dependencies.md"
readonly RECIPE="$R/reference/recipes/rust-dependencies.md"
readonly LEGACY="$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"

while IFS=$'\t' read -r case_id contract candidate consumer resolver \
  query_support evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$contract" == missing || "$candidate" == unknown ||
          "$consumer" == unknown || "$resolver" == unknown ||
          "$evidence" == incomplete ]]; then
    actual=typed-unavailable
  elif [[ "$query_support" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" \
  "$R/workflows/verification.md" "$R/workflows/release.md" \
  "$R/topics/contracts.md" "$OWNER" \
  "$R/profiles/languages/rust/README.md" "$PROFILE" "$RECIPE"

for text in 'Inspection output is candidate evidence' \
  'cannot independently' 'transitive count'; do
  rg -F -q "$text" "$OWNER"
done
for text in '## Candidate Inspection Mechanisms' \
  'After Dependencies defines the requirement' 'graph query cannot select' \
  'written justification into policy'; do
  rg -F -q "$text" "$PROFILE"
done
for text in 'Level: `REFERENCE`' 'This material is non-normative' \
  'cargo tree -p <crate> --depth=0 -e normal' 'cargo tree -i <crate>' \
  'do not select a candidate'; do
  rg -F -q "$text" "$RECIPE"
done

rg -F -q 'topics/dependencies.md#candidate-selection' "$LEGACY"
rg -F -q 'profiles/languages/rust/dependencies.md#candidate-inspection-mechanisms' "$LEGACY"
rg -F -q 'reference/recipes/rust-dependencies.md#candidate-inspection-examples' "$LEGACY"
! rg -F -q '100+ transitive dependencies' "$LEGACY"
! rg -F -q 'cargo tree -p <crate>' "$LEGACY"
! rg -F -q 'cargo tree -i <crate>' "$LEGACY"

mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0732" && $1 <= "STD-0734" {
  print $1 "\t" $2 "\t" $3 "\t" $4
}' "$S/consolidation-dispositions.tsv")
expected=(
  $'STD-0732\tlanguages/rust/RUST-DEPENDENCY-STANDARDS.md\tprofiles/languages/rust/dependencies.md\tsplit'
  $'STD-0733\tlanguages/rust/RUST-DEPENDENCY-STANDARDS.md\treference/recipes/rust-dependencies.md\tmove'
  $'STD-0734\tlanguages/rust/RUST-DEPENDENCY-STANDARDS.md\treference/recipes/rust-dependencies.md\tmove'
)
[[ "${actual[*]}" == "${expected[*]}" ]]

printf 'Rust dependency candidate inspection passed: 14 decisions, 3 exact dispositions\n'
