#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/resilience/recovery-policy-decisions.tsv"
readonly OWNER="$R/topics/resilience.md"
readonly LEGACY="$R/ARCHITECTURE-PATTERNS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id criticality phase failure state_authority \
  degraded retry safety evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$retry" == unbounded ||
        ( "$retry" == bounded && "$safety" != safe ) ]]; then
    actual=typed-invalid
  elif [[ "$failure" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$criticality" == missing || "$phase" == missing ||
          "$evidence" == missing ||
          ( "$criticality" == best-effort && "$degraded" == missing ) ]]; then
    actual=typed-unavailable
  elif [[ "$failure" == corrupt && "$state_authority" == disposable-derived ]]; then
    actual=rebuild-derived
  elif [[ "$criticality" == best-effort && "$degraded" == accepted ]]; then
    actual=degraded-outcome
  elif [[ "$retry" == bounded ]]; then
    actual=retry-then-terminal
  else
    actual=propagate-failure
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected=(STD-{0119..0125})
mapfile -t actual < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0119" && $1 <= "STD-0125" {
    print $1
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  [[ "$id" == id ]] && continue
  [[ "$id" < STD-0119 || "$id" > STD-0125 ]] && continue
  [[ "$source" == ARCHITECTURE-PATTERNS.md ]]
  [[ "$target" == topics/resilience.md ]]
  [[ "$disposition" =~ ^(move|refine|remove|merge)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < "$DISPOSITIONS"

for text in \
  'Failure Classification And Decision' \
  'Startup Resilience' \
  'Best-Effort Dependency Boundaries' \
  'State Reconstruction' \
  'Acceptance Evidence' \
  'disposable derived state' \
  'typed `unsupported`' \
  'Do not report readiness'; do
  rg -F -q "$text" "$OWNER"
done

legacy="$(sed -n '/^## Infrastructure Failure Recovery Index$/,/^---$/p' "$LEGACY")"
rg -F -q 'topics/resilience.md' <<< "$legacy"
rg -F -q 'topics/contracts.md#degraded-outcomes' <<< "$legacy"
rg -F -q 'non-normative migration index' <<< "$legacy"
for removed in \
  'Delete and rebuild from scratch' \
  'Use cached fallback or return partial results' \
  'continue with defaults or degraded mode' \
  'returns safe defaults' \
  'class BestEffortRegistry'; do
  ! rg -F -q "$removed" "$LEGACY" "$OWNER"
done
rg -F -q '| Handling infrastructure failures | [Resilience](topics/resilience.md) |' "$LEGACY"

rg -F -q '`7.4b8aj` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8ak'* ]]
[[ "$next_slice_line" == *'STD-0269'* ]]

"$S/verify-resilience-owner-contract.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Resilience recovery policy passed: 21 decisions, 7 exact dispositions\n'
