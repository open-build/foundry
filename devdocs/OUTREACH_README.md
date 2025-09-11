# Startup Outreach Automation System

Automated PR and outreach tool for Buildly Labs Foundry to connect with startup-focused publications, influencers, platforms, and communities worldwide.

## 🎯 Features

- **Automated Discovery**: Finds new startup publications, influencers, and platforms
- **Smart Contact Extraction**: Scrapes contact information from target websites  
- **Personalized Messaging**: AI-powered message generation based on target type
- **Rate Limiting**: Respectful crawling with configurable delays
- **Duplicate Prevention**: Tracks all contacts and prevents spam
- **Analytics & Reporting**: Comprehensive metrics and performance tracking
- **Multi-Channel Outreach**: Email, social media, and platform messaging
- **Template System**: Category-specific message templates

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements_outreach.txt

# Set up configuration
cp config_template.py config.py
# Edit config.py with your email settings
```

### 2. Basic Usage

```bash
# Discover new contacts and targets
python3 scripts/startup_outreach.py --mode discover

# Send outreach messages  
python3 scripts/startup_outreach.py --mode outreach

# Generate analytics report
python3 scripts/startup_outreach.py --mode report

# Run full cycle (discover + outreach + report)
python3 scripts/startup_outreach.py --mode full

# Test without sending emails
python3 scripts/startup_outreach.py --mode full --dry-run
```

## 📊 Target Categories

### Publications
- **Major Tech**: TechCrunch, VentureBeat, The Next Web
- **Startup-Focused**: First Round Review, AngelList, Startup Grind  
- **Developer**: Dev.to, GitHub Blog, Hacker News
- **AI/ML**: AI News, VentureBeat AI
- **International**: The Startup Magazine (UK), global publications

### Platforms & Communities  
- **Launch Platforms**: Product Hunt, Betalist
- **Developer Communities**: Indie Hackers, Dev.to, GitHub
- **Startup Communities**: AngelList, F6S, Startup Grind
- **Social Platforms**: Twitter, LinkedIn, Reddit

### Influencers & Thought Leaders
- **Startup Advisors**: VCs, accelerator partners, successful founders
- **Tech Journalists**: Startup beat reporters, freelance writers
- **Developer Advocates**: Company evangelists, open source maintainers
- **Solo Founder Champions**: Bootstrapping advocates, indie maker influencers

## 🎨 Message Templates

### Publication Template
Professional pitch focusing on newsworthiness, partnerships, and unique value proposition.

### Influencer Template  
Personal approach highlighting alignment with their content themes and audience interests.

### Platform Template
Partnership-focused message exploring collaboration opportunities.

### Community Template
Community-friendly introduction emphasizing value for members.

## 📈 Analytics & Metrics

- **Discovery Metrics**: New targets found, contacts extracted
- **Outreach Performance**: Messages sent, response rates, template effectiveness
- **Target Analysis**: Categories, geographical distribution, priority scores
- **Response Tracking**: Replies, inquiries, partnership opportunities

## ⚙️ Configuration

### Email Setup (Brevo SMTP) - SECURE
```bash
# Step 1: Run secure credential setup
python setup_credentials.py

# Step 2: Verify .env file is created (and gitignored)
ls -la .env

