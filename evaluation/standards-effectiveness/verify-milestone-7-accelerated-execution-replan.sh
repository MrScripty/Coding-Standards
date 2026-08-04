#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly PACKAGES="$SCRIPT_DIR/milestone-7-accelerated-packages.tsv"
readonly TRAIN="$SCRIPT_DIR/milestone-7-execution-train.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-accelerated-execution-replan.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly DECISION_ENGINE="$SCRIPT_DIR/check-decision-table.sh"
readonly DECISION_ENGINE_FIXTURES="$SCRIPT_DIR/verify-decision-table-engine.sh"
readonly ACTION_FIXTURES="$SCRIPT_DIR/fixtures/execution-train/package-owner-action-decisions.tsv"
readonly DECOMPOSITION="$SCRIPT_DIR/milestone-7-execution-decomposition.tsv"

declare -A train_owner train_owner_state train_wave train_gate seen_orders
while IFS=$'\t' read -r order wave _start _end _source owner _owner_state \
  _activation checkpoint extra; do
  [[ "$order" == order ]] && continue
  [[ -z "${extra:-}" ]]
  train_owner["$order"]="$owner"
  train_owner_state["$order"]="$_owner_state"
  train_wave["$order"]="$wave"
  train_gate["$order"]="$checkpoint"
done < "$TRAIN"

declare -A decomposed_orders transition_count
while IFS=$'\t' read -r order _child _ids _source owner _state _activation \
  _checkpoint _rationale transition extra; do
  [[ "$order" == baseline_order ]] && continue
  [[ -z "${extra:-}" ]]
  decomposed_orders["$order"]=1
  if [[ "$transition" == missing-to-exists ]]; then
    transition_count["$owner"]=$(( ${transition_count[$owner]:-0} + 1 ))
  fi
done < "$DECOMPOSITION"

declare -A package_owner package_risk package_verification package_outcome
declare -A creation_owners creation_decomposed package_seen
row_count=0
while IFS=$'\t' read -r order package risk owner owner_action verification \
  draft_mode integration_gate outcome prerequisites extra; do
  if [[ "$order" == train_order ]]; then
    [[ "$package" == package_id && "$risk" == risk_class ]]
    continue
  fi

  [[ "$order" =~ ^([5-9]|[1-3][0-9]|4[0-7])$ ]]
  [[ -z "${seen_orders[$order]:-}" ]]
  seen_orders["$order"]=1
  [[ "${train_owner[$order]}" == "$owner" ]]
  [[ "$risk" =~ ^(mechanical|consolidation|refinement|safety-critical|new-owner-design)$ ]]
  [[ "$owner_action" =~ ^(existing-review|create-before-populate|populate-after-create|closure-only)$ ]]
  [[ "$verification" =~ ^(decision-table|owner-contract|migration-structure|custom-semantic)$ ]]
  [[ "$draft_mode" =~ ^(isolated-draft|serial-only)$ ]]
  [[ "$integration_gate" =~ ^(focused|full-suite)$ ]]
  [[ -n "$outcome" && -n "$prerequisites" && -z "${extra:-}" ]]

  if [[ "$owner_action" == create-before-populate ]]; then
    [[ "${train_owner_state[$order]}" == missing ]]
    [[ "$risk" == new-owner-design ]]
    [[ "$verification" == owner-contract ]]
    [[ "$integration_gate" == full-suite ]]
    creation_owners["$owner"]=1
    if [[ -n "${decomposed_orders[$order]:-}" ]]; then
      creation_decomposed["$owner"]=1
    fi
  elif [[ "$owner_action" == populate-after-create ]]; then
    [[ "${train_owner_state[$order]}" == missing ]]
    [[ -n "${creation_owners[$owner]:-}" ]]
    [[ "$risk" == consolidation ]]
    [[ "$verification" == migration-structure ]]
  else
    [[ "${train_owner_state[$order]}" == exists ]]
  fi

  if [[ -n "${package_seen[$package]:-}" ]]; then
    [[ "${package_owner[$package]}" == "$owner" ]]
    [[ "${package_risk[$package]}" == "$risk" ]]
    [[ "${package_verification[$package]}" == "$verification" ]]
    [[ "${package_outcome[$package]}" == "$outcome" ]]
  else
    package_seen["$package"]=1
    package_owner["$package"]="$owner"
    package_risk["$package"]="$risk"
    package_verification["$package"]="$verification"
    package_outcome["$package"]="$outcome"
  fi

  if [[ "${train_gate[$order]}" == full-suite ]]; then
    [[ "$integration_gate" == full-suite ]]
  fi
  ((row_count += 1))
