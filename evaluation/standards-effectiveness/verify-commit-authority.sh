#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/commit/authority.tsv"
readonly BYPASS_FIXTURE="$SCRIPT_DIR/fixtures/commit/hook-bypass.tsv"

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

while IFS=$'\t' read -r case_id authority scope reason unmet_checks \
  compensation follow_up fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == missing ]]; then
    actual=typed-invalid
  elif [[ "$scope" == missing || "$reason" == missing ||
          "$unmet_checks" == missing || "$compensation" == missing ||
          "$follow_up" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow-bypass
  fi
  [[ "$actual" == "$expected" ]]
done < "$BYPASS_FIXTURE"

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
  'git commit --no-verify'
  'When absolutely necessary'
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

for text in '## Hook Bypass Authority' 'does not waive' \
  'does not grant authority by itself' 'Do not default to a bypass command' \
  'leave the hook enabled'; do
  rg -F -q "$text" "$REPO_ROOT/workflows/commit.md"
done

for id in STD-0663 STD-0703; do
  awk -F '\t' -v id="$id" '$1 == id && $3 == "workflows/commit.md" && $4 == "refine" { found = 1 } END { exit !found }' \
    "$SCRIPT_DIR/consolidation-dispositions.tsv"
done

printf 'Commit authority fixtures passed: 10 hook-bypass decisions, 2 exact dispositions\n'
