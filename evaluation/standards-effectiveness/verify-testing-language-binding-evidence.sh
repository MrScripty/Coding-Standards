#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/language-bindings/evidence-cohort-decisions.tsv"

while IFS=$'\t' read -r case claim native host package provenance substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none ]]; then
    actual=typed-invalid
  elif [[ "$claim" == not-selected ]]; then
    actual=omit
  elif [[ "$claim" == unsupported || "$host" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$package" == missing ]]; then
    actual=typed-invalid
  elif [[ "$native" == missing || "$host" == missing ||
          "$provenance" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Binding Evidence Cohorts' \
  'select evidence that independently covers the' \
  'native adapter contract and the real host consumer contract' \
  'release cohort or compatibility contract' \
  'sharing a build directory, version string, or generation run is not' \
  'Evidence breadth follows declared consumers' \
  'helper path, wrapper test, native-only test, host-only smoke' \
  'do not infer per-change, pre-push, CI, or release cadence' \
  'Do not substitute another artifact' \
  'host, wrapper, smoke path, schedule, or weaker evidence'; do
  rg -F -q "$text" "$R/profiles/boundaries/language-bindings.md"
done

legacy="$R/TESTING-STANDARDS.md"
rg -F -q 'language-bindings.md' "$legacy"
! rg -F -q 'for most repos this means pre-push' "$legacy"
! rg -F -q 'Recommended coverage split' "$legacy"

row="$(awk -F '\t' '$1=="STD-0616" {print $2 FS $3 FS $4 FS $5}' \
  "$S/consolidation-dispositions.tsv")"
[[ "$row" == $'TESTING-STANDARDS.md\tprofiles/boundaries/language-bindings.md\trefine\trequire claim-selected native real-host and package-cohort compatibility evidence without wrapper native-only host-only generated-type fixed-schedule alternate-artifact or weaker-evidence substitution' ]]

rg -F -q '`7.4b8bw` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bx` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8by` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9e` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing language-binding evidence passed: 16 decisions, 1 disposition\n'
