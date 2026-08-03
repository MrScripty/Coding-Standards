#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id claim ownership discovery context fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$claim" == contradictory ]];then actual=typed-invalid;elif [[ "$claim" == missing || "$ownership" == missing || "$discovery" == missing || "$context" == missing ]];then actual=typed-unavailable;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/test-style-decisions.tsv"
for t in '## Test Design' '## Test Data Authority And Lifecycle' '## Test Placement And Naming' '## Coverage And Durable Evidence Records';do rg -F -q "$t" "$R/workflows/verification.md";done
for t in '## Rust Test-Style Examples' 'condition_expected_behavior' 'illustrative Rust forms only';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Name tests as `condition_expected_behavior`' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0839"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0839\tworkflows/verification.md\trefine' ]]
printf 'Rust test-style refinement passed: 16 decisions, 1 exact disposition\n'
