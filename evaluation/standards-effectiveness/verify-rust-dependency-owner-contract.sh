#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/rust/dependency-owner-decisions.tsv"
P="$R/profiles/languages/rust/dependencies.md"
L="$R/languages/rust/RUST-DEPENDENCY-STANDARDS.md"

while IFS=$'\t' read -r case_id contract consumer resolver mechanism capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ]]; then actual=typed-invalid
  elif [[ "$contract" == missing || "$consumer" == unknown || "$resolver" == unknown ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$F"

"$S/check-metadata.sh" "$R" "$R/CORE-STANDARDS.md" \
  "$R/workflows/verification.md" "$R/workflows/release.md" \
  "$R/topics/contracts.md" "$R/topics/dependencies.md" \
  "$R/profiles/languages/rust/README.md" "$P"
for text in '## Mechanism Authority' 'Generic owners select dependency requirements' \
  'Existing manifests' '## Typed Outcomes' 'Do not fall back to the incumbent manifest' \
  '## Verification'; do rg -F -q "$text" "$P"; done
rg -F -q 'profiles/languages/rust/dependencies.md' "$R/STANDARDS-ROUTER.md"
rg -F -q '[Rust dependency mechanisms](../../profiles/languages/rust/dependencies.md)' "$L"
actual="$(awk -F '\t' '$1 == "STD-0731" {print $1 "\t" $2 "\t" $3 "\t" $4}' "$S/consolidation-dispositions.tsv")"
expected=$'STD-0731\tlanguages/rust/RUST-DEPENDENCY-STANDARDS.md\tprofiles/languages/rust/dependencies.md\tindex'
[[ "$actual" == "$expected" ]]
printf 'Rust dependency owner passed: 14 decisions, 1 exact disposition\n'
