#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly CHECK="$REPO_ROOT/templates/check-decision-traceability.sh"
readonly FIXTURES="$SCRIPT_DIR/fixtures/traceability"
readonly TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

create_repo() {
  local target="$1"

  mkdir -p "$target"
  cp -R "$FIXTURES/." "$target/"
  (
    cd "$target"
    git init -q
    git config user.email "fixtures@example.invalid"
    git config user.name "Standards Fixtures"
    git add .
    git commit -qm "test: add baseline"
  )
}

expect_failure() {
  local description="$1"
  shift

  if "$@" >/dev/null 2>&1; then
    printf 'Expected failure: %s\n' "$description" >&2
    exit 1
  fi
}

staged_repo="$TEMP_ROOT/staged"
create_repo "$staged_repo"
(
  cd "$staged_repo"

  expect_failure "missing explicit mode" \
    "$CHECK" --map map.tsv

  printf '\nexport const stagedChange = true;\n' >> src/api/public.ts
  git add src/api/public.ts

  printf 'trigger_path\tboundary_id\tprofile\tartifact_path\n' > map.tsv
  expect_failure "unstaged map bypassing staged trigger" \
    "$CHECK" --mode staged --map map.tsv
  git restore map.tsv

  expect_failure "staged trigger without mapped artifact" \
    "$CHECK" --mode staged --map map.tsv

  printf '\nStaged contract update.\n' >> src/api/README.md
  expect_failure "unstaged artifact satisfying staged trigger" \
    "$CHECK" --mode staged --map map.tsv

  git add src/api/README.md
  "$CHECK" --mode staged --map map.tsv

  printf '\nexport const unstagedChange = true;\n' >> src/engine/policy.ts
  "$CHECK" --mode staged --map map.tsv
)

range_repo="$TEMP_ROOT/range"
create_repo "$range_repo"
(
  cd "$range_repo"
  base_ref="$(git rev-parse HEAD)"

  printf '\nexport const rangeChange = true;\n' >> src/engine/policy.ts
  printf '\nRange decision update.\n' >> docs/adr/ADR-001-engine.md
  git add src/engine/policy.ts docs/adr/ADR-001-engine.md
  git commit -qm "test: update mapped engine decision"

  printf 'trigger_path\tboundary_id\tprofile\tartifact_path\n' > map.tsv
  printf '# unstaged map must not alter range mode\n' >> map.tsv
  printf '# unstaged artifact must not alter range mode\n' \
    > docs/adr/ADR-001-engine.md
  "$CHECK" --mode range --map map.tsv \
    --base-ref "$base_ref" --head-ref HEAD
)

unrelated_repo="$TEMP_ROOT/unrelated-adr"
create_repo "$unrelated_repo"
(
  cd "$unrelated_repo"
  base_ref="$(git rev-parse HEAD)"

  printf '\nexport const invalidChange = true;\n' >> src/engine/policy.ts
  printf '\nUnrelated update.\n' >> docs/adr/ADR-002-global.md
  git add src/engine/policy.ts docs/adr/ADR-002-global.md
  git commit -qm "test: update unrelated decision"
  expect_failure "unrelated ADR satisfying engine boundary" \
    "$CHECK" --mode range --map map.tsv \
      --base-ref "$base_ref" --head-ref HEAD
)

removed_row_repo="$TEMP_ROOT/removed-row"
create_repo "$removed_row_repo"
(
  cd "$removed_row_repo"

  git rm -q src/engine/policy.ts
  {
    printf 'trigger_path\tboundary_id\tprofile\tartifact_path\n'
    printf 'src/api/public.ts\tapi\tcontract-readme\tsrc/api/README.md\n'
  } > map.tsv
  git add map.tsv
  expect_failure "removed map row hiding deleted trigger" \
    "$CHECK" --mode staged --map map.tsv
)

legacy_patterns=(
  "TRACEABILITY_BASE_REF"
  "TRACEABILITY_HOST_FACING_DIRS"
  "TRACEABILITY_STRUCTURED_PRODUCER_DIRS"
  "origin/master"
  "HEAD~1"
)

for pattern in "${legacy_patterns[@]}"; do
  if rg -F -q -- "$pattern" \
    "$CHECK" \
    "$REPO_ROOT/TOOLING-STANDARDS.md" \
    "$REPO_ROOT/templates/lefthook.yml"; then
    printf 'Legacy traceability policy remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

if ! rg -F -q -- \
    "check-decision-traceability.sh --mode staged --map" \
    "$REPO_ROOT/templates/lefthook.yml"; then
  printf 'Pre-commit traceability invocation is not explicitly staged\n' >&2
  exit 1
fi

printf 'Decision traceability fixtures passed\n'
