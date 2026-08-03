#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/rust/release-owner-decisions.tsv"; P="$R/profiles/languages/rust/release.md"; X="$R/reference/recipes/rust-release.md"; L="$R/languages/rust/RUST-RELEASE-STANDARDS.md"
while IFS=$'\t' read -r id contract unit consumer channel mechanism capability fallback expected extra; do
  [[ "$id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ]]; then actual=typed-invalid
  elif [[ "$contract" == missing || "$unit" == unknown || "$consumer" == unknown || "$channel" == unknown ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported; else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$F"
"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" "$R/workflows/verification.md" "$R/workflows/release.md" "$R/topics/contracts.md" "$R/topics/dependencies.md" "$R/profiles/languages/rust/README.md" "$R/profiles/languages/rust/dependencies.md" "$P" "$X"
for text in '## Mechanism Authority' 'Generic owners select release boundaries' 'create or complete generic policy' '## Typed Outcomes' 'Do not fall back to incumbent metadata' '## Verification'; do rg -F -q "$text" "$P"; done
for text in 'Level: `REFERENCE`' 'This material is non-normative' 'cannot select versions'; do rg -F -q "$text" "$X"; done
rg -F -q 'profiles/languages/rust/release.md' "$R/STANDARDS-ROUTER.md"
rg -F -q 'profiles/languages/rust/release.md' "$R/README.md"
rg -F -q '[Rust release mechanisms](../../profiles/languages/rust/release.md)' "$L"
actual="$(awk -F '\t' '$1=="STD-0810" {print $1 "\t" $2 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")"
[[ "$actual" == $'STD-0810\tlanguages/rust/RUST-RELEASE-STANDARDS.md\tprofiles/languages/rust/release.md\tindex' ]]
printf 'Rust release owner passed: 16 decisions, 1 exact disposition\n'
