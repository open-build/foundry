# Buildly Labs Foundry - File Organization
**Clean, organized codebase with proper documentation and 30-day retention**

## 📁 Directory Structure

```
foundry/
├── 📄 run_automation.py          # Main automation launcher
├── 📄 view_dashboard.sh          # Dashboard quick launcher  
├── 📄 automation_dashboard.html  # Latest dashboard (auto-generated)
├── 📄 config.py                  # Configuration settings
├── 📄 .env                       # Environment variables
├── 📄 cron_foundry.txt          # Cron job configuration
├── 📄 requirements.txt          # Python dependencies
│
├── 📂 scripts/                   # All Python automation scripts
│   ├── daily_automation.py      # Master automation orchestrator
│   ├── startup_outreach.py      # Outreach engine and contact management
│   ├── analytics_reporter.py    # Analytics collection and reporting
│   └── generate_dashboard.py    # Local HTML dashboard generator
│
├── 📂 devdocs/                   # Technical documentation
│   ├── AUTOMATION_DASHBOARD.md  # Dashboard usage and features
│   ├── DAILY_AUTOMATION.md      # Automation system documentation
│   ├── OUTREACH_README.md       # Outreach engine details
│   ├── GOOGLE_APPS_SCRIPT_SETUP.md
│   ├── NEW_SOURCES_DISCOVERY.md
│   └── REPOSITORY_ORGANIZATION.md
│
├── 📂 reports/                   # Generated reports (30-day retention)
│   ├── daily/                   # Daily analytics reports
│   │   └── analytics_YYYYMMDD_HHMMSS.json
│   └── automation/              # Dashboard snapshots
│       └── dashboard_YYYYMMDD_HHMMSS.html
│
├── 📂 outreach_data/            # Contact and outreach databases
│   ├── contacts.json           # Contact database
│   ├── targets.json            # Target organizations
│   ├── pending_outreach.json   # Pending messages
│   ├── outreach_log.json       # Send history
│   ├── opt_outs.json           # Opt-out list
│   └── daily_reports.json      # Legacy analytics (backward compatibility)
│
├── 📂 logs/                     # Automation logs (30-day retention)
│   └── daily_automation_YYYYMMDD_HHMMSS.log
│
└── 📂 docs/                     # Static website files
    └── (existing website content)
```

## 🚀 Quick Start

### Run Daily Automation
```bash
# Full automation (discovery + outreach + analytics)
python3 run_automation.py

# Individual phases
python3 scripts/daily_automation.py --discovery-only
python3 scripts/daily_automation.py --outreach-only
python3 scripts/daily_automation.py --analytics-only
```

### View Dashboard
```bash
# Generate and open dashboard
./view_dashboard.sh

# Manual generation
python3 scripts/generate_dashboard.py
```

### Cron Setup
```bash
# Install daily automation
crontab cron_foundry.txt

# Check status
crontab -l
```

## 📋 File Management

### Automatic Cleanup (30-day retention)
- **Logs**: `logs/*.log` files older than 30 days
- **Reports**: `reports/**/*.{html,json}` files older than 30 days
- **Archives**: Old files are deleted, not moved

### Manual Cleanup
```bash
# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete

# Clean old reports  
find reports/ -name "*.html" -mtime +30 -delete
find reports/ -name "*.json" -mtime +30 -delete
```

## 🔧 Configuration

### Environment Setup
1. Copy `.env.example` to `.env`
2. Configure required variables:
   ```bash
   SMTP_USERNAME=your_brevo_username
   SMTP_PASSWORD=your_brevo_password
   DAILY_NOTIFICATION_EMAIL=your_email@domain.com
   ```

### Documentation Access
- **Dashboard Help**: `devdocs/AUTOMATION_DASHBOARD.md`
- **Automation Guide**: `devdocs/DAILY_AUTOMATION.md`
- **Outreach Details**: `devdocs/OUTREACH_README.md`

## 📊 Monitoring

### Dashboard Features
- Real-time automation metrics
- Environment configuration status
- Error logs and system health
- 30-day performance trends

### Log Analysis
- Structured logging with timestamps
- Error categorization and tracking
- Performance metrics collection
- Automated cleanup and archival

## 🔄 Maintenance

### Weekly Tasks
- Review dashboard recommendations
- Check error logs for patterns
- Validate environment configuration

### Monthly Tasks  
- Archive old reports (automatic)
- Review target organization list
- Update documentation as needed

## 🆘 Troubleshooting

### Common Issues
1. **Script not found**: Use `scripts/` prefix for all automation scripts
2. **Dashboard not opening**: Check `automation_dashboard.html` exists
3. **Automation failing**: Review logs in `logs/` directory
4. **Missing config**: Check `.env` file and dashboard recommendations

### Support Files
- **Error Logs**: `logs/daily_automation_*.log`
- **System Status**: `automation_dashboard.html`
- **Configuration**: `.env` and `config.py`
- **Documentation**: `devdocs/*.md`

This organization provides clean separation of concerns, automatic cleanup, and comprehensive documentation for long-term maintainability.