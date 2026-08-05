#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/pattern-selection-closure-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r case responsibility authority contracts lifecycle capability evidence label fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none && "$fallback" != not-needed ||
        "$authority" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$responsibility" == missing || "$authority" == missing ||
          "$contracts" == missing || "$lifecycle" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
  count=$((count + 1))
done < "$F"
[[ "$count" -eq 18 ]]

for text in '## Choosing Patterns' '[Standards Router](STANDARDS-ROUTER.md)' \
  'actual responsibility' 'A broad situation label does not select' \
  '[Architecture Pattern Reference](reference/patterns/architecture.md)' \
  'nearest example' 'canonical typed outcome'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in '| Situation | Recommended Pattern |' \
  '| Multi-layer application | Layered Separation of Concerns |' \
  '| Client-server state management | Backend-Owned Data |' \
  '| Parallel team development | Immutable Contracts |' \
  '| Single-instance process requirement | Process Instance Coordination |' \
  '| Service that any process may need to start | Discover-or-Create |'; do
  if rg -F -q "$prohibited" "$LEGACY"; then
    printf 'invalid: universal pattern-selection default remains: %s\n' "$prohibited" >&2
    exit 1
  fi
done

[[ "$(awk -F '\t' '$1 == "STD-0134" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'ARCHITECTURE-PATTERNS.md\treference/patterns/architecture.md\tmerge-duplicate' ]]
[[ "$(awk -F '\t' '$1 == "STD-0134" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]
"$S/verify-architecture-discover-or-create-reference.sh"
"$S/verify-milestone-7-row-40-decomposition.sh"
printf 'Architecture pattern-selection closure passed: %d decisions, 1 exact disposition, P32 closed\n' "$count"
