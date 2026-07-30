#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly B="$S/fixtures/language-bindings/surface-contract"
readonly PROFILE="$R/profiles/boundaries/language-bindings.md"
readonly LEGACY="$R/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly INVENTORY="$S/generated/section-inventory.tsv"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"

"$S/check-decision-table.sh" "$B-schema.tsv" "$B-decisions.tsv" "$B-observed.tsv"

while IFS=$'\t' read -r case_id consumer selection semantics support host_subset \
  documentation compatibility evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none || "$semantics" == unknown && "$selection" == selected ]]; then
    actual=typed-invalid
  elif [[ "$selection" == not-selected ]]; then
    actual=omit
  elif [[ "$consumer" == missing || "$selection" == missing ||
          "$support" == missing || "$host_subset" == missing ||
          "$documentation" == missing || "$compatibility" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=expose
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$B-decisions.tsv"

expected_ids=(STD-{0768..0771})
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0768" && $1 <= "STD-0771" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0768" && $1 <= "STD-0771" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

required=(
  '## Exported Surface Contract'
  'Expose only selected client operations'
  'parity nor divergence is a default'
  'no fixed support-tier vocabulary is universal'
  'native and real host evidence'
  'Do not export all technically available operations'
)
for text in "${required[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(sed -n '/^## Binding Surface Policy$/,/^---$/p' "$LEGACY")"
rg -F -q 'language-bindings.md#exported-surface-contract' <<< "$legacy_section"
for removed in \
  'Export only client-facing capabilities by default' \
  'supported`, `experimental`, and `internal-only' \
  'Surface Review Questions'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

"$S/verify-language-binding-boundary.sh"
"$S/verify-milestone-7-row-7-decomposition.sh"

printf 'Language binding surface contract passed: %s decisions, 4 exact dispositions\n' \
  "$(( $(wc -l < "$B-decisions.tsv") - 1 ))"
