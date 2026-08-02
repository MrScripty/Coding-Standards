#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/rust/dependency-graph-inspection-decisions.tsv"
while IFS=$'\t' read -r case_id claim consumer resolver scope capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$claim" == contradictory ]]; then actual=typed-invalid
  elif [[ "$claim" == missing || "$consumer" == unknown || "$resolver" == unknown || "$evidence" == incomplete ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$F"
PROFILE="$R/profiles/languages/rust/dependencies.md"
LEGACY="$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
RECIPE="$R/reference/recipes/rust-dependencies.md"
for text in 'Graph inspection scope comes from the claim' \
  'only their declared graph facts' 'required audit schedule'; do
  rg -F -q "$text" "$PROFILE"
done
for text in '## Dependency Graph Inspection Examples' 'cargo tree --depth 1' \
  'cargo tree --duplicates' 'not establish a required pre-addition'; do
  rg -F -q "$text" "$RECIPE"
done
! rg -F -q 'cargo tree --depth 1' "$LEGACY"
! rg -F -q 'before dependency additions' "$LEGACY"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0741" && $1 <= "STD-0746" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0741\tprofiles/languages/rust/dependencies.md\tsplit' $'STD-0742\treference/recipes/rust-dependencies.md\tmove' $'STD-0743\treference/recipes/rust-dependencies.md\tmove' $'STD-0744\treference/recipes/rust-dependencies.md\tmove' $'STD-0745\treference/recipes/rust-dependencies.md\tmove' $'STD-0746\treference/recipes/rust-dependencies.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust dependency graph inspection passed: 15 decisions, 6 exact dispositions\n'
