# Startup Outreach Bot Configuration
# Copy this to config.py and update with your settings

# Email Configuration
EMAIL_CONFIG = {
    'service': 'gmail',  # 'gmail', 'sendgrid', 'smtp'
    'username': 'your-email@gmail.com',
    'password': 'your-app-password',  # Use app-specific password for Gmail
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'from_name': 'Buildly Labs Foundry Team'
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
    'name': 'Buildly Labs Foundry',
    'url': 'https://www.firstcityfoundry.com',
    'contact_email': 'team@open.build',
    'description': 'Global startup incubator and developer foundry',
    'partners': ['OpenBuild', 'Buildly Labs'],
    'key_features': [
        '100% equity-free support',
        'AI-powered startup analysis',
        'Free cloud hosting credits',
        'Global developer community access',
        'Focus on solo founders and developers'
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
