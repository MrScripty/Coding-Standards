#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/contracts/persisted-artifact-decisions.tsv"

while IFS=$'\t' read -r case role authority version derivation consumer provenance action substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$authority" == inferred ||
        "$derivation" == guessed || "$version" == invalid ]]; then
    actual=typed-invalid
  elif [[ "$version" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$authority" == missing || "$derivation" == missing ||
          "$consumer" == missing || "$provenance" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Persisted Contract Artifacts' \
  'canonical authority, applicable contract version' \
  'Validation proves that the current artifact satisfies' \
  'Regeneration proves deterministic derivation' \
  'it does not by itself prove that consumers accept' \
  'Do not accept a stale artifact'; do
  rg -F -q "$text" "$R/topics/contracts.md"
done
rg -F -q 'topics/contracts.md' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'must be validated or regenerated before commit' \
  "$R/TESTING-STANDARDS.md"

row="$(awk -F '\t' '$1=="STD-0635" {print $2 FS $3 FS $4}' \
  "$S/consolidation-dispositions.tsv")"
[[ "$row" == $'TESTING-STANDARDS.md\ttopics/contracts.md\trefine' ]]
rg -F -q '`7.4b8by` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9j` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing persisted contract artifacts passed: 15 decisions, 1 disposition\n'
