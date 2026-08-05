#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/planning/historical-row-checker-ownership.tsv"
TRAIN="$S/milestone-7-execution-train.tsv"
DISPOSITIONS="$S/consolidation-dispositions.tsv"

[[ -f "$F" ]]

declare -A disposed
while IFS=$'\t' read -r id _rest; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
done < "$DISPOSITIONS"

declare -a forbidden_patterns
fixture_count=0
while IFS=$'\t' read -r forbidden_status reason extra; do
  if [[ "$forbidden_status" == 'forbidden_status' ]]; then
    continue
  fi
  [[ "$forbidden_status" == 'Planned' ]]
  [[ "$reason" == 'completed-row-live-lifecycle' ]]
  [[ -z "${extra:-}" ]]
  forbidden_patterns+=("(\`$forbidden_status\`)")
  fixture_count=$((fixture_count + 1))
done < "$F"
[[ "$fixture_count" -eq 1 ]]

completed_rows=0
checked_rows=0
while IFS=$'\t' read -r row _wave start_id end_id _rest; do
  [[ "$row" == 'order' ]] && continue
  [[ "$row" =~ ^[0-9]+$ ]]
  start_number=$((10#${start_id#STD-}))
  end_number=$((10#${end_id#STD-}))
  complete=1
  for ((number = start_number; number <= end_number; number += 1)); do
    printf -v id 'STD-%04d' "$number"
    if [[ -z "${disposed[$id]:-}" ]]; then
      complete=0
      break
    fi
  done
  [[ "$complete" -eq 1 ]] || continue
  completed_rows=$((completed_rows + 1))

  checker_path="$S/verify-milestone-7-row-$row-decomposition.sh"
  [[ -f "$checker_path" ]] || continue
  for forbidden in "${forbidden_patterns[@]}"; do
    if rg -F -q "$forbidden" "$checker_path"; then
      printf 'invalid: completed row %s checker retains live lifecycle status %s\n' \
        "$row" "$forbidden" >&2
      exit 1
    fi
  done
  checked_rows=$((checked_rows + 1))
done < "$TRAIN"

[[ "$completed_rows" -gt 0 && "$checked_rows" -gt 0 ]]
printf 'Historical row-checker ownership passed: %d completed rows, %d existing checkers, no live lifecycle assertions\n' \
  "$completed_rows" "$checked_rows"
