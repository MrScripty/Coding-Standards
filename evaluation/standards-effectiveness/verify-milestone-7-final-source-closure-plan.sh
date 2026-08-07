#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MANIFEST="$SCRIPT_DIR/milestone-7-final-source-closure.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-final-source-closure.md"
readonly VERIFIER_REPLAN="$SCRIPT_DIR/milestone-7-source-index-verifier-replan.md"
readonly CORPUS="$SCRIPT_DIR/corpus.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A seen_sources
row_count=0
concise_count=0
expanded_count=0
retain_count=0
rewrite_count=0
delete_count=0

while IFS=$'\t' read -r order source owner shape treatment evidence risk \
  concurrency gate extra; do
  if [[ "$order" == order ]]; then
    [[ "$source" == source && "$owner" == canonical_owner ]]
    [[ "$shape" == current_shape && "$treatment" == treatment ]]
    [[ "$evidence" == retention_evidence && "$risk" == risk ]]
    [[ "$concurrency" == concurrency && "$gate" == gate ]]
    continue
  fi

  ((row_count += 1))
  [[ "$order" -eq "$row_count" ]]
  [[ -z "${seen_sources[$source]:-}" ]]
  seen_sources["$source"]=1
  [[ -z "${extra:-}" ]]
  [[ "$shape" =~ ^(concise|expanded)$ ]]
  [[ "$treatment" =~ ^(retain-index|rewrite-index|delete)$ ]]
  [[ "$evidence" == frozen-stable-entrypoint ]]
  [[ "$concurrency" == isolated-draft ]]
  [[ "$gate" == full-suite ]]
  [[ -f "$REPO_ROOT/$source" ]]
  [[ -f "$REPO_ROOT/$owner" ]]

  if [[ "$shape" == concise ]]; then
    ((concise_count += 1))
  else
    ((expanded_count += 1))
  fi

  case "$treatment" in
    retain-index)
      [[ "$risk" == mechanical ]]
      ((retain_count += 1))
      ;;
    rewrite-index)
      [[ "$risk" == consolidation ]]
      ((rewrite_count += 1))
      ;;
    delete)
      [[ "$risk" == consolidation ]]
      ((delete_count += 1))
      ;;
  esac

  map_result="$(awk -F '\t' -v source="$source" \
    'NR > 1 && $1 == source { print $2 "\t" $3 }' "$OWNER_MAP")"
  [[ "$map_result" == "$owner"$'\t'*-and-index ]]

  id_count="$(awk -F '\t' -v source="$source" \
    'NR > 1 && $2 == source { count += 1 } END { print count + 0 }' \
    "$DISPOSITIONS")"
  [[ "$id_count" -gt 0 ]]
done < "$MANIFEST"

[[ "$row_count" -eq 27 ]]
[[ "${#seen_sources[@]}" -eq 27 ]]
[[ "$concise_count" -eq 14 ]]
[[ "$expanded_count" -eq 13 ]]
[[ "$retain_count" -eq 11 ]]
[[ "$rewrite_count" -eq 16 ]]
[[ "$delete_count" -eq 0 ]]

expected_sources="$(awk -F '\t' \
  'NR > 1 && ($2 == "standard" || $2 == "profile") { print $1 }' \
  "$CORPUS" | LC_ALL=C sort)"
manifest_sources="$(awk -F '\t' 'NR > 1 { print $2 }' "$MANIFEST" | LC_ALL=C sort)"
[[ "$manifest_sources" == "$expected_sources" ]]

required_report=(
  '## Re-plan Finding'
  '## Retention Decision'
  'All 27 former stable entrypoints are retained only as concise, non-normative'
  'Eleven already satisfy the expected index shape'
  'Sixteen require replacement with a concise'
  '`7.4c2` removes the two stale Router routes'
  '`7.4c3.1` through `7.4c3.27`'
  '`7.4c4` regenerates derived inventories'
  '## Bounded Write Sets'
  '## Verification Gates'
  'manual `D001` through `D010` review'
  '## Typed Outcomes And No Fallback'
  '## Re-plan Triggers'
  'There is no fallback to the frozen legacy source'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

[[ "$(wc -l < "$OWNER_MAP")" -eq 37 ]]
[[ "$(wc -l < "$DISPOSITIONS")" -eq 917 ]]
rg -F -q '`7.4c1` (`Accepted`)' "$PLAN"
rg -F -q '`7.4c3v` (`Accepted`)' "$PLAN"
rg -F -q '`7.4c3v1` (' "$PLAN"

required_verifier_replan=(
  '## Re-plan Finding'
  'one reusable source-index closure engine'
  'Each accepted source package owns one distinct fixture directory.'
  '## Canonical Inputs'
  '## Engine Contract'
  '## Negative Engine Evidence'
  'same engine used by the live aggregate verifier'
  '`7.4c3v1` establishes the engine and self-tests'
  'durable package contract. It does not own the'
  'mutable lifecycle state of `7.4c3v1`.'
  'live source-index aggregate verifier owns implementation acceptance'
  '## Source-Specific Checker Repair'
  'A source package may update only its own source-specific checker'
  'retain semantic owner, route, disposition, and negative evidence'
  'cannot add dual old/new assertions'
  'Shared engine code, aggregate policy, cross-source checkers'
  'checker-infrastructure re-plan'
  '## Concurrent Preparation And Serial Acceptance'
  'Preparation order and acceptance order are separate contracts.'
  'Workers cannot edit shared acceptance state.'
  'A prepared package is not accepted evidence.'
  'one complete-suite run may accept'
  'Architecture remains excluded from preparation wave `p1`'
  '## Historical Checker Repair'
  'routes established when that row was accepted. It cannot require'
  'mutable source prose to retain a migration-era sentence'
  'the preparation inventory assigns the checker to'
  'negative self-scan prevents the historical checker'
  '## Mixed Documentation Changelog Checker Repair'
  'mixed policy infrastructure and'
  'Separate serial repair `7.4c3hdoc` removes the blanket heading'
  'preserves all 16 exact changelog dispositions'
  'Explicit prohibited legacy policy headings'
  'owned by the aggregate source-closure engine'
  '## Bounded Write Sets'
  '## No Fallback'
  'old bespoke Coding verifier is removed'
  '## Verification Gates'
  '## Re-plan Triggers'
)
for text in "${required_verifier_replan[@]}"; do
  rg -F -q "$text" "$VERIFIER_REPLAN"
done

"$SCRIPT_DIR/verify-milestone-7-source-package-preparation.sh"

transient_state='Planned'
transient_marker="\`7.4c3v1\` (\`$transient_state\`)"
if rg -F -q "$transient_marker" "$0"; then
  printf 'invalid: parent closure checker owns transient 7.4c3v1 state\n' >&2
  exit 1
fi

"$SCRIPT_DIR/verify-consolidation-dispositions.sh"
"$SCRIPT_DIR/verify-undisposed-source-gaps.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"

printf 'Milestone 7 final source-closure plan passed: %s sources, %s retain, %s rewrite\n' \
  "$row_count" "$retain_count" "$rewrite_count"
