#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/csharp/async-owner-contract-decisions.tsv"
readonly OWNER="$R/profiles/languages/csharp/async.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly README="$R/README.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id affinity mechanism capability evidence \
  fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$mechanism" == block ||
        "$evidence" == contradictory ||
        ( "$affinity" == affine && "$mechanism" == suppress ) ]]; then
    actual=typed-invalid
  elif [[ "$affinity" == unknown || "$capability" == missing ||
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
  'ID: `profile.language.csharp.async`' \
  'Specializes: `topic.concurrency`' \
  'Inherit The Generic Lifecycle Contract' \
  'Select Continuation Scheduling From Affinity' \
  'Preserve Invocation Isolation' \
  'typed `invalid`, `unsupported`, or `unavailable`' \
  'Do not continue with context suppression'; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q 'C# `await`, `Task`, continuation scheduling, synchronization context, or thread-affinity mechanism changes' "$ROUTER"
rg -F -q '[profiles/languages/csharp/async.md](profiles/languages/csharp/async.md)' "$README"

disposition="$(
  awk -F '\t' 'NR > 1 && $1 == "STD-0273" {
    print $2 ":" $3 ":" $4 ":" $5
  }' "$DISPOSITIONS"
)"
[[ "$disposition" == 'CONCURRENCY-STANDARDS.md:profiles/languages/csharp/async.md:refine:select C sharp continuation scheduling from explicit affinity capability and evidence rather than library or service placement' ]]

rg -F -q '### C# Continuation Scheduling' "$R/CONCURRENCY-STANDARDS.md"
rg -F -q '[C# Async Profile](profiles/languages/csharp/async.md)' \
  "$R/CONCURRENCY-STANDARDS.md"
! rg -F -q '### Use ConfigureAwait(false) in Library/Service Code' \
  "$R/CONCURRENCY-STANDARDS.md"
! rg -F -q 'should use `ConfigureAwait(false)`' \
  "$R/CONCURRENCY-STANDARDS.md"

overlay_row="$(
  awk -F '\t' '$1 == 13 && $2 == 1 {
    print $3 "\t" $5 "\t" $6 "\t" $7
  }' "$OVERLAY"
)"
[[ "$overlay_row" == $'STD-0273\tprofiles/languages/csharp/async.md\texists\tpre-slice-review' ]]

rg -F -q '`7.4b8am` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8an` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ao` (`Accepted`)' "$PLAN"
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
[[ "$next_slice_line" == *'Milestone 7.4b9g'* ]]

"$S/verify-milestone-7-row-13-decomposition.sh"
"$S/check-plan-structure.sh" "$PLAN"
"$S/verify-plan-fixtures.sh"

printf 'C# Async policy passed: 12 decisions, owner established, STD-0273 disposed\n'
