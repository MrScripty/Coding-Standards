#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WAVES="$SCRIPT_DIR/milestone-7-waves.tsv"
readonly FIRST_SLICE="$SCRIPT_DIR/milestone-7-first-slice.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-decomposition.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed
declare -A disposed_source
declare -A disposed_target
declare -A disposed_disposition
declare -A remaining_by_owner
declare -A remaining_sources
declare -A proposed_owners

while IFS=$'\t' read -r id source target disposition _rationale; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
  disposed_source["$id"]="$source"
  disposed_target["$id"]="$target"
  disposed_disposition["$id"]="$disposition"
done < "$DISPOSITIONS"

remaining_count=0
while IFS=$'\t' read -r id source _line owner _disposition _heading; do
  [[ "$id" == 'id' ]] && continue
  [[ -n "${disposed[$id]:-}" ]] && continue
  ((remaining_count += 1))
  remaining_sources["$source"]=1
  proposed_owners["$owner"]=1
  remaining_by_owner["$owner"]=$(( ${remaining_by_owner[$owner]:-0} + 1 ))
done < "$OWNER_MAP"

[[ "$remaining_count" -le 698 ]]
[[ "${#remaining_sources[@]}" -le 33 ]]
[[ "${#proposed_owners[@]}" -le 33 ]]

missing_owners=0
for owner in "${!proposed_owners[@]}"; do
  [[ -e "$REPO_ROOT/$owner" ]] || ((missing_owners += 1))
done
[[ "$missing_owners" -le 25 ]]

declare -A wave_owners
declare -A wave_orders
wave_total=0
while IFS=$'\t' read -r wave order owner count rationale extra; do
  if [[ "$wave" == 'wave' ]]; then
    [[ "$order" == 'order' && "$owner" == 'future_owner' ]]
    continue
  fi
  [[ "$wave" =~ ^(trust-boundaries|lifecycle-runtime|process-dependencies|application-boundaries|reference-index-closure)$ ]]
  [[ "$order" =~ ^[0-9]+$ ]]
  [[ -n "$owner" && -z "${wave_owners[$owner]:-}" ]]
  [[ -z "${wave_orders[$wave:$order]:-}" ]]
  [[ "$count" =~ ^[0-9]+$ ]]
  [[ "${remaining_by_owner[$owner]:-0}" -le "$count" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  wave_owners["$owner"]=1
  wave_orders["$wave:$order"]=1
  ((wave_total += count))
done < "$WAVES"

[[ "${#wave_owners[@]}" -eq 33 ]]
[[ "$wave_total" -eq 698 ]]
for owner in "${!proposed_owners[@]}"; do
  [[ -n "${wave_owners[$owner]:-}" ]]
done

expected_first=(
  STD-0289 STD-0290 STD-0291 STD-0292 STD-0293
  STD-0584 STD-0585 STD-0586 STD-0587
)
mapfile -t actual_first < <(tail -n +2 "$FIRST_SLICE" | cut -f1)
[[ "${actual_first[*]}" == "${expected_first[*]}" ]]

while IFS=$'\t' read -r id source owner disposition rationale extra; do
  [[ "$id" == 'id' ]] && continue
  [[ "$source" =~ ^(SECURITY-STANDARDS.md|CROSS-PLATFORM-STANDARDS.md)$ ]]
  [[ "$owner" =~ ^topics/(security|cross-platform).md$ ]]
  [[ "$disposition" =~ ^(move|merge|refine)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  inventory_source="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $2 }' "$OWNER_MAP"
  )"
  inventory_owner="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $4 }' "$OWNER_MAP"
  )"
  [[ "$inventory_source" == "$source" ]]
  [[ "$inventory_owner" == "$owner" ]]
  if [[ -n "${disposed[$id]:-}" ]]; then
    [[ "${disposed_source[$id]}" == "$source" ]]
    [[ "${disposed_target[$id]}" == "$owner" ]]
    [[ "${disposed_disposition[$id]}" == "$disposition" ]]
  fi
done < "$FIRST_SLICE"

rg -F -q '[milestone-7-waves.tsv](milestone-7-waves.tsv)' "$REPORT"
rg -F -q '[milestone-7-first-slice.tsv](milestone-7-first-slice.tsv)' "$REPORT"
rg -F -q 'typed diagnostic' "$REPORT"
rg -F -q 'milestone-7-decomposition.md' "$PLAN"

printf 'Milestone 7 rolling decomposition passed: 698 planned IDs; %s IDs, %s sources, %s owners, %s missing owners currently remain.\n' \
  "$remaining_count" "${#remaining_sources[@]}" "${#proposed_owners[@]}" "$missing_owners"
