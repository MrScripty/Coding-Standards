#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/layered-pattern-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case concerns owners contracts changes fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$owners" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$owners" == missing || "$contracts" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$concerns" == one ]]; then
    actual=keep-together
  elif [[ "$changes" == coupled ]]; then
    actual=reconsider-boundary
  else
    actual=illustrate
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Conditional Layered Arrangement' \
  'This shape does not require these names, four layers' \
  'Dependencies in an adaptation point toward the owner of each stable contract' \
  '### Conditional Consequences'; do
  rg -F -q "$text" "$REFERENCE"
done
for text in '[Architecture](topics/architecture.md)' \
  '[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-layered-arrangement)'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'Dependencies point inward only' \
  'Domain is the core and depends on nothing' \
  'Organize code into horizontal layers' \
  'Outer layers depend on inner layers' \
  'Inner layers never depend on outer layers'; do
  if rg -F -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'universal layered default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0028..0033})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0028" && $1 <= "STD-0033" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0028 || "$id" > STD-0033 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-36-owner-validation.tsv"

"$S/verify-architecture-pattern-reference-owner.sh"
printf 'Architecture layered pattern passed: 8 decisions and 6 exact dispositions\n'
