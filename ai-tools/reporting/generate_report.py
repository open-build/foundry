#!/usr/bin/env python3
"""
Report Generator — AI Tools
============================

Generates an HTML analytics report from existing dashboard and outreach data.
Wraps the existing scripts/generate_dashboard.py with a simpler CLI and
adds timestamped output to reports/automation/.

Usage:
    python3 ai-tools/reporting/generate_report.py
    python3 ai-tools/reporting/generate_report.py --output /tmp/reports
"""

import argparse
import importlib.util
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "automation"


def _import_script(name: str, path: Path):
    """Import a Python module by file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def generate(output_dir: Path) -> Path:
    """Run the dashboard generator and return the path to the report."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Change to project root so relative paths in the scripts work
    prev_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)

    try:
        dashboard_script = SCRIPTS_DIR / "generate_dashboard.py"
        if not dashboard_script.exists():
            print(f"Error: {dashboard_script} not found", file=sys.stderr)
            sys.exit(1)

        mod = _import_script("generate_dashboard", dashboard_script)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"dashboard_{timestamp}.html"
        report_path = output_dir / report_name

        # The generate_dashboard module exposes generate_dashboard_html()
        if hasattr(mod, "generate_dashboard_html"):
            html = mod.generate_dashboard_html()
            report_path.write_text(html, encoding="utf-8")
        elif hasattr(mod, "main"):
            mod.main()
            # If main() writes its own file, create a symlink
            latest = sorted(output_dir.glob("dashboard_*.html"))
            if latest:
                report_path = latest[-1]
        else:
            print("Warning: generate_dashboard.py has no known entrypoint, "
                  "running as __main__", file=sys.stderr)
            exec(dashboard_script.read_text(), {"__name__": "__main__"})
            latest = sorted(output_dir.glob("dashboard_*.html"))
            if latest:
                report_path = latest[-1]

        # Update the convenience symlink
        latest_link = output_dir / "dashboard.html"
        if latest_link.is_symlink() or latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(report_path.name)

        return report_path
    finally:
        os.chdir(prev_cwd)


def main():
    parser = argparse.ArgumentParser(description="Generate an analytics report")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory to write the report to",
    )
    args = parser.parse_args()

    print(f"Generating report...")
    path = generate(args.output)
    print(f"Report saved to {path}")


if __name__ == "__main__":
    main()
