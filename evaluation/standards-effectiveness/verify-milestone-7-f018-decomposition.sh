#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MAP="$SCRIPT_DIR/milestone-7-f018-slices.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-f018-decomposition.md"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

expected_ids=(
  STD-0051 STD-0052 STD-0053 STD-0054
  STD-0063 STD-0064 STD-0065 STD-0066 STD-0067 STD-0068
  STD-0592 STD-0593 STD-0594 STD-0595
)
mapfile -t actual_ids < <(tail -n +2 "$MAP" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]
[[ "$(printf '%s\n' "${actual_ids[@]}" | sort | uniq -d | wc -l)" -eq 0 ]]

row_count=0
disposed_b=0
disposed_c=0
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  if [[ "$slice" == 'slice' ]]; then
    [[ "$order" == 'order' && "$id" == 'id' && "$source" == 'source' ]]
    continue
  fi

  [[ "$slice" =~ ^7\.4b2(b|c)$ ]]
  [[ "$order" =~ ^[0-9]+$ ]]
  [[ "$source" =~ ^(ARCHITECTURE-PATTERNS.md|SECURITY-STANDARDS.md)$ ]]
  [[ "$target" =~ ^(topics/(contracts|security).md|profiles/boundaries/ipc.md)$ ]]
  [[ "$disposition" =~ ^(move|merge|refine)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]

  inventory_source="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $2 }' "$INVENTORY"
  )"
  [[ "$inventory_source" == "$source" ]]
  current_disposition="$(
    awk -F '\t' -v expected="$id" '
      NR > 1 && $1 == expected {
        count += 1
        value = $2 "\t" $3 "\t" $4
      }
      END {
        if (count > 1) {
          exit 2
        }
        if (count == 1) {
          print value
        }
      }
    ' "$DISPOSITIONS"
  )"
  if [[ -n "$current_disposition" ]]; then
    [[ "$current_disposition" == \
      "$source"$'\t'"$target"$'\t'"$disposition" ]]
    if [[ "$slice" == '7.4b2b' ]]; then
      ((disposed_b += 1))
    else
      ((disposed_c += 1))
    fi
  fi

  case "$id" in
    STD-0051)
      [[ "$slice:$target:$disposition" == '7.4b2b:topics/contracts.md:merge' ]]
      ;;
    STD-0052|STD-0053|STD-0054)
      [[ "$slice:$target:$disposition" == '7.4b2b:topics/contracts.md:refine' ]]
      ;;
    STD-0063)
      [[ "$slice:$target:$disposition" == '7.4b2c:profiles/boundaries/ipc.md:move' ]]
      ;;
    STD-0064|STD-0065|STD-0067)
      [[ "$slice:$target:$disposition" == '7.4b2c:profiles/boundaries/ipc.md:refine' ]]
      ;;
    STD-0066)
      [[ "$slice:$target:$disposition" == '7.4b2c:profiles/boundaries/ipc.md:move' ]]
      ;;
    STD-0068)
      [[ "$slice:$target:$disposition" == '7.4b2c:profiles/boundaries/ipc.md:merge' ]]
      ;;
    STD-0592)
      [[ "$slice:$target:$disposition" == '7.4b2c:topics/security.md:merge' ]]
      ;;
    STD-0593|STD-0595)
      [[ "$slice:$target:$disposition" == '7.4b2c:profiles/boundaries/ipc.md:refine' ]]
      ;;
    STD-0594)
      [[ "$slice:$target:$disposition" == '7.4b2c:topics/security.md:refine' ]]
      ;;
    *)
      exit 1
      ;;
  esac

  ((row_count += 1))
done < "$MAP"
[[ "$row_count" -eq 14 ]]

required_report_text=(
  '[milestone-7-f018-slices.tsv](milestone-7-f018-slices.tsv)'
  'fixtures/contracts/runtime-decoding-decisions.tsv'
  'fixtures/ipc/action-payload-decisions.tsv'
  'type assertion'
  'typed `unsupported`'
  'no default action'
  'Finding `F018` is resolved'
)
for text in "${required_report_text[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q 'milestone-7-f018-decomposition.md' "$PLAN"
rg -F -q '`7.4b2a` (`Accepted`)' "$PLAN"

b_planned="$(grep -cF '`7.4b2b` (`Planned`)' "$PLAN" || true)"
b_accepted="$(grep -cF '`7.4b2b` (`Accepted`)' "$PLAN" || true)"
c_planned="$(grep -cF '`7.4b2c` (`Planned`)' "$PLAN" || true)"
c_accepted="$(grep -cF '`7.4b2c` (`Accepted`)' "$PLAN" || true)"
[[ "$((b_planned + b_accepted))" -eq 1 ]]
[[ "$((c_planned + c_accepted))" -eq 1 ]]

if [[ "$b_planned" -eq 1 ]]; then
  [[ "$disposed_b" -eq 0 && "$disposed_c" -eq 0 ]]
  [[ "$c_planned" -eq 1 ]]
  rg -F -q '**Next slice:** Milestone 7.4b2b' "$PLAN"
elif [[ "$c_planned" -eq 1 ]]; then
  [[ "$disposed_b" -eq 4 && "$disposed_c" -eq 0 ]]
  rg -F -q '**Next slice:** Milestone 7.4b2c' "$PLAN"
else
  [[ "$b_accepted" -eq 1 && "$c_accepted" -eq 1 ]]
  [[ "$disposed_b" -eq 4 && "$disposed_c" -eq 10 ]]
  if rg -q '^\*\*Next slice:\*\* .*7\.4b2(b|c)' "$PLAN"; then
    printf 'Accepted F018 slices cannot remain the next slice\n' >&2
    exit 1
  fi
fi

printf 'Milestone 7 F018 decomposition passed: 14 IDs across 2 serial slices; dispositions %s/4 and %s/10\n' \
  "$disposed_b" "$disposed_c"
