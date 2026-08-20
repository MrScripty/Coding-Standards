#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-executor-delegation-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly GENERIC="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly CONCURRENCY="$REPO_ROOT/topics/concurrency.md"
readonly ASYNC_PROFILE="$REPO_ROOT/profiles/languages/rust/async.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

while IFS=$'\t' read -r case_id upstream_outcome input_scope input_proof \
  lifecycle_state delegate_capability action fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$upstream_outcome" =~ ^(local-success|explicit-unsupported|invalid|execution-failure|cancelled|resource-failure|lifecycle-failure|unavailable)$ ]]
  [[ "$input_scope" =~ ^(current|retained-prior)$ ]]
  [[ "$input_proof" =~ ^(valid|invalid)$ ]]
  [[ "$lifecycle_state" =~ ^(active|cancelled|unavailable)$ ]]
  [[ "$delegate_capability" =~ ^(available|unavailable|not-required)$ ]]
  [[ "$action" =~ ^(complete|delegate|return-outcome|retry|alternate-executor|detached)$ ]]
  [[ "$fallback" =~ ^(none|catch-all|retry|carry-forward|default-input|alternate-executor|detach)$ ]]
  [[ "$expected" =~ ^(allow-local|allow-delegate|preserve-outcome|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$input_scope" == 'retained-prior' ||
        "$action" =~ ^(retry|alternate-executor|detached)$ ]]; then
    actual='typed-invalid'
  elif [[ "$action" == 'complete' ]]; then
    if [[ "$upstream_outcome" == 'local-success' &&
          "$input_scope" == 'current' &&
          "$input_proof" == 'valid' ]]; then
      actual='allow-local'
    else
      actual='typed-invalid'
    fi
  elif [[ "$action" == 'delegate' ]]; then
    if [[ "$upstream_outcome" == 'explicit-unsupported' &&
          "$input_scope" == 'current' &&
          "$input_proof" == 'valid' &&
          "$lifecycle_state" == 'active' &&
          "$delegate_capability" == 'available' ]]; then
      actual='allow-delegate'
    else
      actual='typed-invalid'
    fi
  elif [[ "$action" == 'return-outcome' ]]; then
    if [[ "$upstream_outcome" == 'local-success' ]]; then
      actual='typed-invalid'
    elif [[ "$upstream_outcome" == 'explicit-unsupported' &&
            "$delegate_capability" == 'unavailable' ]]; then
      actual='typed-unavailable'
    else
      actual='preserve-outcome'
    fi
  else
    actual='typed-invalid'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

[[ "$(awk -F '\t' '$1 == "STD-0781" { count += 1 } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
[[ "$(awk -F '\t' 'NR > 1 && $1 == "STD-0781" { count += 1 } END { print count + 0 }' \
  "$DISPOSITIONS")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0781" {
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
    found = 1
  }
  END { exit !found }
' "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" "$REPO_ROOT/topics/security.md" \
  "$CONCURRENCY" \
  "$REPO_ROOT/profiles/boundaries/interop.md" "$GENERIC" \
  "$RUST_INDEX" "$ASYNC_PROFILE" "$PROFILE"

required_profile=(
  '## Explicit Executor Delegation'
  'exact typed `unsupported` outcome'
  "call's already validated input"
  'Successful local completion is terminal.'
  'Validation, execution, cancellation, resource, lifecycle, and unavailable'
  'selected lifecycle owner before'
  'typed `unavailable`'
  '## Verification'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_composite="$(
  sed -n '/^### Composite Executors$/,/^## Code Generation Strategy$/p' \
    "$LEGACY"
)"
rg -F -q 'language-bindings.md#explicit-executor-delegation' \
  <<< "$legacy_composite"
for text in 'CoreFirstExecutor' 'inputs.clone()' \
  'Err(EngineError::UnsupportedNodeType' 'fall through to the host' \
  'async_trait'; do
  if rg -F -q "$text" <<< "$legacy_composite"; then
    printf 'legacy executor delegation guidance remains: %s\n' "$text" >&2
    exit 1
  fi
done

for heading in '## Code Generation Strategy' '## Memory Ownership Model' \
  '## Async Bridging' '## Testing Strategy'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '| F026 | Resolved in Milestone 7.4b5f |' "$FINDINGS"
"$SCRIPT_DIR/verify-milestone-7-f025-f026-decomposition.sh"

printf 'Rust binding executor delegation passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
