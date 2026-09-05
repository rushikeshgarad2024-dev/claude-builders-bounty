# Generate Changelog Skill & CLI

Automatically generate human-readable, Keep a Changelog formatted `CHANGELOG.md` updates from git history.

## Quick Setup (3 Steps)

1. **Install script**:
   ```bash
   chmod +x skills/generate-changelog/scripts/changelog.sh
   ```

2. **Run Changelog Generator**:
   ```bash
   bash skills/generate-changelog/scripts/changelog.sh --version 1.0.0
   ```

3. **Verify Output**:
   Check `CHANGELOG.md` in your repository root. Done!

## Categorization Rules
- `feat:`, `add:` -> **Added**
- `fix:`, `bug:`, `patch:` -> **Fixed**
- `refactor:`, `perf:`, `update:` -> **Changed**
- `remove:`, `delete:`, `deprecate:` -> **Removed**
- `sec:`, `security:` -> **Security**
- `docs:`, `chore:`, `ci:` -> **Documentation & Maintenance**
