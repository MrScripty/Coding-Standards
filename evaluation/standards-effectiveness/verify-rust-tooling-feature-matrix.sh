#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id contracts tooling verification capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$contracts" == contradictory ]];then actual=typed-invalid;elif [[ "$contracts" == missing || "$tooling" == missing || "$verification" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-feature-matrix-decisions.tsv"
for t in '## Cargo Feature-Matrix Adapter Mechanisms' 'After Dependencies, Contracts, Library, and Cross-Platform' 'cannot select a tool';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Cargo Feature-Matrix Command Examples' 'cargo hack check --each-feature' 'do not select cargo-hack';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q 'Use powerset checks only for small core crates' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0836"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0836\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling feature-matrix adapters passed: 16 decisions, 1 exact disposition\n'
