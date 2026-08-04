#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/data-authority-pattern-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case authority projection synchronization reconciliation fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$authority" == missing || "$projection" == missing || "$synchronization" == missing || "$reconciliation" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$authority" != server ]]; then
    actual=pattern-not-applicable
  elif [[ "$projection" == optimistic ]]; then
    actual=illustrate-optimistic
  else
    actual=illustrate-confirmed
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Conditional Server-Authoritative Projection' \
  'The server location does not create authority' \
  '### Conditional Flow' \
  'Optimistic projection is also valid' \
  'switching projection modes'; do
  rg -F -q "$text" "$REFERENCE"
done
for text in '[Architecture](topics/architecture.md)' \
  '[Frontend application profile](profiles/applications/frontend.md)' \
  '[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-server-authoritative-projection)'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'backend is the **single source of truth**' \
  'Frontend CANNOT hold' \
  'Backend-owned data must never be updated speculatively' \
  'If the backend has no concept of this state' \
  'No state synchronization bugs'; do
  if rg -F -i -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'location-based data-authority default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0040..0045})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0040" && $1 <= "STD-0045" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0040 || "$id" > STD-0045 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-36-owner-validation.tsv"

"$S/verify-architecture-monorepo-pattern.sh"
printf 'Architecture data-authority pattern passed: 10 decisions and 6 exact dispositions\n'
