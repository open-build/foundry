#!/usr/bin/env python3
"""
Add New Targets Script
======================

Script to add new startup-focused targets to the outreach system.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import startup_outreach
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(current_dir))

# Import directly from startup_outreach module
from startup_outreach import OutreachTarget, StartupOutreachBot

def add_new_startup_targets():
    """Add new startup-focused targets to expand outreach reach"""
    
    # Initialize the bot
    bot = StartupOutreachBot()
    
    # New targets focused on startups, solo founders, and developer entrepreneurship
    new_targets = [
        OutreachTarget(
            name="Y Combinator Blog",
            website="https://blog.ycombinator.com",
            category="publication",
            focus_areas=["startups", "funding", "accelerators", "entrepreneurship"],
            contact_methods=["email", "contact_form"],
            priority=5
        ),
        OutreachTarget(
            name="Stripe Blog",
            website="https://stripe.com/blog",
            category="publication",
            focus_areas=["fintech", "startups", "developers", "SaaS"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="a16z Blog",
            website="https://a16z.com/blog",
            category="publication",
            focus_areas=["venture_capital", "startups", "AI", "enterprise"],
            contact_methods=["email", "contact_form"],
            priority=5
        ),
        OutreachTarget(
            name="Founder Stories",
            website="https://founderstories.org",
            category="publication",
            focus_areas=["founder_stories", "entrepreneurship", "startups"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="SaaStr",
            website="https://saastr.com",
            category="community",
            focus_areas=["SaaS", "startups", "funding", "scaling"],
            contact_methods=["email", "platform_message"],
            priority=5
        ),
        OutreachTarget(
            name="Foundr Magazine",
            website="https://foundr.com",
            category="publication",
            focus_areas=["entrepreneurship", "startups", "business", "solo_founders"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="NoCode Founders",
            website="https://nocodefounders.com",
            category="community",
            focus_areas=["no_code", "solo_founders", "indie_makers", "bootstrapping"],
            contact_methods=["email", "platform_message"],
            priority=4
        ),
        OutreachTarget(
            name="Maker Mag",
            website="https://makermag.com",
            category="publication",
            focus_areas=["indie_makers", "solo_founders", "product_development"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="RemoteOK Blog",
            website="https://remoteok.io/blog",
            category="publication",
            focus_areas=["remote_work", "startups", "developers", "entrepreneurs"],
            contact_methods=["email", "contact_form"],
            priority=3
        ),
        OutreachTarget(
            name="Nomad List",
            website="https://nomadlist.com",
            category="community",
            focus_areas=["digital_nomads", "remote_entrepreneurs", "startups"],
            contact_methods=["platform_message", "email"],
            priority=3
        ),
        OutreachTarget(
            name="Startup Grind Global",
            website="https://startupgrind.com/blog",
            category="publication",
            focus_areas=["startups", "entrepreneurship", "community", "events"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="Mind the Product",
            website="https://mindtheproduct.com",
            category="publication",
            focus_areas=["product_management", "startups", "tech", "innovation"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="The Hustle",
            website="https://thehustle.co",
            category="publication",
            focus_areas=["business", "startups", "entrepreneurship", "trends"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="Substack",
            website="https://substack.com",
            category="platform",
            focus_areas=["creators", "newsletters", "indie_creators", "writers"],
            contact_methods=["platform_message", "email"],
            priority=3
        ),
        OutreachTarget(
            name="Built In",
            website="https://builtin.com",
            category="publication",
            focus_areas=["tech", "startups", "careers", "innovation"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="Fast Company",
            website="https://fastcompany.com",
            category="publication",
            focus_areas=["innovation", "startups", "business", "technology"],
            contact_methods=["email", "contact_form"],
            priority=4
        ),
        OutreachTarget(
            name="TechStars Blog",
            website="https://techstars.com/blog",
            category="publication",
            focus_areas=["startups", "accelerators", "funding", "mentorship"],
            contact_methods=["email", "contact_form"],
            priority=5
        ),
        OutreachTarget(
            name="AngelList Blog",
            website="https://angel.co/blog",
            category="publication",
            focus_areas=["startups", "funding", "venture_capital", "jobs"],
            contact_methods=["email", "platform_message"],
            priority=5
        ),
        OutreachTarget(
            name="Crunchbase News",
            website="https://news.crunchbase.com",
            category="publication",
            focus_areas=["startups", "funding", "venture_capital", "M&A"],
            contact_methods=["email", "contact_form"],
            priority=5
        ),
        OutreachTarget(
            name="Hacker Noon",
            website="https://hackernoon.com",
            category="publication",
            focus_areas=["tech", "startups", "programming", "entrepreneurship"],
            contact_methods=["email", "platform_message"],
            priority=4
        )
    ]
    
    # Filter out targets that already exist
    existing_websites = {target.website for target in bot.targets}
    unique_targets = [t for t in new_targets if t.website not in existing_websites]
    
    print(f"Found {len(unique_targets)} new targets to add (out of {len(new_targets)} total)")
    
    if unique_targets:
        # Add new targets
        bot.targets.extend(unique_targets)
        bot.save_targets()
        
        print("✅ Added new targets:")
        for target in unique_targets:
            print(f"  • {target.name} ({target.website})")
            
        print(f"\n🎯 Total targets now: {len(bot.targets)}")
        
        # Immediately try to scrape contacts from new targets
        print("\n🔍 Starting contact discovery for new targets...")
        
        for target in unique_targets[:5]:  # Limit to first 5 to avoid rate limits
            try:
                print(f"\nScraping {target.name}...")
                new_contacts = bot.scrape_contacts_from_target(target)
                
                # Add new contacts (avoid duplicates)
                existing_emails = {contact.email for contact in bot.contacts}
                unique_contacts = [c for c in new_contacts if c.email not in existing_emails]
                
                bot.contacts.extend(unique_contacts)
                print(f"  ✅ Added {len(unique_contacts)} new contacts from {target.name}")
                
                # Rate limiting
                import time, random
                time.sleep(random.uniform(10, 20))
                
            except Exception as e:
                print(f"  ❌ Error scraping {target.name}: {e}")
        
        # Save updated contacts
        bot.save_contacts()
        print(f"\n📊 Total contacts now: {len(bot.contacts)}")
        
    else:
        print("No new targets to add - all targets already exist")

if __name__ == "__main__":
    add_new_startup_targets()
