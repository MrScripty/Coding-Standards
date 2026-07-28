#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/pipeline-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id authenticated immutable claims artifacts \
  destination expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$authenticated" "$immutable" "$claims" "$artifacts" \
    "$destination" "$expected"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual="no"
  if [[ "$authenticated" == "yes" && "$immutable" == "yes" &&
        "$claims" == "yes" && "$artifacts" == "yes" &&
        "$destination" == "yes" ]]; then
    actual="yes"
  fi
  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 552 &&
    substr($1, 5) + 0 <= 560 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 552 &&
    substr($1, 5) + 0 <= 560 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 9 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release pipeline dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(55[2-9]|560)$ ]]; then
    continue
  fi
  [[ "$source" == "RELEASE-STANDARDS.md" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  case "$id" in
    STD-0554|STD-0555|STD-0557)
      [[ "$target" == "none" && "$disposition" == "remove" ]]
      ;;
    *)
      [[ "$target" == "workflows/release.md" &&
         "$disposition" == "move" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$WORKFLOW"

rg -F -q '## Pipeline Mechanics' "$WORKFLOW"
required_rules=(
  'one authenticated release decision'
  'release-dispatch'
  'matrix follows supported target and environment claims'
  'must not ignore a missing required output'
  'Use least-privilege credentials'
  'cannot replace missing behavior or user-workflow evidence'
)
for rule in "${required_rules[@]}"; do
  rg -F -q "$rule" "$WORKFLOW"
done

if rg -q '^## CI/CD Release Pipeline$' "$LEGACY"; then
  printf 'Legacy pipeline policy remains authoritative\n' >&2
  exit 1
fi

for retained in '## GitHub Releases' '## Rollback Procedure' \
  '## Release Tool Recipes'; do
  rg -F -q "$retained" "$LEGACY"
done

removed_rules=(
  'Pushing a `v*` tag'
  '# .github/workflows/release.yml'
  '# .github/workflows/ci.yml'
  'startsWith(github.ref'
  'if-no-files-found: ignore'
  '`macos-latest` on GitHub Actions'
  'runs only on tag pushes'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed pipeline rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release pipeline policy passed\n'
