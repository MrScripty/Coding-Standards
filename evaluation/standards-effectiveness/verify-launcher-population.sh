#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/launcher/population-decisions.tsv"
readonly OWNER="$R/profiles/applications/launcher.md"
readonly LEGACY="$R/LAUNCHER-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id action procedure lifecycle state mechanism \
  outcome_map fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$action" == invalid ]]; then
    actual=typed-invalid
  elif [[ "$procedure" == missing || "$lifecycle" == missing ||
          "$state" == missing || "$mechanism" == missing ||
          "$outcome_map" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

required_owner=(
  'universal fixed flag set'
  'Do not require one help layout'
  'build a missing artifact implicitly'
  'silently using ambient user state'
  'Implementation Mechanism'
  'compiled launchers, task runners'
  'string evaluation, raw interpolation'
  'numeric codes are not universal'
  'explicit lossy-mapping diagnostic'
  'repeated invocations without state carry-forward'
)
for text in "${required_owner[@]}"; do
  rg -F -q "$text" "$OWNER"
done

required_legacy=(
  '# Launcher Standards Legacy Index'
  '[Dependencies](topics/dependencies.md)'
  '[Release](workflows/release.md#build-procedure-selection)'
  '[Security](topics/security.md#generated-command-and-configuration-text)'
)
for text in "${required_legacy[@]}"; do
  rg -F -q "$text" "$LEGACY"
done

prohibited_legacy=(
  '## Core CLI Contract'
  '### Required Flags'
  '### Canonical Usage'
  '## Runtime Standards'
  '## Managed State Standards'
  '## Help Standards'
  '## Exit Codes'
  '## Bash Implementation Rules'
  '## Reference Template'
  '## Compliance Checklist'
  '## Dependency Installation Standards'
  '## Build Standards'
  '## Desktop Entry and Script Generation Safety'
  'check_<name>'
  'install_<name>'
  'app-build-tool'
  'NEEDS_BUILD='
)
for text in "${prohibited_legacy[@]}"; do
  ! rg -F -q "$text" "$LEGACY"
done

expected_ids=(
  STD-0487 STD-0488 STD-0489 STD-0490 STD-0491 STD-0492 STD-0493
  STD-0494 STD-0499 STD-0501 STD-0502 STD-0503 STD-0504 STD-0505
  STD-0506 STD-0507 STD-0511 STD-0512
)
mapfile -t actual_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0487" && $1 <= "STD-0512" &&
    ($3 == "profiles/applications/launcher.md" ||
     ($3 == "LAUNCHER-STANDARDS.md" &&
      ($1 == "STD-0487" || $1 == "STD-0489" ||
       $1 == "STD-0493" || $1 == "STD-0501"))) { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

for id in STD-0508 STD-0509 STD-0510; do
  awk -F '\t' -v id="$id" 'NR > 1 && $1 == id { found = 1 }
    END { exit found ? 0 : 1 }' "$DISPOSITIONS"
done

rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9c'* ]]

"$S/verify-launcher-owner-contract.sh"
"$S/verify-milestone-7-row-14-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Launcher population passed: 13 decisions, 18 exact Launcher dispositions, row 14 complete\n'
