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
  output=""
  if output="$("$CHECK" "$fixture" 2>&1)"; then
    printf 'Invalid plan fixture passed: %s\n' "$fixture" >&2
    exit 1
  fi
  expected=""
  case "$(basename "$fixture")" in
    invalid-accepted-satisfied-without-evidence.md)
      expected="$fixture: satisfied objective A1 requires evidence"
      ;;
    invalid-objective-partial.md)
      expected="$fixture: objective A1 has invalid status partial"
      ;;
  esac
  if [[ -n "$expected" && "$output" != "$expected" ]]; then
    printf 'Invalid plan fixture produced the wrong diagnostic: %s\n' \
      "$fixture" >&2
    printf 'Expected: %s\nObserved: %s\n' "$expected" "$output" >&2
    exit 1
  fi
done

printf 'Plan lifecycle fixtures passed\n'
