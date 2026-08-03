#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id policy scope unsafe capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$policy" == contradictory ]];then actual=typed-invalid;elif [[ "$policy" == missing || "$scope" == unknown || "$unsafe" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-workspace-lint-decisions.tsv"
for t in '## Cargo Workspace Lint-Expression Mechanisms' 'After Tooling selects lint purpose' 'inheritance does not transfer lint-policy authority';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Cargo Workspace Lint Examples' '[workspace.lints.clippy]' 'does not select root ownership';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Configure shared lint policy at the workspace root when possible' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0833"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0833\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling workspace lints passed: 16 decisions, 1 exact disposition\n'
