#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/documentation/directory-readme-closure-decisions.tsv"
WORKFLOW="$R/workflows/documentation.md"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

count=0
while IFS=$'\t' read -r case impact boundary owner profile fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$owner" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$impact" == missing || "$boundary" == missing || "$owner" == missing || "$profile" == missing ]]; then
    actual=typed-unavailable
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
  count=$((count + 1))
done < "$F"
[[ "$count" -eq 13 ]]

for text in 'Directory count, file count' 'boundary-readme' \
  'If the impact cannot be classified' 'Do not default to a `src/` directory'; do
  rg -F -q "$text" "$WORKFLOW"
done

if rg -F -q 'Directory README Requirement' "$LEGACY"; then
  printf 'invalid: legacy directory README authority remains active\n' >&2
  exit 1
fi

[[ "$(awk -F '\t' '$1 == "STD-0088" { n++; row=$2 FS $3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == $'1\tARCHITECTURE-PATTERNS.md\tworkflows/documentation.md\tmerge-duplicate' ]]
"$S/verify-documentation-policy-consolidation.sh"
"$S/verify-undisposed-source-gaps.sh"
printf 'Documentation directory-README closure passed: %d decisions, 1 exact disposition\n' "$count"
