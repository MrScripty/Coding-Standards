#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id build owners capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$build" == contradictory ]];then actual=typed-invalid;elif [[ "$build" == missing || "$owners" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-build-script-decisions.tsv"
for t in '## Cargo Build-Script Expression Mechanisms' 'After Build accepts the action' 'cannot create build authority';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Cargo Build-Script Examples' 'SOURCE_DATE_EPOCH' 'discovery material only';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Use `build.rs` sparingly' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0841"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0841\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling build-script mechanisms passed: 16 decisions, 1 exact disposition\n'
