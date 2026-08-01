#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/concurrency/ownership-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly TOPIC="$REPO_ROOT/topics/concurrency.md"
readonly LEGACY="$REPO_ROOT/CONCURRENCY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id state coordination lock_scope external execution \
  work_owner failure cancellation fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue

  [[ "$state" =~ ^(immutable|mutable|none)$ ]]
  [[ "$coordination" =~ ^(none|ownership|message|atomic|lock|transaction|unprotected|language-specific)$ ]]
  [[ "$lock_scope" =~ ^(released|held|not-applicable)$ ]]
  [[ "$external" =~ ^(none|callback)$ ]]
  [[ "$execution" =~ ^(sync|async-nonblocking|async-blocking)$ ]]
  [[ "$work_owner" =~ ^(declared|missing|unavailable|not-required)$ ]]
  [[ "$failure" =~ ^(observed|discarded|not-required)$ ]]
  [[ "$cancellation" =~ ^(propagated|ignored|not-required)$ ]]
  [[ "$fallback" =~ ^(none|fire-and-forget|sync-block|language-mechanism)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$state" == 'mutable' && "$coordination" == 'unprotected' ]] ||
     [[ "$lock_scope" == 'held' && "$external" == 'callback' ]] ||
     [[ "$execution" == 'async-blocking' ]] ||
     [[ "$work_owner" == 'missing' ]] ||
     [[ "$failure" == 'discarded' ]] ||
     [[ "$cancellation" == 'ignored' ]] ||
     [[ "$fallback" != 'none' ]] ||
     [[ "$coordination" == 'language-specific' ]]; then
    actual='typed-invalid'
  elif [[ "$work_owner" == 'unavailable' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(
  STD-0263 STD-0264 STD-0265 STD-0266 STD-0267
  STD-0268 STD-0270 STD-0271 STD-0272
)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "CONCURRENCY-STANDARDS.md" &&
    ($1 == "STD-0263" || $1 == "STD-0264" || $1 == "STD-0265" ||
     $1 == "STD-0266" || $1 == "STD-0267" || $1 == "STD-0268" ||
     $1 == "STD-0270" || $1 == "STD-0271" || $1 == "STD-0272") {
      print $1
    }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "CONCURRENCY-STANDARDS.md" &&
    ($1 == "STD-0263" || $1 == "STD-0264" || $1 == "STD-0265" ||
     $1 == "STD-0266" || $1 == "STD-0267" || $1 == "STD-0268" ||
     $1 == "STD-0270" || $1 == "STD-0271" || $1 == "STD-0272") {
      print $1
    }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0263|STD-0264)
      expected_disposition='move'
      ;;
    STD-0265|STD-0266|STD-0267|STD-0268|STD-0270|STD-0271|STD-0272)
      expected_disposition='refine'
      ;;
    *)
      continue
      ;;
  esac
  [[ "$source" == 'CONCURRENCY-STANDARDS.md' ]]
  [[ "$target" == 'topics/concurrency.md' ]]
  [[ "$disposition" == "$expected_disposition" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$TOPIC"

for file in "$REPO_ROOT/README.md" "$REPO_ROOT/STANDARDS-ROUTER.md" "$LEGACY"; do
  rg -F -q 'topics/concurrency.md' "$file"
done

required_topic=(
  'Immutable or otherwise thread-safe data does not require a lock'
  'Message passing can remove shared mutation, but it is not a universal'
  'Do not invoke callbacks, signals, user code, plugin code'
  'Async request, startup, shutdown, health, and supervision paths'
  'Every asynchronous operation that can outlive its immediate call site'
  'Cancellation must propagate through all owned work'
  'typed `invalid`, `unsupported`, or `unavailable`'
  'Do not continue through fire-and-forget work'
)
for text in "${required_topic[@]}"; do
  rg -F -q "$text" "$TOPIC"
done

retained_legacy=(
  '## C# Async/Await Index'
  'This is a non-normative migration index'
  '### C# Continuation Scheduling'
  '## Rust Concurrency Routing Index'
  '## TypeScript Async Index'
  '## Godot Framework Index'
)
for text in "${retained_legacy[@]}"; do
  rg -F -q "$text" "$LEGACY"
done

removed_patterns=(
  'SelectionChanged?.Invoke(_state);'
  'protect them with a single lock'
  '_ = DoWorkAsync();'
  '_ = Task.Run(async () =>'
  'ConfigureAwait(false).GetAwaiter().GetResult()'
  'Thread.Sleep(200);'
)
for pattern in "${removed_patterns[@]}"; do
  if rg -F -q "$pattern" "$LEGACY" "$TOPIC"; then
    printf 'migrated concurrency fallback remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

awk -F '\t' 'NR > 1 && $1 == "STD-0269" {
  print $2 ":" $3 ":" $4 ":" $5
}' "$DISPOSITIONS" |
  grep -Fx 'CONCURRENCY-STANDARDS.md:CONCURRENCY-STANDARDS.md:index:convert the C sharp async parent heading into a non-normative routing index while preserving separately owned child specializations'

awk -F '\t' 'NR > 1 && $1 == "STD-0274" {
  print $2 ":" $3 ":" $4 ":" $5
}' "$DISPOSITIONS" |
  grep -Fx 'CONCURRENCY-STANDARDS.md:CONCURRENCY-STANDARDS.md:index:replace legacy Rust concurrency cross references with a non-normative route to canonical Rust Async and Rust Security profiles'

rg -F -q '[Rust Async profile](profiles/languages/rust/async.md)' "$LEGACY"
rg -F -q '[Rust Security profile](profiles/languages/rust/security.md)' "$LEGACY"
! rg -F -q 'languages/rust/RUST-ASYNC-STANDARDS.md' "$LEGACY"
! rg -F -q 'languages/rust/RUST-SECURITY-STANDARDS.md' "$LEGACY"
! rg -F -q '## C# Async/Await Rules' "$LEGACY"
rg -F -q '`7.4b8ak` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9k'* ]]

rg -F -q '| F019 | Resolved in Milestone 7.4b4b |' "$FINDINGS"
rg -F -q '`7.4b4b` (`Accepted`)' "$PLAN"

"$SCRIPT_DIR/verify-milestone-7-trust-lifecycle-replan.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Concurrency policy passed: %s decisions, %s exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))" "${#expected_ids[@]}"
