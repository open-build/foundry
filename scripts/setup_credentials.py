#!/usr/bin/env python3
"""
Secure Credentials Setup for Startup Outreach Bot
=================================================

This script helps you securely configure your SMTP credentials.
"""

import os
from pathlib import Path
import getpass

def setup_brevo_credentials():
    """Securely set up Brevo SMTP credentials"""
    print("🔐 Setting up Brevo SMTP Credentials")
    print("=" * 50)
    
    env_file = Path(".env")
    
    # Read existing .env or create new
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key] = value
    
    print("Please provide your Brevo SMTP key:")
    print("(From your Brevo dashboard: Settings > SMTP & API)")
    print()
    
    # Get credentials securely
    smtp_key = getpass.getpass("BREVO SMTP Key (hidden input): ").strip()
    if smtp_key:
        env_content['BREVO_SMTP_KEY'] = smtp_key
    
    from_email = input("From Email Address (default: hello@firstcityfoundry.com): ").strip()
    if from_email:
        env_content['FROM_EMAIL'] = from_email
    else:
        env_content['FROM_EMAIL'] = 'hello@firstcityfoundry.com'
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write("# Environment Variables for First City Foundry\n")
        f.write("# NEVER commit this file to git!\n\n")
        
        f.write("# Brevo SMTP Configuration\n")
        f.write(f"BREVO_SMTP_KEY={env_content.get('BREVO_SMTP_KEY', '')}\n")
        f.write(f"FROM_EMAIL={env_content.get('FROM_EMAIL', 'hello@firstcityfoundry.com')}\n")
        
        # Add other optional variables
        f.write("\n# Optional: Search API Keys\n")
        f.write(f"GOOGLE_API_KEY={env_content.get('GOOGLE_API_KEY', '')}\n")
        f.write(f"OPENAI_API_KEY={env_content.get('OPENAI_API_KEY', '')}\n")
    
    print("\n✅ Credentials saved to .env file")
    print("⚠️  IMPORTANT: .env file is excluded from git for security")
    print("⚠️  Never share or commit your .env file!")
    
    # Test the connection
    print("\n🧪 Testing SMTP connection...")
    test_smtp_connection(env_content)

def test_smtp_connection(env_content):
    """Test SMTP connection with provided credentials"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        username = env_content.get('BREVO_SMTP_LOGIN')
        password = env_content.get('BREVO_SMTP_KEY')
        
        if not password:
            print("❌ Missing SMTP key, skipping connection test")
            return
        
        # Test connection
        server = smtplib.SMTP('smtp-relay.brevo.com', 587)
        server.starttls()
        server.login(username, password)
        server.quit()
        
        print("✅ SMTP connection successful!")
        print("✅ Ready to send outreach emails")
        
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        print("Please check your credentials and try again")

def show_security_reminder():
    """Show important security reminders"""
    print("\n" + "🔒 SECURITY REMINDERS" + "🔒")
    print("=" * 50)
    print("✅ Credentials are stored in .env file")
    print("✅ .env file is excluded from git")
    print("⚠️  Never commit credentials to version control")
    print("⚠️  Never share your .env file")
    print("⚠️  Use environment variables in production")
    print("⚠️  Rotate credentials regularly")
    print("=" * 50)

if __name__ == "__main__":
    setup_brevo_credentials()
    show_security_reminder()
