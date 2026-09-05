#!/usr/bin/env bash
# Generate Keep a Changelog formatted changelog from git history
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/generate_changelog.py" "$@"
