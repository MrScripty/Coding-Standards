#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)";R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id claim scope capability environment fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$claim" == contradictory ]];then actual=typed-invalid;elif [[ "$claim" == missing || "$scope" == unknown || "$environment" == unknown ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-baseline-command-decisions.tsv"
for t in '## Cargo Baseline Command Mechanisms' 'After Verification selects claims' 'does not create a universal baseline';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Cargo Baseline Command Examples' 'cargo clippy --workspace' 'illustrative only after Verification';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Every Rust workspace should define local and CI commands' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0832"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0832\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling baseline commands passed: 16 decisions, 1 exact disposition\n'
