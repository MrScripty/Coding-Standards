#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/resilience/owner-contract-decisions.tsv"
readonly OWNER="$R/topics/resilience.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id criticality phase outcome retry evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$retry" == unbounded ||
        "$outcome" == ignore || "$fallback" == alternate-dependency ||
        ( "$criticality" == unknown ) ]]; then
    actual=typed-invalid
  elif [[ "$criticality" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
done < "$FIXTURE"

for text in 'ID: `topic.resilience`' 'Failure And Recovery Authority' 'Criticality And Degradation' 'Retry And Recovery' 'typed `invalid`' 'typed `unsupported`' 'typed `unavailable`' 'No Fallback'; do
  rg -F -q "$text" "$OWNER"
done
rg -F -q 'Dependency or service failure, retry, degradation, startup resilience, or recovery semantics' "$ROUTER"
rg -F -q '`7.4b8ai` (`Accepted`)' "$PLAN"

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Resilience owner contract passed: 12 decisions, owner established\n'
