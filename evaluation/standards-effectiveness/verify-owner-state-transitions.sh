#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while IFS=$'\t' read -r case baseline transition completion filesystem expected; do
  [[ "$case" == case ]] && continue
  actual=allow
  if [[ ! "$baseline" =~ ^(exists|missing)$ ||
        ! "$completion" =~ ^(pending|complete)$ ||
        ! "$transition" =~ ^(none|missing-to-exists)$ ]]; then
    actual=typed-invalid
  elif [[ "$transition" == missing-to-exists && "$baseline" != missing ]]; then
    actual=typed-invalid
  else
    effective="$baseline"
    [[ "$transition" == missing-to-exists && "$completion" == complete ]] && effective=exists
    [[ "$effective" == "$filesystem" ]] || actual=typed-invalid
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/execution-train/owner-state-transition-decisions.tsv"
while IFS=$'\t' read -r case transition activation expected; do
  [[ "$case" == case ]] && continue
  actual=allow
  if [[ ! "$transition" =~ ^(none|missing-to-exists)$ ||
        ! "$activation" =~ ^(pre-slice-review|owner-review|final-closure)$ ]]; then
    actual=typed-invalid
  elif [[ "$transition" == missing-to-exists && "$activation" != owner-review ]]; then
    actual=typed-invalid
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/execution-train/owner-activation-decisions.tsv"
while IFS=$'\t' read -r case baseline prior current completion filesystem expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  actual=allow
  if [[ ! "$baseline" =~ ^(exists|missing)$ ||
        ! "$prior" =~ ^(none|pending|complete)$ ||
        ! "$current" =~ ^(none|missing-to-exists)$ ||
        ! "$completion" =~ ^(pending|complete)$ ]]; then
    actual=typed-invalid
  elif [[ "$baseline" == exists &&
          ("$prior" != none || "$current" != none) ]]; then
    actual=typed-invalid
  elif [[ "$prior" != none && "$current" != none ]]; then
    actual=typed-invalid
  else
    effective="$baseline"
    [[ "$prior" == complete ]] && effective=exists
    [[ "$current" == missing-to-exists &&
       "$completion" == complete ]] && effective=exists
    [[ "$effective" == "$filesystem" ]] || actual=typed-invalid
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/execution-train/shared-owner-state-transition-decisions.tsv"
printf 'Owner-state transitions passed: 11 row, 7 activation, and 15 shared-owner decisions\n'
