#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r id contract tooling owner capability evidence fallback expected extra; do
  [[ "$id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ]]; then actual=typed-invalid
  elif [[ "$contract" == missing || "$tooling" == missing || "$owner" == unknown || "$evidence" == incomplete ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported; else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/rust/dependency-audit-adapter-decisions.tsv"
for text in '## Dependency Audit Adapter Mechanisms' 'use supported Rust audit adapters only' 'does not select its product'; do rg -F -q "$text" "$R/profiles/languages/rust/dependencies.md"; done
for text in '## Audit Adapter Examples' 'alternatives, not a required suite' 'rg "use <crate>|<crate>::"'; do rg -F -q "$text" "$R/reference/recipes/rust-dependencies.md"; done
! rg -F -q 'cargo machete' "$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"
mapfile -t actual < <(awk -F '\t' '$1 >= "STD-0747" && $1 <= "STD-0748" {print $1 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")
expected=($'STD-0747\tprofiles/languages/rust/dependencies.md\tsplit' $'STD-0748\treference/recipes/rust-dependencies.md\tmove')
[[ "${actual[*]}" == "${expected[*]}" ]]
printf 'Rust dependency audit adapters passed: 12 decisions, 2 exact dispositions\n'