# Your .env file will contain:
# BREVO_SMTP_USERNAME=your-username@smtp-brevo.com
# BREVO_SMTP_PASSWORD=your-master-password
# FROM_EMAIL=team@open.build
```

### Alternative: Gmail Setup
```bash
# Set environment variables
export BREVO_SMTP_USERNAME="your-gmail@gmail.com"
export BREVO_SMTP_PASSWORD="your-app-password"
export FROM_EMAIL="team@open.build"
```

### Rate Limiting
```python
RATE_LIMITS = {
    'min_delay': 30,  # Seconds between requests
    'max_delay': 60,
    'max_daily_outreach': 50,  # Daily email limit
    'max_per_organization': 4  # Max contacts per target
}
```

## 🔒 Security & Privacy

### Credential Security
- **Environment Variables**: All sensitive data stored in .env (never committed)
- **Secure Setup**: Use `python setup_credentials.py` for safe credential entry
- **Hidden Input**: Passwords entered with masked input (getpass)
- **Git Exclusion**: .env files automatically excluded from version control

### Data Privacy
- **Local Storage**: All contact data stored locally and gitignored
- **No Cloud Storage**: Contact information never sent to third-party services
- **Opt-out Compliance**: Automatic unsubscribe handling
- **GDPR Ready**: Easy data deletion and export capabilities

### Operational Security
- **Respect Rate Limits**: Built-in delays prevent server overload
- **Duplicate Prevention**: Never contacts the same person twice within 30 days
- **Professional Messaging**: Templates maintain professional tone and clear value proposition
- **Audit Trail**: Complete logging of all outreach activities

## 📁 Data Structure

```
outreach_data/
├── contacts.json         # All discovered contacts
├── targets.json          # Outreach targets and metadata  
├── outreach_log.json     # Complete outreach history
└── analytics.json        # Performance metrics
```

## 🛠 Advanced Features

### AI-Powered Personalization
```bash
# Enable in config.py
ADVANCED_CONFIG = {
    'use_ai_personalization': True,
    'openai_api_key': 'your-key'
}
```

### Search API Integration
```bash
# Google Custom Search for target discovery
SEARCH_CONFIG = {
    'google_api_key': 'your-key',
    'google_cse_id': 'your-cse-id',
    'use_search_apis': True
}
```

### Social Media Integration
```bash
# Twitter and LinkedIn outreach
ADVANCED_CONFIG = {
    'social_media_integration': True
}
```

## 📅 Scheduled Automation

### Cron Job Setup (Linux/Mac)
```bash
# Run discovery daily at 9 AM
0 9 * * * cd /path/to/foundry && python3 scripts/startup_outreach.py --mode discover

# Run outreach Mon/Wed/Fri at 10 AM  
0 10 * * 1,3,5 cd /path/to/foundry && python3 scripts/startup_outreach.py --mode outreach

# Generate weekly reports on Sundays
0 18 * * 0 cd /path/to/foundry && python3 scripts/startup_outreach.py --mode report
```

### GitHub Actions (Alternative)
```yaml
name: Startup Outreach
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
jobs:
  outreach:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Outreach
        run: python3 scripts/startup_outreach.py --mode discover
```

## 🎯 Target Outreach Strategy

### Phase 1: Foundation (Weeks 1-2)
- Major publications (TechCrunch, Product Hunt)
- Key developer communities (Hacker News, Dev.to)
- Startup platforms (AngelList, Indie Hackers)

### Phase 2: Expansion (Weeks 3-4)  
- Niche publications and newsletters
- International startup media
- AI/ML focused publications

### Phase 3: Influencer Network (Weeks 5-6)
- Startup advisors and VCs
- Tech journalists and writers  
- Developer advocates

### Phase 4: Long-tail (Ongoing)
- Local startup communities
- University entrepreneurship programs
- Industry-specific publications

## 📞 Support & Contact

- **Questions**: team@open.build
- **Issues**: Create GitHub issue
- **Feature Requests**: team@open.build with subject "Outreach Feature Request"

## 🚨 Important Notes

1. **Test First**: Always run with `--dry-run` initially
2. **Monitor Responses**: Check team@open.build regularly for replies
3. **Update Templates**: Customize messages for your brand voice
4. **Respect Limits**: Don't exceed rate limits or daily quotas
5. **Track Performance**: Review analytics weekly for optimization

## 🔄 Maintenance

- **Weekly**: Review analytics, update templates
- **Monthly**: Clean contact list, add new targets  
- **Quarterly**: Major template updates, strategy review
