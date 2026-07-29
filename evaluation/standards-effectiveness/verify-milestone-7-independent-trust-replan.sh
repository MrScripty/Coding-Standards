#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly GROUP_FILE="$SCRIPT_DIR/milestone-7-independent-trust-groups.tsv"
readonly NEXT_SLICE="$SCRIPT_DIR/milestone-7-independent-trust-next-slice.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-independent-trust-replan.md"
readonly PARENT="$SCRIPT_DIR/milestone-7-decomposition.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed
declare -A disposed_source
declare -A disposed_target
declare -A disposed_disposition
declare -A remaining_by_owner
declare -A remaining_sources
declare -A remaining_owners
declare -A source_by_id
declare -A owner_by_id

while IFS=$'\t' read -r id source target disposition _rationale; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
  disposed_source["$id"]="$source"
  disposed_target["$id"]="$target"
  disposed_disposition["$id"]="$disposition"
done < "$DISPOSITIONS"

expected_ids=(STD-0596 STD-0597 STD-0598 STD-0599 STD-0600)
next_dispositions=0
for id in "${expected_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((next_dispositions += 1))
done
[[ "$next_dispositions" -eq 0 || "$next_dispositions" -eq 5 ]]

global_remaining=0
while IFS=$'\t' read -r id source _line owner _disposition _heading; do
  [[ "$id" == 'id' ]] && continue
  source_by_id["$id"]="$source"
  owner_by_id["$id"]="$owner"
  [[ -n "${disposed[$id]:-}" ]] && continue
  ((global_remaining += 1))
  remaining_sources["$source"]=1
  remaining_owners["$owner"]=1
  remaining_by_owner["$owner"]=$(( ${remaining_by_owner[$owner]:-0} + 1 ))
done < "$OWNER_MAP"
[[ "$global_remaining" -eq $((613 - next_dispositions)) ]]
[[ "${#remaining_sources[@]}" -eq 30 ]]
[[ "${#remaining_owners[@]}" -eq 29 ]]

missing_owners=0
for owner in "${!remaining_owners[@]}"; do
  [[ -e "$REPO_ROOT/$owner" ]] || ((missing_owners += 1))
done
[[ "$missing_owners" -eq 14 ]]

for dependency in \
  topics/security.md \
  topics/cross-platform.md \
  topics/contracts.md \
  topics/concurrency.md \
  profiles/boundaries/interop.md \
  profiles/boundaries/language-bindings.md \
  profiles/languages/rust/async.md; do
  [[ -e "$REPO_ROOT/$dependency" ]]
done

expected_groups=(
  $'1\ttopics/security.md\t12\texists\tnone\tnext-owner-audit'
  $'2\ttopics/cross-platform.md\t15\texists\tnone\tindependent-audit'
  $'3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tindependent-audit'
  $'4\tprofiles/languages/rust/cross-platform.md\t5\tmissing\ttopics/cross-platform.md\tdependent-audit'
  $'5\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/boundaries/interop.md\tdependent-audit'
  $'6\tprofiles/languages/rust/security.md\t3\texists\ttopics/security.md,profiles/languages/rust/async.md\tdependent-audit'
  $'7\tprofiles/languages/rust/language-bindings.md\t34\texists\tprofiles/boundaries/language-bindings.md,profiles/languages/rust/async.md\tdependent-audit'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

baseline_trust_total=0
current_trust_total=0
while IFS=$'\t' read -r order owner count owner_state prerequisite status extra; do
  [[ "$order" == 'order' ]] && continue
  [[ "$order" =~ ^[1-7]$ && "$count" =~ ^[0-9]+$ ]]
  expected_count="$count"
  if [[ "$owner" == 'topics/security.md' ]]; then
    expected_count=$((count - next_dispositions))
  fi
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$expected_count" ]]
  if [[ -e "$REPO_ROOT/$owner" ]]; then
    actual_state='exists'
  else
    actual_state='missing'
  fi
  [[ "$actual_state" == "$owner_state" ]]
  [[ -n "$prerequisite" && -n "$status" && -z "${extra:-}" ]]
  ((baseline_trust_total += count))
  ((current_trust_total += expected_count))
done < "$GROUP_FILE"
[[ "$baseline_trust_total" -eq 80 ]]
[[ "$current_trust_total" -eq $((80 - next_dispositions)) ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

row_count=0
expected_order=1
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b7a' && "$order" -eq "$expected_order" ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == "$target" ]]
  [[ "$source" == 'SECURITY-STANDARDS.md' ]]
  [[ "$target" == 'topics/security.md' ]]
  [[ "$disposition" == 'refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  if [[ -n "${disposed[$id]:-}" ]]; then
    [[ "${disposed_source[$id]}" == "$source" ]]
    [[ "${disposed_target[$id]}" == "$target" ]]
    [[ "${disposed_disposition[$id]}" == "$disposition" ]]
  fi
  ((row_count += 1))
  ((expected_order += 1))
done < "$NEXT_SLICE"
[[ "$row_count" -eq 5 ]]

required_report=(
  '613 frozen identifiers across 30 legacy'
  'seven groups total 80 undisposed identifiers'
  '`F016`'
  'Select `STD-0596` through `STD-0600`'
  '## Accepted Slice 7.4b6: Planning-Only Re-plan'
  'No normative standard, legacy standard, final disposition'
  'derive listener interface/address exposure from the declared service'
  'selected lifecycle owner and consume generic'
  'Concurrency for failure observation'
  '**No fallback:**'
  '**Pre-slice review:** accepted.'
  '**Resolved re-plan trigger:**'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '(milestone-7-independent-trust-replan.md)' "$PARENT"
rg -F -q '`7.4b5f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b6` (`Accepted`)' "$PLAN"
if [[ "$next_dispositions" -eq 0 ]]; then
  rg -F -q '| F016 | Planned for Milestone 7.4b7a |' "$FINDINGS"
  rg -F -q '## Planned Slice 7.4b7a: Generic Network Transport Contract' \
    "$REPORT"
  rg -F -q '`7.4b7a` (`Planned`)' "$PLAN"
  rg -F -q '**Next slice:** Milestone 7.4b7a' "$PLAN"
else
  rg -F -q '| F016 | Resolved in Milestone 7.4b7a |' "$FINDINGS"
  rg -F -q '## Accepted Slice 7.4b7a: Generic Network Transport Contract' \
    "$REPORT"
  rg -F -q '## Planned Slice 7.4b7b: Independent Trust-Boundary Remainder Re-plan' \
    "$REPORT"
  rg -F -q '`7.4b7a` (`Accepted`)' "$PLAN"
  rg -F -q '`7.4b7b` (`Planned`)' "$PLAN"
  rg -F -q '**Next slice:** Milestone 7.4b7b' "$PLAN"
fi

"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 independent trust re-plan passed: %s baseline IDs, %s current across 7 owners; next-slice dispositions %s/5\n' \
  "$baseline_trust_total" "$current_trust_total" "$next_dispositions"
