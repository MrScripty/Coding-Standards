#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id procedure tool capability evidence fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$procedure" == contradictory ]];then actual=typed-invalid;elif [[ "$procedure" == missing || "$tool" == missing || "$evidence" == incomplete ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/release-automation-adapter-decisions.tsv"
for t in '## Rust Release-Automation Adapter Mechanisms' 'Tooling selects the automation' 'does not select `cargo-release`';do rg -F -q "$t" "$R/profiles/languages/rust/release.md";done
for t in '## Cargo-Release Adapter Example' 'shared-version = true' 'does not recommend `cargo-release`';do rg -F -q "$t" "$R/reference/recipes/rust-release.md";done
! rg -F -q '`cargo-release` is recommended' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
for spec in $'STD-0818\tprofiles/languages/rust/release.md\tsplit' $'STD-0819\treference/recipes/rust-release.md\tmove';do id="${spec%%$'\t'*}";actual="$(awk -F '\t' -v id="$id" '$1==id{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == "$spec" ]];done
printf 'Rust release automation adapter passed: 16 decisions, 2 exact dispositions\n'
