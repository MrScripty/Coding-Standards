#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly F="$S/fixtures/tooling/owner-contract-decisions.tsv"
readonly O="$R/workflows/tooling.md"

while IFS=$'\t' read -r case_id facts authority capability scope schedule fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$facts" == contradictory || "$authority" == missing ]]; then
    actual=typed-invalid
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$scope" == missing || "$schedule" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in 'ID: `workflow.tooling`' 'Tooling Authority' 'Hook Selection And Configuration' \
  'Scheduling And Cost' 'Persisted Artifact Checks' 'typed `invalid`' \
  'typed `unavailable`' 'typed `unsupported`' 'successful no-op' \
  'Do not default to a hook product'; do
  rg -F -q "$text" "$O"
done

for id in STD-0654 STD-0655 STD-0660 STD-0662 STD-0664 STD-0665; do
  awk -F '\t' -v id="$id" '$1 == id && $3 == "workflows/tooling.md" && $4 == "refine" { found = 1 } END { exit !found }' \
    "$S/consolidation-dispositions.tsv"
done

rg -F -q '[workflows/tooling.md](workflows/tooling.md)' "$R/README.md"
rg -F -q '[Tooling](workflows/tooling.md)' "$R/STANDARDS-ROUTER.md"
printf 'Tooling owner contract passed: 12 decisions, 6 exact dispositions\n'
