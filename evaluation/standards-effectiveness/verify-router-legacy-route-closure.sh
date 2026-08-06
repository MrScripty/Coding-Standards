#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly ROUTER="$REPO_ROOT/STANDARDS-ROUTER.md"
readonly REPLACEMENTS="$SCRIPT_DIR/fixtures/router/legacy-route-replacements.tsv"
readonly SOURCES="$SCRIPT_DIR/milestone-7-final-source-closure.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A seen_concerns seen_legacy
replacement_count=0
while IFS=$'\t' read -r concern legacy canonical expected extra; do
  if [[ "$concern" == concern ]]; then
    [[ "$legacy" == legacy_route && "$canonical" == canonical_owner ]]
    [[ "$expected" == expected ]]
    continue
  fi

  [[ -n "$concern" && -z "${seen_concerns[$concern]:-}" ]]
  [[ -n "$legacy" && -z "${seen_legacy[$legacy]:-}" ]]
  [[ "$expected" == canonical-only && -z "${extra:-}" ]]
  [[ -f "$REPO_ROOT/$legacy" && -f "$REPO_ROOT/$canonical" ]]
  rg -F -q "($canonical)" "$ROUTER"
  if rg -F -q "$legacy" "$ROUTER"; then
    printf 'invalid: Router retains legacy route %s for %s\n' \
      "$legacy" "$concern" >&2
    exit 1
  fi

  seen_concerns["$concern"]=1
  seen_legacy["$legacy"]=1
  ((replacement_count += 1))
done < "$REPLACEMENTS"
[[ "$replacement_count" -eq 2 ]]

source_count=0
while IFS=$'\t' read -r _order source _owner _shape _treatment _evidence \
  _risk _concurrency _gate extra; do
  [[ "$source" == source ]] && continue
  [[ -z "${extra:-}" ]]
  if rg -F -q "$source" "$ROUTER"; then
    printf 'invalid: Router selects former normative entrypoint %s\n' \
      "$source" >&2
    exit 1
  fi
  ((source_count += 1))
done < "$SOURCES"
[[ "$source_count" -eq 27 ]]

required_router=(
  'Select a canonical topic only when its observable condition is present'
  '## Legacy Entry Points'
  'Canonical modules own all normative rules.'
  'non-normative navigation only'
  'It does not establish'
  'applicability, preserve an older rule, or provide fallback authority.'
  'return an Invalid Routing diagnostic'
  'instead of selecting a legacy entrypoint'
)
for text in "${required_router[@]}"; do
  rg -F -q "$text" "$ROUTER"
done

for prohibited in 'until migration' \
  'Existing files retain authority only for rules not yet moved'; do
  if rg -F -q "$prohibited" "$ROUTER"; then
    printf 'invalid: stale Router migration authority remains: %s\n' \
      "$prohibited" >&2
    exit 1
  fi
done

rg -F -q '`7.4c2` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-root-router-evidence.sh"
"$SCRIPT_DIR/verify-milestone-7-final-source-closure-plan.sh"

printf 'Router legacy-route closure passed: %s replacements, %s excluded legacy sources\n' \
  "$replacement_count" "$source_count"
