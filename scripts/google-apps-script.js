/**
 * Google Apps Script for Buildly Labs Foundry Applications
 * Handles form submissions and AI evaluations
 * 
 * Setup Instructions:
 * 1. Open script.google.com
 * 2. Create new project
 * 3. Replace Code.gs with this content
 * 4. Deploy as web app
 * 5. Copy the deployment URL to form.js
 */

// Configuration
const SHEET_ID = '1CXtcY76rIECYdY8o2m1I7Rq7CMQA8p9CZ6_5jSSQWmE';
const APPLICATIONS_SHEET_NAME = 'Applications';
const AI_EVALUATIONS_SHEET_NAME = 'AI_Evaluations';
const BABBLE_BEAVER_API = 'https://babble.buildly.io/api/analyze';
const PYTHON_SMTP_ENDPOINT = 'https://www.firstcityfoundry.com/api/send-notification';
const NOTIFICATION_EMAIL = 'greg@open.build';

/**
 * Main function to handle POST requests from the form
 */
function doPost(e) {
  try {
    Logger.log('Received POST request');
    
    // Parse form data
    const formData = parseFormData(e);
    Logger.log('Parsed form data: ' + JSON.stringify(formData));
    
    // Store application in Google Sheets
    const applicationId = storeApplication(formData);
    Logger.log('Stored application with ID: ' + applicationId);
    
    // Send to BabbleBeaver for AI analysis (async)
    requestAIAnalysis(formData, applicationId);
    
    // Send notification email
    sendNotificationEmail(formData, applicationId);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        applicationId: applicationId,
        message: 'Application submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    Logger.log('Error processing form: ' + error.toString());
    
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle GET requests (for testing)
 */
function doGet(e) {
  return ContentService
    .createTextOutput('Buildly Labs Foundry Application Handler - Ready')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Parse form data from POST request
 */
function parseFormData(e) {
  const data = {};
  
  if (e.parameter) {
    // Handle URL encoded form data
    Object.keys(e.parameter).forEach(key => {
      data[key] = e.parameter[key];
    });
  } else if (e.postData && e.postData.contents) {
    // Handle JSON data
    try {
      const jsonData = JSON.parse(e.postData.contents);
      Object.assign(data, jsonData);
    } catch (jsonError) {
      Logger.log('Failed to parse JSON, trying form data');
      // Fallback to form data parsing
      const formData = e.postData.contents.split('&');
      formData.forEach(pair => {
        const [key, value] = pair.split('=');
        if (key && value) {
          data[decodeURIComponent(key)] = decodeURIComponent(value);
        }
      });
    }
  }
  
  return data;
}

/**
 * Store application data in Google Sheets
 */
function storeApplication(formData) {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  let sheet = spreadsheet.getSheetByName(APPLICATIONS_SHEET_NAME);
  
  // Create Applications sheet if it doesn't exist
  if (!sheet) {
    sheet = spreadsheet.insertSheet(APPLICATIONS_SHEET_NAME);
    
    // Add headers
    const headers = [
      'Timestamp', 'Application ID', 'Company Name', 'Contact Email', 'Business Description',
      'Legal Structure', 'Annual Revenue', 'Funding Amount', 'Outstanding Debt',
      'Founder Names', 'Team Members', 'Target Audience', 'Market Size', 'Competition Analysis',
      'Development Stage', 'Technology Stack', 'Key Features', 'User Feedback',
      'Revenue Model', 'Current Funding Sources', 'Future Funding Plans', 'Growth Strategy',
      'Competitive Advantage', 'Marketing Strategy', 'AI Analysis Status', 'Notes'
    ];
    
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  
  // Generate unique application ID
  const applicationId = 'APP_' + new Date().getTime();
  const timestamp = new Date();
  
  // Prepare row data
  const rowData = [
    timestamp,
    applicationId,
    formData.company_name || '',
    formData.contact_email || '',
    formData.business_description || '',
    formData.legal_structure || '',
    parseFloat(formData.annual_revenue) || 0,
    parseFloat(formData.funding_amount) || 0,
    parseFloat(formData.outstanding_debt) || 0,
    formData.founder_names || '',
    formData.team_members || '',
    formData.target_audience || '',
    formData.market_size || '',
    formData.competition_analysis || '',
    formData.development_stage || '',
    formData.technology_stack || '',
    formData.key_features || '',
    formData.user_feedback || '',
    formData.revenue_model || '',
    formData.current_funding_sources || '',
    formData.future_funding_plans || '',
    formData.growth_strategy || '',
    formData.competitive_advantage || '',
    formData.marketing_strategy || '',
    'Pending AI Analysis',
    ''
  ];
  
  // Add row to sheet
  sheet.appendRow(rowData);
  
  // Auto-resize columns
  sheet.autoResizeColumns(1, rowData.length);
  
  return applicationId;
}

/**
 * Request AI analysis from BabbleBeaver
 */
function requestAIAnalysis(formData, applicationId) {
  try {
    const analysisData = {
      startup_idea: formData.business_description,
      business_model: formData.revenue_model,
      target_market: formData.target_audience,
      competition_analysis: formData.competition_analysis || 'Not provided',
      team_info: `Founders: ${formData.founder_names}. Team: ${formData.team_members || 'Not specified'}`,
      development_stage: formData.development_stage,
      funding_status: `Current: ${formData.current_funding_sources}. Future: ${formData.future_funding_plans}`,
      competitive_advantage: formData.competitive_advantage || 'Not specified',
      contact_email: formData.contact_email,
      company_name: formData.company_name,
      application_id: applicationId
    };
    
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(analysisData)
    };
    
    const response = UrlFetchApp.fetch(BABBLE_BEAVER_API, options);
    const responseData = JSON.parse(response.getContentText());
    
    Logger.log('BabbleBeaver response: ' + JSON.stringify(responseData));
    
    // Store AI analysis result
    storeAIAnalysis(applicationId, formData, responseData);
    
    // Update application status
    updateApplicationStatus(applicationId, 'AI Analysis Complete');
    
  } catch (error) {
    Logger.log('Error requesting AI analysis: ' + error.toString());
    updateApplicationStatus(applicationId, 'AI Analysis Failed: ' + error.toString());
  }
}

/**
 * Store AI analysis results in separate sheet
 */
function storeAIAnalysis(applicationId, formData, analysisResult) {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  let sheet = spreadsheet.getSheetByName(AI_EVALUATIONS_SHEET_NAME);
  
  // Create AI Evaluations sheet if it doesn't exist
  if (!sheet) {
    sheet = spreadsheet.insertSheet(AI_EVALUATIONS_SHEET_NAME);
    
    // Add headers
    const headers = [
      'Timestamp', 'Application ID', 'Company Name', 'Contact Email',
      'AI Analysis Score', 'Strengths', 'Weaknesses', 'Recommendations',
      'Market Potential', 'Technical Feasibility', 'Business Model Score',
      'Team Assessment', 'Competition Risk', 'Overall Rating',
      'Detailed Analysis', 'Follow-up Actions', 'Status'
    ];
    
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  
  // Parse AI analysis result
  const analysis = analysisResult.analysis || analysisResult;
  
  const rowData = [
    new Date(),
    applicationId,
    formData.company_name || '',
    formData.contact_email || '',
    analysis.overall_score || 'N/A',
    analysis.strengths || 'Analysis pending',
    analysis.weaknesses || 'Analysis pending',
    analysis.recommendations || 'Analysis pending',
    analysis.market_potential || 'N/A',
    analysis.technical_feasibility || 'N/A',
    analysis.business_model_score || 'N/A',
    analysis.team_assessment || 'N/A',
    analysis.competition_risk || 'N/A',
    analysis.overall_rating || 'Pending',
    JSON.stringify(analysis),
    analysis.follow_up_actions || 'Standard review process',
    'Complete'
  ];
  
  sheet.appendRow(rowData);
  sheet.autoResizeColumns(1, rowData.length);
}

/**
 * Update application status in the Applications sheet
 */
function updateApplicationStatus(applicationId, status) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName(APPLICATIONS_SHEET_NAME);
    
    if (!sheet) return;
    
    const data = sheet.getDataRange().getValues();
    
    // Find the application row (Application ID is in column B, index 1)
    for (let i = 1; i < data.length; i++) {
      if (data[i][1] === applicationId) {
        // Update AI Analysis Status column (column Y, index 24)
        sheet.getRange(i + 1, 25).setValue(status);
        sheet.getRange(i + 1, 25).setNote('Updated: ' + new Date().toLocaleString());
        break;
      }
    }
  } catch (error) {
    Logger.log('Error updating application status: ' + error.toString());
  }
}

/**
 * Send notification email via Python SMTP system
 */
function sendNotificationEmail(formData, applicationId) {
  try {
    const subject = `🚀 New Foundry Application: ${formData.company_name || 'Unknown Company'}`;
    
    const htmlBody = `
    <h2>New Application Submitted to Buildly Labs Foundry</h2>
    
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
      <h3 style="color: #2563eb; margin-top: 0;">Application Summary</h3>
      <p><strong>Application ID:</strong> ${applicationId}</p>
      <p><strong>Company:</strong> ${formData.company_name || 'Not provided'}</p>
      <p><strong>Contact:</strong> ${formData.contact_email || 'Not provided'}</p>
      <p><strong>Founders:</strong> ${formData.founder_names || 'Not provided'}</p>
    </div>
    
    <div style="background: #fff; border: 1px solid #e5e7eb; padding: 20px; border-radius: 8px; margin: 20px 0;">
      <h4 style="color: #374151; margin-top: 0;">Business Description:</h4>
      <p style="line-height: 1.6;">${formData.business_description || 'Not provided'}</p>
    </div>
    
    <div style="background: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
      <h4 style="color: #92400e; margin-top: 0;">Financial Information:</h4>
      <p><strong>Funding Sought:</strong> $${formatCurrency(formData.funding_amount || '0')}</p>
      <p><strong>Annual Revenue:</strong> $${formatCurrency(formData.annual_revenue || '0')}</p>
      <p><strong>Outstanding Debt:</strong> $${formatCurrency(formData.outstanding_debt || '0')}</p>
    </div>
    
    <div style="background: #ecfdf5; padding: 15px; border-radius: 8px; margin: 20px 0;">
      <h4 style="color: #065f46; margin-top: 0;">Additional Details:</h4>
      <p><strong>Legal Structure:</strong> ${formData.legal_structure || 'Not specified'}</p>
      <p><strong>Development Stage:</strong> ${formData.development_stage || 'Not specified'}</p>
      <p><strong>Target Market:</strong> ${formData.target_audience || 'Not specified'}</p>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
      <a href="https://docs.google.com/spreadsheets/d/${SHEET_ID}/edit" 
         style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
        📊 View Full Application in Google Sheets
      </a>
    </div>
    
    <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 14px; color: #6b7280;">
      <p><strong>Next Steps:</strong></p>
      <ul>
        <li>AI analysis will be processed automatically by BabbleBeaver</li>
        <li>Results will be stored in the AI_Evaluations sheet</li>
        <li>Review application and follow up as needed</li>
      </ul>
      
      <hr style="margin: 15px 0; border: none; border-top: 1px solid #d1d5db;">
      <p style="margin: 0;"><em>Buildly Labs Foundry Application System</em><br>
      Automated notification via Google Apps Script</p>
    </div>
    `;
    
    // Prepare notification data for Python SMTP system
    const notificationData = {
      to: NOTIFICATION_EMAIL,
      subject: subject,
      html_body: htmlBody,
      application_data: {
        id: applicationId,
        company: formData.company_name,
        contact: formData.contact_email,
        founders: formData.founder_names,
        description: formData.business_description,
        funding_sought: formData.funding_amount,
        revenue: formData.annual_revenue,
        legal_structure: formData.legal_structure,
        development_stage: formData.development_stage
      }
    };
    
    // Try to send via Python SMTP endpoint first
    try {
      const response = UrlFetchApp.fetch(PYTHON_SMTP_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        payload: JSON.stringify(notificationData)
      });
      
      if (response.getResponseCode() === 200) {
        Logger.log('✅ Notification sent via Python SMTP to: ' + NOTIFICATION_EMAIL);
        return;
      } else {
        throw new Error('Python SMTP endpoint returned: ' + response.getResponseCode());
      }
    } catch (smtpError) {
      Logger.log('⚠️ Python SMTP failed: ' + smtpError.toString());
      Logger.log('Falling back to Gmail API...');
    }
    
    // Fallback to Gmail API if Python SMTP fails
    try {
      const plainTextBody = htmlBody.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
      GmailApp.sendEmail(NOTIFICATION_EMAIL, subject, plainTextBody, {
        htmlBody: htmlBody
      });
      Logger.log('✅ Fallback notification sent via Gmail to: ' + NOTIFICATION_EMAIL);
    } catch (gmailError) {
      Logger.log('❌ Both notification methods failed:');
      Logger.log('SMTP Error: ' + smtpError);
      Logger.log('Gmail Error: ' + gmailError);
      throw new Error('Failed to send notification via both SMTP and Gmail');
    }
    
  } catch (error) {
    Logger.log('❌ Error in sendNotificationEmail: ' + error.toString());
    throw error;
  }
}

/**
 * Helper function to format currency
 */
function formatCurrency(amount) {
  if (!amount || amount === '0') return '0';
  return parseFloat(amount).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

/**
 * Test function to verify setup
 */
function testSetup() {
  Logger.log('Testing Buildly Labs Foundry Application Handler...');
  
  // Test sheet access
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    Logger.log('✅ Successfully accessed spreadsheet: ' + spreadsheet.getName());
  } catch (error) {
    Logger.log('❌ Error accessing spreadsheet: ' + error.toString());
    return;
  }
  
  // Test email sending
  try {
    GmailApp.sendEmail(NOTIFICATION_EMAIL, 'Test: Foundry Application Handler', 'Setup test successful');
    Logger.log('✅ Successfully sent test email');
  } catch (error) {
    Logger.log('❌ Error sending test email: ' + error.toString());
  }
  
  Logger.log('Setup test complete. Check logs for any errors.');
}

/**
 * Function to initialize sheets with proper structure
 */
function initializeSheets() {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  
  // Ensure Applications sheet exists with proper headers
  let applicationsSheet = spreadsheet.getSheetByName(APPLICATIONS_SHEET_NAME);
  if (!applicationsSheet) {
    applicationsSheet = spreadsheet.insertSheet(APPLICATIONS_SHEET_NAME);
  }
  
  // Ensure AI Evaluations sheet exists with proper headers  
  let evaluationsSheet = spreadsheet.getSheetByName(AI_EVALUATIONS_SHEET_NAME);
  if (!evaluationsSheet) {
    evaluationsSheet = spreadsheet.insertSheet(AI_EVALUATIONS_SHEET_NAME);
  }
  
  Logger.log('Sheets initialized successfully');
}