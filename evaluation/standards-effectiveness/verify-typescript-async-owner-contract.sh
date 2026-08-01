#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/typescript/async-owner-contract-decisions.tsv"
readonly OWNER="$R/profiles/languages/typescript/async.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly README="$R/README.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id overlap authority cancellation completion \
  application capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$authority" == process-global ||
        "$application" == stale || "$completion" == discarded ||
        "$cancellation" == ignored ]]; then
    actual=typed-invalid
  elif [[ "$authority" == missing || "$capability" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in \
  'ID: `profile.language.typescript.async`' \
  'Specializes: `topic.concurrency`' \
  'Establish Current-Invocation Authority' \
  'Classify Every Completion' \
  'scope-owned generation token' \
  'process-global counter' \
  'typed `invalid`, `unsupported`, or `unavailable`' \
  'Do not continue with a process-global counter'; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q 'TypeScript `Promise`, overlapping invocation, stale-result, cancellation, or async state-application mechanism changes' "$ROUTER"
rg -F -q '[profiles/languages/typescript/async.md](profiles/languages/typescript/async.md)' "$README"

mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0275" || $1 == "STD-0276") {
    print $1 ":" $2 ":" $3 ":" $4 ":" $5
  }' "$DISPOSITIONS"
)
expected_dispositions=(
  'STD-0275:CONCURRENCY-STANDARDS.md:CONCURRENCY-STANDARDS.md:index:convert the TypeScript concurrency parent heading into a non-normative route to the canonical TypeScript Async profile'
  'STD-0276:CONCURRENCY-STANDARDS.md:profiles/languages/typescript/async.md:refine:replace the global request counter and silent stale-result discard recipe with scoped invocation authority and explicit terminal classification'
)
[[ "${dispositions[*]}" == "${expected_dispositions[*]}" ]]

readonly LEGACY="$R/CONCURRENCY-STANDARDS.md"
rg -F -q '## TypeScript Async Index' "$LEGACY"
rg -F -q '[TypeScript Async Profile](profiles/languages/typescript/async.md)' \
  "$LEGACY"
! rg -F -q '## TypeScript Concurrency Rules' "$LEGACY"
! rg -F -q '### Guard Against Stale Async Responses' "$LEGACY"
! rg -F -q 'let currentRequestId = 0;' "$LEGACY"
! rg -F -q 'Stale — discard' "$LEGACY"

overlay_row="$(
  awk -F '\t' '$1 == 13 && $2 == 3 {
    print $3 "\t" $5 "\t" $6 "\t" $7
  }' "$OVERLAY"
)"
[[ "$overlay_row" == $'STD-0275,STD-0276\tprofiles/languages/typescript/async.md\texists\tpre-slice-review' ]]

rg -F -q '`7.4b8ap` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aq` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ar` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8as` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8at` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8au` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9i'* ]]

"$S/verify-milestone-7-row-13-decomposition.sh"
"$S/check-plan-structure.sh" "$PLAN"
"$S/verify-plan-fixtures.sh"

printf 'TypeScript Async policy passed: 14 decisions, owner established, STD-0275 and STD-0276 disposed\n'
