#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/verification/acceptance-claims.tsv"

validate_claim() {
  local case_id="$1"
  local claim="$2"
  local kind
  local environment
  local mode
  local extra

  IFS='@' read -r kind environment mode extra <<< "$claim"
  if [[ -n "${extra:-}" ||
        ! "$kind" =~ ^(focused|integration|contract|system|user-workflow|release-artifact)$ ||
        ! "$environment" =~ ^(not-applicable|simulated|representative|required-real)$ ||
        ! "$mode" =~ ^(automated|manual|either)$ ]]; then
    printf '%s: invalid acceptance claim %s\n' "$case_id" "$claim" >&2
    exit 1
  fi
}

is_observed() {
  local required="$1"
  local observed="$2"
  local candidate

  IFS=';' read -ra observed_claims <<< "$observed"
  for candidate in "${observed_claims[@]}"; do
    if [[ "$required" == "$candidate" ]]; then
      return 0
    fi
    if [[ "$required" == *@either &&
          "${required%@*}" == "${candidate%@*}" &&
          "$candidate" =~ @(automated|manual)$ ]]; then
      return 0
    fi
  done
  return 1
}

while IFS=$'\t' read -r case_id required observed expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  if [[ ! "$expected" =~ ^(satisfied|unsatisfied)$ ]]; then
    printf '%s: invalid expected result %s\n' "$case_id" "$expected" >&2
    exit 1
  fi

  actual="satisfied"
  IFS=';' read -ra required_claims <<< "$required"
  for claim in "${required_claims[@]}"; do
    validate_claim "$case_id" "$claim"
    if ! is_observed "$claim" "$observed"; then
      actual="unsatisfied"
    fi
  done

  IFS=';' read -ra observed_claims <<< "$observed"
  for claim in "${observed_claims[@]}"; do
    validate_claim "$case_id" "$claim"
  done

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

printf 'Acceptance claim fixtures passed\n'
