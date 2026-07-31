#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/godot/owner-contract-decisions.tsv"
readonly OWNER="$R/profiles/frameworks/godot.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly README="$R/README.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id affinity dispatch completion lifetime \
  check_timing evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none ||
        ( "$affinity" == worker && "$dispatch" == direct ) ||
        "$completion" == detached || "$lifetime" == invalid ||
        "$lifetime" == stale || "$check_timing" == before-await ]]; then
    actual=typed-invalid
  elif [[ "$affinity" == missing || "$lifetime" == missing ||
          "$evidence" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$evidence" == unsupported ]]; then
    actual=typed-unsupported
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in \
  'ID: `profile.framework.godot`' \
  'Specializes: `topic.concurrency`' \
  'Establish Engine Affinity' \
  'Prove Object Lifetime At Use' \
  '`CallDeferred`' \
  '`GodotObject.IsInstanceValid`' \
  'check-to-use gap' \
  'typed `invalid`, `unsupported`, or `unavailable`' \
  'Do not continue with off-thread engine access'; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q 'Godot object, node, scene-tree, signal, resource, thread-affinity, deferred-dispatch, or object-lifetime mechanism changes' "$ROUTER"
rg -F -q '[profiles/frameworks/godot.md](profiles/frameworks/godot.md)' "$README"

mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0277" && $1 <= "STD-0279" {
    print $1 ":" $2 ":" $3 ":" $4 ":" $5
  }' "$DISPOSITIONS"
)
expected_dispositions=(
  'STD-0277:CONCURRENCY-STANDARDS.md:CONCURRENCY-STANDARDS.md:index:convert the Godot thread-safety parent heading into a non-normative route to the canonical Godot framework profile'
  'STD-0278:CONCURRENCY-STANDARDS.md:profiles/frameworks/godot.md:refine:select Godot engine affinity and observable dispatch from the operation contract rather than requiring one main-thread mechanism'
  'STD-0279:CONCURRENCY-STANDARDS.md:profiles/frameworks/godot.md:refine:replace validity-check-only guidance with point-of-use object lifetime and identity proof across async and deferred boundaries'
)
[[ "${dispositions[*]}" == "${expected_dispositions[*]}" ]]

readonly LEGACY="$R/CONCURRENCY-STANDARDS.md"
rg -F -q '## Godot Framework Index' "$LEGACY"
rg -F -q '[Godot Framework Profile](profiles/frameworks/godot.md)' "$LEGACY"
! rg -F -q '## Godot Thread Safety' "$LEGACY"
! rg -F -q '### Main Thread Rule' "$LEGACY"
! rg -F -q '### `IsInstanceValid` Before Use' "$LEGACY"
! rg -F -q 'Use `CallDeferred`' "$LEGACY"
! rg -F -q 'Always check `GodotObject.IsInstanceValid(node)`' "$LEGACY"

overlay_row="$(
  awk -F '\t' '$1 == 13 && $2 == 4 {
    print $3 "\t" $5 "\t" $6 "\t" $7
  }' "$OVERLAY"
)"
[[ "$overlay_row" == $'STD-0277,STD-0278,STD-0279\tprofiles/frameworks/godot.md\texists\tpre-slice-review' ]]

rg -F -q '`7.4b8ar` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8as` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8at` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8au` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8ba'* ]]

"$S/verify-milestone-7-row-13-decomposition.sh"
"$S/check-plan-structure.sh" "$PLAN"
"$S/verify-plan-fixtures.sh"

printf 'Godot policy passed: 14 decisions, owner established, row-13 dispositions complete\n'
