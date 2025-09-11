# Development Context & Prompts

This folder contains prompts and context files to help developers and AI assistants understand the current state and development workflow of the Buildly Labs Foundry project.

## 📋 Quick Context

### Project Status: ✅ FULLY OPERATIONAL
- **Launch Date**: September 10, 2025
- **Outreach Campaign**: 27 messages sent successfully
- **Analytics System**: Daily reporting active
- **Website**: Live at https://www.firstcityfoundry.com

### Current Architecture
- **Frontend**: Static HTML/Tailwind CSS site deployed via GitHub Pages
- **Backend**: Python automation scripts for outreach and analytics
- **Email Service**: Brevo SMTP for campaign delivery
- **Data Storage**: JSON files for contacts and analytics
- **Deployment**: Automated via GitHub Actions

## 🎯 Development Workflow Prompts

### For New Feature Development
```
"I'm working on the Buildly Labs Foundry project. It's a global startup incubator website with an automated outreach system. The project structure is:
- `/devdocs/` - All markdown documentation
- `/scripts/` - Python automation scripts
- Website files in root (HTML/CSS/JS)
- Deployed via GitHub Pages

Current status: Fully operational with 27 outreach messages sent to startup publications like TechCrunch, AI News, StartupGrind, and Entrepreneur.com.

Please help me with [specific feature/issue]."
```

### For Documentation Updates
```
"I need to update documentation for the Buildly Labs Foundry project. Key context:
- Documentation is in `/devdocs/` folder
- Scripts documentation in `/scripts/README.md`
- Project is a global equity-free startup incubator
- Features automated outreach to startup publications
- Uses Brevo SMTP, daily analytics reports, BCC monitoring

Please help me document [specific aspect]."
```

### For Script Modifications
```
"I'm modifying automation scripts for Buildly Labs Foundry. Current setup:
- Main script: `scripts/startup_outreach.py` (1312 lines)
- Analytics: `scripts/analytics_reporter.py`
- Configuration: `config.py` and `.env` files
- Uses Brevo SMTP for email delivery
- Targets startup publications and communities
- Has rate limiting, BCC functionality, and comprehensive logging

I need help with [specific script modification]."
```

### For Website Updates
```
"I'm updating the Buildly Labs Foundry website. Current details:
- Static site: HTML5 + Tailwind CSS + JavaScript
- Global startup incubator focus (removed Oregon City references)
- Emphasizes OpenBuild partnership and Buildly Labs collaboration
- 100% equity-free model for solo founders and developers
- Deployed via GitHub Pages with custom domain
- SEO optimized with structured data

Please help me update [specific website aspect]."
```

## 📊 Key Metrics & Status

### Outreach Campaign Results
- **Messages Sent**: 27 successful deliveries
- **Target Organizations**: TechCrunch, AI News, StartupGrind, Entrepreneur.com
- **Response Rate**: Tracking in progress
- **BCC Monitoring**: All messages copied to team@open.build

### Website Performance
- **Domain**: https://www.firstcityfoundry.com
- **Hosting**: GitHub Pages
- **Analytics**: Daily HTML reports via email
- **Mobile Responsive**: Yes
- **SEO Optimized**: Yes

### Technical Infrastructure
- **Email Service**: Brevo SMTP (fully configured)
- **Rate Limiting**: 30-60 second delays between messages
- **Data Storage**: JSON files in `outreach_data/` directory
- **Security**: Environment variables for credentials
- **Monitoring**: Comprehensive logging and error tracking

## 🔄 Recent Changes & Evolution

### Migration History
1. **Django to Static Site**: Converted from Django webapp to GitHub Pages compatible HTML/CSS/JS
2. **Local to Global**: Removed Oregon City focus, emphasizing global reach
3. **Manual to Automated**: Built comprehensive outreach automation system
4. **Basic to Advanced**: Added analytics, BCC monitoring, rate limiting
5. **Development to Production**: Successfully deployed and operational

### File Organization (Completed)
- **Documentation**: Moved to `/devdocs/` folder
- **Scripts**: Organized in `/scripts/` folder  
- **Configuration**: Centralized in root directory
- **Data**: Structured in `outreach_data/` directory

## 🛠️ Development Guidelines

### Code Style
- **Python**: PEP 8 compliant, comprehensive docstrings
- **HTML/CSS**: Semantic markup, Tailwind CSS classes
- **JavaScript**: Vanilla JS, progressive enhancement
- **Documentation**: Markdown with clear structure

### Commit Messages
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Examples**: 
  - `feat(outreach): add BCC functionality to email campaigns`
  - `docs(devdocs): organize documentation structure`
  - `fix(analytics): correct daily report email formatting`

### Testing Approach
- **Dry Run Mode**: All scripts support `--dry-run` flag
- **Environment Separation**: `.env` for development, production configs
- **Monitoring**: BCC copies and comprehensive logging
- **Error Handling**: Graceful degradation and retry logic

---

Use these prompts and context when working with AI assistants or onboarding new developers to quickly understand the project state and architecture.
