#!/usr/bin/env bash
# Claude Code Pre-Tool-Use Hook wrapper
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/block_destructive.py" "$@"
