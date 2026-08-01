#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/verification/gui-smoke-decisions.tsv"
readonly OWNER="$R/workflows/verification.md"
readonly LEGACY="$R/LAUNCHER-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id claim environment mode capabilities lifecycle \
  assertions fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$environment" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$claim" == missing || "$environment" == missing ||
          "$mode" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$capabilities" == missing || "$lifecycle" != bounded ||
          "$assertions" != passed ]]; then
    actual=acceptance-blocked
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

required_owner=(
  '### GUI Smoke Evidence'
  'display or session capability'
  'sandbox policy'
  'software rendering, sandbox flags'
  'state isolation'
  'bounded process-lifecycle behavior'
  'verification-only procedure separate from normal interactive startup'
  'Verification owns its evidence kind'
  'runner behavior, missing required capability'
  'does not fall back to startup-only evidence'
)
for text in "${required_owner[@]}"; do
  rg -F -q "$text" "$OWNER"
done

! rg -F -q '## GUI CI Smoke Requirements' "$LEGACY"
! rg -F -q 'xvfb' "$LEGACY"
! rg -F -q 'CI-like environment variables' "$LEGACY"

disposition="$(
  awk -F '\t' '$1 == "STD-0495" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)"
[[ "$disposition" == $'STD-0495\tLAUNCHER-STANDARDS.md\tworkflows/verification.md\trefine' ]]

rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b9d'* ]]

"$S/verify-verification-ownership.sh"
"$S/verify-launcher-population.sh"
"$S/verify-milestone-7-row-14-decomposition.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'GUI smoke evidence passed: 14 decisions, STD-0495 refined, active child 14.4\n'
