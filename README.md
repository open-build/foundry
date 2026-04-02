# Buildly Labs Foundry

**Status**: ✅ FULLY OPERATIONAL | **Launch Date**: September 10, 2025

A global startup incubator website with automated outreach capabilities, targeting startup publications and communities worldwide.

## 🌟 Current Features

- **Live Website**: https://www.firstcityfoundry.com (GitHub Pages deployment)
- **Automated Outreach**: 27 messages sent to major startup publications
- **Daily Analytics**: HTML reports with website traffic and campaign metrics
- **BCC Monitoring**: All outreach messages copied to team@open.build
- **Rate Limited**: Ethical outreach with 30-60 second delays

## 🎯 Active Campaigns

- **TechCrunch**: 2 contacts (tips & events teams)
- **AI News**: 3 contacts (editorial team)
- **StartupGrind**: 1 contact (community management)
- **Entrepreneur.com**: 4 contacts (business development, franchise, events)

## 📁 Project Structure

```
foundry/
├── docs/                  # 🌐 Static website (deployed to GitHub Pages)
├── ForgeWeb/              # 🛠️ Content management admin (git submodule, local only)
├── ai-tools/              # 🤖 AI-powered reporting & automation
│   ├── reporting/         #    Report generation scripts
│   ├── automation/        #    Task runner & scheduling
│   └── openclaw/          #    OpenClaw cron jobs & skill definitions
├── scripts/               # 🐍 Outreach & analytics scripts
├── devdocs/               # 📚 Development documentation
├── reports/               # 📊 Generated reports
└── .github/prompts/       # 💡 AI assistant context
```

## 🚀 Quick Start

### Website Development
```bash
# Serve the site locally
npm run serve            # http://localhost:3000

# Or use ForgeWeb admin interface
npm run forgeweb         # http://localhost:8000/admin/
```

### Content Management (ForgeWeb)
ForgeWeb is included as a git submodule and provides a local admin UI for
editing the site in `docs/`. After cloning, initialise the submodule:
```bash
git submodule update --init --recursive
cd ForgeWeb && ./ops/startup.sh start
# Open http://localhost:8000/admin/
```

### For Outreach Automation
```bash
# Install dependencies
pip3 install -r requirements_outreach.txt

# Run outreach campaign
python3 scripts/startup_outreach.py --mode outreach

# Generate analytics report
python3 scripts/startup_outreach.py --mode analytics
```

### AI Tools & Reporting
```bash
# Generate a dashboard report
npm run report

# Build a weekly summary
npm run report:weekly

# Or directly
python3 ai-tools/reporting/generate_report.py
python3 ai-tools/reporting/weekly_summary.py
```

### OpenClaw Local Automation
OpenClaw is installed locally and can schedule recurring tasks:
```bash
# Register cron jobs
openclaw cron add --file ai-tools/openclaw/cron-jobs.json

# List jobs
openclaw cron list

# Run a job now (debug)
openclaw cron run foundry-daily-report
```

## 📖 Documentation

- **[Development Docs](devdocs/README.md)** - Complete development guide
- **[Scripts Guide](scripts/README.md)** - Automation system documentation
- **[AI Tools](ai-tools/README.md)** - Reporting & automation tools
- **[Project Status](.github/prompts/project-status.md)** - Current operational status
- **[Development Context](.github/prompts/development-context.md)** - AI assistant prompts

## 🛠️ Local Development

```bash
# Install dependencies
npm install

# Serve locally
npm run serve

# Open in browser
open http://localhost:3000
```

## 🔗 Key Integrations

### Google Sheets
Forms automatically submit to Google Sheets for data collection and management.

### BabbleBeaver AI
Startup applications receive AI-powered analysis and feedback via BabbleBeaver API.

### GitHub Pages
Optimized for seamless deployment and hosting on GitHub Pages.

## 📱 Browser Support

- **Modern Browsers**: Chrome 60+, Firefox 60+, Safari 12+, Edge 79+
- **Mobile**: iOS Safari 12+, Chrome Mobile 60+
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `npm run serve`
5. Submit a pull request

## 📞 Support

- **Email**: foundry@buildly.io
- **Buildly Labs**: https://labs.buildly.io
- **BabbleBeaver**: https://babble.buildly.io
- **Buildly Platform**: https://www.buildly.io

## 📄 License

© 2025 Buildly Labs Foundry. All rights reserved.

---

**Join the Buildly Labs Foundry network and accelerate your startup journey today!**
