#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/documentation.md"
readonly TEMPLATE="$REPO_ROOT/templates/README-TEMPLATE.md"
readonly LEGACY="$REPO_ROOT/DOCUMENTATION-STANDARDS.md"

mapfile -t expected_ids < <(
  awk -F '\t' '
    function selected(id) {
      number = substr(id, 5) + 0
      return (number >= 350 && number <= 375) ||
        (number >= 400 && number <= 420) ||
        (number >= 437 && number <= 448)
    }
    $2 == "DOCUMENTATION-STANDARDS.md" && selected($1) { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    function selected(id) {
      number = substr(id, 5) + 0
      return (number >= 350 && number <= 375) ||
        (number >= 400 && number <= 420) ||
        (number >= 437 && number <= 448)
    }
    NR > 1 &&
      $2 == "DOCUMENTATION-STANDARDS.md" &&
      selected($1) { print $1 }
  ' "$DISPOSITIONS"
)

if [[ "${#expected_ids[@]}" -ne 59 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ]]; then
  printf 'Documentation policy disposition count mismatch\n' >&2
  exit 1
fi

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Documentation policy dispositions are not exact or ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  number="${id#STD-}"
  number="$((10#$number))"
  if ! (( (number >= 350 && number <= 375) ||
          (number >= 400 && number <= 420) ||
          (number >= 437 && number <= 448) )); then
    continue
  fi

  [[ "$source" == "DOCUMENTATION-STANDARDS.md" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  if [[ "$disposition" == "remove" ]]; then
    [[ "$target" == "none" ]]
  else
    [[ "$disposition" == "move" ]]
    [[ "$target" == "workflows/documentation.md" ||
       "$target" == "templates/README-TEMPLATE.md" ]]
  fi
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$WORKFLOW"

for file in "$LEGACY" "$TEMPLATE"; do
  if ! rg -F -q "workflows/documentation.md" "$file"; then
    printf '%s does not link the documentation workflow\n' \
      "${file#"$REPO_ROOT"/}" >&2
    exit 1
  fi
done

required_workflow_sections=(
  "## Artifact Placement"
  "## Documentation Profiles"
  "## Repository Entry Point"
  "## Decision Traceability"
)
for section in "${required_workflow_sections[@]}"; do
  if ! rg -F -q "$section" "$WORKFLOW"; then
    printf 'Documentation workflow is missing %s\n' "$section" >&2
    exit 1
  fi
done

legacy_headings='^## (Documentation Artifact Layout|Architecture Decision Records \(ADRs\)|README.md \(Project Root\)|Documentation Review Checklist)$'
if rg -q "$legacy_headings" "$LEGACY"; then
  printf 'Legacy documentation policy section remains authoritative\n' >&2
  exit 1
fi
if ! rg -q '^## Changelog' "$LEGACY"; then
  printf 'Release-owned changelog section was removed before Milestone 7.2c\n' >&2
  exit 1
fi

removed_rules=(
  'Every directory under `src/`'
  'directories with 3+ files'
  'Every PR that changes `src/<module>/`'
  'Every required section must contain'
  '## Project Structure'
  'All public functions, classes, and types should be documented'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$LEGACY" "$WORKFLOW" "$TEMPLATE"; then
    printf 'Removed blanket documentation rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Documentation policy consolidation passed\n'
