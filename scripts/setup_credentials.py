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
    
    print("Please provide your Brevo SMTP credentials:")
    print("(From your Brevo dashboard: Settings > SMTP & API)")
    print()
    
    # Get credentials securely
    username = input("BREVO SMTP Username (e.g., 96af72001@smtp-brevo.com): ").strip()
    if username:
        env_content['BREVO_SMTP_USERNAME'] = username
    
    password = getpass.getpass("BREVO Master Password (hidden input): ").strip()
    if password:
        env_content['BREVO_SMTP_PASSWORD'] = password
    
    from_email = input("From Email Address (default: team@open.build): ").strip()
    if from_email:
        env_content['FROM_EMAIL'] = from_email
    else:
        env_content['FROM_EMAIL'] = 'team@open.build'
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write("# Environment Variables for Startup Outreach Bot\n")
        f.write("# NEVER commit this file to git!\n\n")
        
        f.write("# Brevo SMTP Configuration\n")
        f.write(f"BREVO_SMTP_USERNAME={env_content.get('BREVO_SMTP_USERNAME', 'your-username')}\n")
        f.write(f"BREVO_SMTP_PASSWORD={env_content.get('BREVO_SMTP_PASSWORD', 'your-password')}\n")
        f.write(f"FROM_EMAIL={env_content.get('FROM_EMAIL', 'team@open.build')}\n")
        
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
        
        username = env_content.get('BREVO_SMTP_USERNAME')
        password = env_content.get('BREVO_SMTP_PASSWORD')
        
        if not username or not password:
            print("❌ Missing credentials, skipping connection test")
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
