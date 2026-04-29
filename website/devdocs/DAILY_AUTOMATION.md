# Daily Automation System Documentation
**Buildly Labs Foundry - Master Automation Orchestrator**

## Overview

The daily automation system (`scripts/daily_automation.py`) is the master orchestrator that runs the complete outreach pipeline in the proper sequence with comprehensive error handling, logging, and status reporting.

## Architecture

### Execution Flow
```
1. Discovery Phase  → Find new contacts and sources
2. Outreach Phase   → Process and send email campaigns  
3. Analytics Phase  → Collect performance data
4. Notification     → Send daily summary email
5. Completion       → Final status and cleanup
```

### Phase Dependencies
- **Outreach** depends on **Discovery** (new contacts)
- **Analytics** depends on **Outreach** (latest metrics)
- **Notification** depends on **All Phases** (complete data)

## Usage

### Command Line Options

```bash
# Full daily automation (recommended)
python3 scripts/daily_automation.py

# Individual phases
python3 scripts/daily_automation.py --discovery-only
python3 scripts/daily_automation.py --outreach-only
python3 scripts/daily_automation.py --analytics-only

# Testing and development
python3 scripts/daily_automation.py --dry-run
python3 scripts/daily_automation.py --interactive
```

### Cron Integration

The system is designed for daily automation via cron:

```bash
# Install cron job (runs daily at 9:00 AM)
crontab cron_foundry.txt

# Check cron status
crontab -l

# View cron logs
grep CRON /var/log/syslog
```

## Phase Details

### 1. Discovery Phase
**Purpose**: Find new startup sources and contacts

**Actions**:
- Scrapes configured target websites
- Discovers new publications and platforms
- Extracts contact information
- Updates `outreach_data/targets.json`
- Adds contacts to `outreach_data/contacts.json`

**Success Criteria**:
- No critical scraping errors
- New contacts discovered (optional)
- Target list updated

**Error Handling**:
- Individual site failures don't stop process
- Rate limiting prevents IP blocking
- Retries for temporary failures

### 2. Outreach Phase
**Purpose**: Send personalized outreach emails

**Actions**:
- Loads pending outreach queue
- Filters for eligible contacts (not recently contacted)
- Generates personalized messages
- Sends emails via Brevo SMTP
- Updates contact status and logs

**Success Criteria**:
- Messages sent successfully
- No SMTP errors
- Contact database updated

**Error Handling**:
- Individual email failures logged
- SMTP connection retries
- Rate limiting prevents spam flagging
- Automatic opt-out handling

### 3. Analytics Phase
**Purpose**: Collect performance metrics and generate reports

**Actions**:
- Analyzes outreach performance
- Collects website traffic data (if configured)
- Gathers YouTube analytics (if configured)
- Generates daily report data
- Saves metrics to `reports/daily/`

**Success Criteria**:
- Analytics data collected
- Report generated successfully
- Historical data updated

**Error Handling**:
- Graceful fallback for missing APIs
- Mock data for unconfigured services
- Report generation continues with available data

### 4. Notification Phase
**Purpose**: Send daily summary email with complete metrics

**Actions**:
- Compiles data from all phases
- Formats comprehensive HTML report
- Sends to configured recipients
- Includes CC to secondary email

**Success Criteria**:
- Email sent successfully
- Contains real data from day's activities
- Delivered to all recipients

**Error Handling**:
- Email sending retries
- Fallback to basic text format
- Logs delivery status

## Configuration

### Environment Variables
```bash
# Required for full automation
SMTP_USERNAME=your_brevo_username
SMTP_PASSWORD=your_brevo_password
DAILY_NOTIFICATION_EMAIL=primary@domain.com
DAILY_CC_EMAIL=secondary@domain.com

# Optional but recommended
GOOGLE_ANALYTICS_PROPERTY_ID=GA_property_id
YOUTUBE_CHANNEL_ID=your_channel_id
WEBSITE_URL=https://your-site.com

# Rate limiting and safety
MAX_DAILY_OUTREACH=50
MAX_PER_ORGANIZATION=4
MIN_DELAY_SECONDS=30
```

