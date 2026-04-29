# Quick Setup Reference Card 🚀

## **Google Apps Script Setup - 5 Minutes**

### **🔗 Your Google Sheet**
```
https://docs.google.com/spreadsheets/d/1CXtcY76rIECYdY8o2m1I7Rq7CMQA8p9CZ6_5jSSQWmE/edit
```

### **⚡ Quick Steps**

1. **Go to**: https://script.google.com/
2. **New Project** → Replace code with `scripts/google-apps-script.js`
3. **Run** `testSetup` → Grant permissions
4. **Deploy** → Web app → "Anyone" access
5. **Copy URL** → Update `form.js` line 7
6. **Test** → Submit application form

### **🎯 Critical Configuration**

**Replace this line in `assets/js/form.js`:**
```javascript
GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_GOOGLE_SCRIPT_ID/exec',
```

**With your actual deployment URL:**
```javascript
GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbwXXXXXXXXXXX/exec',
```

### **📊 What You'll Get**

**✅ Automatic Data Storage:**
- All applications stored in Google Sheets
- AI evaluations from BabbleBeaver
- Email notifications to team@open.build

**✅ Two Sheet Structure:**
- **Applications** - All form submissions
- **AI_Evaluations** - BabbleBeaver analysis results

### **🔍 Verification**

**Test successful when:**
1. ✅ Form submits without errors
2. ✅ Data appears in Google Sheet
3. ✅ Email notification received
4. ✅ AI analysis stored (may take a few minutes)

---
**💡 Need help?** Check `devdocs/GOOGLE_APPS_SCRIPT_SETUP.md` for detailed instructions