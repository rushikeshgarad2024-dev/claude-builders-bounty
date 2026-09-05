#!/usr/bin/env python3
"""
Claude Code Pre-Tool-Use Hook: Blocks Destructive Commands
Location: ~/.claude/hooks/pre-tool-use or project hooks
Intercepts dangerous bash commands (rm -rf, DROP TABLE, TRUNCATE, git push --force, DELETE without WHERE)
Logs blocked attempts to ~/.claude/hooks/blocked.log
"""

import sys
import os
import re
import json
from datetime import datetime

DANGEROUS_PATTERNS = [
    (r'\brm\s+.*(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r|(-r|-R|--recursive)\s+(-f|--force)|(-f|--force)\s+(-r|-R|--recursive))\b', "Recursive forced file deletion ('rm -rf') is dangerous and blocked."),
    (r'\bDROP\s+(TABLE|DATABASE|SCHEMA)\b', "Dropping tables or databases without explicit sandbox authorization is blocked."),
    (r'\bTRUNCATE\s+(TABLE)?\b', "Table truncation is blocked to prevent catastrophic data loss."),
    (r'\bgit\s+push\s+.*(--force|-f)\b', "Force pushing to git remotes is blocked to prevent overwriting history.")
]

def get_log_path():
    home = os.path.expanduser("~")
    hooks_dir = os.path.join(home, ".claude", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    return os.path.join(hooks_dir, "blocked.log")

def log_blocked(command, reason, cwd):
    log_file = get_log_path()
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"[{timestamp}] BLOCKED: '{command}' | REASON: {reason} | CWD: {cwd}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to write to {log_file}: {e}\n")

def check_command(command, cwd=None):
    cwd = cwd or os.getcwd()
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            log_blocked(command, reason, cwd)
            return False, reason
    # Check DELETE FROM without WHERE
    if re.search(r'\bDELETE\s+FROM\b', command, re.IGNORECASE):
        if not re.search(r'\bWHERE\b', command, re.IGNORECASE):
            reason = "Unrestricted DELETE FROM without a WHERE clause is blocked."
            log_blocked(command, reason, cwd)
            return False, reason
    return True, "OK"

def main():
    # Read tool input from stdin or args
    input_data = ""
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
    else:
        try:
            raw = sys.stdin.read()
            if raw.strip().startswith("{"):
                payload = json.loads(raw)
                command = payload.get("command", payload.get("input", {}).get("command", raw))
            else:
                command = raw.strip()
        except Exception:
            command = ""

    if not command:
        sys.exit(0)

    allowed, reason = check_command(command)
    if not allowed:
        sys.stderr.write(f"\n[SECURITY ERROR] Destructive command blocked by safety hook:\n")
        sys.stderr.write(f"Command: {command}\n")
        sys.stderr.write(f"Reason:  {reason}\n\n")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
