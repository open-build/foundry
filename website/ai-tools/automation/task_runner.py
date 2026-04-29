#!/usr/bin/env python3
"""
Task Runner — AI Tools
=======================

Thin wrapper for running project scripts with structured logging and
optional timestamped output capture. Useful for cron-style automation.

Usage:
    python3 ai-tools/automation/task_runner.py scripts/generate_dashboard.py
    python3 ai-tools/automation/task_runner.py scripts/analytics_reporter.py --log-dir logs/
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = PROJECT_ROOT / "logs"


def run_task(script: str, log_dir: Path, extra_args: list) -> int:
    """Execute a script and capture output to a log file."""
    script_path = PROJECT_ROOT / script
    if not script_path.exists():
        print(f"Error: {script_path} does not exist", file=sys.stderr)
        return 1

    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = script_path.stem
    log_file = log_dir / f"{stem}_{ts}.log"

    cmd = [sys.executable, str(script_path)] + extra_args
    print(f"[{datetime.now().isoformat()}] Running: {' '.join(cmd)}")
    print(f"  Log: {log_file}")

    with open(log_file, "w") as lf:
        lf.write(f"# Task: {script}\n")
        lf.write(f"# Started: {datetime.now().isoformat()}\n")
        lf.write(f"# Command: {' '.join(cmd)}\n\n")

        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            stdout=lf,
            stderr=subprocess.STDOUT,
        )

        lf.write(f"\n# Exit code: {result.returncode}\n")
        lf.write(f"# Finished: {datetime.now().isoformat()}\n")

    status = "OK" if result.returncode == 0 else "FAIL"
    print(f"  [{status}] exit code {result.returncode}")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run a project script with logging"
    )
    parser.add_argument("script", help="Relative path to the script (from project root)")
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=DEFAULT_LOG_DIR,
        help="Directory for log files",
    )
    args, extra = parser.parse_known_args()
    sys.exit(run_task(args.script, args.log_dir, extra))


if __name__ == "__main__":
    main()
