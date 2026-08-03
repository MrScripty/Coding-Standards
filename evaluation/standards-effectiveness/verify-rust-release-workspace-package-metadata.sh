#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id unit facts capability evidence fallback expected extra; do
 [[ "$id" == case ]]&&continue; [[ -z "${extra:-}" ]]; if [[ "$fallback" != none || "$unit" == contradictory ]];then actual=typed-invalid;elif [[ "$unit" == missing || "$facts" == missing || "$evidence" == incomplete ]];then actual=typed-unavailable;elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi; [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/release-workspace-package-metadata-decisions.tsv"
for t in '## Cargo Workspace Package-Metadata Mechanisms' 'Each inherited field remains an accepted fact' 'cannot require lockstep versioning';do rg -F -q "$t" "$R/profiles/languages/rust/release.md";done
for t in '## Workspace Package-Metadata Example' '[workspace.package]' 'separately owned Rust Dependency mechanisms';do rg -F -q "$t" "$R/reference/recipes/rust-release.md";done
! rg -F -q 'Use `[workspace.package]` to define shared version metadata once' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
for spec in $'STD-0815\tprofiles/languages/rust/release.md\tsplit' $'STD-0816\treference/recipes/rust-release.md\tmove' $'STD-0817\treference/recipes/rust-release.md\tmove';do id="${spec%%$'\t'*}"; actual="$(awk -F '\t' -v id="$id" '$1==id{print $1"\t"$3"\t"$4}' "$S/consolidation-dispositions.tsv")"; [[ "$actual" == "$spec" ]];done
printf 'Rust release workspace package metadata passed: 16 decisions, 3 exact dispositions\n'
