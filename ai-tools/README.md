# AI Tools

Automation and AI-powered tooling for the Buildly Labs Foundry project.

## Structure

```
ai-tools/
├── reporting/        # Automated report generation and analytics
│   ├── generate_report.py   # CLI for on-demand HTML reports
│   └── weekly_summary.py    # Weekly digest builder
├── automation/       # Task scheduling and workflow runners
│   └── task_runner.py       # Wrapper for running scripts with logging
├── openclaw/         # OpenClaw agent integration
│   ├── cron-jobs.json       # Cron job definitions for OpenClaw scheduler
│   └── skills.json          # Skill definitions for the OpenClaw agent
└── README.md
```

## Quick Start

### Generate an analytics report
```bash
python3 ai-tools/reporting/generate_report.py --output reports/automation/
```

### Run the weekly summary
```bash
python3 ai-tools/reporting/weekly_summary.py
```

### Manage via OpenClaw
```bash
# Register cron jobs with OpenClaw gateway
openclaw cron add --file ai-tools/openclaw/cron-jobs.json

# List registered jobs
openclaw cron list

# Run a job immediately (debug)
openclaw cron run <job-id>
```

## OpenClaw Integration

OpenClaw (`openclaw`) provides local agent automation, cron scheduling, and
message delivery. The definitions in `openclaw/` configure daily and weekly
automation tasks that run through the OpenClaw gateway.

See `openclaw/cron-jobs.json` for the schedule and `openclaw/skills.json` for
the agent skill definitions used when running reports via the agent.
