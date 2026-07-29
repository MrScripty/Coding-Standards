#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly CHECK="$SCRIPT_DIR/check-decision-table.sh"
readonly FIXTURES="$SCRIPT_DIR/fixtures/decision-table"
readonly SCHEMA="$FIXTURES/valid-schema.tsv"
readonly DECISIONS="$FIXTURES/valid-decisions.tsv"
readonly OBSERVED="$FIXTURES/valid-observed.tsv"

"$CHECK" "$SCHEMA" "$DECISIONS" "$OBSERVED"

assert_rejected() {
  local expected="$1"
  shift
  local output
  if output="$("$CHECK" "$@" 2>&1)"; then
    printf 'invalid decision-table fixture passed: %s\n' "$*" >&2
    exit 1
  fi
  [[ "$output" == *"$expected"* ]] || {
    printf 'decision-table diagnostic mismatch: expected %s, got %s\n' \
      "$expected" "$output" >&2
    exit 1
  }
}

assert_rejected \
  'duplicate decision schema column: contract' \
  "$FIXTURES/invalid-schema-duplicate.tsv" "$DECISIONS" "$OBSERVED"
assert_rejected \
  'decision schema wildcard is allowed only for case' \
  "$FIXTURES/invalid-schema-wildcard.tsv" "$DECISIONS" "$OBSERVED"
assert_rejected \
  'decision value outside schema for selected: contract=guessed' \
  "$SCHEMA" "$FIXTURES/invalid-decisions-domain.tsv" "$OBSERVED"
assert_rejected \
  'duplicate decision case: selected' \
  "$SCHEMA" "$FIXTURES/invalid-decisions-duplicate.tsv" "$OBSERVED"
assert_rejected \
  'selected: expected allow, observed typed-unavailable' \
  "$SCHEMA" "$DECISIONS" "$FIXTURES/invalid-observed-mismatch.tsv"
assert_rejected \
  'missing observed decision case: fallback' \
  "$SCHEMA" "$DECISIONS" "$FIXTURES/invalid-observed-missing.tsv"
assert_rejected \
  'observed decision has unknown case: extra' \
  "$SCHEMA" "$DECISIONS" "$FIXTURES/invalid-observed-extra.tsv"
assert_rejected \
  'decision table input is unavailable:' \
  "$SCHEMA" "$DECISIONS" "$FIXTURES/absent.tsv"

printf 'Decision-table engine fixtures passed\n'
