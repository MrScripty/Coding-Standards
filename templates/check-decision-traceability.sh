#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${SOURCE_ROOT:-src}"
ADR_DIR="${ADR_DIR:-docs/adr}"
BASE_REF="${TRACEABILITY_BASE_REF:-origin/main}"

required_headers=(
  "## Purpose"
  "## Contents"
  "## Problem"
  "## Constraints"
  "## Decision"
  "## Alternatives Rejected"
  "## Invariants"
  "## Revisit Triggers"
  "## Dependencies"
  "## Related ADRs"
  "## Usage Examples"
)

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository."
  exit 1
fi

if [ ! -d "$SOURCE_ROOT" ]; then
  echo "Skipping decision traceability check: '$SOURCE_ROOT/' does not exist."
  exit 0
fi

diff_range=""
if git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  diff_range="$BASE_REF...HEAD"
elif git rev-parse --verify "origin/master" >/dev/null 2>&1; then
  diff_range="origin/master...HEAD"
elif git rev-parse --verify "main" >/dev/null 2>&1; then
  diff_range="main...HEAD"
elif git rev-parse --verify "master" >/dev/null 2>&1; then
  diff_range="master...HEAD"
elif git rev-parse --verify "HEAD~1" >/dev/null 2>&1; then
  diff_range="HEAD~1...HEAD"
else
  echo "Skipping decision traceability check: unable to resolve diff base."
  exit 0
fi

mapfile -t changed_files < <(git diff --name-only --diff-filter=ACMR "$diff_range")
if [ "${#changed_files[@]}" -eq 0 ]; then
  echo "No changed files detected for decision traceability check."
  exit 0
fi

adr_changed=false
for file in "${changed_files[@]}"; do
  if [[ "$file" == "$ADR_DIR/"*.md ]]; then
    adr_changed=true
    break
  fi
done

declare -A modules=()
for file in "${changed_files[@]}"; do
  [[ "$file" == "$SOURCE_ROOT/"* ]] || continue

  relative="${file#"$SOURCE_ROOT/"}"
  module="${relative%%/*}"
  if [[ "$module" == "$relative" ]]; then
    module="."
  fi
  modules["$module"]=1
done

if [ "${#modules[@]}" -eq 0 ]; then
  echo "No '$SOURCE_ROOT/' module changes detected."
  exit 0
fi

failures=0
for module in "${!modules[@]}"; do
  if [ "$module" = "." ]; then
    module_dir="$SOURCE_ROOT"
    readme_path="$SOURCE_ROOT/README.md"
  else
    module_dir="$SOURCE_ROOT/$module"
    readme_path="$module_dir/README.md"
  fi

  if [ ! -f "$readme_path" ]; then
    echo "Missing README.md for changed module: $module_dir"
    failures=$((failures + 1))
    continue
  fi

  missing_header=false
  for header in "${required_headers[@]}"; do
    if ! rg -F -x -q "$header" "$readme_path"; then
      echo "Missing required heading in $readme_path: $header"
      missing_header=true
    fi
  done
  if [ "$missing_header" = true ]; then
    failures=$((failures + 1))
  fi

  readme_changed=false
  if printf '%s\n' "${changed_files[@]}" | rg -F -x -q "$readme_path"; then
    readme_changed=true
  fi

  if [ "$readme_changed" = false ] && [ "$adr_changed" = false ]; then
    echo "Changed module without decision traceability update: $module_dir"
    echo "Update $readme_path or add/update an ADR under $ADR_DIR/."
    failures=$((failures + 1))
  fi
done

if [ "$failures" -gt 0 ]; then
  echo "Decision traceability check failed ($failures issue(s))."
  exit 1
fi

echo "Decision traceability check passed."
