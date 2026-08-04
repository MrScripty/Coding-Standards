#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)";R="$(cd -- "$S/../.." && pwd)";F="$S/fixtures/rust/tooling-owner-decisions.tsv";P="$R/profiles/languages/rust/tooling.md";X="$R/reference/recipes/rust-tooling.md";L="$R/languages/rust/RUST-TOOLING-STANDARDS.md"
while IFS=$'\t' read -r id contract scope tool target mechanism capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$contract" == contradictory ]];then actual=typed-invalid;elif [[ "$contract" == missing || "$scope" == unknown || "$tool" == missing || "$target" == unknown ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$F"
"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" "$R/workflows/implementation.md" "$R/workflows/commit.md" "$R/workflows/verification.md" "$R/workflows/tooling.md" "$R/profiles/languages/rust/README.md" "$P" "$X"
for t in '## Mechanism Authority' 'Generic owners select claims' 'cannot create or complete generic policy' '## Typed Outcomes' 'Do not fall back to an installed' '## Verification';do rg -F -q "$t" "$P";done
for t in 'Level: `REFERENCE`' 'This material is non-normative' 'cannot select tools';do rg -F -q "$t" "$X";done
rg -F -q 'profiles/languages/rust/tooling.md' "$R/STANDARDS-ROUTER.md";rg -F -q '(../../profiles/languages/rust/tooling.md)' "$L"
actual="$(awk -F '\t' '$1=="STD-0831"{print $1"\t"$2"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0831\tlanguages/rust/RUST-TOOLING-STANDARDS.md\tprofiles/languages/rust/tooling.md\tindex' ]]
printf 'Rust tooling owner passed: 16 decisions, 1 exact disposition\n'
