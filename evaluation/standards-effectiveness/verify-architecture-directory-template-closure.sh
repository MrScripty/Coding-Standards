#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/directory-template-closure-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case boundaries documentation ownership fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$ownership" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$boundaries" == missing || "$documentation" == missing || "$ownership" == missing ]]; then
    actual=typed-unavailable
  else
    actual=route
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '[Concern Boundaries](topics/architecture.md#concern-boundaries)' \
  '[Documentation Workflow](workflows/documentation.md)' \
  'No general-purpose project tree is retained' \
  'not select responsibilities'; do
  rg -F -q "$text" "$LEGACY"
done
for text in '## Activity Tracing Pattern' '## Process Instance Coordination' \
  '## Discover-or-Create Pattern'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'A general-purpose project layout' \
  'presentation/           # UI layer' 'application/            # Application layer' \
  'domain/                 # Domain layer' 'shared/                 # Cross-cutting concerns' \
  'Directory README Requirement'; do
  if rg -F -q "$prohibited" "$LEGACY"; then
    printf 'universal directory default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

[[ "$(awk -F '\t' '$1 == "STD-0087" { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == $'1\ttopics/architecture.md\tmerge-duplicate' ]]
mapfile -t row_ids < <(awk -F '\t' 'NR > 1 { print $1 }' "$S/milestone-7-row-37-owner-validation.tsv")
[[ "${#row_ids[@]}" -eq 19 ]]
for id in "${row_ids[@]}"; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]
done

"$S/verify-frontend-view-model-lineage.sh"
printf 'Architecture directory-template closure passed: 10 decisions, 1 exact disposition, 19 row IDs complete\n'
