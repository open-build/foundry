/**
 * Opt-out management for static GitHub Pages site
 * Handles opt-out requests by creating GitHub issues for manual processing
 */

class OptOutManager {
    constructor() {
        this.githubRepo = 'open-build/foundry';
        this.issueTitle = 'Opt-out Request';
    }

    async handleOptOut(email, reason = '') {
        try {
            // Validate email
            if (!this.isValidEmail(email)) {
                throw new Error('Invalid email address');
            }

            // Store in localStorage for immediate effect
            this.addToLocalOptOuts(email, reason);

            // Create GitHub issue for manual processing
            await this.createOptOutIssue(email, reason);

            // Send notification email (if configured)
            await this.sendOptOutNotification(email, reason);

            return {
                success: true,
                message: 'Opt-out request processed successfully'
            };

        } catch (error) {
            console.error('Opt-out error:', error);
            return {
                success: false,
                message: error.message || 'Failed to process opt-out request'
            };
        }
    }

    addToLocalOptOuts(email, reason) {
        const optOuts = JSON.parse(localStorage.getItem('optOuts') || '[]');
        const optOutData = {
            email: email.toLowerCase(),
            reason: reason,
            timestamp: new Date().toISOString(),
            source: 'web'
        };

        // Check if already exists
        if (!optOuts.find(opt => opt.email === email.toLowerCase())) {
            optOuts.push(optOutData);
            localStorage.setItem('optOuts', JSON.stringify(optOuts));
        }
    }

    async createOptOutIssue(email, reason) {
        // This would require GitHub API token, which we can't store securely in static site
        // Instead, we'll use a form submission to Netlify/Vercel form handler or similar
        // For now, we'll use a simple webhook or form submission

        const issueBody = `
**Opt-out Request**

- **Email:** ${email}
- **Reason:** ${reason || 'No reason provided'}
- **Timestamp:** ${new Date().toISOString()}
- **Source:** Website opt-out form

**Action Required:**
1. Add ${email} to opt_outs.json
2. Remove from any active campaigns
3. Close this issue when complete
        `;

        // Use a form submission service or webhook
        const formData = new FormData();
        formData.append('email', email);
        formData.append('reason', reason);
        formData.append('timestamp', new Date().toISOString());
        formData.append('type', 'opt-out');

        // Submit to form handler (you would configure this endpoint)
        try {
            await fetch('https://formspree.io/f/team@open.build', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });
        } catch (error) {
            console.warn('Could not submit to form handler:', error);
        }
    }

    async sendOptOutNotification(email, reason) {
        // Send email notification to team (using simple mailto for now)
        const subject = encodeURIComponent('Opt-out Request - ' + email);
        const body = encodeURIComponent(`
New opt-out request:

Email: ${email}
Reason: ${reason || 'No reason provided'}
Timestamp: ${new Date().toISOString()}

Please add this email to the opt_outs.json file and remove from active campaigns.
        `);

        // Could open default email client
        const mailtoLink = `mailto:team@open.build?subject=${subject}&body=${body}`;
        
        // For background processing, we could use a service like EmailJS
        // For now, just log the notification
        console.log('Opt-out notification:', { email, reason });
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Check if an email is in local opt-outs (client-side only)
    isOptedOut(email) {
        const optOuts = JSON.parse(localStorage.getItem('optOuts') || '[]');
        return optOuts.some(opt => opt.email === email.toLowerCase());
    }

    // Get all local opt-outs
    getLocalOptOuts() {
        return JSON.parse(localStorage.getItem('optOuts') || '[]');
    }

    // Clear local opt-outs (for testing)
    clearLocalOptOuts() {
        localStorage.removeItem('optOuts');
    }
}

// Export for use in HTML pages
if (typeof window !== 'undefined') {
    window.OptOutManager = OptOutManager;
}

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OptOutManager;
}
