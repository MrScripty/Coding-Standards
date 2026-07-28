#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CHECK="$SCRIPT_DIR/check-plan-structure.sh"
readonly FIXTURES="$SCRIPT_DIR/fixtures/plans"

"$CHECK" \
  "$FIXTURES/valid-active.md" \
  "$FIXTURES/valid-blocked.md" \
  "$FIXTURES/valid-accepted.md" \
  "$FIXTURES/valid-superseded.md"

for fixture in "$FIXTURES"/invalid-*.md; do
  if "$CHECK" "$fixture" >/dev/null 2>&1; then
    printf 'Invalid plan fixture passed: %s\n' "$fixture" >&2
    exit 1
  fi
done

printf 'Plan lifecycle fixtures passed\n'
