#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/tooling/editor-configuration-decisions.tsv"
O="$R/workflows/tooling.md"

while IFS=$'\t' read -r case_id facts mechanism scope precedence representable fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none ]]; then
    actual=typed-invalid
  elif [[ "$facts" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$mechanism" == missing || "$scope" == missing || "$precedence" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$representable" == no ]]; then
    actual=typed-unsupported
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Editor And File Configuration' 'editor-neutral configuration mechanism' \
  'file-format semantics' 'generated-file authority' "configuration's scope" \
  'EditorConfig is one possible transport' 'Do not default to spaces' \
  'typed `invalid`' 'typed `unavailable`' 'typed `unsupported`'; do
  rg -F -q "$text" "$O"
done

for id in STD-0666 STD-0673; do
  awk -F '\t' -v id="$id" '$1 == id && $3 == "workflows/tooling.md" && $4 == "refine" { found = 1 } END { exit !found }' \
    "$S/consolidation-dispositions.tsv"
done

rg -F -q '[Tooling](workflows/tooling.md#editor-and-file-configuration)' \
  "$R/TOOLING-STANDARDS.md"
! rg -F -q '| Setting | Recommended |' "$R/TOOLING-STANDARDS.md"
printf 'Tooling editor configuration passed: 12 decisions, 2 exact dispositions\n'
