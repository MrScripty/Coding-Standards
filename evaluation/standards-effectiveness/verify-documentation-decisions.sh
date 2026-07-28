#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/documentation/decisions.tsv"

while IFS=$'\t' read -r case_id boundary contract decision operation expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi

  for value in "$boundary" "$contract" "$decision" "$operation"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  profiles=()
  if [[ "$contract" == "yes" ]]; then
    profiles+=("contract-readme")
  elif [[ "$boundary" == "yes" ]]; then
    profiles+=("boundary-readme")
  fi
  if [[ "$decision" == "yes" ]]; then
    profiles+=("adr")
  fi
  if [[ "$operation" == "yes" ]]; then
    profiles+=("runbook")
  fi
  if [[ "${#profiles[@]}" -eq 0 ]]; then
    profiles+=("none")
  fi

  actual="$(IFS=,; printf '%s' "${profiles[*]}")"
  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

required_links=(
  "STANDARDS-ROUTER.md"
  "DOCUMENTATION-STANDARDS.md"
  "ARCHITECTURE-PATTERNS.md"
  "templates/README-TEMPLATE.md"
)

for file in "${required_links[@]}"; do
  if ! rg -F -q "workflows/documentation.md" "$REPO_ROOT/$file"; then
    printf '%s does not link the canonical documentation workflow\n' \
      "$file" >&2
    exit 1
  fi
done

legacy_patterns=(
  'Every directory under `src/`'
  'Every changed directory under `src/`'
  'Every PR that changes `src/<module>/`'
  'universal requirement takes precedence'
)

for pattern in "${legacy_patterns[@]}"; do
  if rg -F -q "$pattern" \
    "$REPO_ROOT/DOCUMENTATION-STANDARDS.md" \
    "$REPO_ROOT/ARCHITECTURE-PATTERNS.md" \
    "$REPO_ROOT/templates/README-TEMPLATE.md" \
    "$REPO_ROOT/templates/PULL_REQUEST_TEMPLATE.md"; then
    printf 'Legacy documentation requirement remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

printf 'Documentation decision fixtures passed\n'
