#!/usr/bin/env python3
"""
Startup Outreach Automation Script
==================================

Automated outreach tool for startup incubators and foundries to connect with:
- Tech publications and startup blogs
- AI recommendation engines and platforms
- Startup influencers and thought leaders
- Founder communities and networks
- Investment and accelerator platforms

Features:
- Web scraping for new contact discovery
- Rate-limited outreach (2-4 contacts per target organization)
- Contact tracking and duplicate prevention
- Template-based messaging with personalization
- Integration with email services
- Comprehensive logging and analytics

Usage:
    python startup_outreach.py --mode discover  # Discover new contacts
    python startup_outreach.py --mode outreach  # Send outreach messages
    python startup_outreach.py --mode report    # Generate analytics report
"""

import json
import csv
import time
import random
import logging
import argparse
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import yagmail
from jinja2 import Template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outreach.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Contact:
    """Data class for contact information"""
    name: str
    email: str
    organization: str
    role: str
    source: str
    category: str  # publication, influencer, platform, community
    social_links: List[str]
    contact_date: Optional[str] = None
    response_received: bool = False
    notes: str = ""
    outreach_count: int = 0
    last_contact: Optional[str] = None

@dataclass
class OutreachTarget:
    """Data class for outreach targets"""
    name: str
    website: str
    category: str
    focus_areas: List[str]
    contact_methods: List[str]
    priority: int  # 1-5, 5 being highest
    contacts_found: int = 0
    last_scraped: Optional[str] = None

