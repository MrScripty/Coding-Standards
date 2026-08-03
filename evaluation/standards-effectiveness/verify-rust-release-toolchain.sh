#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id contract release_claim dependency mechanism capability evidence fallback expected extra; do
  [[ "$id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ]]; then actual=typed-invalid
  elif [[ "$contract" == missing || "$release_claim" == missing || "$evidence" == incomplete || ( "$mechanism" == lockfile && "$dependency" == missing ) ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$mechanism" == lockfile ]]; then actual=route-rust-dependency; else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/release-toolchain-decisions.tsv"
for text in '## Toolchain Declaration Mechanisms' 'select supported Rust toolchain declaration mechanisms' 'Lockfile selection and resolution policy remain' 're-own, alias, or infer'; do rg -F -q "$text" "$R/profiles/languages/rust/release.md"; done
for text in '## Toolchain Declaration Example' 'channel = "1.78.0"' 'does not require pinning'; do rg -F -q "$text" "$R/reference/recipes/rust-release.md"; done
for text in '[Release](../../workflows/release.md)' '[Dependencies](../../topics/dependencies.md)' '[Rust dependency mechanisms](../../profiles/languages/rust/dependencies.md)' '[Rust release mechanisms](../../profiles/languages/rust/release.md)'; do rg -F -q "$text" "$R/languages/rust/RUST-RELEASE-STANDARDS.md"; done
! rg -F -q 'Application repositories and production workspaces should commit' "$R/languages/rust/RUST-RELEASE-STANDARDS.md"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0811" && $1 <= "STD-0812" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0811\tprofiles/languages/rust/release.md\tsplit' $'STD-0812\treference/recipes/rust-release.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust release toolchain passed: 15 decisions, 2 exact dispositions\n'
