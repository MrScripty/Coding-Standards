#!/usr/bin/env bash
set -euo pipefail

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
    "Acceptance status" \
    "Execution ledger" \
    "Issues"; do
    if [[ "$(grep -c "^\\*\\*${field}:\\*\\* " "$file" || true)" -ne 1 ]]; then
      printf '%s: expected one %s field\n' "$file" "$field" >&2
      exit 1
    fi
  done

  status="$(value_for "$file" "Plan status")"
  acceptance_status="$(value_for "$file" "Acceptance status")"

  if [[ ! "$status" =~ ^(Planned|Active|Blocked|Implemented|Verifying|Accepted|Deferred|Superseded)$ ]]; then
    printf '%s: invalid plan status %s\n' "$file" "$status" >&2
    exit 1
  fi
  if [[ ! "$acceptance_status" =~ ^(pending|partial|blocked|satisfied)$ ]]; then
    printf '%s: invalid acceptance status %s\n' \
      "$file" "$acceptance_status" >&2
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
    if [[ "$acceptance_status" != "satisfied" ]]; then
      printf '%s: accepted plan has %s acceptance\n' \
        "$file" "$acceptance_status" >&2
      exit 1
    fi
    if rg -q '^\*\*Status:\*\* `(Planned|Active|Blocked|Implemented|Verifying)`' "$file"; then
      printf '%s: accepted plan has unfinished milestone\n' "$file" >&2
      exit 1
    fi
  fi
  if [[ "$status" != "Accepted" && "$acceptance_status" == "satisfied" ]]; then
    printf '%s: satisfied acceptance requires Accepted plan status\n' \
      "$file" >&2
    exit 1
  fi
done
