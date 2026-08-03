#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)"
while IFS=$'\t' read -r id claim tooling owner capability fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$claim" == contradictory ]];then actual=typed-invalid;elif [[ "$claim" == missing || "$tooling" == missing || "$owner" == missing ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/tooling-adapter-inventory-decisions.tsv"
for t in '## Capability-Matched Tool Adapters' 'Rust Dependency owns' 'Miri applicability';do rg -F -q "$t" "$R/profiles/languages/rust/tooling.md";done
for t in '## Rust Tool Catalog Example' 'cargo llvm-cov' 'illustrative discovery material only';do rg -F -q "$t" "$R/reference/recipes/rust-tooling.md";done
! rg -F -q '| `cargo fmt` | Required |' "$R/languages/rust/RUST-TOOLING-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0840"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0840\tprofiles/languages/rust/tooling.md\tsplit' ]]
printf 'Rust tooling adapter inventory passed: 16 decisions, 1 exact disposition\n'
