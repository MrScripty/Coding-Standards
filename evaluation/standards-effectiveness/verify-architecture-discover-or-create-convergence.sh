#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/discover-or-create-convergence-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r case service_owner discovery identity exclusion readiness transport retry lifecycle fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$service_owner" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$service_owner" == missing || "$discovery" == missing ||
          "$identity" == missing || "$exclusion" == missing ||
          "$readiness" == missing || "$transport" == missing ||
          "$lifecycle" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$transport" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
  count=$((count + 1))
done < "$F"
[[ "$count" -eq 16 ]]

for text in '## Discover-or-Create Pattern' \
  '[Architecture](topics/architecture.md)' '[Contracts](topics/contracts.md)' \
  '[Concurrency](topics/concurrency.md#select-coordination-from-the-invariant)' \
  '[Resilience](topics/resilience.md)' \
  '[Security](topics/security.md#network-transport-boundary)' \
  'possible mechanisms' 'cannot establish applicability'; do
  rg -F -q "$text" "$LEGACY"
done

for text in '## Conditional Discover-Or-Create Convergence' \
  'selected discovery operation' 'creation authorized' \
  'Neither discovery failure' \
  'does not require connection before creation' 'loop until success'; do
  rg -F -q "$text" "$REFERENCE"
done

section="$(awk '/^## Discover-or-Create Pattern/{on=1} /^### Example/{on=0} on{print}' "$LEGACY")"
for prohibited in '### The Pattern' '### Instance Convergence Flow' \
  '### Rules' '### Ownership Models' 'Attempt connection before creation' \
  'Retry with backoff after lock failure' 'Last-client-standing' \
  'Independent daemon'; do
  if [[ "$section" == *"$prohibited"* ]]; then
    printf 'invalid: prohibited discover-or-create default remains: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0099..0103})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0099" && $1 <= "STD-0103" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 >= "STD-0099" && $1 <= "STD-0103" && NF != 5 { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 0 ]]
"$S/verify-architecture-process-instance-coordination.sh"
printf 'Architecture discover-or-create convergence passed: %d decisions, 5 exact dispositions\n' "$count"
