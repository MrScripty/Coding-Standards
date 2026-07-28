#!/usr/bin/env bash
set -euo pipefail

readonly -A EVIDENCE_RANK=(
  [none]=0
  [focused]=1
  [integration]=2
  [contract]=3
  [system]=4
  [user-workflow]=5
  [environment]=6
  [release]=7
  [manual]=8
)

value_for() {
  local file="$1"
  local field="$2"
  sed -n "s/^\\*\\*${field}:\\*\\* //p" "$file" | tr -d '`'
}

for file in "$@"; do
  for heading in \
    "## Objective" \
    "## Objective Acceptance" \
    "## Binding Decisions" \
    "## Milestones" \
    "## Blockers" \
    "## Re-Plan Triggers" \
    "## Final Acceptance"; do
    if [[ "$(grep -cFx "$heading" "$file")" -ne 1 ]]; then
      printf '%s: expected one %s heading\n' "$file" "$heading" >&2
      exit 1
    fi
  done

  for field in \
    "Plan status" \
    "Current phase" \
    "Next slice" \
    "Objective acceptance level" \
    "Current evidence level" \
    "Execution ledger" \
    "Issues"; do
    if [[ "$(grep -c "^\\*\\*${field}:\\*\\* " "$file" || true)" -ne 1 ]]; then
      printf '%s: expected one %s field\n' "$file" "$field" >&2
      exit 1
    fi
  done

  status="$(value_for "$file" "Plan status")"
  objective_level="$(value_for "$file" "Objective acceptance level")"
  evidence_level="$(value_for "$file" "Current evidence level")"

  if [[ ! "$status" =~ ^(Planned|Active|Blocked|Implemented|Verifying|Accepted|Deferred|Superseded)$ ]]; then
    printf '%s: invalid plan status %s\n' "$file" "$status" >&2
    exit 1
  fi
  if [[ -z "${EVIDENCE_RANK[$objective_level]:-}" && "$objective_level" != "none" ]]; then
    printf '%s: invalid objective level %s\n' "$file" "$objective_level" >&2
    exit 1
  fi
  if [[ -z "${EVIDENCE_RANK[$evidence_level]:-}" && "$evidence_level" != "none" ]]; then
    printf '%s: invalid evidence level %s\n' "$file" "$evidence_level" >&2
    exit 1
  fi
  if rg -q '^## (Execution Notes|History|Daily Log)$' "$file"; then
    printf '%s: execution history belongs in the ledger\n' "$file" >&2
    exit 1
  fi

  while IFS= read -r milestone_status; do
    if [[ ! "$milestone_status" =~ ^(Planned|Active|Blocked|Implemented|Verifying|Accepted|Deferred|Superseded)$ ]]; then
      printf '%s: invalid milestone status %s\n' \
        "$file" "$milestone_status" >&2
      exit 1
    fi
  done < <(sed -n 's/^\*\*Status:\*\* `\([^`]*\)`.*/\1/p' "$file")

  if [[ "$status" == "Accepted" ]]; then
    if (( EVIDENCE_RANK[$evidence_level] < EVIDENCE_RANK[$objective_level] )); then
      printf '%s: accepted evidence %s is weaker than objective %s\n' \
        "$file" "$evidence_level" "$objective_level" >&2
      exit 1
    fi
    if rg -q '^\*\*Status:\*\* `(Planned|Active|Blocked|Implemented|Verifying)`' "$file"; then
      printf '%s: accepted plan has unfinished milestone\n' "$file" >&2
      exit 1
    fi
  fi
done
