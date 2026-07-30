#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly B="$S/fixtures/contracts/binding-generation-authority"
readonly CONTRACTS="$R/topics/contracts.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly INVENTORY="$S/generated/section-inventory.tsv"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

"$S/check-decision-table.sh" "$B-schema.tsv" "$B-decisions.tsv" "$B-observed.tsv"

while IFS=$'\t' read -r case_id authority generator derivation evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none || "$authority" =~ ^(compiled-artifact|source-annotation|consumer-output)$ ]]; then
    actual=typed-invalid
  elif [[ "$authority" == missing || "$generator" == missing ||
          "$derivation" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$B-decisions.tsv"

expected_ids=(STD-0782 STD-0783)
mapfile -t inventory_ids < <(awk -F '\t' '$1 == "STD-0782" || $1 == "STD-0783" { print $1 }' "$INVENTORY")
mapfile -t disposition_ids < <(awk -F '\t' 'NR > 1 && ($1 == "STD-0782" || $1 == "STD-0783") { print $1 }' "$DISPOSITIONS")
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

for text in \
  'Select canonical generation authority' \
  'compiled implementation artifact' \
  'source annotation' \
  'consumer output' \
  'deterministic derivation' \
  'producer/consumer'; do
  rg -F -q "$text" "$CONTRACTS"
done

legacy_section="$(sed -n '/^## Code Generation Strategy$/,/^### Annotation Approach$/p' "$LEGACY")"
rg -F -q 'topics/contracts.md#cross-language-contract-selection' <<< "$legacy_section"
for removed in \
  'Bindings are generated from the compiled core library' \
  'The annotated Rust code is the single source of truth' \
  'uniffi-bindgen generate'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

"$S/verify-binding-contract-evolution.sh"
"$S/verify-milestone-7-row-8-decomposition.sh"

printf 'Binding generation authority passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$B-decisions.tsv") - 1 ))"
