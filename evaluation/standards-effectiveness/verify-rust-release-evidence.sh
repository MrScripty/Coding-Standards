#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)";R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id claim scope capability evidence fallback expected extra;do [[ "$id" == case ]]&&continue;[[ -z "${extra:-}" ]];if [[ "$fallback" != none || "$claim" == contradictory ]];then actual=typed-invalid;elif [[ "$claim" == missing || "$scope" == unknown || "$evidence" == incomplete ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi;[[ "$actual" == "$expected" ]];done < "$S/fixtures/rust/release-evidence-decisions.tsv"
for t in '## Rust Release Evidence Mechanisms' 'proves only its declared claim' 'No fixed command set applies';do rg -F -q "$t" "$R/profiles/languages/rust/release.md";done
for t in '## Release Evidence Command Examples' 'cargo clippy --workspace' 'do not form an every-release checklist';do rg -F -q "$t" "$R/reference/recipes/rust-release.md";done
for t in '# Rust Release Standards Migration Index' 'defines no release' '[Rust release mechanisms]';do rg -F -q "$t" "$R/languages/rust/RUST-RELEASE-STANDARDS.md";done
! rg -q '^## |^Before every Rust release:|cargo (fmt|clippy|test|check)' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0820"{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")";[[ "$actual" == $'STD-0820\tprofiles/languages/rust/release.md\tsplit' ]]
printf 'Rust release evidence passed: 17 decisions, 1 exact disposition, legacy source closed\n'