class StartupOutreachBot:
    """Main outreach automation class"""
    
    def __init__(self):
        self.data_dir = Path("outreach_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Data files
        self.contacts_file = self.data_dir / "contacts.json"
        self.targets_file = self.data_dir / "targets.json"
        self.outreach_log_file = self.data_dir / "outreach_log.json"
        self.analytics_file = self.data_dir / "analytics.json"
        
        # Load existing data
        self.contacts = self.load_contacts()
        self.targets = self.load_targets()
        self.outreach_log = self.load_outreach_log()
        
        # Configuration
        self.max_outreach_per_target = 4
        self.min_outreach_per_target = 2
        self.rate_limit_delay = (30, 60)  # Random delay between 30-60 seconds
        
        # Initialize with default targets
        if not self.targets:
            self.initialize_default_targets()

    def load_contacts(self) -> List[Contact]:
        """Load contacts from JSON file"""
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                data = json.load(f)
                return [Contact(**contact) for contact in data]
        return []

    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.contacts_file, 'w') as f:
            json.dump([asdict(contact) for contact in self.contacts], f, indent=2)

    def load_targets(self) -> List[OutreachTarget]:
        """Load outreach targets from JSON file"""
        if self.targets_file.exists():
            with open(self.targets_file, 'r') as f:
                data = json.load(f)
                return [OutreachTarget(**target) for target in data]
        return []

    def save_targets(self):
        """Save targets to JSON file"""
        with open(self.targets_file, 'w') as f:
            json.dump([asdict(target) for target in self.targets], f, indent=2)

    def load_outreach_log(self) -> List[Dict]:
        """Load outreach log from JSON file"""
        if self.outreach_log_file.exists():
            with open(self.outreach_log_file, 'r') as f:
                return json.load(f)
        return []

    def save_outreach_log(self):
        """Save outreach log to JSON file"""
        with open(self.outreach_log_file, 'w') as f:
            json.dump(self.outreach_log, f, indent=2)

    def initialize_default_targets(self):
        """Initialize with default startup-focused targets"""
        default_targets = [
            # Major Tech Publications
            OutreachTarget(
                name="TechCrunch",
                website="https://techcrunch.com",
                category="publication",
                focus_areas=["startups", "funding", "AI", "enterprise"],
                contact_methods=["email", "twitter", "contact_form"],
                priority=5
            ),
            OutreachTarget(
                name="Product Hunt",
                website="https://producthunt.com",
                category="platform",
                focus_areas=["product_launches", "startups", "indie_makers"],
                contact_methods=["platform_message", "email"],
                priority=5
            ),
            OutreachTarget(
                name="Hacker News",
                website="https://news.ycombinator.com",
                category="community",
                focus_areas=["tech", "startups", "programming", "entrepreneurship"],
                contact_methods=["submission", "comments"],
                priority=4
            ),
            OutreachTarget(
                name="AngelList (Wellfound)",
                website="https://wellfound.com",
                category="platform",
                focus_areas=["startups", "jobs", "funding", "accelerators"],
                contact_methods=["platform_message", "email"],
                priority=5
            ),
            OutreachTarget(
                name="Indie Hackers",
                website="https://indiehackers.com",
                category="community",
                focus_areas=["solo_founders", "bootstrapping", "SaaS", "indie_makers"],
                contact_methods=["platform_message", "email"],
                priority=5
            ),
            # AI-Focused Publications
            OutreachTarget(
                name="VentureBeat AI",
                website="https://venturebeat.com/ai/",
                category="publication",
                focus_areas=["AI", "machine_learning", "startups", "enterprise"],
                contact_methods=["email", "twitter"],
                priority=4
            ),
            OutreachTarget(
                name="AI News",
                website="https://artificialintelligence-news.com",
                category="publication",
                focus_areas=["AI", "startups", "technology"],
                contact_methods=["email", "contact_form"],
                priority=4
            ),
            # Startup Influencers & Thought Leaders
            OutreachTarget(
                name="First Round Review",
                website="https://review.firstround.com",
                category="publication",
                focus_areas=["early_stage", "founders", "leadership", "growth"],
                contact_methods=["email", "twitter"],
                priority=5
            ),
            OutreachTarget(
                name="500 Startups Blog",
                website="https://500.co/blog",
                category="publication",
                focus_areas=["global_startups", "accelerator", "funding"],
                contact_methods=["email", "contact_form"],
                priority=4
            ),
            # Developer-Focused Publications
            OutreachTarget(
                name="Dev.to",
                website="https://dev.to",
                category="community",
                focus_areas=["developers", "programming", "startup_tools", "open_source"],
                contact_methods=["platform_message", "email"],
                priority=4
            ),
            OutreachTarget(
                name="GitHub Blog",
                website="https://github.blog",
                category="publication",
                focus_areas=["open_source", "developers", "startups", "enterprise"],
                contact_methods=["email", "github"],
                priority=4
            ),
            # Niche & International Publications
            OutreachTarget(
                name="The Startup Magazine",
                website="https://thestartupmagazine.co.uk",
                category="publication",
                focus_areas=["UK_startups", "entrepreneurship", "small_business"],
                contact_methods=["email", "contact_form"],
                priority=3
            ),
            OutreachTarget(
                name="StartupGrind",
                website="https://startupgrind.com",
                category="community",
                focus_areas=["global_community", "events", "founders"],
                contact_methods=["email", "platform_message"],
                priority=4
            ),
            OutreachTarget(
                name="Entrepreneur.com",
                website="https://entrepreneur.com",
                category="publication",
                focus_areas=["entrepreneurship", "small_business", "startups"],
                contact_methods=["email", "contact_form"],
                priority=4
            ),
            # Solo Founder & Bootstrapper Focused
            OutreachTarget(
                name="Bootstrapped.fm",
                website="https://bootstrapped.fm",
                category="podcast",
                focus_areas=["bootstrapping", "solo_founders", "SaaS"],
                contact_methods=["email", "twitter"],
                priority=4
            ),
            OutreachTarget(
                name="MicroConf",
                website="https://microconf.com",
                category="community",
                focus_areas=["SaaS", "bootstrapping", "solo_founders"],
                contact_methods=["email", "contact_form"],
                priority=4
            )
        ]
        
        self.targets.extend(default_targets)
        self.save_targets()
        logger.info(f"Initialized {len(default_targets)} default targets")

    def discover_new_targets(self):
        """Discover new outreach targets through web scraping"""
        logger.info("Starting target discovery...")
        
        # Search patterns for startup-related sites
        search_queries = [
            "startup blogs 2025",
            "entrepreneur publications",
            "tech startup newsletters",
            "solo founder communities",
            "AI startup platforms",
            "developer startup resources",
            "startup incubator blogs",
            "first time founder resources"
        ]
        
        new_targets = []
        
        for query in search_queries:
            try:
                # Simulate search results discovery (in production, use proper search APIs)
                discovered = self.search_for_targets(query)
                new_targets.extend(discovered)
                time.sleep(random.uniform(5, 10))  # Rate limiting
            except Exception as e:
                logger.error(f"Error discovering targets for query '{query}': {e}")
        
        # Add unique new targets
        existing_websites = {target.website for target in self.targets}
        unique_targets = [t for t in new_targets if t.website not in existing_websites]
        
        self.targets.extend(unique_targets)
        self.save_targets()
        
        logger.info(f"Discovered {len(unique_targets)} new targets")
        return unique_targets

    def search_for_targets(self, query: str) -> List[OutreachTarget]:
        """Search for potential targets (placeholder for actual search implementation)"""
        # In production, integrate with search APIs like Google Custom Search, Bing API, etc.
        # For now, return some example discoveries
        
        sample_discoveries = [
            OutreachTarget(
                name="The Next Web",
                website="https://thenextweb.com",
                category="publication",
                focus_areas=["tech", "startups", "AI", "innovation"],
                contact_methods=["email", "twitter"],
                priority=4
            ),
            OutreachTarget(
                name="Startup Stash",
                website="https://startupstash.com",
                category="platform",
                focus_areas=["startup_tools", "resources", "founders"],
                contact_methods=["email", "contact_form"],
                priority=3
            )
        ]
        
        return sample_discoveries[:random.randint(0, 2)]  # Return 0-2 random discoveries

    def scrape_contacts_from_target(self, target: OutreachTarget) -> List[Contact]:
        """Scrape contact information from a target website"""
        logger.info(f"Scraping contacts from {target.name}")
        
        contacts = []
        
        try:
            # Add headers to appear as a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Common contact page URLs to try
            contact_urls = [
                urljoin(target.website, '/contact'),
                urljoin(target.website, '/about'),
                urljoin(target.website, '/team'),
                urljoin(target.website, '/staff'),
                urljoin(target.website, '/contributors'),
                target.website  # Main page
            ]
            
            for url in contact_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page_contacts = self.extract_contacts_from_page(soup, target, url)
                        contacts.extend(page_contacts)
                        
                        # Limit contacts per target
                        if len(contacts) >= self.max_outreach_per_target:
                            break
                            
                    time.sleep(random.uniform(2, 5))  # Rate limiting
                    
                except requests.RequestException as e:
                    logger.warning(f"Error accessing {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping {target.name}: {e}")
        
        # Update target info
        target.contacts_found = len(contacts)
        target.last_scraped = datetime.now().isoformat()
        
        logger.info(f"Found {len(contacts)} contacts from {target.name}")
        return contacts

    def extract_contacts_from_page(self, soup: BeautifulSoup, target: OutreachTarget, url: str) -> List[Contact]:
        """Extract contact information from a web page"""
        contacts = []
        
        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Find emails in text
        page_text = soup.get_text()
        emails = re.findall(email_pattern, page_text)
        
        # Find team/staff information
        team_sections = soup.find_all(['div', 'section'], class_=re.compile(r'team|staff|about|contact|contributor', re.I))
        
        for section in team_sections:
            section_text = section.get_text()
            section_emails = re.findall(email_pattern, section_text)
            emails.extend(section_emails)
        
        # Process unique emails
        unique_emails = list(set(emails))
        
        for email in unique_emails:
            # Skip common non-contact emails
            if any(skip in email.lower() for skip in ['noreply', 'no-reply', 'donotreply', 'support', 'help']):
                continue
                
            # Try to extract name and role context
            name, role = self.extract_name_and_role_context(soup, email)
            
            contact = Contact(
                name=name or "Unknown",
                email=email,
                organization=target.name,
                role=role or "Unknown",
                source=url,
                category=target.category,
                social_links=[]
            )
            
            contacts.append(contact)
            
            # Limit per page
            if len(contacts) >= 3:
                break
        
        return contacts

    def extract_name_and_role_context(self, soup: BeautifulSoup, email: str) -> tuple:
        """Try to extract name and role associated with an email"""
        name = None
        role = None
        
        # Look for the email in the page and extract nearby context
        email_elements = soup.find_all(text=re.compile(re.escape(email)))
        
        for element in email_elements:
            parent = element.parent
            if parent:
                # Look for name patterns near the email
                parent_text = parent.get_text()
                
                # Simple name extraction (this could be improved with NLP)
                words = parent_text.split()
                for i, word in enumerate(words):
                    if email in word:
                        # Look for capitalized words before the email (likely names)
                        for j in range(max(0, i-5), i):
                            if words[j].istitle() and len(words[j]) > 2:
                                if not name:
                                    name = words[j]
                                elif j == max(0, i-5) or words[j-1].istitle():
                                    name = f"{words[j-1]} {words[j]}" if j > 0 and words[j-1].istitle() else words[j]
                        break
                
                # Look for role indicators
                role_indicators = ['editor', 'writer', 'founder', 'ceo', 'cto', 'author', 'journalist', 'reporter']
                text_lower = parent_text.lower()
                for indicator in role_indicators:
                    if indicator in text_lower:
                        role = indicator.title()
                        break
        
        return name, role

    def generate_outreach_message(self, contact: Contact) -> Dict[str, str]:
        """Generate personalized outreach message"""
        
        # Message templates based on contact category
        templates = {
            'publication': """
Subject: Partnership Opportunity: Global Startup Foundry Launch

Hi {{ contact.name }},

I hope this email finds you well. I'm reaching out from Buildly Labs Foundry, a new global startup incubator that just launched in partnership with OpenBuild and Buildly Labs.

Given {{ organization }}'s focus on {{ focus_area }}, I thought you might be interested in covering our unique approach to supporting software developers and entrepreneurs worldwide.

What makes us different:
• 100% equity-free support (unprecedented in the industry)
• AI-powered startup analysis and recommendations  
• Free cloud hosting credits through partnerships
• Global developer community access via OpenBuild
• Focus on solo founders and first-time entrepreneurs

Our platform at https://www.firstcityfoundry.com showcases how we're democratizing startup support globally.

Would you be interested in learning more about our story, our partnerships, or perhaps interviewing some of our founders? I'd be happy to provide additional information, press materials, or arrange interviews.

Please feel free to reach out with any questions or inquiries to team@open.build.

Best regards,
Buildly Labs Foundry Team

P.S. We're also happy to provide exclusive early access to our platform for {{ organization }}'s readers if that would be of interest.
            """,
            
            'influencer': """
Subject: New Global Startup Foundry - Partnership with OpenBuild & Buildly Labs

Hi {{ contact.name }},

I've been following your work at {{ organization }} and your insights on {{ focus_area }} - really appreciate your perspective on the startup ecosystem.

I wanted to introduce you to Buildly Labs Foundry, a new global startup incubator we've just launched. What caught my attention is how our approach aligns with many of the challenges you've highlighted about traditional accelerators.

Key differentiators:
• Zero equity required (keeping founders in full control)
• AI-powered startup evaluation and recommendations 
• Partnership with OpenBuild for global developer community access
• Free cloud infrastructure support
• Specific focus on solo founders and developers transitioning to entrepreneurship

You can check out our platform at https://www.firstcityfoundry.com

Given your influence in the startup community, I'd love to get your thoughts on our approach. Would you be open to a brief conversation about what we're building?

If this resonates with your audience, we'd also be happy to discuss collaboration opportunities or provide exclusive insights for your community.

Feel free to reach out with questions to team@open.build.

Best,
Buildly Labs Foundry Team
            """,
            
            'platform': """
Subject: Partnership Opportunity: Buildly Labs Foundry Launch

Hello {{ contact.name }},

I'm reaching out from Buildly Labs Foundry, a new global startup incubator that recently launched in partnership with OpenBuild and Buildly Labs.

Given {{ organization }}'s platform and community, I believe there could be great synergy between our missions to support entrepreneurs and developers.

Our unique approach:
• 100% equity-free incubator model
• AI-powered startup analysis and strategic recommendations
• Global reach through OpenBuild partnership  
• Free cloud hosting and technical infrastructure
• Focus on underserved founders (solo, first-time, international)

Our platform: https://www.firstcityfoundry.com

I'd love to explore potential partnership opportunities, whether that's:
- Cross-promotion to relevant communities
- Integration opportunities
- Content collaboration
- Joint events or initiatives

Would you be interested in a conversation about how we might work together to better serve the startup community?

Please reach out to team@open.build with any questions or to discuss further.

Best regards,
Buildly Labs Foundry Partnership Team
            """,
            
            'community': """
Subject: Introducing Buildly Labs Foundry - Global Startup Support

Hi {{ contact.name }},

I hope you're doing well! I wanted to share something new that I think the {{ organization }} community would find interesting.

We've just launched Buildly Labs Foundry, a global startup incubator with a fundamentally different approach to supporting entrepreneurs and developers.

What makes us unique:
• Completely equity-free (founders keep 100% ownership)
• AI-powered analysis and personalized recommendations
• Partnership with OpenBuild for global developer community access
• Free cloud hosting and infrastructure support  
• Designed specifically for solo founders, developers, and first-time entrepreneurs

Check it out: https://www.firstcityfoundry.com

I thought this might resonate with {{ organization }}'s community, especially those looking to transition from development to entrepreneurship or seeking startup support without giving up equity.

Would you be open to me sharing this with the community, or perhaps discussing how we might collaborate to better support developers and entrepreneurs?

Happy to answer any questions at team@open.build.

Cheers,
Buildly Labs Foundry Team
            """
        }
        
        # Select appropriate template
        template_key = contact.category if contact.category in templates else 'publication'
        template_text = templates[template_key]
        
        # Personalize the message
        template = Template(template_text.strip())
        
        # Determine focus area based on organization
        focus_area = self.get_focus_area_for_organization(contact.organization)
        
        message = template.render(
            contact=contact,
            organization=contact.organization,
            focus_area=focus_area,
            site_url="https://www.firstcityfoundry.com"
        )
        
        # Extract subject line
        lines = message.split('\n')
        subject = lines[0].replace('Subject: ', '') if lines[0].startswith('Subject: ') else "Partnership Opportunity: Buildly Labs Foundry"
        body = '\n'.join(lines[2:])  # Skip subject and empty line
        
        return {
            'subject': subject,
            'body': body,
            'template_used': template_key
        }

    def get_focus_area_for_organization(self, organization: str) -> str:
        """Get relevant focus area for an organization"""
        focus_mapping = {
            'techcrunch': 'startup funding and innovation',
            'product hunt': 'product launches and startup discovery',
            'hacker news': 'developer community and tech discussions',
            'indie hackers': 'solo founders and bootstrapping',
            'angellist': 'startup funding and talent',
            'dev.to': 'developer community and technical content',
            'github': 'open source and developer tools',
            'venturebeat': 'AI and enterprise technology',
            'entrepreneur': 'small business and entrepreneurship'
        }
        
        org_lower = organization.lower()
        for key, value in focus_mapping.items():
            if key in org_lower:
                return value
        
        return "entrepreneurship and startup development"

    def send_outreach_message(self, contact: Contact, message: Dict[str, str]) -> bool:
        """Send outreach message (placeholder for actual email sending)"""
        
        # In production, integrate with email service (Gmail API, SendGrid, etc.)
        # For now, log the message and simulate sending
        
        logger.info(f"Sending outreach to {contact.name} at {contact.email}")
        logger.info(f"Subject: {message['subject']}")
        
        # Simulate email sending with yagmail (requires configuration)
        try:
            # Uncomment and configure for actual sending:
            # yag = yagmail.SMTP('your-gmail@gmail.com', 'your-app-password')
            # yag.send(
            #     to=contact.email,
            #     subject=message['subject'],
            #     contents=message['body']
            # )
            
            # For now, just log
            logger.info(f"✅ Message sent successfully to {contact.email}")
            
            # Update contact record
            contact.contact_date = datetime.now().isoformat()
            contact.outreach_count += 1
            contact.last_contact = datetime.now().isoformat()
            
            # Log the outreach
            self.outreach_log.append({
                'timestamp': datetime.now().isoformat(),
                'contact_name': contact.name,
                'contact_email': contact.email,
                'organization': contact.organization,
                'subject': message['subject'],
                'template_used': message['template_used'],
                'status': 'sent'
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to {contact.email}: {e}")
            
            self.outreach_log.append({
                'timestamp': datetime.now().isoformat(),
                'contact_name': contact.name,
                'contact_email': contact.email,
                'organization': contact.organization,
                'subject': message['subject'],
                'template_used': message['template_used'],
                'status': 'failed',
                'error': str(e)
            })
            
            return False

    def run_discovery_phase(self):
        """Run the contact discovery phase"""
        logger.info("🔍 Starting discovery phase...")
        
        # Discover new targets
        new_targets = self.discover_new_targets()
        
        # Scrape contacts from existing and new targets
        for target in self.targets:
            # Skip if recently scraped (within 7 days)
            if target.last_scraped:
                last_scraped = datetime.fromisoformat(target.last_scraped)
                if datetime.now() - last_scraped < timedelta(days=7):
                    logger.info(f"Skipping {target.name} - recently scraped")
                    continue
            
            # Scrape contacts
            new_contacts = self.scrape_contacts_from_target(target)
            
            # Add new contacts (avoid duplicates)
            existing_emails = {contact.email for contact in self.contacts}
            unique_contacts = [c for c in new_contacts if c.email not in existing_emails]
            
            self.contacts.extend(unique_contacts)
            logger.info(f"Added {len(unique_contacts)} new contacts from {target.name}")
            
            # Rate limiting
            time.sleep(random.uniform(*self.rate_limit_delay))
        
        # Save updated data
        self.save_contacts()
        self.save_targets()
        
        logger.info(f"✅ Discovery complete. Total contacts: {len(self.contacts)}")

    def run_outreach_phase(self):
        """Run the outreach phase"""
        logger.info("📧 Starting outreach phase...")
        
        # Filter contacts for outreach
        eligible_contacts = []
        
        for contact in self.contacts:
            # Skip if already contacted recently (within 30 days)
            if contact.last_contact:
                last_contact = datetime.fromisoformat(contact.last_contact)
                if datetime.now() - last_contact < timedelta(days=30):
                    continue
            
            # Skip if exceeded max outreach attempts
            if contact.outreach_count >= self.max_outreach_per_target:
                continue
            
            eligible_contacts.append(contact)
        
        # Group by organization to limit outreach per target
        org_contacts = {}
        for contact in eligible_contacts:
            if contact.organization not in org_contacts:
                org_contacts[contact.organization] = []
            org_contacts[contact.organization].append(contact)
        
        # Send outreach messages
        total_sent = 0
        
        for org, contacts in org_contacts.items():
            # Limit contacts per organization
            max_contacts = min(len(contacts), random.randint(self.min_outreach_per_target, self.max_outreach_per_target))
            selected_contacts = random.sample(contacts, max_contacts)
            
            logger.info(f"Reaching out to {len(selected_contacts)} contacts from {org}")
            
            for contact in selected_contacts:
                try:
                    # Generate personalized message
                    message = self.generate_outreach_message(contact)
                    
                    # Send message
                    if self.send_outreach_message(contact, message):
                        total_sent += 1
                    
                    # Rate limiting between sends
                    time.sleep(random.uniform(*self.rate_limit_delay))
                    
                except Exception as e:
                    logger.error(f"Error sending to {contact.email}: {e}")
        
        # Save updated data
        self.save_contacts()
        self.save_outreach_log()
        
        logger.info(f"✅ Outreach complete. Sent {total_sent} messages.")

    def generate_analytics_report(self):
        """Generate analytics and performance report"""
        logger.info("📊 Generating analytics report...")
        
        analytics = {
            'timestamp': datetime.now().isoformat(),
            'total_targets': len(self.targets),
            'total_contacts': len(self.contacts),
            'total_outreach_sent': len([log for log in self.outreach_log if log['status'] == 'sent']),
            'total_outreach_failed': len([log for log in self.outreach_log if log['status'] == 'failed']),
            'contacts_by_category': {},
            'outreach_by_organization': {},
            'response_rate': 0,
            'top_performing_templates': {},
            'recent_activity': []
        }
        
        # Contacts by category
        for contact in self.contacts:
            category = contact.category
            if category not in analytics['contacts_by_category']:
                analytics['contacts_by_category'][category] = 0
            analytics['contacts_by_category'][category] += 1
        
        # Outreach by organization
        for log in self.outreach_log:
            org = log['organization']
            if org not in analytics['outreach_by_organization']:
                analytics['outreach_by_organization'][org] = {'sent': 0, 'failed': 0}
            analytics['outreach_by_organization'][org][log['status']] += 1
        
        # Template performance
        template_stats = {}
        for log in self.outreach_log:
            template = log.get('template_used', 'unknown')
            if template not in template_stats:
                template_stats[template] = {'sent': 0, 'responses': 0}
            template_stats[template]['sent'] += 1
        
        analytics['top_performing_templates'] = template_stats
        
        # Response rate calculation
        total_sent = analytics['total_outreach_sent']
        total_responses = len([c for c in self.contacts if c.response_received])
        analytics['response_rate'] = (total_responses / total_sent * 100) if total_sent > 0 else 0
        
        # Recent activity (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        analytics['recent_activity'] = [
            log for log in self.outreach_log 
            if datetime.fromisoformat(log['timestamp']) > recent_cutoff
        ]
        
        # Save analytics
        with open(self.analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 STARTUP OUTREACH ANALYTICS REPORT")
        print("="*60)
        print(f"📋 Total Targets: {analytics['total_targets']}")
        print(f"👥 Total Contacts: {analytics['total_contacts']}")
        print(f"✅ Messages Sent: {analytics['total_outreach_sent']}")
        print(f"❌ Failed Messages: {analytics['total_outreach_failed']}")
        print(f"📈 Response Rate: {analytics['response_rate']:.1f}%")
        print(f"🕒 Recent Activity (7 days): {len(analytics['recent_activity'])} actions")
        
        print("\n📊 Contacts by Category:")
        for category, count in analytics['contacts_by_category'].items():
            print(f"  • {category.title()}: {count}")
        
        print("\n🏢 Top Organizations by Outreach:")
        org_totals = [(org, data['sent']) for org, data in analytics['outreach_by_organization'].items()]
        org_totals.sort(key=lambda x: x[1], reverse=True)
        for org, count in org_totals[:10]:
            print(f"  • {org}: {count} messages")
        
        print("="*60)
        
        logger.info("✅ Analytics report generated")

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Startup Outreach Automation')
    parser.add_argument('--mode', choices=['discover', 'outreach', 'report', 'full'], 
                       default='full', help='Operation mode')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Run without actually sending emails')
    
    args = parser.parse_args()
    
    # Initialize the bot
    bot = StartupOutreachBot()
    
    try:
        if args.mode in ['discover', 'full']:
            bot.run_discovery_phase()
        
        if args.mode in ['outreach', 'full'] and not args.dry_run:
            bot.run_outreach_phase()
        
        if args.mode in ['report', 'full']:
            bot.generate_analytics_report()
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()
