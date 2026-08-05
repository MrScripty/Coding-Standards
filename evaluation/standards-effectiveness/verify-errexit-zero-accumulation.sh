#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
F="$S/fixtures/planning/errexit-zero-accumulation.tsv"

[[ -f "$F" ]]

count=0
while IFS=$'\t' read -r checker_path accumulator addend extra; do
  if [[ "$checker_path" == 'checker_path' ]]; then
    continue
  fi
  [[ -n "$checker_path" && -n "$accumulator" && -n "$addend" ]]
  [[ -z "${extra:-}" ]]
  [[ "$accumulator" =~ ^[a-z_]+$ && "$addend" =~ ^[a-z_]+$ ]]
  [[ -f "$R/$checker_path" ]]

  unsafe="(($accumulator += $addend))"
  safe="$accumulator=\$(($accumulator + $addend))"
  if rg -F -q "$unsafe" "$R/$checker_path"; then
    printf 'invalid: zero-valued arithmetic command can trip errexit in %s\n' \
      "$checker_path" >&2
    exit 1
  fi
  rg -F -q "$safe" "$R/$checker_path"

  printf -v command \
    '%s=0; %s=0; %s; [[ $%s -eq 0 ]]' \
    "$accumulator" "$addend" "$safe" "$accumulator"
  bash -euo pipefail -c "$command"
  count=$((count + 1))
done < "$F"

[[ "$count" -eq 1 ]]
printf 'Errexit zero-accumulation passed: %d protected verifier path\n' "$count"
