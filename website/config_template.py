# Startup Outreach Bot Configuration
# Copy this to config.py and update with your settings

# Email Configuration - Brevo SMTP
# Use environment variables for security
import os

EMAIL_CONFIG = {
    'service': 'brevo',
    'username': os.getenv('BREVO_SMTP_LOGIN', ''),
    'password': os.getenv('BREVO_SMTP_KEY', ''),
    'smtp_server': os.getenv('BREVO_SMTP_HOST', 'smtp-relay.brevo.com'),
    'smtp_port': int(os.getenv('BREVO_SMTP_PORT', '587')),
    'from_email': os.getenv('FROM_EMAIL', 'hello@firstcityfoundry.com'),
    'from_name': 'First City Foundry',
    'use_tls': True
}

# SendGrid Configuration (Alternative)
SENDGRID_CONFIG = {
    'api_key': 'your-sendgrid-api-key',
    'from_email': 'team@open.build',
    'from_name': 'Buildly Labs Foundry Team'
}

# Rate Limiting
RATE_LIMITS = {
    'min_delay': 30,  # Minimum seconds between requests
    'max_delay': 60,  # Maximum seconds between requests
    'max_daily_outreach': 50,  # Maximum emails per day
    'max_per_organization': 4,  # Maximum contacts per organization
    'min_per_organization': 2   # Minimum contacts per organization
}

# Search API Configuration (Optional)
SEARCH_CONFIG = {
    'google_api_key': 'your-google-api-key',
    'google_cse_id': 'your-custom-search-engine-id',
    'bing_api_key': 'your-bing-api-key',
    'use_search_apis': False  # Set to True when APIs are configured
}

# Site Information
SITE_CONFIG = {
    'name': 'First City Foundry',
    'url': 'https://www.firstcityfoundry.com',
    'contact_email': 'hello@firstcityfoundry.com',
    'description': 'Portland-based startup foundry — AI tools, community, and structured support for solo founders',
    'partners': ['Buildly', 'Kurent Co', 'Open.Build', 'Startup Grind PDX', 'Prepare4VC'],
    'key_features': [
        'AI-powered startup analysis via the VMI Index',
        'Structured founder-to-CEO pathways',
        'Global partner ecosystem',
        'Portland Metro regional focus',
        'Free cloud hosting and developer tools'
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'file': 'outreach.log',
    'max_file_size': '10MB',
    'backup_count': 5
}

# Data Directories
DATA_CONFIG = {
    'base_dir': 'outreach_data',
    'contacts_file': 'contacts.json',
    'targets_file': 'targets.json',
    'outreach_log_file': 'outreach_log.json',
    'analytics_file': 'analytics.json'
}

# Advanced Features
ADVANCED_CONFIG = {
    'use_ai_personalization': False,  # Requires OpenAI API
    'openai_api_key': 'your-openai-api-key',
    'use_selenium': False,  # For JavaScript-heavy sites
    'proxy_rotation': False,  # For large-scale scraping
    'social_media_integration': False  # Twitter, LinkedIn APIs
}

# Interactive CLI Configuration
CLI_CONFIG = {
    'interactive_mode': True,  # Show preview before sending
    'auto_approve_trusted': False,  # Auto-approve known good contacts
    'batch_size': 5,  # Number of messages to preview at once
    'show_full_message': True,  # Show complete message in preview
    'require_confirmation': True  # Require explicit confirmation
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    'daily_summary': True,  # Send daily summary
    'summary_time': '09:00',  # Time for daily summary (24-hour format)
    'notification_email': 'greg@open.build',  # Where to send notifications
    'include_analytics': True,  # Include performance metrics
    'include_pending_approvals': True  # Show messages waiting for approval
}
