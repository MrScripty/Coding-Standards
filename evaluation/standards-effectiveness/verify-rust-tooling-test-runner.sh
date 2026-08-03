#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id tooling verification resilience capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$tooling" == contradictory ]];then actual=typed-invalid;elif [[ "$tooling" == missing || "$verification" == missing || "$resilience" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-test-runner-decisions.tsv"
for t in '## Rust Test-Runner Adapter Mechanisms' 'After Tooling selects a test runner' 'cannot select';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Nextest Command Examples' 'cargo nextest run --workspace' 'do not select nextest';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Use nextest when it materially improves' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0835"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0835\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling test-runner adapters passed: 16 decisions, 1 exact disposition\n'
