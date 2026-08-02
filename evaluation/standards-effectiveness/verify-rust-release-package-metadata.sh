#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id contracts unit channel metadata capability evidence fallback expected extra; do
  [[ "$id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contracts" == contradictory ]]; then actual=typed-invalid
  elif [[ "$contracts" == missing || "$unit" == unknown || "$channel" == unknown || "$evidence" == incomplete ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported; else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/release-package-metadata-decisions.tsv"
for text in '## Cargo Package Release Metadata Mechanisms' 'express the selected Rust package facts' 'Cargo metadata does not select a package name' 'registry acceptance cannot complete missing authority'; do rg -F -q "$text" "$R/profiles/languages/rust/release.md"; done
for text in '## Cargo Package Metadata Example' 'name = "my-library"' 'does not define required fields'; do rg -F -q "$text" "$R/reference/recipes/rust-release.md"; done
for text in 'Release](../../workflows/release.md)' 'Contracts](../../topics/contracts.md)' 'Rust Release profile](../../profiles/languages/rust/release.md#cargo-package-release-metadata-mechanisms)'; do rg -F -q "$text" "$R/languages/rust/RUST-RELEASE-STANDARDS.md"; done
! rg -F -q 'Publishable crates should have complete metadata' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
actual="$(awk -F '\t' '$1=="STD-0813" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")"
[[ "$actual" == $'STD-0813\tprofiles/languages/rust/release.md\tsplit' ]]
printf 'Rust release package metadata passed: 16 decisions, 1 exact disposition\n'
