# Google Apps Script Setup for Buildly Labs Foundry

## 📋 **Complete Setup Instructions**

### **Step 1: Create Google Apps Script Project**

1. **Open Google Apps Script**
   - Go to https://script.google.com/
   - Click "New Project"

2. **Replace Default Code**
   - Delete the default `function myFunction() {}` code
   - Copy and paste the entire content from `scripts/google-apps-script.js`

3. **Name Your Project**
   - Click "Untitled project" at the top
   - Rename to "Buildly Labs Foundry Application Handler"

### **Step 2: Configure Permissions**

1. **Enable Required APIs**
   - Click "Services" (+ icon) in the left sidebar
   - Add "Gmail API" if you want email notifications
   - Add "Google Sheets API" (usually enabled by default)

2. **Test the Script**
   - Click the "Run" button (▶️) next to `testSetup`
   - Grant permissions when prompted:
     - "See, edit, create, and delete your spreadsheets"
     - "Send email as you" (for notifications)

### **Step 3: Deploy as Web App**

1. **Deploy the Script**
   - Click "Deploy" → "New deployment"
   - Click the gear icon ⚙️ next to "Type"
   - Select "Web app"

2. **Configure Deployment**
   - **Description**: "Foundry Application Handler v1.0"
   - **Execute as**: "Me (your email)"
   - **Who has access**: "Anyone" ⚠️ *Important: Must be "Anyone" for form submissions*

3. **Get Your Web App URL**
   - Click "Deploy"
   - Copy the "Web app URL" (looks like: `https://script.google.com/macros/s/ABC...XYZ/exec`)
   - ⚠️ **Save this URL - you'll need it for Step 4**

### **Step 4: Update Your Website Form**

1. **Edit form.js**
   - Open `/Users/greglind/Projects/open-build/foundry/assets/js/form.js`
   - Find line ~7: `GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_GOOGLE_SCRIPT_ID/exec'`
   - Replace `YOUR_GOOGLE_SCRIPT_ID` with your actual deployment URL

**Example:**
```javascript
const CONFIG = {
    GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbw1234567890abcdef/exec',
    BABBLE_BEAVER_API: 'https://babble.buildly.io/api/analyze'
};
```

### **Step 5: Test the Integration**

1. **Submit a Test Application**
   - Go to https://www.firstcityfoundry.com/register.html
   - Fill out and submit the form
   - Check your Google Sheet for the new application data

2. **Verify Data Storage**
   - Open your Google Sheet: https://docs.google.com/spreadsheets/d/1CXtcY76rIECYdY8o2m1I7Rq7CMQA8p9CZ6_5jSSQWmE/edit
   - Look for new sheets: "Applications" and "AI_Evaluations"
   - Check for application data and AI analysis results

## 📊 **What Gets Stored in Your Google Sheet**

### **Applications Sheet Columns:**
- Timestamp, Application ID, Company Name, Contact Email
- Business Description, Legal Structure, Financial Info
- Founder Names, Team Members, Market Analysis
- Development Stage, Technology Stack, Revenue Model
- AI Analysis Status, Notes

### **AI_Evaluations Sheet Columns:**
- Application ID, AI Analysis Score, Strengths, Weaknesses
- Recommendations, Market Potential, Technical Feasibility
- Business Model Score, Team Assessment, Overall Rating
- Detailed Analysis (JSON), Follow-up Actions, Status

## 🔧 **Configuration Options**

### **In the Google Apps Script:**
```javascript
// You can modify these constants:
const SHEET_ID = '1CXtcY76rIECYdY8o2m1I7Rq7CMQA8p9CZ6_5jSSQWmE';
const NOTIFICATION_EMAIL = 'greg@open.build';  // Change notification email
const BREVO_API_KEY = 'your-brevo-api-key-here'; // Your Brevo API key
const FROM_EMAIL = 'noreply@open.build'; // Your verified Brevo sender email
const BABBLE_BEAVER_API = 'https://babble.buildly.io/api/analyze';
```

### **Email Notifications:**
- Sends automatic email via **Brevo SMTP** to `greg@open.build` for each new application
- Includes rich HTML formatting with application summary and link to Google Sheet
- Falls back to Gmail API if Brevo fails
- Can be disabled by commenting out the `sendNotificationEmail()` call

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **"Permission denied" errors**
   - Re-run authorization: Script editor → Run → testSetup
   - Grant all requested permissions

2. **Form submissions not appearing in sheet**
   - Check the deployment URL is correct in form.js
   - Verify deployment is set to "Anyone" access
   - Check Google Apps Script logs for errors

3. **AI analysis not working**
   - Check BabbleBeaver API availability
   - Verify network connectivity in Apps Script environment

### **Debugging:**
1. **View Logs**: Script editor → Execution transcript
2. **Test Functions**: Run `testSetup()` and `initializeSheets()`
3. **Check Sheet**: Verify both sheets are created with proper headers

## 🚀 **Go Live Steps**

1. ✅ Complete Google Apps Script setup
2. ✅ Update form.js with deployment URL  
3. ✅ Deploy website changes to GitHub Pages
4. ✅ Test with real application submission
5. ✅ Monitor Google Sheet for data
6. ✅ Verify email notifications are working

**Your foundry application system will be fully operational!** 🎯