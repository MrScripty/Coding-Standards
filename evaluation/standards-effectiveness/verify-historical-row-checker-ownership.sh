#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/planning/historical-row-checker-ownership.tsv"

[[ -f "$F" ]]

count=0
while IFS=$'\t' read -r checker_path owned_row forbidden reason extra; do
  if [[ "$checker_path" == "checker_path" ]]; then
    continue
  fi
  [[ -n "$checker_path" && -n "$owned_row" && -n "$forbidden" && -n "$reason" ]]
  [[ -z "${extra:-}" ]]
  [[ "$owned_row" =~ ^[0-9]+$ ]]
  [[ "$reason" == "later-row-lifecycle" ]]
  [[ -f "$R/$checker_path" ]]

  if rg -F -q "$forbidden" "$R/$checker_path"; then
    printf 'invalid: historical row %s checker owns later milestone %s\n' \
      "$owned_row" "$forbidden" >&2
    exit 1
  fi
  count=$((count + 1))
done < "$F"

[[ "$count" -eq 2 ]]
printf 'Historical row-checker ownership passed: %d later-milestone exclusions\n' "$count"
