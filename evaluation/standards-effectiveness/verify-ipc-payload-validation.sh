#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/ipc/action-payload-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly IPC="$REPO_ROOT/profiles/boundaries/ipc.md"
readonly SECURITY="$REPO_ROOT/topics/security.md"
readonly LEGACY_ARCH="$REPO_ROOT/ARCHITECTURE-PATTERNS.md"
readonly LEGACY_INTEROP="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly LEGACY_SECURITY="$REPO_ROOT/SECURITY-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

while IFS=$'\t' read -r case_id envelope pair schema payload metadata \
  producer_proof extra_fields dispatch expected; do
  [[ "$case_id" == 'case' ]] && continue

  [[ "$envelope" =~ ^(valid|invalid)$ ]]
  [[ "$pair" =~ ^(supported|unknown-category|unknown-action|mismatch|not-selected)$ ]]
  [[ "$schema" =~ ^(available|unavailable|not-selected)$ ]]
  [[ "$payload" =~ ^(valid|missing-field|wrong-type|not-checked)$ ]]
  [[ "$metadata" =~ ^(valid|invalid|not-required)$ ]]
  [[ "$producer_proof" =~ ^(none|static-only)$ ]]
  [[ "$extra_fields" =~ ^(absent|accepted|rejected|unspecified)$ ]]
  [[ "$dispatch" =~ ^(validated-variant|raw|default|none)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]

  if [[ "$envelope" == 'invalid' ]]; then
    actual='typed-invalid'
  elif [[ "$pair" =~ ^(unknown-category|unknown-action|mismatch)$ ]]; then
    actual='typed-unsupported'
  elif [[ "$schema" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$pair" != 'supported' ||
          "$schema" != 'available' ||
          "$payload" != 'valid' ||
          "$metadata" == 'invalid' ||
          "$extra_fields" =~ ^(rejected|unspecified)$ ||
          "$dispatch" != 'validated-variant' ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(
  STD-0063 STD-0064 STD-0065 STD-0066 STD-0067 STD-0068
  STD-0476
  STD-0592 STD-0593 STD-0594 STD-0595
)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    ($2 == "ARCHITECTURE-PATTERNS.md" &&
     $1 >= "STD-0063" && $1 <= "STD-0068") ||
    ($2 == "INTEROP-STANDARDS.md" && $1 == "STD-0476") ||
    ($2 == "SECURITY-STANDARDS.md" &&
     $1 >= "STD-0592" && $1 <= "STD-0595") {
      print $1
    }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 &&
    (($2 == "ARCHITECTURE-PATTERNS.md" &&
      $1 >= "STD-0063" && $1 <= "STD-0068") ||
     ($2 == "INTEROP-STANDARDS.md" && $1 == "STD-0476") ||
     ($2 == "SECURITY-STANDARDS.md" &&
      $1 >= "STD-0592" && $1 <= "STD-0595")) {
      print $1
    }
  ' "$DISPOSITIONS" | sort
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0063|STD-0066)
      [[ "$source:$target:$disposition" == \
        'ARCHITECTURE-PATTERNS.md:profiles/boundaries/ipc.md:move' ]]
      ;;
    STD-0064|STD-0065|STD-0067)
      [[ "$source:$target:$disposition" == \
        'ARCHITECTURE-PATTERNS.md:profiles/boundaries/ipc.md:refine' ]]
      ;;
    STD-0068)
      [[ "$source:$target:$disposition" == \
        'ARCHITECTURE-PATTERNS.md:profiles/boundaries/ipc.md:merge' ]]
      ;;
    STD-0476)
      [[ "$source:$target:$disposition" == \
        'INTEROP-STANDARDS.md:profiles/boundaries/ipc.md:refine' ]]
      ;;
    STD-0592)
      [[ "$source:$target:$disposition" == \
        'SECURITY-STANDARDS.md:topics/security.md:merge' ]]
      ;;
    STD-0593|STD-0595)
      [[ "$source:$target:$disposition" == \
        'SECURITY-STANDARDS.md:profiles/boundaries/ipc.md:refine' ]]
      ;;
    STD-0594)
      [[ "$source:$target:$disposition" == \
        'SECURITY-STANDARDS.md:topics/security.md:refine' ]]
      ;;
    *)
      continue
      ;;
  esac
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$SECURITY" \
  "$IPC"

