#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/commit/authority.tsv"

while IFS=$'\t' read -r case_id event history authority recoverable topology \
  expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi

  [[ "$event" =~ ^(commit|milestone|pre-push|pr|history-maintenance)$ ]]
  [[ "$history" =~ ^(unshared|shared)$ ]]
  [[ "$authority" =~ ^(yes|no)$ ]]
  [[ "$recoverable" =~ ^(yes|no)$ ]]
  [[ "$topology" =~ ^(linear|merge)$ ]]

  if [[ "$event" == "commit" ]]; then
    actual="staged-review"
  elif [[ "$event" != "history-maintenance" || "$authority" == "no" ]]; then
    if [[ "$event" == "history-maintenance" ]]; then
      actual="refuse-unauthorized"
    else
      actual="history-review"
    fi
  elif [[ "$history" == "shared" ]]; then
    actual="refuse-shared"
  elif [[ "$recoverable" == "no" ]]; then
    actual="refuse-unrecoverable"
  elif [[ "$topology" == "merge" ]]; then
    actual="rewrite-merge"
  else
    actual="rewrite-linear"
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

required_links=(
  "STANDARDS-ROUTER.md"
  "README.md"
  "COMMIT-STANDARDS.md"
  "TOOLING-STANDARDS.md"
  "workflows/implementation.md"
)

for file in "${required_links[@]}"; do
  if ! rg -F -q "workflows/commit.md" "$REPO_ROOT/$file" &&
      ! rg -F -q "(commit.md)" "$REPO_ROOT/$file"; then
    printf '%s does not link the canonical commit workflow\n' "$file" >&2
    exit 1
  fi
done

legacy_patterns=(
  "Mandatory History Cleanup Before Commit"
  "must rewrite unpushed history"
  "mandatory cleanup rule"
  "Rewriting unpushed merge commits is allowed"
  "Drop regression commits and fixup fixes"
  "@{u}"
)

for pattern in "${legacy_patterns[@]}"; do
  if rg -F -q "$pattern" \
    "$REPO_ROOT/COMMIT-STANDARDS.md" \
    "$REPO_ROOT/TOOLING-STANDARDS.md" \
    "$REPO_ROOT/templates/lefthook.yml" \
    "$REPO_ROOT/workflows/implementation.md"; then
    printf 'Legacy history policy remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

printf 'Commit authority fixtures passed\n'
