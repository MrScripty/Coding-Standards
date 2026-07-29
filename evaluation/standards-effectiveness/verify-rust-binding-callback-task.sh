#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-callback-task-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id contract task authority input correlation \
  execution ownership cancellation completion capability evidence fallback \
  expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$contract" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$task" =~ ^(supported|unsupported)$ ]]
  [[ "$authority" =~ ^(selected|missing|wrong)$ ]]
  [[ "$input" =~ ^(validated|invalid|carried)$ ]]
  [[ "$correlation" =~ ^(valid|missing|mismatch|duplicate)$ ]]
  [[ "$execution" =~ ^(inline|async)$ ]]
  [[ "$ownership" =~ ^(scoped|tracked|detached)$ ]]
  [[ "$cancellation" =~ ^(preserved|lost)$ ]]
  [[ "$completion" =~ ^(success|failure|unresolved)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(native-host|native-only|missing)$ ]]
  [[ "$fallback" =~ ^(none|noop|polling|alternate-runtime|default-output|default-success)$ ]]
  [[ "$expected" =~ ^(allow|preserve-failure|typed-invalid|typed-unsupported|typed-unavailable|typed-incomplete)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$contract" == contradictory ||
        "$authority" == wrong ||
        "$input" != validated ||
        "$correlation" != valid ||
        "$ownership" == detached ||
        "$cancellation" == lost ]]; then
    actual=typed-invalid
  elif [[ "$task" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing ||
          "$authority" == missing ||
          "$capability" == unavailable ||
          "$evidence" != native-host ]]; then
    actual=typed-unavailable
  elif [[ "$completion" == unresolved ]]; then
    actual=typed-incomplete
  elif [[ "$completion" == failure ]]; then
    actual=preserve-failure
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 22 ]]

[[ "$(awk -F '\t' '$1 == "STD-0780" { count++ } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0780" {
    count += 1
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/concurrency.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" \
  "$REPO_ROOT/profiles/boundaries/language-bindings.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$REPO_ROOT/profiles/languages/rust/async.md" \
  "$PROFILE"

required_profile=(
  '## Host Callback Task Adaptation'
  'supported task identities and checked input and output representations'
  'synchronous or asynchronous completion and correlation identity'
  'Neither generated host code nor the adapter owns domain behavior'
  'release synchronization guards'
  'Each invocation has fresh task identity'
  'does not authorize carrying state from an earlier invocation'
  'resolve terminal completion'
  'with the selected Rust Async and Concurrency lifecycle owner'
  'does not synchronously drive async work'
  'Preserve host task failure and cancellation'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  'selected typed incomplete outcome'
  'Do not install a no-op executor'
  'snapshot polling'
  'report default success'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_callback="$(
  sed -n '/^### Callback-Based Task Execution$/,/^### Composite Executors$/p' \
    "$LEGACY"
)"
rg -F -q \
  'profiles/languages/rust/language-bindings.md#host-callback-task-adaptation' \
  <<< "$legacy_callback"
for pattern in \
  'TaskExecutor: Send + Sync' \
  'NoopTaskExecutor' \
  'polling snapshots' \
  'oneshot channel' \
  'UniFFI' \
  'Rustler' \
  '```'; do
  ! rg -F -q "$pattern" <<< "$legacy_callback"
done

rg -F -q '### Composite Executors' "$LEGACY"
rg -F -q '`7.4b8j` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-async-lifecycle.sh"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-rust-binding-executor-delegation.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Rust binding callback task passed: %s decisions, 1 exact disposition\n' \
  "$count"
