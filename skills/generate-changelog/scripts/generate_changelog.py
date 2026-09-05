#!/usr/bin/env python3
"""
Generate a Keep a Changelog formatted CHANGELOG.md from git commit history.
Works standalone or as a Claude Code skill.
"""

import subprocess
import re
import sys
import argparse
from datetime import datetime

CATEGORIES = {
    'Added': [r'^feat(\(.*?\))?:', r'^add(\(.*?\))?:', r'^feature(\(.*?\))?:'],
    'Fixed': [r'^fix(\(.*?\))?:', r'^bug(\(.*?\))?:', r'^patch(\(.*?\))?:'],
    'Changed': [r'^refactor(\(.*?\))?:', r'^perf(\(.*?\))?:', r'^style(\(.*?\))?:', r'^update(\(.*?\))?:'],
    'Removed': [r'^remove(\(.*?\))?:', r'^delete(\(.*?\))?:', r'^deprecate(\(.*?\))?:'],
    'Security': [r'^sec(\(.*?\))?:', r'^security(\(.*?\))?:'],
    'Documentation & Maintenance': [r'^docs(\(.*?\))?:', r'^chore(\(.*?\))?:', r'^ci(\(.*?\))?:', r'^test(\(.*?\))?:']
}

def run_git_cmd(cmd):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_latest_tag():
    return run_git_cmd(['git', 'describe', '--tags', '--abbrev=0'])

def get_commits_since(tag=None):
    if tag:
        range_spec = f"{tag}..HEAD"
    else:
        range_spec = "HEAD"
    
    log = run_git_cmd(['git', 'log', range_spec, '--pretty=format:%s||%h||%an'])
    if not log:
        return []
    
    commits = []
    for line in log.splitlines():
        parts = line.split('||')
        if len(parts) >= 3:
            commits.append({'subject': parts[0].strip(), 'hash': parts[1].strip(), 'author': parts[2].strip()})
    return commits

def categorize_commits(commits):
    buckets = {cat: [] for cat in CATEGORIES}
    buckets['Other Changes'] = []
    
    for c in commits:
        subj = c['subject']
        matched = False
        for cat, patterns in CATEGORIES.items():
            for pat in patterns:
                if re.search(pat, subj, re.IGNORECASE):
                    # Clean conventional prefix
                    clean_subj = re.sub(pat, '', subj, flags=re.IGNORECASE).strip()
                    clean_subj = clean_subj[0].upper() + clean_subj[1:] if clean_subj else subj
                    buckets[cat].append(f"- {clean_subj} ({c['hash']}) by @{c['author']}")
                    matched = True
                    break
            if matched:
                break
        if not matched:
            buckets['Other Changes'].append(f"- {subj} ({c['hash']}) by @{c['author']}")
            
    return {k: v for k, v in buckets.items() if v}

def build_changelog(version, date_str, categorized):
    lines = [
        f"## [{version}] - {date_str}",
        ""
    ]
    for cat, items in categorized.items():
        lines.append(f"### {cat}")
        lines.extend(items)
        lines.append("")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate CHANGELOG.md from git history")
    parser.add_argument("--version", default="Unreleased", help="Release version tag (default: Unreleased)")
    parser.add_argument("--output", default="CHANGELOG.md", help="Output file (default: CHANGELOG.md)")
    args = parser.parse_args()

    latest_tag = get_latest_tag()
    print(f"Latest git tag: {latest_tag if latest_tag else 'None (reading full history)'}")
    
    commits = get_commits_since(latest_tag)
    print(f"Found {len(commits)} commits since {latest_tag or 'initial commit'}.")
    
    categorized = categorize_commits(commits)
    today = datetime.now().strftime("%Y-%m-%d")
    new_section = build_changelog(args.version, today, categorized)
    
    print("\n" + "="*50)
    print(new_section)
    print("="*50)
    
    # Prepend or write to output file
    existing = ""
    try:
        with open(args.output, "r", encoding="utf-8") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
        
    if not existing.startswith("# Changelog"):
        existing = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n" + existing
        
    # Insert new section after header
    header_end = existing.find("\n\n") + 2
    updated = existing[:header_end] + new_section + "\n" + existing[header_end:]
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(updated)
        
    print(f"Successfully updated {args.output}")

if __name__ == '__main__':
    main()
