#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id contract source tooling verification capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$contract" == contradictory ]];then actual=typed-invalid;elif [[ "$contract" == missing || "$source" == missing || "$tooling" == missing || "$verification" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-compile-fail-decisions.tsv"
for t in '## Compile-Fail Harness Adapter Mechanisms' 'After Contracts accepts a compile-time rejection contract' 'cannot select trybuild';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Compile-Fail Harness Examples' 'single-use tokens' 'illustrative only';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Use `trybuild` when the API promises' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0837"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0837\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling compile-fail adapters passed: 16 decisions, 1 exact disposition\n'