required_ipc=(
  '## Decode Before Dispatch'
  'decode the complete category/action discriminant'
  'select the schema for that exact supported pair'
  'construct a closed validated variant'
  '`unsupported` for a well-formed category/action pair'
  '`unavailable` when the required schema or decoder'
  'When no extra-field policy is defined'
  'Dispatch accepts only closed validated variants.'
  'use a default action or fall-through branch'
  'retry through an alternate permissive decoder'
)
for text in "${required_ipc[@]}"; do
  rg -F -q "$text" "$IPC"
done

required_security=(
  '## Untrusted Structured Input'
  'before it can authorize work, resource access, or side effects'
  'profiles/boundaries/ipc.md'
  'Do not continue with'
)
for text in "${required_security[@]}"; do
  rg -F -q "$text" "$SECURITY"
done

for file in "$REPO_ROOT/README.md" "$REPO_ROOT/STANDARDS-ROUTER.md"; do
  rg -F -q 'profiles/boundaries/ipc.md' "$file"
done
rg -F -q 'profiles/boundaries/ipc.md' "$LEGACY_ARCH"
rg -F -q 'profiles/boundaries/ipc.md#decode-before-dispatch' "$LEGACY_INTEROP"
rg -F -q 'profiles/boundaries/ipc.md' "$LEGACY_SECURITY"
rg -F -q 'topics/security.md#untrusted-structured-input' "$LEGACY_SECURITY"

legacy_arch_section="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "## IPC/Message Contract Pattern" { capture = 1 }
    line == "## Composition Root Pattern" { capture = 0 }
    capture { print }
  ' "$LEGACY_ARCH"
)"
legacy_security_section="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "## Message/API Payload Validation" { capture = 1 }
    line == "## Network Transport Safety" { capture = 0 }
    capture { print }
  ' "$LEGACY_SECURITY"
)"
for section in "$legacy_arch_section" "$legacy_security_section"; do
  if rg -q '^### |```| as ValidatedMessage|payload as |JsonSerializer.Deserialize|ipcMain.handle' \
    <<< "$section"; then
    printf 'legacy payload-validation policy remains active\n' >&2
    exit 1
  fi
done

legacy_interop_section="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "### Validate Received Messages" { capture = 1 }
    line == "---" { capture = 0 }
    capture { print }
  ' "$LEGACY_INTEROP"
)"
if rg -q '```|JSON\.parse|typeof parsed|console\.error|return;' \
  <<< "$legacy_interop_section"; then
  printf 'legacy Interop partial-message validation remains active\n' >&2
  exit 1
fi
rg -F -q 'profiles/boundaries/ipc.md#decode-before-dispatch' \
  <<< "$legacy_interop_section"

removed_patterns=(
  "msg.payload as SelectItemCommand['payload']"
  'msg as ValidatedMessage'
  'parsed as Record<string, unknown>'
  'JsonSerializer.Deserialize<OpenProjectRequest>'
)
for pattern in "${removed_patterns[@]}"; do
  if rg -F -q "$pattern" "$IPC" "$SECURITY" "$LEGACY_ARCH" "$LEGACY_SECURITY"; then
    printf 'unsafe payload-validation guidance remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

rg -F -q '| F018 | Resolved in Milestone 7.4b2c |' "$FINDINGS"
rg -F -q '| F059 | Resolved in Milestone 7.4b8d |' "$FINDINGS"
rg -F -q '`7.4b2c` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8d` (`Accepted`)' "$PLAN"
if rg -q '^\*\*Next slice:\*\* .*7\.4b2(b|c)' "$PLAN"; then
  printf 'accepted F018 slice remains next\n' >&2
  exit 1
fi

printf 'IPC action-specific payload validation passed: 11 exact dispositions\n'
