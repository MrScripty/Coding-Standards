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

  objective_rows="$(
    sed -n '/^## Objective Acceptance$/,/^## /p' "$file" |
      awk -F'|' '
        /^\|/ {
          id = $2
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", id)
          if (id == "ID") {
            for (column = 2; column < NF; column++) {
              heading = $column
              gsub(/^[[:space:]]+|[[:space:]]+$/, "", heading)
              if (heading == "Status") status_column = column
              if (heading == "Evidence") evidence_column = column
            }
            next
          }
          if (id == "" || id ~ /^-+$/) next
          value = status_column == 0 ? "" : $status_column
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
          gsub(/`/, "", value)
          evidence = evidence_column == 0 ? "" : $evidence_column
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", evidence)
          gsub(/`/, "", evidence)
          print id "\t" value "\t" (evidence == "" ? "<missing>" : evidence)
        }
      '
  )"
  if [[ -z "$objective_rows" ]]; then
    printf '%s: expected at least one objective-acceptance row\n' "$file" >&2
    exit 1
  fi
  while IFS=$'\t' read -r objective_id objective_status objective_evidence; do
    if [[ ! "$objective_status" =~ ^(pending|blocked|satisfied)$ ]]; then
      printf '%s: objective %s has invalid status %s\n' \
        "$file" "$objective_id" "$objective_status" >&2
      exit 1
    fi
    if [[ "$objective_status" == "satisfied" ]] &&
      [[ "$objective_evidence" == "<missing>" || "$objective_evidence" == "pending" ]]; then
      printf '%s: satisfied objective %s requires evidence\n' \
        "$file" "$objective_id" >&2
      exit 1
    fi
    if [[ "$status" == "Accepted" && "$objective_status" != "satisfied" ]]; then
      printf '%s: accepted plan has unsatisfied objective %s\n' \
        "$file" "$objective_id" >&2
      exit 1
    fi
  done <<<"$objective_rows"

  final_acceptance_count="$(grep -c '^- Acceptance status: `' "$file" || true)"
  final_status_count="$(grep -c '^- Final status: `' "$file" || true)"
  if [[ "$final_acceptance_count" -gt 1 || "$final_status_count" -gt 1 ]]; then
    printf '%s: final acceptance projections must be unique\n' "$file" >&2
    exit 1
  fi
  if [[ "$status" == "Accepted" ]] &&
    [[ "$final_acceptance_count" -ne 1 || "$final_status_count" -ne 1 ]]; then
    printf '%s: accepted plan requires both final acceptance projections\n' \
      "$file" >&2
    exit 1
  fi
  final_acceptance_status="$(sed -n 's/^- Acceptance status: `\([^`]*\)`$/\1/p' "$file")"
  final_status="$(sed -n 's/^- Final status: `\([^`]*\)`$/\1/p' "$file")"
  if [[ -n "$final_acceptance_status" ]] &&
    [[ "$final_acceptance_status" != "$acceptance_status" ]]; then
    printf '%s: final acceptance status does not match header\n' "$file" >&2
    exit 1
  fi
  if [[ -n "$final_status" ]] && [[ "$final_status" != "$status" ]]; then
    printf '%s: final plan status does not match header\n' "$file" >&2
    exit 1
  fi
done
