#!/usr/bin/env python3
"""
report_lint.py — enforces Master_Report.json bloat-prevention rule.
Run this after ANY edit to Master_Report.json, before declaring the edit done.
Exits non-zero and lists every offending field if limits are exceeded.
"""
import json, sys

MAX_CHANGELOG_CHARS = 200
MAX_KNOWN_ISSUE_CHARS = 300

with open('Master_Report.json') as f:
    report = json.load(f)

violations = []

for i, entry in enumerate(report.get('changelog', [])):
    text = entry.get('change', '')
    if len(text) > MAX_CHANGELOG_CHARS:
        violations.append(f"changelog[{i}] ({entry.get('date')}): {len(text)} chars (max {MAX_CHANGELOG_CHARS}) -- move detail to reference/")

for key, text in report.get('known_issues', {}).items():
    if isinstance(text, str) and len(text) > MAX_KNOWN_ISSUE_CHARS:
        violations.append(f"known_issues.{key}: {len(text)} chars (max {MAX_KNOWN_ISSUE_CHARS}) -- move detail to reference/")

if violations:
    print("❌ REPORT LINT FAILED -- bloat-prevention rule violated:")
    for v in violations:
        print("  -", v)
    print("\nFix: shorten to a one-line summary + add/update a '_reference' pointer to a file in reference/")
    sys.exit(1)
else:
    print(f"✅ Report lint passed -- {len(report.get('changelog', []))} changelog entries, {len(report.get('known_issues', {}))} known_issues, all within limits")
