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
declare -A remaining_by_owner
declare -A remaining_sources
declare -A remaining_owners
declare -A source_by_id
declare -A owner_by_id

while IFS=$'\t' read -r id _source _target _disposition _rationale; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
done < "$DISPOSITIONS"

expected_ids=(
  STD-0280 STD-0281 STD-0282 STD-0283 STD-0284
  STD-0285 STD-0286 STD-0287 STD-0288
)
next_dispositions=0
for id in "${expected_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((next_dispositions += 1))
done
[[ "$next_dispositions" -eq 0 ]]

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
[[ "$global_remaining" -eq 608 ]]
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
  $'1\ttopics/security.md\t7\texists\tnone\tindependent-audit'
  $'2\ttopics/cross-platform.md\t15\texists\tnone\tnext-owner-audit'
  $'3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tindependent-audit'
  $'4\tprofiles/languages/rust/cross-platform.md\t5\tmissing\ttopics/cross-platform.md\tdependent-audit'
  $'5\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/boundaries/interop.md\tdependent-audit'
  $'6\tprofiles/languages/rust/security.md\t3\texists\ttopics/security.md,profiles/languages/rust/async.md\tdependent-audit'
  $'7\tprofiles/languages/rust/language-bindings.md\t34\texists\tprofiles/boundaries/language-bindings.md,profiles/languages/rust/async.md\tdependent-audit'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

trust_total=0
while IFS=$'\t' read -r order owner count owner_state prerequisite status extra; do
  [[ "$order" == 'order' ]] && continue
  [[ "$order" =~ ^[1-7]$ && "$count" =~ ^[0-9]+$ ]]
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$count" ]]
  if [[ -e "$REPO_ROOT/$owner" ]]; then
    actual_state='exists'
  else
    actual_state='missing'
  fi
  [[ "$actual_state" == "$owner_state" ]]
  [[ -n "$prerequisite" && -n "$status" && -z "${extra:-}" ]]
  ((trust_total += count))
done < "$GROUP_FILE"
[[ "$trust_total" -eq 75 ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

row_count=0
expected_order=1
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b7c' && "$order" -eq "$expected_order" ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == "$target" ]]
  [[ "$source" == 'CROSS-PLATFORM-STANDARDS.md' ]]
  [[ "$target" == 'topics/cross-platform.md' ]]
  if [[ "$order" -eq 1 ]]; then
    [[ "$disposition" == 'move' ]]
  else
    [[ "$disposition" == 'refine' ]]
  fi
  [[ -n "$rationale" && -z "${extra:-}" ]]
  [[ -z "${disposed[$id]:-}" ]]
  ((row_count += 1))
  ((expected_order += 1))
done < "$NEXT_SLICE"
[[ "$row_count" -eq 9 ]]

required_report=(
  '608 frozen identifiers across 30 legacy'
  'seven groups total 75 undisposed identifiers'
  '`F046`'
  'Select `STD-0280` through `STD-0288`'
  '## Accepted Slice 7.4b7b: Planning-Only Remainder Re-plan'
  'No normative or legacy standard, final disposition'
  'derive supported targets and support claims from an'
  'select compile-time, runtime, composition, and dispatch mechanisms'
  'unblocks the missing Rust'
  '## Planned Slice 7.4b7c: Generic Platform Target And Isolation Contract'
  '**No fallback:**'
  '**Pre-slice review:** accepted.'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '(milestone-7-independent-trust-replan.md)' "$PARENT"
rg -F -q '| F046 | Planned for Milestone 7.4b7c |' "$FINDINGS"
rg -F -q '`7.4b7a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7b` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7c` (`Planned`)' "$PLAN"
rg -F -q '**Next slice:** Milestone 7.4b7c' "$PLAN"

"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 independent trust re-plan passed: %s IDs across 7 owners; next slice 9 IDs with %s dispositions\n' \
  "$trust_total" "$next_dispositions"
