#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/launcher/owner-contract-decisions.tsv"
readonly OWNER="$R/profiles/applications/launcher.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly README="$R/README.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly TRAIN="$S/milestone-7-execution-train.tsv"
readonly PACKAGES="$S/milestone-7-accelerated-packages.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id selection action procedure arguments target \
  lifecycle evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$selection" == multiple ||
        "$selection" == none || "$action" == unknown ||
        "$arguments" == invalid ]]; then
    actual=typed-invalid
  elif [[ "$action" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$procedure" == missing || "$target" == missing ||
          "$lifecycle" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in \
  'ID: `profile.application.launcher`' \
  'Launcher Authority' \
  'Select Actions From Declared Capabilities' \
  'Delegate Without Upgrading Evidence' \
  'Own Process And State Boundaries' \
  'does not own application business logic' \
  'typed `invalid`, `unsupported`, or `unavailable`' \
  'Do not continue through a guessed action'; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q 'Common application launcher command projection, lifecycle, delegation, or outcome-preservation contract is required' "$ROUTER"
rg -F -q '[profiles/applications/launcher.md](profiles/applications/launcher.md)' "$README"

mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0487" && $1 <= "STD-0512" {
    print $1
  }' "$DISPOSITIONS"
)
[[ "${#dispositions[@]}" -eq 26 ]]

train_row="$(
  awk -F '\t' '$1 == 14 {
    print $3 "\t" $4 "\t" $6 "\t" $7 "\t" $8 "\t" $9
  }' "$TRAIN"
)"
[[ "$train_row" == $'STD-0487\tSTD-0512\tprofiles/applications/launcher.md\texists\towner-review\tfull-suite' ]]

package_row="$(
  awk -F '\t' '$1 == 14 {
    print $3 "\t" $4 "\t" $5 "\t" $6 "\t" $8
  }' "$PACKAGES"
)"
[[ "$package_row" == $'refinement\tprofiles/applications/launcher.md\texisting-review\tdecision-table\tfull-suite' ]]

rg -F -q '`7.4b8at` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8au` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8bl'* ]]

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"
"$S/check-plan-structure.sh" "$PLAN"
"$S/verify-plan-fixtures.sh"

printf 'Launcher owner contract passed: 16 decisions, owner established\n'
