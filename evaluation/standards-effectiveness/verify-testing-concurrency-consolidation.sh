#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/concurrency/verification-resource-decisions.tsv"

while IFS=$'\t' read -r case overlap owner coordination cleanup lifecycle substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$owner" == unavailable ]]; then
    actual=typed-unavailable
  elif [[ "$owner" == missing || "$owner" == ambient ||
          "$coordination" == missing || "$coordination" == implicit ||
          "$cleanup" == missing || "$lifecycle" == missing ||
          "$substitute" != none ]]; then
    actual=typed-invalid
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Isolate Verification Resources' \
  'Restore borrowed global state and terminate owned work' \
  'Serialization is a valid selected mechanism only when' \
  'Do not serialize as a fallback' \
  'timer, subscription, polling, and retry cleanup' \
  'current-invocation results winning over stale overlapping work' \
  'passing build, startup smoke, happy path, serialized rerun'; do
  rg -F -q "$text" "$R/topics/concurrency.md"
done

rg -F -q '[Concurrency](topics/concurrency.md)' \
  "$R/TESTING-STANDARDS.md"
rg -F -q '[Concurrency](topics/concurrency.md)' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'If isolation is impossible, serialize' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Run affected suites with normal parallelism enabled' \
  "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1=="STD-0611"||$1=="STD-0639"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0611 STD-0639' ]]
awk -F '\t' '$1=="STD-0611"||$1=="STD-0639" {
  if ($2!="TESTING-STANDARDS.md" || $3!="topics/concurrency.md" ||
      $4!="refine" || $5=="") exit 1
  count += 1
} END { exit count == 2 ? 0 : 1 }' "$S/consolidation-dispositions.tsv"

rg -F -q '`7.4b8bv` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bw` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bx` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8by` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9f` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing concurrency consolidation passed: 15 decisions, 2 dispositions\n'
