#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly B="$S/fixtures/verification/platform-evidence"

"$S/check-decision-table.sh" "$B-schema.tsv" "$B-decisions.tsv" "$B-observed.tsv"

while IFS=$'\t' read -r case_id contract support coverage environment result \
  schedule orchestration fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$schedule" == fixed || "$orchestration" == fixed-fail-fast ||
        "$environment" == simulated-substitute ]]; then
    actual=typed-invalid
  elif [[ "$support" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing || "$coverage" == unknown ||
          "$schedule" == unknown || "$orchestration" == unknown ]]; then
    actual=typed-unavailable
  elif [[ "$support" == required &&
          ( "$coverage" == partial || "$environment" == missing ||
            "$result" != passed ) ]]; then
    actual=acceptance-blocked
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$B-decisions.tsv"

expected=(STD-0298 STD-0299)
mapfile -t actual < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0298" || $1 == "STD-0299") { print $1 }' \
    "$S/consolidation-dispositions.tsv"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

for text in \
  '## Platform Evidence Coverage' \
  'record every required target' \
  'result from one target does not prove' \
  'remain explicit and cannot satisfy' \
  'Failure fan-out and early termination' \
  'required target result is missing' \
  'Do not infer Linux and Windows' \
  'fixed pre-commit'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done

legacy="$(sed -n '/^## CI Matrix$/,$p' "$R/CROSS-PLATFORM-STANDARDS.md")"
rg -F -q 'workflows/verification.md#platform-evidence-coverage' <<< "$legacy"
for removed in 'ubuntu-latest' 'windows-latest' 'fail-fast: false' \
  '| Pre-commit |' '| Pre-push |' 'CI (push/PR)'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

rg -F -q '`7.4b8v` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-verification-ownership.sh"
"$S/verify-milestone-7-row-6-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Platform evidence coverage passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$B-decisions.tsv") - 1 ))"