done < "$PACKAGES"

[[ "$row_count" -eq 43 ]]
[[ "${#seen_orders[@]}" -eq 43 ]]
[[ "${#package_seen[@]}" -eq 40 ]]
[[ "${#creation_owners[@]}" -eq 4 ]]
for owner in "${!creation_decomposed[@]}"; do
  [[ "${transition_count[$owner]:-0}" -eq 1 ]]
done

while IFS=$'\t' read -r case owner_action baseline prior_creation risk \
  verification integration_gate expected; do
  [[ "$case" == case ]] && continue
  actual=allow
  if [[ ! "$owner_action" =~ ^(existing-review|create-before-populate|populate-after-create|closure-only)$ ||
        ! "$baseline" =~ ^(exists|missing)$ ]]; then
    actual=typed-invalid
  elif [[ "$owner_action" == create-before-populate ]]; then
    if [[ "$baseline" != missing || "$risk" != new-owner-design ||
          "$verification" != owner-contract || "$integration_gate" != full-suite ]]; then
      actual=typed-invalid
    fi
  elif [[ "$owner_action" == populate-after-create ]]; then
    if [[ "$baseline" != missing || "$prior_creation" != yes ||
          "$risk" != consolidation || "$verification" != migration-structure ]]; then
      actual=typed-invalid
    fi
  elif [[ "$baseline" != exists ]]; then
    actual=typed-invalid
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$ACTION_FIXTURES"

for order in $(seq 5 47); do
  [[ -n "${seen_orders[$order]:-}" ]]
done

expected_multi_packages=(
  'P08:2'
  'P30:2'
  'P32:2'
)
for expected in "${expected_multi_packages[@]}"; do
  package="${expected%%:*}"
  count="${expected##*:}"
  [[ "$(awk -F '\t' -v package="$package" 'NR > 1 && $2 == package { n += 1 } END { print n + 0 }' "$PACKAGES")" -eq "$count" ]]
done
[[ "$(awk -F '\t' 'NR > 1 { n[$2] += 1 } END { for (p in n) if (n[p] > 1 && p != "P08" && p != "P30" && p != "P32") print p }' "$PACKAGES")" == "" ]]

required_report=(
  '570 frozen identifiers remain in 43 pending logical clusters'
  'maps every pending immutable-train row to one of 40 packages'
  'Every legacy identifier receives exactly one final disposition'
  'No risk class permits compatibility copies'
  '`decision-table`'
  '`owner-contract`'
  '`migration-structure`'
  '`custom-semantic`'
  'There is no wholesale checker rewrite'
  'Twelve canonical owners are still missing'
  '`isolated-draft`'
  '`serial-only`'
  'Both reviews are required'
  'final `7.4c` milestone'
  'set -euo pipefail'
  'changes no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '| F070 | Resolved in Milestone 7.4b8l |' "$FINDINGS"
rg -F -q '| F071 | Resolved in Milestone 7.4b8m |' "$FINDINGS"
rg -F -q '| F072 | Resolved in Milestone 7.4b8n |' "$FINDINGS"
rg -F -q '`7.4b8l` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8m` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8n` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8o` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8p` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8q` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8r` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8s` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8t` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8u` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8v` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8w` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8x` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8y` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8z` (`Accepted`)' "$PLAN"
[[ -x "$DECISION_ENGINE" && -x "$DECISION_ENGINE_FIXTURES" ]]
"$DECISION_ENGINE_FIXTURES"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 accelerated execution re-plan passed: %s rows, %s packages, %s creation owners\n' \
  "$row_count" "${#package_seen[@]}" "${#creation_owners[@]}"
