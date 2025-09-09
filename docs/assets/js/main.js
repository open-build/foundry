// Main JavaScript for Buildly Labs Foundry

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                if (mobileMenu) {
                    mobileMenu.classList.add('hidden');
                }
            }
        });
    });

    // Add scroll effect to navigation
    let lastScroll = 0;
    const nav = document.querySelector('nav');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            nav.classList.remove('scroll-up');
            return;
        }
        
        if (currentScroll > lastScroll && !nav.classList.contains('scroll-down')) {
            // Scroll down
            nav.classList.remove('scroll-up');
            nav.classList.add('scroll-down');
        } else if (currentScroll < lastScroll && nav.classList.contains('scroll-down')) {
            // Scroll up
            nav.classList.remove('scroll-down');
            nav.classList.add('scroll-up');
        }
        
        lastScroll = currentScroll;
    });

    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.group, .partner-logo, .flex.items-start').forEach(el => {
        observer.observe(el);
    });
});

// Google Sheets integration for form submission
async function submitToGoogleSheets(formData) {
    const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
    
    try {
        const response = await fetch(GOOGLE_SCRIPT_URL, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(formData)
        });
        
        if (response.ok) {
            return { success: true };
        } else {
            throw new Error('Failed to submit form');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        return { success: false, error: error.message };
    }
}

// BabbleBeaver API integration for startup analysis
async function submitToBabbleBeaver(startupData) {
    const BABBLE_BEAVER_API = 'https://babble.buildly.io/api/analyze';
    
    try {
        const response = await fetch(BABBLE_BEAVER_API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                startup_idea: startupData.idea,
                business_model: startupData.businessModel,
                target_market: startupData.targetMarket,
                competition_analysis: startupData.competition,
                team_info: startupData.team
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            return { success: true, data: result };
        } else {
            throw new Error('Failed to analyze startup idea');
        }
    } catch (error) {
        console.error('Error analyzing startup:', error);
        return { success: false, error: error.message };
    }
}

// Form validation helper
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        const errorElement = field.parentNode.querySelector('.error-message');
        
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
            
            if (!errorElement) {
                const error = document.createElement('div');
                error.className = 'error-message text-red-500 text-sm mt-1';
                error.textContent = 'This field is required';
                field.parentNode.appendChild(error);
            }
        } else {
            field.classList.remove('border-red-500');
            if (errorElement) {
                errorElement.remove();
            }
        }
    });
    
    // Email validation
    const emailFields = formElement.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            isValid = false;
            field.classList.add('border-red-500');
            
            const errorElement = field.parentNode.querySelector('.error-message');
            if (!errorElement) {
                const error = document.createElement('div');
                error.className = 'error-message text-red-500 text-sm mt-1';
                error.textContent = 'Please enter a valid email address';
                field.parentNode.appendChild(error);
            }
        }
    });
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show loading state
function showLoading(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="spinner mr-2"></span>Processing...';
    return originalText;
}

// Hide loading state
function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}

// Show success/error messages
function showMessage(message, type = 'success') {
    const messageElement = document.createElement('div');
    messageElement.className = `alert-${type}`;
    messageElement.textContent = message;
    
    const container = document.querySelector('.message-container') || document.body;
    container.insertBefore(messageElement, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}
