#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/architecture/durable-workflow-decisions.tsv"
LEGACY="$R/ARCHITECTURE-PATTERNS.md"
REFERENCE="$R/reference/patterns/architecture.md"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

while IFS=$'\t' read -r case authority contracts durability replay ordering fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$authority" == missing || "$contracts" == missing || "$durability" == missing || "$replay" == missing || "$ordering" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$durability" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$durability" == not-required ]]; then
    actual=omit-durable
  else
    actual=illustrate
  fi
  [[ "$actual" == "$expected" ]]
done < "$F"

for text in '## Conditional Durable Workflow Map' \
  'After canonical owners select a workflow' \
  'This map does not require commands, events, event sourcing' \
  'can omit the durable' 'than selecting the illustrated mechanism'; do
  rg -F -q "$text" "$REFERENCE"
done
for text in '[Architecture](topics/architecture.md#data-and-state-authority)' \
  '[Invariant Contracts](topics/contracts.md#invariant-contracts)' \
  '[Persistence contract](profiles/boundaries/persistence.md#durable-mutation-contract)' \
  '[Resilience](topics/resilience.md#replay-and-resumption-evidence)' \
  '[Conditional Durable Workflow Map](reference/patterns/architecture.md#conditional-durable-workflow-map)'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'append canonical event(s)' \
  'Use stable command identifiers' \
  'Persist canonical events or equivalent durable state transitions' \
  'Build read models/projections' '### Typical Components' \
  'require tests for replay/bootstrap'; do
  if rg -F -i -q "$prohibited" "$LEGACY" "$REFERENCE"; then
    printf 'fixed durable-workflow default remains active: %s\n' "$prohibited" >&2
    exit 1
  fi
done

expected=(STD-{0074..0080})
mapfile -t ids < <(
  awk -F '\t' '$1 >= "STD-0074" && $1 <= "STD-0080" { print $1 }' "$DISPOSITIONS"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
while IFS=$'\t' read -r id owner disposition reference_treatment rationale; do
  [[ "$id" == id || "$id" < STD-0074 || "$id" > STD-0080 ]] && continue
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { n++; row=$3 FS $4 } END { print n+0 FS row }' "$DISPOSITIONS")" == "1	$owner	$disposition" ]]
done < "$S/milestone-7-row-37-owner-validation.tsv"

"$S/verify-architecture-composition-root-pattern.sh"
printf 'Architecture durable-workflow pattern passed: 12 decisions and 7 exact dispositions\n'
