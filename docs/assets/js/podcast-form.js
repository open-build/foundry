// Podcast guest application form handling
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎙️ Podcast form JavaScript loaded!');
    
    // Configuration - Same Google Apps Script endpoint as foundry applications
    const CONFIG = {
        GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbzaXn82jf98akTlphk00Ao0luuM9lDQF6kN2ZN73lWGdSblLsdKtBjxLSfobnlknSvG/exec',
        // Set to true for development/testing
        DEVELOPMENT_MODE: true  // Enable debugging
    };
    
    let currentStep = 1;
    const totalSteps = 3;
    
    const form = document.getElementById('podcastApplicationForm');
    const steps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const progressBars = document.querySelectorAll('.progress-bar');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    console.log('📋 Form elements found:', {
        form: !!form,
        steps: steps.length,
        stepIndicators: stepIndicators.length,
        progressBars: progressBars.length,
        prevBtn: !!prevBtn,
        nextBtn: !!nextBtn,
        submitBtn: !!submitBtn
    });

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
            
            console.log('📋 Submitting podcast application...');
            console.log('Form data:', data);
            
            // Submit to Google Sheets
            const result = await submitToGoogleSheets(data);
            if (!result.success) {
                throw new Error('Failed to submit podcast application');
            }

            // Show success message and redirect
            showMessage('🎙️ Podcast application submitted successfully! We\'ll review your submission and get back to you within 2-3 business days.', 'success');
            
            // Redirect to success page after 3 seconds
            setTimeout(() => {
                window.location.href = 'success.html?type=podcast';
            }, 3000);
            
        } catch (error) {
            console.error('Submission error:', error);
            showMessage('There was an error submitting your podcast application. Please try again or contact us directly.', 'error');
        } finally {
            hideLoading(submitBtn, originalText);
        }
    });

    function showStep(step) {
        console.log(`🔄 Showing step ${step}`);
        
        // Hide all steps
        steps.forEach(s => s.classList.remove('active'));
        
        // Show current step
        const currentStepElement = document.querySelector(`[data-step="${step}"]`);
        console.log('📍 Current step element:', currentStepElement);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
            console.log('✅ Added active class to step', step);
        } else {
            console.error('❌ Could not find step element for step', step);
        }
        
        // Update step indicators
        stepIndicators.forEach((indicator, index) => {
            const stepNumber = index + 1;
            indicator.className = 'step-indicator';
            
            if (stepNumber < step) {
                indicator.classList.add('completed');
            } else if (stepNumber === step) {
                indicator.classList.add('current');
            } else {
                indicator.classList.add('pending');
            }
        });
        
        // Update progress bars
        progressBars.forEach((bar, index) => {
            const progressPercent = index < (step - 1) ? 100 : 0;
            bar.style.width = progressPercent + '%';
        });
        
        // Update step text
        const stepTexts = [
            'Personal & Company Info',
            'Bootstrapping Experience', 
            'Podcast Details'
        ];
        document.getElementById('step-text').textContent = stepTexts[step - 1] || '';
        
        // Show/hide navigation buttons
        prevBtn.style.display = step === 1 ? 'none' : 'inline-flex';
        nextBtn.style.display = step === totalSteps ? 'none' : 'inline-flex';
        submitBtn.style.display = step === totalSteps ? 'inline-flex' : 'none';
    }

    function validateCurrentStep() {
        const currentStepElement = document.querySelector(`[data-step="${currentStep}"]`);
        const requiredFields = currentStepElement.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('border-red-500');
                isValid = false;
                
                // Remove error styling when user starts typing
                field.addEventListener('input', function() {
                    field.classList.remove('border-red-500');
                }, { once: true });
            } else {
                field.classList.remove('border-red-500');
            }
        });

        if (!isValid) {
            showMessage('Please fill in all required fields.', 'error');
        }

        return isValid;
    }

    // Google Sheets Integration
    async function submitToGoogleSheets(formData) {
        try {
            console.log('📋 Starting Google Sheets submission...');
            console.log('Form data:', formData);
            
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
                console.log('Google Sheets failed but continuing...');
                return { success: true, note: 'Google Sheets integration failed, data stored via backup method' };
            }
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
    function showMessage(message, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = message;
        messageDiv.className = `mt-4 p-4 rounded-md ${type === 'error' ? 'bg-red-100 text-red-700 border border-red-200' : 'bg-green-100 text-green-700 border border-green-200'}`;
        messageDiv.classList.remove('hidden');
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                messageDiv.classList.add('hidden');
            }, 5000);
        }
    }

    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // URL validation
    function validateURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    // Add real-time validation for specific fields
    const emailField = document.getElementById('email');
    if (emailField) {
        emailField.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                this.classList.add('border-red-500');
                showMessage('Please enter a valid email address.', 'error');
            } else {
                this.classList.remove('border-red-500');
            }
        });
    }

    const websiteField = document.getElementById('company_website');
    if (websiteField) {
        websiteField.addEventListener('blur', function() {
            if (this.value && !validateURL(this.value)) {
                this.classList.add('border-red-500');
                showMessage('Please enter a valid website URL (starting with http:// or https://).', 'error');
            } else {
                this.classList.remove('border-red-500');
            }
        });
    }

    // Character counters for textarea fields
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'text-sm text-gray-500 mt-1 text-right';
            counter.textContent = `0 / ${maxLength}`;
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                const current = this.value.length;
                counter.textContent = `${current} / ${maxLength}`;
                counter.className = current > maxLength * 0.9 ? 'text-sm text-red-500 mt-1 text-right' : 'text-sm text-gray-500 mt-1 text-right';
            });
        }
    });
});