# Buildly Labs Foundry - Static Site

A modern, responsive website for the Buildly Labs Foundry program, built with HTML, CSS (Tailwind), and JavaScript for GitHub Pages deployment.

## Features

### 🚀 Modern Design
- **Tailwind CSS**: Modern, responsive design with utility-first approach
- **Mobile-First**: Fully responsive across all device sizes
- **Interactive Elements**: Smooth animations and transitions
- **Professional UI/UX**: Clean, modern interface with excellent user experience

### 📝 Multi-Step Registration Form
- **4-Step Application Process**: Company Info → Team & Market → Development → Strategy
- **Real-time Validation**: Form validation with error messages
- **Auto-Save**: Automatically saves progress in localStorage
- **File Upload**: Support for pitch deck uploads
- **Progress Indicator**: Visual progress tracking

### 🔗 Integrations
- **Google Sheets**: Form submissions stored in Google Sheets
- **BabbleBeaver AI**: Startup idea analysis via AI
- **Email Notifications**: Automated email responses

### 🎯 Key Pages
- **Homepage**: Hero section, benefits, partner showcase
- **Registration Form**: Comprehensive multi-step application
- **Success Page**: Post-submission confirmation and next steps

## Setup Instructions

### 1. Google Sheets Integration

1. Create a new Google Sheets spreadsheet
2. Go to [Google Apps Script](https://script.google.com/)
3. Create a new project and paste this code:

```javascript
function doPost(e) {
    const sheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID').getActiveSheet();
    
    // Add headers if first row is empty
    if (sheet.getLastRow() === 0) {
        const headers = [
            'Timestamp', 'Company Name', 'Contact Email', 'Business Description',
            'Legal Structure', 'Annual Revenue', 'Funding Amount', 'Outstanding Debt',
            'Founder Names', 'Team Members', 'Advisors Mentors', 'Target Audience',
            'Competition Analysis', 'Market Demand Proof', 'Marketing Strategy',
            'Development Stage', 'Intellectual Property', 'Customer Base',
            'Customer Acquisition Strategy', 'Current Funding Sources', 'Future Funding Plans',
            'Revenue Model', 'Pricing Strategy', 'Competitive Advantage',
            'Milestones Achievements', 'Social Impact', 'References Recommendations',
            'Referral Code'
        ];
        sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    }
    
    const data = e.parameter;
    const timestamp = new Date();
    
    const row = [
        timestamp,
        data.company_name || '',
        data.contact_email || '',
        data.business_description || '',
        data.legal_structure || '',
        data.annual_revenue || '',
        data.funding_amount || '',
        data.outstanding_debt || '',
        data.founder_names || '',
        data.team_members || '',
        data.advisors_mentors || '',
        data.target_audience || '',
        data.competition_analysis || '',
        data.market_demand_proof || '',
        data.marketing_strategy || '',
        data.development_stage || '',
        data.intellectual_property || '',
        data.customer_base || '',
        data.customer_acquisition_strategy || '',
        data.current_funding_sources || '',
        data.future_funding_plans || '',
        data.revenue_model || '',
        data.pricing_strategy || '',
        data.competitive_advantage || '',
        data.milestones_achievements || '',
        data.social_impact || '',
        data.references_recommendations || '',
        data.referral_code || ''
    ];
    
    sheet.appendRow(row);
    
    return ContentService.createTextOutput(JSON.stringify({result: 'success'}))
        .setMimeType(ContentService.MimeType.JSON);
}
```

4. Deploy as a web app with "Anyone" access
5. Copy the web app URL and update `GOOGLE_SCRIPT_URL` in `/assets/js/form.js`

### 2. BabbleBeaver Integration

Update the `BABBLE_BEAVER_API` URL in `/assets/js/form.js` with the actual BabbleBeaver API endpoint:

```javascript
const CONFIG = {
    GOOGLE_SCRIPT_URL: 'YOUR_GOOGLE_SCRIPT_URL_HERE',
    BABBLE_BEAVER_API: 'https://babble.buildly.io/api/analyze'
};
```

### 3. GitHub Pages Deployment

#### Option A: Direct Deployment from /docs folder

1. Push your code to the repository
2. Go to Repository Settings → Pages
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/docs" folder
5. Save and wait for deployment

#### Option B: Custom Domain Setup

1. Add your domain to the `CNAME` file (already created)
2. Configure DNS records with your provider:
   - **CNAME Record**: `foundry` → `open-build.github.io`
3. Enable "Enforce HTTPS" in GitHub Pages settings

### 4. Customization

#### Update Branding
- Replace logo images in `/assets/img/`
- Update colors in Tailwind config (both HTML files)
- Modify text content in HTML files

#### Form Fields
- Add/remove fields in `register.html`
- Update validation in `form.js`
- Adjust Google Sheets headers accordingly

#### Styling
- Modify `/assets/css/main.css` for custom styles
- Update Tailwind config for color schemes
- Adjust responsive breakpoints as needed

## File Structure

```
docs/
├── index.html              # Homepage
├── register.html           # Registration form
├── success.html            # Success page
├── CNAME                   # Custom domain configuration
├── assets/
│   ├── css/
│   │   └── main.css        # Custom styles
│   ├── js/
│   │   ├── main.js         # General JavaScript
│   │   └── form.js         # Form handling
│   └── img/                # Images and logos
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions (optional)
```

## Browser Support

- **Modern Browsers**: Chrome 60+, Firefox 60+, Safari 12+, Edge 79+
- **Mobile**: iOS Safari 12+, Chrome Mobile 60+
- **Features**: ES6+, CSS Grid, Flexbox, Fetch API

## Performance Features

- **CDN Assets**: Tailwind CSS and Font Awesome loaded from CDN
- **Optimized Images**: Compressed images with appropriate formats
- **Minimal JavaScript**: Lightweight, vanilla JavaScript implementation
- **Auto-Save**: Prevents data loss during form completion

## Development

### Local Development
```bash
# Serve locally (any HTTP server)
python -m http.server 8000
# or
npx serve docs
```

### Testing
- Test form validation with various inputs
- Verify Google Sheets integration
- Test on multiple devices and browsers
- Validate accessibility with screen readers

## Security Considerations

- **Form Validation**: Client and server-side validation
- **File Upload**: Size and type restrictions
- **API Calls**: Error handling and timeout management
- **Data Privacy**: No sensitive data stored in localStorage

## Support

For questions or issues:
- Email: foundry@buildly.io
- Documentation: [GitHub Repository](https://github.com/open-build/foundry)
- BabbleBeaver: https://babble.buildly.io
- Buildly Labs: https://labs.buildly.io

## License

© 2025 Buildly Labs Foundry. All rights reserved.
