#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/cross-platform/platform-target-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/topics/cross-platform.md"
readonly LEGACY="$REPO_ROOT/CROSS-PLATFORM-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id targets target_contract support behavior \
  isolation selection layout capability semantics evidence fallback expected \
  extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$targets" =~ ^(single|multiple|unknown|default)$ ]]
  [[ "$target_contract" =~ ^(declared|missing|contradictory)$ ]]
  [[ "$support" =~ ^(required|optional|unsupported|unknown|default)$ ]]
  [[ "$behavior" =~ ^(available|unavailable|invalid)$ ]]
  [[ "$isolation" =~ ^(cohesive|domain-inline|universal|missing)$ ]]
  [[ "$selection" =~ ^(compile-time|runtime|composition|dispatch|unknown|default)$ ]]
  [[ "$layout" =~ ^(cohesive|one-per-platform|default)$ ]]
  [[ "$capability" =~ ^(available|unsupported|unavailable)$ ]]
  [[ "$semantics" =~ ^(preserved|stub|false-result|omitted|alternate)$ ]]
  [[ "$evidence" =~ ^(matched|simulated-substitute|missing|not-required)$ ]]
  [[ "$fallback" =~ ^(none|default-targets|default-tier|strategy-factory|one-file-per-platform|runtime-only|compile-only|stub|silent-omission|alternate-mechanism|weaker-evidence)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$targets" == 'default' ||
        "$target_contract" == 'contradictory' ||
        "$support" == 'default' ||
        "$behavior" == 'invalid' ||
        "$isolation" =~ ^(domain-inline|universal)$ ||
        "$selection" == 'default' ||
        "$layout" != 'cohesive' ||
        "$semantics" != 'preserved' ]]; then
    actual='typed-invalid'
  elif [[ "$support" == 'unsupported' || "$capability" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$targets" == 'unknown' ||
          "$target_contract" == 'missing' ||
          "$support" == 'unknown' ||
          "$behavior" == 'unavailable' ||
          "$isolation" == 'missing' ||
          "$selection" == 'unknown' ||
          "$capability" == 'unavailable' ||
          "$evidence" == 'missing' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected_ids=(
  STD-0280 STD-0281 STD-0282 STD-0283 STD-0284
  STD-0285 STD-0286 STD-0287 STD-0288
)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0280" && $1 <= "STD-0288" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0280" && $1 <= "STD-0288" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-028[0-8]) ;; *) continue ;; esac
  [[ "$source" == 'CROSS-PLATFORM-STANDARDS.md' ]]
  [[ "$target" == 'topics/cross-platform.md' ]]
  if [[ "$id" == 'STD-0280' ]]; then
    [[ "$disposition" == 'move' ]]
  else
    [[ "$disposition" == 'refine' ]]
  fi
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$PROFILE"

required_profile=(
  '## Platform Support Contract'
  'project, product, or release contract'
  'Product target names and support tiers are project facts'
  '## Platform Behavior Isolation'
  'smallest cohesive boundary'
  'Select compile-time, runtime, composition, and dispatch mechanisms'
  'No Strategy/Factory'
  'not graceful degradation'
  'typed `invalid`'
  '`unsupported`'
  '`unavailable`'
  '### No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_opening="$(
  sed -n '1,/^## File System Conventions$/p' "$LEGACY"
)"
rg -F -q 'topics/cross-platform.md#platform-support-contract' \
  <<< "$legacy_opening"
rg -F -q 'STANDARDS-ROUTER.md' <<< "$legacy_opening"
for pattern in 'Linux x86_64' 'Windows x86_64' 'Best-effort' \
  'Strategy + Factory Pattern' 'One Platform Per File' \
  'Use runtime detection only' 'FeatureServiceFactory' \
  'RUST-CROSS-PLATFORM-STANDARDS.md'; do
  if rg -F -q "$pattern" <<< "$legacy_opening"; then
    printf 'legacy platform default remains: %s\n' "$pattern" >&2
    exit 1
  fi
done
rg -F -q '## File System Conventions' "$LEGACY"
rg -F -q '## Native Library Rules' "$LEGACY"
rg -F -q '## CI Matrix' "$LEGACY"

rg -F -q '| F046 | Resolved in Milestone 7.4b7c |' "$FINDINGS"
rg -F -q '`7.4b7c` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-filesystem-containment-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Platform target policy passed: %s decisions, 9 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
