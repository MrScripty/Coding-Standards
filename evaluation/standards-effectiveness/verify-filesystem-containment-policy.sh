#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/security/path-containment-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly SECURITY="$REPO_ROOT/topics/security.md"
readonly CROSS_PLATFORM="$REPO_ROOT/topics/cross-platform.md"
readonly LEGACY_SECURITY="$REPO_ROOT/SECURITY-STANDARDS.md"
readonly LEGACY_CROSS_PLATFORM="$REPO_ROOT/CROSS-PLATFORM-STANDARDS.md"

while IFS=$'\t' read -r case_id path_state relation root_policy symlink \
  parent_anchor race_control filesystem_facts expected; do
  [[ "$case_id" == 'case' ]] && continue

  [[ "$path_state" =~ ^(existing|non-existing)$ ]]
  [[ "$relation" =~ ^(descendant|root|sibling|traversal|unknown)$ ]]
  [[ "$root_policy" =~ ^(allow|deny|not-applicable)$ ]]
  [[ "$symlink" =~ ^(inside|outside|none|unknown)$ ]]
  [[ "$parent_anchor" =~ ^(validated|unvalidated|not-applicable)$ ]]
  [[ "$race_control" =~ ^(capability|none)$ ]]
  [[ "$filesystem_facts" =~ ^(known|unknown)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable|typed-unsupported)$ ]]

  if [[ "$filesystem_facts" == 'unknown' || "$relation" == 'unknown' ||
        "$symlink" == 'unknown' ]]; then
    actual='typed-unavailable'
  elif [[ "$relation" =~ ^(sibling|traversal)$ || "$symlink" == 'outside' ]]; then
    actual='typed-invalid'
  elif [[ "$relation" == 'root' && "$root_policy" == 'deny' ]]; then
    actual='typed-invalid'
  elif [[ "$path_state" == 'non-existing' &&
          "$parent_anchor" != 'validated' ]]; then
    actual='typed-invalid'
  elif [[ "$race_control" == 'none' ]]; then
    actual='typed-unsupported'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(
  STD-0289 STD-0290 STD-0291 STD-0292 STD-0293
  STD-0584 STD-0585 STD-0586 STD-0587
)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    ($2 == "CROSS-PLATFORM-STANDARDS.md" && $1 >= "STD-0289" && $1 <= "STD-0293") ||
    ($2 == "SECURITY-STANDARDS.md" && $1 >= "STD-0584" && $1 <= "STD-0587") {
      print $1
    }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 &&
    (($2 == "CROSS-PLATFORM-STANDARDS.md" && $1 >= "STD-0289" && $1 <= "STD-0293") ||
     ($2 == "SECURITY-STANDARDS.md" && $1 >= "STD-0584" && $1 <= "STD-0587")) {
      print $1
    }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0289|STD-0290|STD-0293)
      [[ "$source" == 'CROSS-PLATFORM-STANDARDS.md' ]]
      [[ "$target" == 'topics/cross-platform.md' ]]
      [[ "$disposition" == 'move' ]]
      ;;
    STD-0291|STD-0292)
      [[ "$source" == 'CROSS-PLATFORM-STANDARDS.md' ]]
      [[ "$target" == 'topics/cross-platform.md' ]]
      [[ "$disposition" == 'refine' ]]
      ;;
    STD-0584)
      [[ "$source" == 'SECURITY-STANDARDS.md' ]]
      [[ "$target" == 'topics/security.md' ]]
      [[ "$disposition" == 'move' ]]
      ;;
    STD-0585|STD-0587)
      [[ "$source" == 'SECURITY-STANDARDS.md' ]]
      [[ "$target" == 'topics/security.md' ]]
      [[ "$disposition" == 'merge' ]]
      ;;
    STD-0586)
      [[ "$source" == 'SECURITY-STANDARDS.md' ]]
      [[ "$target" == 'topics/security.md' ]]
      [[ "$disposition" == 'refine' ]]
      ;;
    *)
      continue
      ;;
  esac
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$SECURITY" \
  "$CROSS_PLATFORM"

for file in "$REPO_ROOT/README.md" "$REPO_ROOT/STANDARDS-ROUTER.md"; do
  rg -F -q 'topics/security.md' "$file"
  rg -F -q 'topics/cross-platform.md' "$file"
done
rg -F -q 'topics/security.md' "$LEGACY_SECURITY"
rg -F -q 'topics/cross-platform.md' "$LEGACY_CROSS_PLATFORM"

required_security=(
  'A string-prefix test is not containment.'
  'nearest existing ancestor'
  'handle-relative, capability-based'
  'typed `unsupported` or'
)
for rule in "${required_security[@]}"; do
  rg -F -q "$rule" "$SECURITY"
done

required_cross_platform=(
  'display form is presentation'
  'lexical normalization'
  'canonical identity'
  'Do not use raw string prefix'
)
for rule in "${required_cross_platform[@]}"; do
  rg -F -q "$rule" "$CROSS_PLATFORM"
done

removed_patterns=(
  'StartsWith('
  '.startsWith('
  'Normalize before comparing.'
  'StringComparison.OrdinalIgnoreCase'
)
for pattern in "${removed_patterns[@]}"; do
  if rg -F -q "$pattern" \
    "$SECURITY" "$CROSS_PLATFORM" \
    "$LEGACY_SECURITY" "$LEGACY_CROSS_PLATFORM"; then
    printf 'unsafe path-containment guidance remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

printf 'Filesystem containment policy passed\n'
