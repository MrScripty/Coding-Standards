#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case users tasks platforms modalities conformance capability evidence fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$users" == contradictory || "$tasks" == contradictory ||
          "$modalities" == contradictory || "$conformance" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$platforms" == unsupported || "$capability" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$users" == missing || "$tasks" == missing ||
          "$platforms" == missing || "$modalities" == missing ||
          "$conformance" == missing || "$capability" == missing ||
          "$evidence" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/accessibility/owner-contract-decisions.tsv"
for text in 'ID: `topic.accessibility`' '## Accessibility Authority' \
  '## Outcome And Modality Selection' '## Responsibility Boundaries' \
  '## Typed Outcomes' 'external accessibility standard' \
  'not a universal checklist' 'No mechanism, tool, browser'; do
  rg -F -q "$text" "$R/topics/accessibility.md"
done
for text in 'ID: `reference.recipes.accessibility`' \
  'This material is non-normative' '## Adapting A Mechanism'; do
  rg -F -q "$text" "$R/reference/recipes/accessibility.md"
done
rg -F -q '[topics/accessibility.md](topics/accessibility.md)' "$R/README.md"
rg -F -q '[Accessibility](topics/accessibility.md)' "$R/STANDARDS-ROUTER.md"
rg -F -q '[Accessibility](topics/accessibility.md)' "$R/ACCESSIBILITY-STANDARDS.md"
rg -F -q $'STD-0007\tACCESSIBILITY-STANDARDS.md\ttopics/accessibility.md\tindex' \
  "$S/consolidation-dispositions.tsv"
[[ "$(awk -F '\t' '$1==28&&($6!="exists"||$7!="pre-slice-review"){n++}END{print n+0}' \
  "$S/milestone-7-execution-decomposition.tsv")" -eq 0 ]]
rg -F -q '`7.4b18b` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b18br` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
printf 'Accessibility owner contract passed: 17 decisions, 1 disposition\n'
