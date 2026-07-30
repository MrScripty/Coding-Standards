#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE_DIR="$SCRIPT_DIR/fixtures/cross-platform"
readonly SCHEMA="$FIXTURE_DIR/native-artifact-loading-schema.tsv"
readonly DECISIONS="$FIXTURE_DIR/native-artifact-loading-decisions.tsv"
readonly OBSERVED="$FIXTURE_DIR/native-artifact-loading-observed.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/topics/cross-platform.md"
readonly LEGACY="$REPO_ROOT/CROSS-PLATFORM-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

"$SCRIPT_DIR/check-decision-table.sh" "$SCHEMA" "$DECISIONS" "$OBSERVED"

while IFS=$'\t' read -r case_id artifact_contract target identity delivery \
  mechanism capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$artifact_contract" == contradictory ||
        "$identity" == ambiguous ]]; then
    actual=typed-invalid
  elif [[ "$target" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$artifact_contract" == missing ||
          "$target" == unknown ||
          "$identity" == missing ||
          "$delivery" == unknown ||
          "$mechanism" == unknown ||
          "$capability" == unavailable ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$DECISIONS"

expected_ids=(STD-0294 STD-0295)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 == "STD-0294" || $1 == "STD-0295" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0294" || $1 == "STD-0295") { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target_owner disposition rationale extra; do
  case "$id" in
    STD-0294|STD-0295)
      [[ "$source:$target_owner:$disposition" == \
        'CROSS-PLATFORM-STANDARDS.md:topics/cross-platform.md:refine' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

required_profile=(
  '## Native Artifact Loading'
  'artifact identity or immutable revision'
  'target, architecture, ABI'
  'delivery authority and location contract'
  'Select static linking, dynamic loading'
  'package resolver or operating-system search path'
  'ambient discovery is not artifact identity'
  'Shipped artifact identity'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  '### No Fallback'
  'Do not mandate Strategy/Factory'
  'try another loader or artifact'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(
  sed -n '/^## Native Library Rules$/,/^### Library Naming$/p' "$LEGACY"
)"
rg -F -q 'topics/cross-platform.md#native-artifact-loading' \
  <<< "$legacy_section"
for removed in \
  'should be loaded' \
  'Strategy pattern' \
  'embedded in managed assemblies' \
  '`.so`' \
  '`.dll`' \
  '`.dylib`'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

rg -F -q '`7.4b8t` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-platform-target-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-row-6-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Native artifact loading passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$DECISIONS") - 1 ))"
