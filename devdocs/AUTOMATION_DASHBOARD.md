# Automation Dashboard Documentation
**Buildly Labs Foundry - Local HTML Dashboard**

## Overview

The automation dashboard provides a comprehensive view of your foundry's outreach automation system, including real-time metrics, configuration status, error logs, and actionable recommendations.

## Features

### 📊 Real-Time Metrics
- **Automation Status**: Success/failure rates for last day, week, month
- **Outreach Performance**: Contact discovery, email sending, pending queue
- **Contact Database**: Total contacts, sources, recent discoveries
- **Target Management**: Organization sources and categories

### ⚙️ Configuration Management
- **Environment Variables**: Shows configured vs missing `.env` variables
- **Required vs Optional**: Distinguishes critical configuration
- **Security**: Sensitive data (passwords, API keys) are masked
- **Validation**: Checks file permissions and system health

### 📋 System Diagnostics
- **Error Logs**: Recent automation errors with timestamps
- **Log File Access**: Direct links to detailed log files
- **System Health**: Directory/file permissions and accessibility
- **Performance**: Tracks automation execution times

### 💡 Recommendations Engine
- **Missing Configuration**: Identifies required environment variables
- **Performance Issues**: Highlights bottlenecks and failures
- **Queue Management**: Alerts for high pending message volumes
- **Maintenance**: Suggests cleanup and optimization tasks

## Usage

### Quick Start
```bash
# Generate and open dashboard
./view_dashboard.sh

# Manual generation
python3 scripts/generate_dashboard.py
```

### Dashboard Sections

#### 1. Overview Panel
- Quick stats and key metrics
- System health indicators
- Priority recommendations

#### 2. Outreach Details Tab
- Contact source breakdown
- Target category analysis
- Outreach timeline and volume
- Success/failure rates

#### 3. Environment Tab
- **Configured Variables**: Shows active configuration
- **Missing Variables**: Required setup items
- **Optional Variables**: Enhancement opportunities

#### 4. Error Logs Tab
- **Recent Errors**: Last 20 unique errors
- **Log Files**: Direct access to automation logs
- **Error Patterns**: Common issues and solutions

#### 5. System Health Tab
- **Directories**: Permission and access status
- **Key Files**: Configuration and script validation
- **Dependencies**: Required modules and services

## Configuration

### Required Environment Variables
```bash
# Email Configuration (Required)
SMTP_USERNAME=your_brevo_username
SMTP_PASSWORD=your_brevo_password
DAILY_NOTIFICATION_EMAIL=your_email@domain.com
DAILY_CC_EMAIL=cc_email@domain.com

# Website Monitoring (Required)
WEBSITE_URL=https://your-site.com

# Analytics (Optional but Recommended)
GOOGLE_ANALYTICS_PROPERTY_ID=your_ga_property_id
YOUTUBE_CHANNEL_ID=your_youtube_channel_id
YOUTUBE_API_KEY=your_youtube_api_key
```

### Auto-Refresh
- Dashboard auto-refreshes every 5 minutes
- Manual refresh: Re-run `generate_dashboard.py`
- Real-time data from live system files

## File Structure

```
foundry/
├── scripts/
│   ├── generate_dashboard.py    # Dashboard generator
│   ├── startup_outreach.py      # Main outreach automation
│   ├── analytics_reporter.py    # Analytics and reporting
│   └── daily_automation.py      # Master automation script
├── reports/
│   ├── daily/                   # Daily analytics reports
│   ├── automation/              # Automation dashboard files
│   └── archive/                 # Historical reports (30 days)
├── outreach_data/
│   ├── contacts.json           # Contact database
│   ├── targets.json            # Target organizations
│   ├── pending_outreach.json   # Pending messages
│   └── outreach_log.json       # Send history
└── logs/
    └── daily_automation_*.log   # Automation execution logs
```

## Troubleshooting

### Common Issues

1. **"No environment variables configured"**
   - Check `.env` file exists in root directory
   - Verify variable names match required format
   - Ensure no extra spaces or quotes

2. **"No automation logs found"**
   - Run `python3 scripts/daily_automation.py` once
   - Check `logs/` directory permissions
   - Verify logging configuration

3. **"Dashboard not opening"**
   - Use full file path: `file:///absolute/path/to/automation_dashboard.html`
   - Try different browser if needed
   - Check file permissions

4. **"Missing outreach data"**
   - Run discovery phase: `python3 scripts/startup_outreach.py --mode discover`
   - Check `outreach_data/` directory exists
   - Verify JSON file formats

### Performance Optimization

- **Log Rotation**: Logs older than 30 days are automatically archived
- **Data Cleanup**: Reports older than 1 month are moved to archive
- **Cache Management**: Dashboard generates fresh data each run
- **Memory Usage**: Large log files are truncated for display

## API Reference

### Dashboard Generator Functions

```python
# Environment analysis
load_env_variables() -> Dict[str, Any]

# Log analysis  
analyze_automation_logs() -> Dict[str, Any]

# Outreach metrics
analyze_outreach_data() -> Dict[str, Any]

# System health
get_system_health() -> Dict[str, Any]

# Recommendations
get_recommendations() -> List[Dict[str, str]]
```

### Data Sources

- **Logs**: `logs/daily_automation_*.log`
- **Contacts**: `outreach_data/contacts.json`
- **Outreach**: `outreach_data/outreach_log.json`
- **Environment**: `.env` file
- **Configuration**: `config.py`

## Security Considerations

- **Sensitive Data**: API keys and passwords are masked in display
- **Local Only**: Dashboard runs entirely offline, no external calls
- **File Access**: Read-only access to log and data files
- **Permissions**: Validates but doesn't modify system permissions

## Integration

The dashboard integrates with:
- **Daily Automation**: `scripts/daily_automation.py`
- **Outreach System**: `scripts/startup_outreach.py`
- **Analytics**: `scripts/analytics_reporter.py`
- **Configuration**: `.env` and `config.py`

For advanced customization, modify `scripts/generate_dashboard.py` with additional metrics or visualizations.