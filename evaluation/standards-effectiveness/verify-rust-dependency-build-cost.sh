#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id claim measurement inputs baseline capability evidence fallback expected extra; do
  [[ "$id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$claim" == contradictory ]]; then actual=typed-invalid
  elif [[ "$claim" == missing || "$inputs" == unknown || "$baseline" == missing || "$evidence" == incomplete ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported; else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/dependency-build-cost-decisions.tsv"
for text in '## Build-Cost Measurement Mechanisms' 'Performance defines the build-cost claim' 'does not select a percentage threshold'; do rg -F -q "$text" "$R/profiles/languages/rust/dependencies.md"; done
for text in '## Build-Cost Measurement Examples' 'cargo build --timings' 'do not establish a 20 percent threshold'; do rg -F -q "$text" "$R/reference/recipes/rust-dependencies.md"; done
for text in '# Rust Dependency Standards Migration Index' 'This is a non-normative migration index' '[Performance](../../topics/performance.md)'; do rg -F -q "$text" "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"; done
! rg -F -q 'more than 20%' "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
! rg -F -q 'cargo build --timings' "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0749" && $1 <= "STD-0751" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0749\tprofiles/languages/rust/dependencies.md\tsplit' $'STD-0750\treference/recipes/rust-dependencies.md\tmove' $'STD-0751\treference/recipes/rust-dependencies.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust dependency build cost passed: 14 decisions, 3 exact dispositions, legacy source closed\n'
