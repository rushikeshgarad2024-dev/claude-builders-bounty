# Pre-Tool-Use Hook: Block Destructive Commands

Prevents accidental or malicious execution of destructive commands (`rm -rf`, `DROP TABLE`, `TRUNCATE`, `git push --force`, unrestricted `DELETE FROM`) by Claude Code.

## Quick Install (2 Commands)

```bash
mkdir -p ~/.claude/hooks/pre-tool-use
cp hooks/pre-tool-use/block_destructive.py ~/.claude/hooks/pre-tool-use/
```

## Features
- **Zero-Friction Interception**: Fast regex check executes in < 5ms before tool execution.
- **Audit Trail**: Writes all blocked attempts to `~/.claude/hooks/blocked.log` with timestamp, project directory, and attempted command.
- **Safe Operations Untouched**: Normal commands (`npm test`, `git status`, `rm single_file.txt`, `DELETE FROM ... WHERE id = ...`) run freely.

## Testing the Hook
```bash
python3 hooks/pre-tool-use/test_block_destructive.py
```
