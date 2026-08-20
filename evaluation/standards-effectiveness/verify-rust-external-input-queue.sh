#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/external-input-queue-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/security.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

count=0
while IFS=$'\t' read -r case_id contract capacity overload ownership telemetry \
  input_state capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$contract" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$capacity" =~ ^(available|missing|fixed|unbounded)$ ]]
  [[ "$overload" =~ ^(reject|retain|evict|unsupported|default-reject|default-evict|missing)$ ]]
  [[ "$ownership" =~ ^(declared|missing)$ ]]
  [[ "$telemetry" =~ ^(emitted|not-required|missing|silent)$ ]]
  [[ "$input_state" =~ ^(current|prior)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(rust-operation|missing|producer-only)$ ]]
  [[ "$fallback" =~ ^(none|fixed-capacity|default-overflow|drop-oldest|unbounded|silent-discard|alternate-queue|alternate-runtime|prior-input|weaker-evidence)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable|typed-overload)$ ]]
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$contract" == contradictory ||
        "$capacity" =~ ^(fixed|unbounded)$ || "$overload" =~ ^default ||
        "$telemetry" == silent || "$input_state" == prior ]]; then actual=typed-invalid
  elif [[ "$overload" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$contract" == missing || "$capacity" == missing ||
          "$ownership" == missing || "$telemetry" == missing ||
          "$capability" == unavailable || "$evidence" != rust-operation ]]; then actual=typed-unavailable
  elif [[ "$overload" == reject ]]; then actual=typed-overload
  else actual=allow; fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 18 ]]

awk -F '\t' '
  NR > 1 && $1 == "STD-0824" {
    count += 1
    if ($2 != "languages/rust/RUST-SECURITY-STANDARDS.md" ||
        $3 != "profiles/languages/rust/security.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 1 }
' "$DISPOSITIONS"
[[ "$(awk -F '\t' '$1 == "STD-0824" { count++ } END { print count + 0 }' "$INVENTORY")" -eq 1 ]]

"$SCRIPT_DIR/check-metadata.sh" "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" "$REPO_ROOT/workflows/verification.md" "$REPO_ROOT/topics/security.md" "$REPO_ROOT/profiles/languages/rust/README.md" "$PROFILE"
required_profile_text=(
  '## External-Input Queues'
  'operation and resource contract'
  'Capacity is not a universal numeric constant'
  'current input'
  'typed `invalid`'
  '## No Fallback'
  'fixed capacity'
  '## Verification'
)
for text in "${required_profile_text[@]}"; do
  rg -F -q "$text" "$PROFILE"
done
legacy="$(sed -n '/^## Bounded Queues$/,/^## Network Listener Limits$/p' "$LEGACY")"
before_head="$(git -C "$REPO_ROOT" show HEAD:languages/rust/RUST-SECURITY-STANDARDS.md | sed '/^## Bounded Queues$/,$d')"
before_current="$(sed '/^## Bounded Queues$/,$d' "$LEGACY")"
after_head="$(git -C "$REPO_ROOT" show HEAD:languages/rust/RUST-SECURITY-STANDARDS.md | sed -n '/^## Network Listener Limits$/,$p')"
after_current="$(sed -n '/^## Network Listener Limits$/,$p' "$LEGACY")"
[[ "$before_current" == "$before_head" && "$after_current" == "$after_head" ]]
rg -F -q 'security.md#external-input-queues' <<< "$legacy"
for pattern in 'MAX_QUEUE' 'drop_oldest' 'msgs.drain' 'tracing::warn'; do
  ! rg -F -q "$pattern" <<< "$legacy"
done
rg -F -q '| F052 | Resolved in Milestone 7.4b7k |' "$FINDINGS"
"$SCRIPT_DIR/verify-rust-boundary-arithmetic.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"
printf 'Rust external-input queue policy passed: %s decisions, 1 exact disposition\n' "$count"
