// Multi-step form handling and submission
document.addEventListener('DOMContentLoaded', function() {
    
    // Configuration - Replace with your actual URLs
    const CONFIG = {
        COLLABHUB_API: 'https://collab.buildly.io/onboarding/api/foundry-intake/applications/',
        DEVELOPMENT_MODE: false
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

        // Validate Turnstile CAPTCHA
        const turnstileToken = window.turnstile && window.turnstile.getResponse();
        if (!turnstileToken) {
            showMessage('Please complete the CAPTCHA verification before submitting.', 'error');
            return;
        }

        const originalText = showLoading(submitBtn);

        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            await submitToCollabHub(data, turnstileToken);

            localStorage.removeItem('startupApplicationDraft');

            showMessage('Application submitted successfully! You will receive a confirmation email shortly.', 'success');
            setTimeout(() => {
                window.location.href = 'success.html';
            }, 2000);

        } catch (error) {
            console.error('Submission error:', error);
            if (window.turnstile) window.turnstile.reset();
            showMessage(error.userMessage || 'There was an error submitting your application. Please try again.', 'error');
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

        // Show Turnstile widget on final step
        const turnstileWidget = document.getElementById('turnstileWidget');
        if (turnstileWidget) {
            turnstileWidget.style.display = step === totalSteps ? 'block' : 'none';
        }

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
    // CollabHub Intake API Integration
    function generateIdempotencyKey() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }

    async function submitToCollabHub(data, captchaToken) {
        const nameParts = (data.founder_names || '').trim().split(/\s+/);
        const firstName = nameParts[0] || '';
        const lastName = nameParts.slice(1).join(' ') || '';

        const payload = {
            source: 'firstcityfoundry_register',
            captcha_token: captchaToken,
            contact: {
                email: data.contact_email || '',
                full_name: data.founder_names || '',
                first_name: firstName,
                last_name: lastName
            },
            company: {
                name: data.company_name || '',
                legal_structure: data.legal_structure || ''
            },
            application: {
                business_description: data.business_description || '',
                development_stage: data.development_stage || '',
                annual_revenue: parseFloat(data.annual_revenue) || 0,
                funding_amount: parseFloat(data.funding_amount) || 0,
                outstanding_debt: parseFloat(data.outstanding_debt) || 0,
                revenue_model: data.revenue_model || '',
                target_audience: data.target_audience || '',
                competition_analysis: data.competition_analysis || '',
                market_demand_proof: data.market_demand_proof || '',
                marketing_strategy: data.marketing_strategy || '',
                intellectual_property: data.intellectual_property || '',
                customer_base: data.customer_base || '',
                customer_acquisition_strategy: data.customer_acquisition_strategy || '',
                current_funding_sources: data.current_funding_sources || '',
                future_funding_plans: data.future_funding_plans || '',
                pricing_strategy: data.pricing_strategy || '',
                competitive_advantage: data.competitive_advantage || '',
                milestones_achievements: data.milestones_achievements || '',
                social_impact: data.social_impact || '',
                team_members: data.team_members || '',
                advisors_mentors: data.advisors_mentors || '',
                references_recommendations: data.references_recommendations || '',
                referral_code: data.referral_code || ''
            },
            attachments: []
        };

        const response = await fetch(CONFIG.COLLABHUB_API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Idempotency-Key': generateIdempotencyKey()
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            return await response.json();
        }

        let errorBody = {};
        try { errorBody = await response.json(); } catch (_) {}

        const err = new Error(`Submission failed: HTTP ${response.status}`);
        if (response.status === 400) {
            err.userMessage = errorBody.detail || 'Please check your form entries and try again.';
        } else if (response.status === 429) {
            err.userMessage = 'Too many submissions. Please wait a few minutes and try again.';
        } else {
            err.userMessage = 'An unexpected error occurred. Please try again later.' +
                (errorBody.trace_id ? ` (Ref: ${errorBody.trace_id})` : '');
        }
        throw err;
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

});

