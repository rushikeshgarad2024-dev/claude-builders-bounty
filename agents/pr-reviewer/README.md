# Claude Code PR Reviewer Agent

Automated agent that inspects GitHub PR diffs, identifies architectural & security risks, and generates structured Markdown reviews with confidence ratings.

## Usage

### 1. CLI Execution
```bash
python3 agents/pr-reviewer/review_pr.py --pr https://github.com/owner/repo/pull/123
```

### 2. Auto-Post Review Comment
```bash
python3 agents/pr-reviewer/review_pr.py --pr https://github.com/owner/repo/pull/123 --post --token $GITHUB_TOKEN
```

### 3. GitHub Actions Workflow
Add `.github/workflows/pr-reviewer.yml` to your repository for automatic PR reviews on every pull request.
