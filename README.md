# Buildly Labs Foundry

A modern static website for the Buildly Labs Foundry program, helping startups accelerate their journey with equity-free assistance, partner connections, and expert guidance.

## 🌟 Features

- **Modern Design**: Built with Tailwind CSS for a professional, responsive experience
- **Multi-Step Application**: Comprehensive startup application form with validation
- **AI Integration**: BabbleBeaver AI analysis for startup ideas
- **Google Sheets**: Automatic form submission to Google Sheets
- **GitHub Pages**: Optimized for easy deployment and hosting

## 🚀 Live Site

- **Production**: https://www.firstcityfoundry.com
- **GitHub Pages**: https://open-build.github.io/foundry

## 📁 Site Structure

- **Homepage** (`index.html`): Hero section, benefits, partner showcase
- **Application Form** (`register.html`): Multi-step startup application
- **Success Page** (`success.html`): Post-submission confirmation
- **Assets** (`assets/`): CSS, JavaScript, and images

## 🔧 Quick Start

The static site files are in the root directory and ready for GitHub Pages deployment.

### GitHub Pages Setup
- Go to Repository Settings → Pages
- Set source to "Deploy from a branch"
- Select "main" branch and "/ (root)" folder

### Custom Domain
- The `CNAME` file is configured for `foundry.buildly.io`
- Configure DNS: `CNAME foundry -> open-build.github.io`

### Integrations
- Set up Google Sheets integration (see site-README.md)
- Configure BabbleBeaver API endpoint

## 📖 Documentation

Complete setup and customization documentation is available in `site-README.md`.

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
