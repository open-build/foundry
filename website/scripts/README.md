# Buildly Labs Foundry - Scripts Documentation

This folder contains all automation scripts and utilities for the Buildly Labs Foundry project.

## 📁 Script Inventory

### 🚀 Core Outreach System
- **[startup_outreach.py](startup_outreach.py)** - Main outreach automation engine
  - Contact discovery and web scraping
  - Email campaign management with rate limiting
  - Interactive CLI for message review and approval
  - Comprehensive logging and analytics tracking

### 📊 Analytics & Reporting
- **[analytics_reporter.py](analytics_reporter.py)** - Daily analytics and reporting system
  - Google Analytics integration (configurable)
  - YouTube performance metrics (configurable)
  - Website traffic analysis and reporting
  - HTML email report generation

### 🔍 Utilities & Tools
- **[preview_outreach.py](preview_outreach.py)** - Message preview and testing tool
- **[run_outreach.py](run_outreach.py)** - Quick outreach execution wrapper
- **[setup_credentials.py](setup_credentials.py)** - Credential configuration helper
- **[setup_outreach.py](setup_outreach.py)** - Initial system setup and configuration

### 🛠️ Deployment & Maintenance
- **[cleanup-deploy.sh](cleanup-deploy.sh)** - Deployment cleanup and optimization script

## 🎯 Usage Examples

### Running Outreach Campaign
```bash
# From the root directory
cd /Users/greglind/Projects/open-build/foundry

# Discover new contacts
python3 scripts/startup_outreach.py --mode discover

# Preview messages before sending
python3 scripts/preview_outreach.py

# Send outreach messages (interactive)
python3 scripts/startup_outreach.py --mode outreach

# Send all pending messages (non-interactive)
python3 scripts/startup_outreach.py --mode send

# Generate analytics report
python3 scripts/startup_outreach.py --mode report

# Send daily analytics email
python3 scripts/startup_outreach.py --mode analytics
```

### Daily Operations
```bash
# Full automated cycle
python3 scripts/startup_outreach.py --mode full --non-interactive

# Check system status
python3 scripts/startup_outreach.py --mode report

# Preview upcoming messages
python3 scripts/preview_outreach.py
```

## ⚙️ Configuration Requirements

### Environment Variables (`.env`)
```bash
# Brevo SMTP Configuration
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=your-smtp-user
BREVO_SMTP_PASSWORD=your-smtp-password

# Email Settings
FROM_EMAIL=team@open.build
FROM_NAME=Open Build Foundry Team
BCC_EMAIL=team@open.build
DAILY_NOTIFICATION_EMAIL=team@open.build

# Analytics (Optional)
GOOGLE_ANALYTICS_PROPERTY_ID=
YOUTUBE_CHANNEL_ID=
YOUTUBE_API_KEY=

# Rate Limiting
MAX_DAILY_OUTREACH=50
MAX_PER_ORGANIZATION=4
MIN_DELAY_SECONDS=30
MAX_DELAY_SECONDS=60
```

### Dependencies
```bash
pip3 install -r requirements_outreach.txt
```

## 📈 Data Management

### File Structure
```
outreach_data/
├── contacts.json          # Discovered contacts database
├── targets.json           # Target organizations list
├── outreach_log.json      # Sent message history
├── pending_outreach.json  # Messages awaiting approval
├── daily_reports.json     # Analytics history
└── analytics.json         # Campaign performance data
```

### Contact Data Schema
```json
{
  "name": "Contact Name",
  "email": "contact@example.com",
  "organization": "Organization Name",
  "role": "Title/Role",
  "category": "publication|community|influencer",
  "source": "discovery_url",
  "outreach_count": 0,
  "last_contact": "2025-09-10T12:00:00",
  "response_received": false
}
```

## 🔧 Automation Features

### Contact Discovery
- **Web Scraping**: Automated contact extraction from target websites
- **Duplicate Prevention**: Intelligent deduplication across sources
- **Quality Filtering**: Role-based contact validation
- **Source Tracking**: Maintain discovery audit trail

### Email Campaigns
- **Template System**: Personalized message generation
- **Rate Limiting**: Respectful sending delays (30-60 seconds)
- **BCC Monitoring**: All messages copied to monitoring address
- **Delivery Tracking**: Success/failure logging and retry logic

### Analytics & Reporting
- **Daily Reports**: Comprehensive HTML email reports
- **Traffic Analysis**: Website performance integration
- **Campaign Metrics**: Open rates, click tracking, response analysis
- **Trend Analysis**: Historical performance comparison

## 🛡️ Security & Compliance

### Data Protection
- **Environment Variables**: Sensitive credentials externalized
- **Local Storage**: JSON files for development simplicity
- **Audit Logging**: Comprehensive activity tracking
- **Rate Limiting**: Anti-spam protection

### Ethical Outreach
- **Respectful Delays**: 30-60 second intervals between messages
- **Volume Limits**: Maximum 50 messages per day
- **Organization Caps**: Maximum 4 contacts per organization
- **Opt-out Ready**: Framework for unsubscribe handling

## 🚨 Troubleshooting

### Common Issues
1. **SMTP Authentication Failures**
   - Verify Brevo credentials in `.env`
   - Check `config.py` for conflicting settings
   - Test connection with standalone SMTP test

2. **Import Errors**
   - Ensure all scripts are in `scripts/` directory
   - Run from project root directory
   - Check Python path configuration

3. **Missing Dependencies**
   - Install: `pip3 install -r requirements_outreach.txt`
   - Update: `pip3 install --upgrade -r requirements_outreach.txt`

### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH=/Users/greglind/Projects/open-build/foundry
python3 scripts/startup_outreach.py --mode discover --dry-run
```

---

For detailed implementation guides, see the `../devdocs/` folder.
