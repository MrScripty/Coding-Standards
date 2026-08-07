#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

python3 "$REPO_ROOT/tools/standards_verifier/generate_inventory.py" \
  --repo-root "$REPO_ROOT" --check
exec python3 "$REPO_ROOT/tools/standards_verifier/verify.py" \
  --repo-root "$REPO_ROOT" --all
