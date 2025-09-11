#!/usr/bin/env python3
"""
Preview Outreach Messages
=========================

Shows exactly what messages would be sent to discovered contacts.
"""

import json
import sys
import os
from pathlib import Path

# Add the scripts directory to Python path
sys.path.append(str(Path(__file__).parent))

from startup_outreach import StartupOutreachBot

def preview_messages():
    """Preview all outreach messages that would be sent"""
    
    print("🔍 BUILDLY LABS FOUNDRY - OUTREACH PREVIEW")
    print("=" * 80)
    
    # Initialize bot
    bot = StartupOutreachBot()
    
    if not bot.contacts:
        print("❌ No contacts found. Run discovery first: python3 startup_outreach.py --mode discover")
        return
    
    print(f"📊 Found {len(bot.contacts)} total contacts")
    print(f"📧 Will reach out to contacts from these organizations:")
    
    # Group contacts by organization
    org_contacts = {}
    for contact in bot.contacts:
        # Skip if already contacted recently
        if contact.outreach_count >= bot.max_outreach_per_target:
            continue
            
        if contact.organization not in org_contacts:
            org_contacts[contact.organization] = []
        org_contacts[contact.organization].append(contact)
    
    for org, contacts in org_contacts.items():
        max_contacts = min(len(contacts), bot.max_outreach_per_target)
        print(f"  • {org}: {max_contacts} contacts")
    
    print("\n" + "=" * 80)
    print("📧 SAMPLE OUTREACH MESSAGES")
    print("=" * 80)
    
    # Show sample messages for each organization
    message_count = 0
    for org, contacts in org_contacts.items():
        if message_count >= 3:  # Show only first 3 organizations
            break
            
        contact = contacts[0]  # Show message for first contact
        message = bot.generate_outreach_message(contact)
        
        print(f"\n📨 MESSAGE {message_count + 1}: TO {contact.organization}")
        print("-" * 60)
        print(f"To: {contact.email}")
        print(f"From: {os.getenv('FROM_EMAIL', 'team@open.build')}")
        print(f"Subject: {message['subject']}")
        print(f"Template: {message['template_used']}")
        print("\nMessage Body:")
        print(message['body'])
        print("-" * 60)
        
        message_count += 1
    
    print(f"\n✅ Preview complete. Would send to {sum(min(len(contacts), bot.max_outreach_per_target) for contacts in org_contacts.values())} contacts total.")
    print(f"🔧 To actually send: python3 startup_outreach.py --mode outreach")
    print(f"🧪 To test safely: python3 startup_outreach.py --mode outreach --dry-run")

if __name__ == "__main__":
    preview_messages()
