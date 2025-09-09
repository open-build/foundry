# Buildly Labs Foundry

A modern static website for the Buildly Labs Foundry program, helping startups accelerate their journey with equity-free assistance, partner connections, and expert guidance.

## 🌟 Features

- **Modern Design**: Built with Tailwind CSS for a professional, responsive experience
- **Multi-Step Application**: Comprehensive startup application form with validation
- **AI Integration**: BabbleBeaver AI analysis for startup ideas
- **Google Sheets**: Automatic form submission to Google Sheets
- **GitHub Pages**: Optimized for easy deployment and hosting

## 🚀 Live Site

- **Production**: https://foundry.buildly.io
- **GitHub Pages**: https://open-build.github.io/foundry

## 📁 Site Structure

- **Homepage** (`docs/index.html`): Hero section, benefits, partner showcase
- **Application Form** (`docs/register.html`): Multi-step startup application
- **Success Page** (`docs/success.html`): Post-submission confirmation
- **Assets** (`docs/assets/`): CSS, JavaScript, and images

## 🔧 Quick Start

The static site is located in the `/docs` directory and is ready for GitHub Pages deployment.

### 1. Enable GitHub Pages
- Go to Repository Settings → Pages
- Set source to "Deploy from a branch"
- Select "main" branch and "/docs" folder

### 2. Custom Domain (Optional)
- Update `docs/CNAME` with your domain
- Configure DNS: `CNAME foundry -> open-build.github.io`

### 3. Configure Integrations
- Set up Google Sheets integration (see docs/README.md)
- Configure BabbleBeaver API endpoint

## 📖 Documentation

Complete setup and customization documentation is available in `/docs/README.md`.

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

## startups datasources
Finding a public API that lists startup companies with product descriptions, current stage, and founder details can be quite useful for market research and networking. Here are a few APIs and platforms you might consider:

1. **Crunchbase API**:
   - **Description**: Crunchbase is a platform for finding business information about private and public companies. Their API provides access to data about startups, including company descriptions, funding stages, and founder details.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Crunchbase API](https://www.crunchbase.com/apps)

2. **AngelList API**:
   - **Description**: AngelList is a platform for startups, angel investors, and job-seekers looking to work at startups. Their API allows access to data about startups, including product descriptions and founder information.
   - **Access**: Requires an API key available upon request.
   - **Link**: [AngelList API](https://angel.co/api)

3. **Product Hunt API**:
   - **Description**: Product Hunt is a community where product enthusiasts share and discover new products. The API provides data on newly launched products, including descriptions and founder information.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Product Hunt API](https://api.producthunt.com/v2/docs)

4. **Mattermark API** (Note: Mattermark has been acquired, so availability may vary):
   - **Description**: Mattermark provided data on startups, including growth signals, funding rounds, and key people. This might still be accessible through other means or their acquiring company.
   - **Access**: Typically requires an API key, but it may be subject to change post-acquisition.

5. **Clearbit API**:
   - **Description**: Clearbit provides business intelligence APIs that can be used to find information about companies and people, including startups, product descriptions, and key personnel.
   - **Access**: Requires an API key which you can obtain by signing up for a developer account.
   - **Link**: [Clearbit API](https://clearbit.com/docs#company-api)

Each of these APIs requires signing up for access and often an API key. Depending on your specific needs and the depth of information you require, one of these options should be a good fit.
