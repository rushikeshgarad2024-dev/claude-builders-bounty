---
name: generate-changelog
description: Automatically generates a Keep a Changelog formatted CHANGELOG.md from git commit history since the last release tag.
---

# Generate Changelog Skill

Generate a clean, standardized `CHANGELOG.md` according to [Keep a Changelog](https://keepachangelog.com/) standards directly from git commit history.

## Features
- Detects the latest semver git tag automatically
- Parses conventional commits (`feat:`, `fix:`, `refactor:`, `perf:`, `docs:`, `chore:`, `breaking:`)
- Categorizes changes into `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`
- Generates markdown formatted for humans and releases

## Usage

### Slash Command
```bash
/generate-changelog
```

### CLI Script
```bash
bash skills/generate-changelog/scripts/changelog.sh
# or python version
python skills/generate-changelog/scripts/generate_changelog.py --output CHANGELOG.md
```
