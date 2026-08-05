#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/discover-or-create-reference-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r case contracts discovery creation coordination readiness retry lifecycle evidence fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contracts" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$contracts" == missing || "$discovery" == missing ||
          "$creation" == missing || "$coordination" == missing ||
          "$readiness" == missing || "$lifecycle" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$creation" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=retain
  fi
  [[ "$actual" == "$expected" ]]
  count=$((count + 1))
done < "$F"
[[ "$count" -eq 14 ]]

for text in '### Conditional Pseudocode' \
  'resolve_selected_service(contracts)' 'creation.authorizes(observed)' \
  'readiness.observe_within_selected_budget' \
  'Every named operation above is a selected contract' \
  'does not carry prior invocation state' '### Conditional Consequences' \
  'remain separate claims'; do
  rg -F -q "$text" "$REFERENCE"
done

for prohibited in 'function get_or_create_service(address)' \
  'retry connect(address) until ready or timeout' \
  'No duplicate services consuming resources' \
  'Automatic recovery from crashed instances' \
  'Race-condition-safe startup sequence'; do
  if rg -F -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'invalid: prohibited discover-or-create example default remains: %s\n' "$prohibited" >&2
    exit 1
  fi
done

[[ "$(awk -F '\t' '$1 >= "STD-0104" && $1 <= "STD-0105" { print $1 FS $3 FS $4 }' "$DISPOSITIONS")" == $'STD-0104\treference/patterns/architecture.md\tmove\nSTD-0105\treference/patterns/architecture.md\tmove' ]]
[[ "$(awk -F '\t' '$1 >= "STD-0104" && $1 <= "STD-0105" && NF != 5 { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 0 ]]
"$S/verify-architecture-discover-or-create-convergence.sh"
printf 'Architecture discover-or-create reference closure passed: %d decisions, 2 exact dispositions\n' "$count"
