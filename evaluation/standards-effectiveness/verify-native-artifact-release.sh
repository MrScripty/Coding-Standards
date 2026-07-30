#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly B="$S/fixtures/release/native-artifact"

"$S/check-decision-table.sh" "$B-schema.tsv" "$B-decisions.tsv" "$B-observed.tsv"

while IFS=$'\t' read -r case_id contract channel identity target info evidence \
  fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$identity" == ambiguous ]]; then
    actual=typed-invalid
  elif [[ "$target" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing || "$channel" == unknown ||
          "$identity" == missing || "$target" == unknown ||
          "$info" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$B-decisions.tsv"

expected=(STD-0296 STD-0297)
mapfile -t actual < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0296" || $1 == "STD-0297") { print $1 }' \
    "$S/consolidation-dispositions.tsv"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

for text in \
  'For a native artifact' \
  'operating-system name alone' \
  'authoritative acquisition location' \
  'install or provision, and load' \
  'do not attach installation prose' \
  'unresolved artifact-plan diagnostic' \
  'guess a conventional filename' \
  'publish with incomplete consumer information'; do
  rg -F -q "$text" "$R/workflows/release.md"
done

legacy="$(sed -n '/^### Library Naming$/,/^## CI Matrix$/p' "$R/CROSS-PLATFORM-STANDARDS.md")"
rg -F -q 'workflows/release.md#artifact-plan' <<< "$legacy"
for removed in '| Linux |' '| Windows |' '| macOS |' 'platform-specific class'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

rg -F -q '`7.4b8u` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-release-artifact-policy.sh"
"$S/verify-milestone-7-row-6-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Native artifact release passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$B-decisions.tsv") - 1 ))"