### Dependencies
- Python 3.8+
- Required modules: `requests`, `beautifulsoup4`, `jinja2`, `rich`
- Optional: `google-analytics-data`, `yagmail`
- Email service: Brevo SMTP access

## Logging and Monitoring

### Log Files
```
logs/
├── daily_automation_YYYYMMDD_HHMMSS.log
├── daily_automation_YYYYMMDD_HHMMSS.log
└── ... (30 days retained)
```

### Log Levels
- **INFO**: Normal operation progress
- **WARNING**: Non-critical issues (missing optional config)
- **ERROR**: Phase failures, retryable errors
- **CRITICAL**: System failures, unrecoverable errors

### Monitoring Points
1. **Phase Success/Failure**: Each phase reports completion status
2. **Contact Discovery**: Number of new contacts found
3. **Email Delivery**: Success rates and failures
4. **System Health**: File permissions, dependencies

## Error Handling Strategy

### Graceful Degradation
- Missing optional configuration doesn't stop automation
- Individual contact failures don't abort batch
- API failures fall back to mock data
- Email delivery issues are logged but don't fail automation

### Retry Logic
- Network requests: 3 retries with exponential backoff
- Email sending: 2 retries with delay
- File operations: Immediate retry once

### Failure Recovery
- Each phase is independent
- Failed phases don't prevent subsequent phases
- Partial success is acceptable and reported
- Manual recovery tools available

## Performance Optimization

### Rate Limiting
- Email sending: 30-60 second delays between messages
- Web scraping: Respects robots.txt and implements delays
- API calls: Batched where possible

### Resource Management
- Log rotation: 30-day retention
- Memory usage: Processes data in chunks
- Disk space: Automatic cleanup of old reports

### Scalability
- Configurable batch sizes
- Parallel processing where safe
- Database-ready architecture (currently JSON)

## Security Considerations

### Data Protection
- Email addresses encrypted in logs
- API keys masked in output
- Opt-out list maintained and respected
- GDPR compliance features

### Access Control
- Scripts require local file system access
- No remote execution capabilities
- Logging doesn't expose sensitive data
- Configuration validation

## Troubleshooting

### Common Issues

1. **"Phase failed with network error"**
   - Check internet connectivity
   - Verify API keys and credentials
   - Review rate limiting settings

2. **"SMTP authentication failed"**
   - Verify Brevo credentials in `.env`
   - Check SMTP server settings
   - Ensure account has sending permissions

3. **"No new contacts discovered"**
   - Check target website availability
   - Review scraping logic for site changes
   - Verify target list is not exhausted

4. **"Analytics data missing"**
   - Configure Google Analytics API
   - Set up YouTube Data API
   - Check API quotas and limits

### Recovery Procedures

1. **Restart Failed Automation**:
   ```bash
   python3 scripts/daily_automation.py --analytics-only
   ```

2. **Manual Phase Execution**:
   ```bash
   python3 scripts/startup_outreach.py --mode discover
   python3 scripts/startup_outreach.py --mode outreach
   ```

3. **Data Validation**:
   ```bash
   python3 scripts/generate_dashboard.py
   # Check reports/automation/dashboard.html
   ```

## Integration Points

### External Services
- **Brevo SMTP**: Email delivery
- **Google Analytics**: Website metrics
- **YouTube API**: Video analytics
- **Target Websites**: Contact discovery

### Internal Components
- **Outreach Engine**: `scripts/startup_outreach.py`
- **Analytics Reporter**: `scripts/analytics_reporter.py`
- **Dashboard Generator**: `scripts/generate_dashboard.py`
- **Configuration**: `config.py` and `.env`

### Data Flow
```
Targets → Discovery → Contacts → Outreach → Logs → Analytics → Reports
```

## Future Enhancements

### Planned Features
- Database backend (PostgreSQL/MySQL)
- Advanced analytics and ML insights
- Multi-channel outreach (LinkedIn, Twitter)
- A/B testing for email templates
- API endpoint for external integrations

### Scalability Improvements
- Distributed processing
- Cloud deployment options
- Real-time monitoring dashboard
- Advanced error recovery
- Performance optimization

For implementation details, see the source code in `scripts/daily_automation.py`.