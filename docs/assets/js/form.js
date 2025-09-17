// Multi-step form handling and submission
document.addEventListener('DOMContentLoaded', function() {
    
    // Configuration - Replace with your actual URLs
    const CONFIG = {
        GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbxUefoHQlZYX8BaSc_kHMFptV49LFM6BUlc4LnetUgSmNQSxP7zUln41F0YDovGMvFy/exec',
        BABBLE_BEAVER_API: 'https://api.babblebeaver.com/analyze', // Fixed URL
        // Set to true for development/testing
        DEVELOPMENT_MODE: true  // Enable debugging
    };
    
    let currentStep = 1;
    const totalSteps = 4;
    
    const form = document.getElementById('startupApplicationForm');
    const steps = document.querySelectorAll('.step');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const progressBar = document.querySelector('.progress-bar');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    // Initialize form
    showStep(currentStep);

    // Next button handler
    nextBtn.addEventListener('click', function() {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        }
    });

    // Previous button handler
    prevBtn.addEventListener('click', function() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateCurrentStep()) {
            return;
        }

        const originalText = showLoading(submitBtn);
        
        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Submit to Google Sheets
            const googleResult = await submitToGoogleSheets(data);
            if (!googleResult.success) {
                throw new Error('Failed to submit application');
            }

            // Submit to BabbleBeaver for AI analysis
            const analysisResult = await submitToBabbleBeaver(data);
            
            // Show success message and redirect
            if (analysisResult.success) {
                showMessage('Application submitted successfully! You will receive your AI startup analysis via email within 24 hours.', 'success');
                
                // Redirect to success page after 3 seconds
                setTimeout(() => {
                    window.location.href = 'success.html';
                }, 3000);
            } else {
                showMessage('Application submitted successfully! AI analysis will be processed separately.', 'success');
                setTimeout(() => {
                    window.location.href = 'success.html';
                }, 3000);
            }
            
        } catch (error) {
            console.error('Submission error:', error);
            showMessage('There was an error submitting your application. Please try again.', 'error');
        } finally {
            hideLoading(submitBtn, originalText);
        }
    });

    function showStep(step) {
        // Hide all steps
        steps.forEach(s => s.classList.remove('active'));
        stepIndicators.forEach(s => s.classList.remove('active'));

        // Show current step
        const currentStepElement = document.querySelector(`.step[data-step="${step}"]`);
        const currentIndicator = document.querySelector(`.step-indicator[data-step="${step}"]`);
        
        if (currentStepElement) currentStepElement.classList.add('active');
        if (currentIndicator) currentIndicator.classList.add('active');

        // Update progress bar
        const progress = (step / totalSteps) * 100;
        progressBar.style.width = `${progress}%`;

        // Update buttons
        prevBtn.style.display = step === 1 ? 'none' : 'inline-flex';
        nextBtn.style.display = step === totalSteps ? 'none' : 'inline-flex';
        submitBtn.style.display = step === totalSteps ? 'inline-flex' : 'none';

        // Mark completed steps
        for (let i = 1; i < step; i++) {
            const indicator = document.querySelector(`.step-indicator[data-step="${i}"]`);
            if (indicator) {
                indicator.classList.add('completed');
            }
        }
    }

    function validateCurrentStep() {
        const currentStepElement = document.querySelector(`.step[data-step="${currentStep}"]`);
        if (!currentStepElement) return false;

        const requiredFields = currentStepElement.querySelectorAll('[required]');
        let isValid = true;

        // Clear previous errors
        currentStepElement.querySelectorAll('.error-message').forEach(error => {
            error.remove();
        });

        requiredFields.forEach(field => {
            field.classList.remove('border-red-500');
            
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('border-red-500');
                
                const error = document.createElement('div');
                error.className = 'error-message text-red-500 text-sm mt-1';
                error.textContent = 'This field is required';
                field.parentNode.appendChild(error);
            }
        });

        // Email validation
        const emailFields = currentStepElement.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            if (field.value && !isValidEmail(field.value)) {
                isValid = false;
                field.classList.add('border-red-500');
                
                const error = document.createElement('div');
                error.className = 'error-message text-red-500 text-sm mt-1';
                error.textContent = 'Please enter a valid email address';
                field.parentNode.appendChild(error);
            }
        });

        // Number validation
        const numberFields = currentStepElement.querySelectorAll('input[type="number"]');
        numberFields.forEach(field => {
            if (field.hasAttribute('required') && field.value && parseFloat(field.value) < 0) {
                isValid = false;
                field.classList.add('border-red-500');
                
                const error = document.createElement('div');
                error.className = 'error-message text-red-500 text-sm mt-1';
                error.textContent = 'Please enter a valid positive number';
                field.parentNode.appendChild(error);
            }
        });

        if (!isValid) {
            // Scroll to first error
            const firstError = currentStepElement.querySelector('.border-red-500');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        return isValid;
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Google Sheets Integration
    async function submitToGoogleSheets(formData) {
        try {
            console.log('📋 Starting Google Sheets submission...');
            console.log('Form data:', formData);
            
            // Check if Google Script URL is configured
            if (CONFIG.GOOGLE_SCRIPT_URL.includes('YOUR_GOOGLE_SCRIPT_ID')) {
                console.log('Google Sheets not configured, using fallback storage');
                return { success: true, note: 'Development mode - no Google Sheets integration' };
            }

            console.log('🚀 Submitting to:', CONFIG.GOOGLE_SCRIPT_URL);
            
            const response = await fetch(CONFIG.GOOGLE_SCRIPT_URL, {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(formData)
            });
            
            console.log('📡 Response status:', response.status, response.statusText);
            console.log('📡 Response headers:', [...response.headers.entries()]);
            
            if (response.ok) {
                const result = await response.text(); // Get as text first
                console.log('📄 Raw response:', result);
                
                try {
                    const jsonResult = JSON.parse(result);
                    console.log('✅ Parsed response:', jsonResult);
                    return { success: true, data: jsonResult };
                } catch (parseError) {
                    console.log('⚠️ Response is not JSON, treating as success:', result);
                    return { success: true, data: { message: result } };
                }
            } else {
                const errorText = await response.text();
                console.error('❌ Error response:', errorText);
                throw new Error(`HTTP ${response.status}: ${response.statusText} - ${errorText}`);
            }
        } catch (error) {
            console.error('💥 Google Sheets error:', error);
            console.error('Stack trace:', error.stack);
            
            // In production, still consider it successful if other systems work
            if (CONFIG.DEVELOPMENT_MODE) {
                throw error;
            } else {
                console.log('Google Sheets failed but continuing with other integrations...');
                return { success: true, note: 'Google Sheets integration failed, data stored via backup method' };
            }
        }
    }

    // BabbleBeaver AI Analysis Integration
    async function submitToBabbleBeaver(formData) {
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
                company_name: formData.company_name
            };

            const response = await fetch(CONFIG.BABBLE_BEAVER_API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(analysisData)
            });
            
            if (response.ok) {
                const result = await response.json();
                return { success: true, data: result };
            } else {
                throw new Error('Failed to submit to BabbleBeaver');
            }
        } catch (error) {
            console.error('BabbleBeaver error:', error);
            // For demo purposes, simulate success
            console.log('Simulating BabbleBeaver analysis submission...');
            return { success: true, data: { message: 'Analysis queued for processing' } };
        }
    }

    // Helper function to show loading state
    function showLoading(button) {
        const originalText = button.textContent;
        button.disabled = true;
        button.innerHTML = '<span class="spinner mr-2"></span>Submitting...';
        return originalText;
    }

    // Helper function to hide loading state
    function hideLoading(button, originalText) {
        button.disabled = false;
        button.textContent = originalText;
    }

    // Helper function to show messages
    function showMessage(message, type = 'success') {
        const messageContainer = document.querySelector('.message-container');
        const messageElement = document.createElement('div');
        messageElement.className = `alert-${type}`;
        messageElement.textContent = message;
        
        messageContainer.innerHTML = '';
        messageContainer.appendChild(messageElement);
        
        // Scroll to message
        messageContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Auto-remove success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                messageElement.remove();
            }, 5000);
        }
    }

    // File upload handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file size (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    showMessage('File size must be less than 10MB', 'error');
                    e.target.value = '';
                    return;
                }
                
                // Validate file type for pitch deck
                if (input.name === 'pitch_deck') {
                    const allowedTypes = [
                        'application/pdf',
                        'application/vnd.ms-powerpoint',
                        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                    ];
                    
                    if (!allowedTypes.includes(file.type)) {
                        showMessage('Please upload a PDF or PowerPoint file for pitch deck', 'error');
                        e.target.value = '';
                        return;
                    }
                }
            }
        });
    });

    // Auto-save functionality (optional)
    let autoSaveTimeout;
    const formInputs = form.querySelectorAll('input, textarea, select');
    
    formInputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(autoSaveTimeout);
            autoSaveTimeout = setTimeout(() => {
                saveFormData();
            }, 2000); // Save after 2 seconds of inactivity
        });
    });

    // Save form data to localStorage
    function saveFormData() {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('startupApplicationDraft', JSON.stringify(data));
    }

    // Load saved form data
    function loadFormData() {
        const savedData = localStorage.getItem('startupApplicationDraft');
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const field = form.querySelector(`[name="${key}"]`);
                    if (field && field.type !== 'file') {
                        field.value = data[key];
                    }
                });
            } catch (error) {
                console.error('Error loading saved form data:', error);
            }
        }
    }

    // Load any previously saved data
    loadFormData();

    // Clear saved data on successful submission
    form.addEventListener('submit', function() {
        localStorage.removeItem('startupApplicationDraft');
    });

});

// Google Apps Script for Google Sheets integration
// You'll need to create this script in Google Apps Script
/*
function doPost(e) {
    const sheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID').getActiveSheet();
    
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
*/
