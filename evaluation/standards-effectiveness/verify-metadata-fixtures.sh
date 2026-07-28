#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly CHECK="$SCRIPT_DIR/check-metadata.sh"
readonly FIXTURES="$SCRIPT_DIR/fixtures/metadata"

"$CHECK" "$ROOT" "$FIXTURES/valid-core.md" "$FIXTURES/valid-workflow.md"

for fixture in \
  "$FIXTURES/invalid-level.md" \
  "$FIXTURES/invalid-missing-owner.md" \
  "$FIXTURES/invalid-owner.md" \
  "$FIXTURES/invalid-self-dependency.md" \
  "$FIXTURES/invalid-missing-dependency.md"; do
  if "$CHECK" "$ROOT" "$fixture" >/dev/null 2>&1; then
    printf 'Invalid metadata fixture passed: %s\n' "$fixture" >&2
    exit 1
  fi
done

if "$CHECK" "$ROOT" \
  "$FIXTURES/invalid-cycle-a.md" \
  "$FIXTURES/invalid-cycle-b.md" >/dev/null 2>&1; then
  printf 'Invalid metadata cycle passed\n' >&2
  exit 1
fi

if "$CHECK" "$ROOT" \
  "$FIXTURES/invalid-duplicate-a.md" \
  "$FIXTURES/invalid-duplicate-b.md" >/dev/null 2>&1; then
  printf 'Duplicate metadata IDs passed\n' >&2
  exit 1
fi

printf 'Metadata fixtures passed\n'
