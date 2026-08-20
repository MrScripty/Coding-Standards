#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r case concerns owners lifecycle deployment contracts fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$owners" == contradictory ]]; then actual=typed-invalid
  elif [[ "$owners" == missing || "$contracts" == missing ]]; then actual=typed-unavailable
  elif [[ "$deployment" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$lifecycle" == long-lived ]]; then actual=compose
  elif [[ "$concerns" == one ]]; then actual=keep-together
  else actual=separate
  fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/architecture/owner-contract-decisions.tsv"
for text in 'ID: `topic.architecture`' '## Concern Boundaries' \
  'repository shape does not create them' '## Data And State Authority' \
  'location does not determine ownership' '## Runtime Composition' \
  'Do not fall back to the incumbent structure'; do
  rg -F -q "$text" "$R/topics/architecture.md"
done
mapfile -t populated < <(
  awk -F '\t' '$1>="STD-0137"&&$1<="STD-0147"{print $1}' \
    "$S/consolidation-dispositions.tsv" | sort
)
expected_populated=(STD-{0137..0147})
[[ "${populated[*]}" == "${expected_populated[*]}" ]]
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Architecture owner contract passed: 14 decisions, 11 dispositions\n'
