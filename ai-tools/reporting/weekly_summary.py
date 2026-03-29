#!/usr/bin/env python3
"""
Weekly Summary Builder — AI Tools
===================================

Aggregates the daily dashboard reports from the past 7 days into a single
weekly summary HTML file.

Usage:
    python3 ai-tools/reporting/weekly_summary.py
    python3 ai-tools/reporting/weekly_summary.py --days 14
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports" / "automation"
DEFAULT_OUTPUT = REPORTS_DIR


def collect_reports(reports_dir: Path, days: int) -> list:
    """Find dashboard_*.html files from the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    reports = []
    for f in sorted(reports_dir.glob("dashboard_*.html")):
        match = re.search(r"dashboard_(\d{8})_(\d{6})\.html$", f.name)
        if match:
            ts = datetime.strptime(f"{match.group(1)}_{match.group(2)}", "%Y%m%d_%H%M%S")
            if ts >= cutoff:
                reports.append((ts, f))
    return reports


def build_summary(reports: list, days: int) -> str:
    """Build a simple weekly summary HTML page."""
    now = datetime.now()
    start = now - timedelta(days=days)

    rows = ""
    for ts, path in reports:
        rel = os.path.relpath(path, REPORTS_DIR)
        rows += f"<tr><td>{ts.strftime('%Y-%m-%d %H:%M')}</td><td><a href='{rel}'>{path.name}</a></td></tr>\n"

    if not rows:
        rows = "<tr><td colspan='2'>No reports found for this period.</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weekly Summary — {start.strftime('%b %d')} to {now.strftime('%b %d, %Y')}</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8 font-sans">
<div class="max-w-3xl mx-auto">
  <h1 class="text-2xl font-bold mb-2">Weekly Summary</h1>
  <p class="text-gray-600 mb-6">{start.strftime('%B %d')} — {now.strftime('%B %d, %Y')} ({len(reports)} reports)</p>
  <table class="w-full bg-white shadow rounded overflow-hidden">
    <thead class="bg-blue-600 text-white">
      <tr><th class="p-3 text-left">Date</th><th class="p-3 text-left">Report</th></tr>
    </thead>
    <tbody class="divide-y">
      {rows}
    </tbody>
  </table>
  <p class="mt-4 text-sm text-gray-400">Generated {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Build a weekly summary of reports")
    parser.add_argument("--days", type=int, default=7, help="Number of days to include")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    reports = collect_reports(args.output, args.days)
    html = build_summary(reports, args.days)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = args.output / f"weekly_summary_{ts}.html"
    args.output.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Weekly summary saved to {out_path}")


if __name__ == "__main__":
    main()
