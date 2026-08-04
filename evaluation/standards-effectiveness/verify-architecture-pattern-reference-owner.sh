#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/reference-owner-decisions.tsv"
REFERENCE="$R/reference/patterns/architecture.md"
ARCHITECTURE="$R/topics/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case architecture facts capability fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$architecture" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$architecture" == missing || "$facts" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=adapt
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

"$S/check-metadata.sh" "$R" \
  "$R/CORE-STANDARDS.md" \
  "$R/workflows/verification.md" \
  "$R/topics/contracts.md" \
  "$ARCHITECTURE" \
  "$REFERENCE"

for text in 'Role: `reference`' 'Level: `REFERENCE`' \
  'This material is non-normative' \
  'Pattern presence does not establish applicability' \
  '## Adaptation Boundary' '## Reading A Pattern' '## Typed Outcomes' \
  '[Architecture](../../topics/architecture.md)'; do
  rg -F -q "$text" "$REFERENCE"
done
rg -F -q '[Architecture Pattern Reference](../reference/patterns/architecture.md)' "$ARCHITECTURE"

for prohibited in 'Dependencies point inward only' \
  'Organize code into horizontal layers' \
  'single source of truth' \
  'No Optimistic Updates for Backend-Owned Data'; do
  if rg -F -q "$prohibited" "$REFERENCE"; then
    printf 'reference owner contains unapproved legacy authority: %s\n' "$prohibited" >&2
    exit 1
  fi
done

[[ "$(awk -F '\t' '$1 == "STD-0027" { n++; row=$2 FS $3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == $'1\tARCHITECTURE-PATTERNS.md\treference/patterns/architecture.md\tindex' ]]
printf 'Architecture pattern reference owner passed: 7 decisions and 1 exact disposition\n'
