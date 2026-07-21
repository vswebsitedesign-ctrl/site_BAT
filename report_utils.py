#!/usr/bin/env python3
"""
report_utils.py — the ONLY sanctioned way to read/write Master_Report.json.

Usage pattern for any future edit:

    from report_utils import load_report, save_report
    report = load_report()
    # ... mutate report dict ...
    save_report(report)   # lints BEFORE committing; raises and rolls back if it fails

This makes the bloat-prevention rule structurally enforced rather than dependent on
an AI remembering to run report_lint.py separately. A write that would violate the
rule never reaches Master_Report.json at all.
"""
import json, sys, shutil, os

REPORT_PATH = 'Master_Report.json'
MAX_CHANGELOG_CHARS = 200
MAX_KNOWN_ISSUE_CHARS = 300


def load_report():
    with open(REPORT_PATH) as f:
        return json.load(f)


def _lint(report):
    violations = []
    for i, entry in enumerate(report.get('changelog', [])):
        text = entry.get('change', '')
        if len(text) > MAX_CHANGELOG_CHARS:
            violations.append(f"changelog[{i}] ({entry.get('date')}): {len(text)} chars (max {MAX_CHANGELOG_CHARS})")
    for key, text in report.get('known_issues', {}).items():
        if isinstance(text, str) and len(text) > MAX_KNOWN_ISSUE_CHARS:
            violations.append(f"known_issues.{key}: {len(text)} chars (max {MAX_KNOWN_ISSUE_CHARS})")
    return violations


def _warnings(report):
    # Non-blocking: flags known_issues that look resolved but haven't been
    # archived out yet. Does not stop the save -- just surfaces it every time,
    # per AI_PLAYBOOK.md principle 12 (enforce with a script, not memory).
    warnings = []
    for key, text in report.get('known_issues', {}).items():
        upper = text.upper() if isinstance(text, str) else ''
        starts_resolved = upper.startswith('FIXED') or upper.startswith('RESOLVED')
        if starts_resolved:
            warnings.append(f"known_issues.{key} looks resolved but is still inline -- consider archiving to Archive/known_issues/")
    return warnings


def save_report(report):
    """
    Lints the proposed report BEFORE writing. If it fails, prints violations and
    raises SystemExit(1) WITHOUT touching Master_Report.json — the file on disk is
    left exactly as it was. This guarantees a bloated write can never land, even if
    the caller forgot to lint manually.
    """
    violations = _lint(report)
    if violations:
        print("❌ SAVE BLOCKED — report_lint violations found, Master_Report.json NOT modified:")
        for v in violations:
            print("  -", v)
        print("\nFix: shorten the offending entry, move detail to reference/, then save_report() again.")
        sys.exit(1)

    # Write to a temp file first, then atomically replace — avoids ever leaving a
    # half-written or corrupt Master_Report.json on disk if something fails mid-write.
    tmp_path = REPORT_PATH + '.tmp'
    with open(tmp_path, 'w') as f:
        json.dump(report, f, indent=2)

    # Verify the temp file is valid JSON before committing
    with open(tmp_path) as f:
        json.load(f)  # raises if invalid

    shutil.move(tmp_path, REPORT_PATH)
    print(f"✅ Saved and verified — {len(report.get('changelog', []))} changelog entries, "
          f"{len(report.get('known_issues', {}))} known_issues, all within limits")

    warnings = _warnings(report)
    if warnings:
        print("\n⚠️  Non-blocking bloat warnings:")
        for w in warnings:
            print("  -", w)


if __name__ == '__main__':
    # Running this file directly just lints the current on-disk report (read-only check)
    report = load_report()
    violations = _lint(report)
    if violations:
        print("❌ Current Master_Report.json has violations:")
        for v in violations:
            print("  -", v)
        sys.exit(1)
    print("✅ Current Master_Report.json passes lint")
