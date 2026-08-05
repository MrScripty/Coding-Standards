#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/process-instance-coordination-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r case identity invariant coordination capability lifecycle recovery diagnostic fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$identity" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$identity" == missing || "$invariant" == missing ||
          "$coordination" == missing || "$capability" == missing ||
          "$lifecycle" == missing || "$recovery" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
  count=$((count + 1))
done < "$F"
[[ "$count" -eq 15 ]]

for text in '## Process Instance Coordination' \
  '[Concurrency](topics/concurrency.md#select-coordination-from-the-invariant)' \
  '[Contracts](topics/contracts.md)' \
  '[Cross-Platform](topics/cross-platform.md#platform-support-contract)' \
  '[Resilience](topics/resilience.md#failure-classification-and-decision)' \
  'No PID contents' 'canonical typed outcome'; do
  rg -F -q "$text" "$LEGACY"
done

for text in '## Conditional Process Instance Coordination' \
  'selected instance identity' 'selected coordination boundary' \
  'Evidence that appears stale is not deletion authority' \
  'this pattern does not apply' 'the diagram or successful startup proves none'; do
  rg -F -q "$text" "$REFERENCE"
done

for prohibited in '### PID File Rules' '### PID File Contents' \
  '### Handling PID Reuse' '### Stale PID File Cleanup' \
  'kill(pid, 0)' '/proc/[pid]/stat' 'Always log when reclaiming'; do
  if rg -F -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'invalid: prohibited process-instance default remains: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0093..0098})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0093" && $1 <= "STD-0098" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 >= "STD-0093" && $1 <= "STD-0098" && NF != 5 { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 0 ]]
"$S/verify-milestone-7-row-39-decomposition.sh"
printf 'Architecture process-instance coordination passed: %d decisions, 6 exact dispositions\n' "$count"
