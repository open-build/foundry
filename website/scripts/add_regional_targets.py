#!/usr/bin/env python3
"""
Regional and International Targets Discovery
============================================

Adds smaller regional publications, angel groups, incubators, and accelerators
from around the world to expand outreach beyond major US platforms.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def get_regional_targets():
    """Return comprehensive list of regional and international targets"""
    return [
        # EUROPEAN STARTUP ECOSYSTEM
        {
            "name": "TechEU",
            "website": "https://tech.eu",
            "category": "publication",
            "focus_areas": ["European startups", "funding", "tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "EU-Startups",
            "website": "https://www.eu-startups.com",
            "category": "publication", 
            "focus_areas": ["European startups", "funding", "events"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "Tech.eu",
            "website": "https://tech.eu",
            "category": "publication",
            "focus_areas": ["European tech", "startups", "funding"],
            "contact_methods": ["email", "twitter"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "Sifted",
            "website": "https://sifted.eu",
            "category": "publication",
            "focus_areas": ["European startups", "VC", "tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "Rocket Internet",
            "website": "https://www.rocket-internet.com",
            "category": "platform",
            "focus_areas": ["incubator", "global startups", "scaling"],
            "contact_methods": ["email", "contact_form"],
            "priority": 3,
            "region": "Europe"
        },
        
        # UK SPECIFIC
        {
            "name": "TechCityNews",
            "website": "https://techcitynews.com",
            "category": "publication",
            "focus_areas": ["UK startups", "fintech", "tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "UK"
        },
        {
            "name": "UKTech.news",
            "website": "https://uktech.news",
            "category": "publication",
            "focus_areas": ["UK tech", "startups", "investment"],
            "contact_methods": ["email", "twitter"],
            "priority": 4,
            "region": "UK"
        },
        {
            "name": "Techround",
            "website": "https://techround.co.uk",
            "category": "publication",
            "focus_areas": ["UK startups", "tech news", "entrepreneurship"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "UK"
        },
        {
            "name": "Seedcamp",
            "website": "https://seedcamp.com",
            "category": "platform",
            "focus_areas": ["European accelerator", "early stage", "mentorship"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "UK"
        },
        {
            "name": "Techstars London",
            "website": "https://www.techstars.com/accelerators/london",
            "category": "platform", 
            "focus_areas": ["accelerator", "mentorship", "funding"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "UK"
        },
        
        # GERMANY
        {
            "name": "Deutsche Startups",
            "website": "https://www.deutsche-startups.de",
            "category": "publication",
            "focus_areas": ["German startups", "funding", "ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Germany"
        },
        {
            "name": "Gruenderszene",
            "website": "https://www.gruenderszene.de",
            "category": "publication",
            "focus_areas": ["German startups", "entrepreneurship", "investment"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Germany"
        },
        {
            "name": "Rocket Internet",
            "website": "https://www.rocket-internet.com",
            "category": "platform",
            "focus_areas": ["global incubator", "scaling", "international"],
            "contact_methods": ["email", "contact_form"],
            "priority": 3,
            "region": "Germany"
        },
        
        # FRANCE
        {
            "name": "Maddyness",
            "website": "https://www.maddyness.com",
            "category": "publication",
            "focus_areas": ["French startups", "innovation", "tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "France"
        },
        {
            "name": "Frenchweb",
            "website": "https://www.frenchweb.fr",
            "category": "publication",
            "focus_areas": ["French tech", "startups", "digital"],
            "contact_methods": ["email", "twitter"],
            "priority": 4,
            "region": "France"
        },
        {
            "name": "Station F",
            "website": "https://stationf.co",
            "category": "platform",
            "focus_areas": ["startup campus", "incubator", "French ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "France"
        },
        
        # NETHERLANDS
        {
            "name": "StartupJuncture",
            "website": "https://startupjuncture.com",
            "category": "publication",
            "focus_areas": ["Dutch startups", "ecosystem", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Netherlands"
        },
        {
            "name": "Rockstart",
            "website": "https://www.rockstart.com",
            "category": "platform",
            "focus_areas": ["accelerator", "early stage", "global"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Netherlands"
        },
        
        # NORDIC COUNTRIES
        {
            "name": "Arctic Startup",
            "website": "https://arcticstartup.com",
            "category": "publication",
            "focus_areas": ["Nordic startups", "ecosystem", "funding"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Nordic"
        },
        {
            "name": "Nordic Startup News",
            "website": "https://nordicstartupnews.com",
            "category": "publication",
            "focus_areas": ["Nordic ecosystem", "startups", "investment"],
            "contact_methods": ["email", "twitter"],
            "priority": 4,
            "region": "Nordic"
        },
        {
            "name": "Startup Norway",
            "website": "https://startupnorway.com",
            "category": "publication",
            "focus_areas": ["Norwegian startups", "ecosystem", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Norway"
        },
        
        # ASIA-PACIFIC
        {
            "name": "TechNode",
            "website": "https://technode.com",
            "category": "publication",
            "focus_areas": ["Chinese tech", "startups", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "China"
        },
        {
            "name": "KrAsia",
            "website": "https://kr-asia.com",
            "category": "publication",
            "focus_areas": ["Asian startups", "investment", "tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Asia"
        },
        {
            "name": "TechInAsia",
            "website": "https://www.techinasia.com",
            "category": "publication",
            "focus_areas": ["Asian tech", "startups", "funding"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Asia"
        },
        {
            "name": "StartupAsia",
            "website": "https://www.startupasia.org",
            "category": "platform",
            "focus_areas": ["Asian startups", "ecosystem", "events"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Asia"
        },
        
        # JAPAN
        {
            "name": "The Bridge",
            "website": "https://thebridge.jp",
            "category": "publication",
            "focus_areas": ["Japanese startups", "tech", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Japan"
        },
        {
            "name": "TechCrunch Japan",
            "website": "https://jp.techcrunch.com",
            "category": "publication",
            "focus_areas": ["Japanese tech", "startups", "global"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Japan"
        },
        
        # SINGAPORE
        {
            "name": "e27",
            "website": "https://e27.co",
            "category": "publication",
            "focus_areas": ["Southeast Asian startups", "ecosystem", "funding"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Singapore"
        },
        {
            "name": "Vulcan Post",
            "website": "https://vulcanpost.com",
            "category": "publication",
            "focus_areas": ["Southeast Asian tech", "startups", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Singapore"
        },
        
        # AUSTRALIA
        {
            "name": "StartupSmart",
            "website": "https://www.startupsmart.com.au",
            "category": "publication",
            "focus_areas": ["Australian startups", "entrepreneurship", "SME"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Australia"
        },
        {
            "name": "Startup Daily",
            "website": "https://www.startupdaily.net",
            "category": "publication",
            "focus_areas": ["Australian tech", "startups", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Australia"
        },
        
        # CANADA
        {
            "name": "BetaKit",
            "website": "https://betakit.com",
            "category": "publication",
            "focus_areas": ["Canadian startups", "tech", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Canada"
        },
        {
            "name": "MobileSyrup",
            "website": "https://mobilesyrup.com",
            "category": "publication",
            "focus_areas": ["Canadian tech", "mobile", "startups"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Canada"
        },
        {
            "name": "Techvibes",
            "website": "https://techvibes.com",
            "category": "publication",
            "focus_areas": ["Canadian tech", "startups", "ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Canada"
        },
        
        # LATIN AMERICA
        {
            "name": "LAVCA",
            "website": "https://lavca.org",
            "category": "platform",
            "focus_areas": ["Latin American VC", "startups", "investment"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Latin America"
        },
        {
            "name": "Contxto",
            "website": "https://www.contxto.com",
            "category": "publication",
            "focus_areas": ["Latin American startups", "ecosystem", "funding"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Latin America"
        },
        {
            "name": "ABVCAP",
            "website": "https://www.abvcap.com.br",
            "category": "platform",
            "focus_areas": ["Brazilian VC", "startups", "private equity"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Brazil"
        },
        
        # MIDDLE EAST & AFRICA
        {
            "name": "Wamda",
            "website": "https://www.wamda.com",
            "category": "publication",
            "focus_areas": ["MENA startups", "entrepreneurship", "investment"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "MENA"
        },
        {
            "name": "Magnitt",
            "website": "https://magnitt.com",
            "category": "platform",
            "focus_areas": ["MENA startups", "funding", "ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "MENA"
        },
        {
            "name": "Disrupt Africa",
            "website": "https://disrupt-africa.com",
            "category": "publication",
            "focus_areas": ["African startups", "tech", "investment"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Africa"
        },
        
        # ACCELERATORS & INCUBATORS WORLDWIDE
        {
            "name": "Founder Institute",
            "website": "https://fi.co",
            "category": "platform",
            "focus_areas": ["global accelerator", "pre-seed", "mentorship"],
            "contact_methods": ["email", "contact_form"],
            "priority": 5,
            "region": "Global"
        },
        {
            "name": "SOSV",
            "website": "https://sosv.com",
            "category": "platform",
            "focus_areas": ["global VC", "accelerator", "deep tech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Global"
        },
        {
            "name": "Antler",
            "website": "https://antler.co",
            "category": "platform",
            "focus_areas": ["global VC", "early stage", "founder matching"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Global"
        },
        {
            "name": "Plug and Play",
            "website": "https://plugandplaytechcenter.com",
            "category": "platform",
            "focus_areas": ["corporate accelerator", "innovation", "global"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Global"
        },
        {
            "name": "APX",
            "website": "https://apx.ac",
            "category": "platform",
            "focus_areas": ["European accelerator", "early stage", "Porsche Digital"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "BEAM",
            "website": "https://beam.camp",
            "category": "platform",
            "focus_areas": ["European accelerator", "sustainability", "impact"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        
        # ANGEL GROUPS & NETWORKS
        {
            "name": "Angel Investment Network",
            "website": "https://www.angelinvestmentnetwork.co.uk",
            "category": "platform",
            "focus_areas": ["angel investing", "early stage", "global"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Global"
        },
        {
            "name": "European Business Angels Network",
            "website": "https://www.eban.org",
            "category": "platform",
            "focus_areas": ["European angels", "investment", "ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "French Business Angels",
            "website": "https://www.franceangels.org",
            "category": "platform",
            "focus_areas": ["French angels", "investment", "mentorship"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "France"
        },
        
        # REGIONAL STARTUP COMMUNITIES
        {
            "name": "Silicon Canals",
            "website": "https://siliconcanals.com",
            "category": "publication",
            "focus_areas": ["European tech", "startups", "ecosystem"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Europe"
        },
        {
            "name": "Startup Lithuania",
            "website": "https://www.startuplithuania.lt",
            "category": "platform",
            "focus_areas": ["Lithuanian startups", "ecosystem", "fintech"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Lithuania"
        },
        {
            "name": "Startup Estonia",
            "website": "https://startupestonia.ee",
            "category": "platform",
            "focus_areas": ["Estonian startups", "digital", "e-residency"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Estonia"
        },
        {
            "name": "Swiss Startup",
            "website": "https://www.swissstartup.org",
            "category": "platform",
            "focus_areas": ["Swiss startups", "ecosystem", "innovation"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Switzerland"
        },
        {
            "name": "Austria Startups",
            "website": "https://austriastartups.com",
            "category": "platform",
            "focus_areas": ["Austrian startups", "ecosystem", "community"],
            "contact_methods": ["email", "contact_form"],
            "priority": 4,
            "region": "Austria"
        }
    ]

def add_regional_targets():
    """Add regional targets to the existing targets.json file"""
    data_dir = Path("outreach_data")
    targets_file = data_dir / "targets.json"
    
    # Load existing targets
    try:
        with open(targets_file, 'r') as f:
            existing_targets = json.load(f)
    except FileNotFoundError:
        existing_targets = []
    
    # Get new regional targets
    new_targets = get_regional_targets()
    
    # Check which targets are new (avoid duplicates)
    existing_names = {target.get('name', '').lower() for target in existing_targets}
    added_count = 0
    
    for target in new_targets:
        if target['name'].lower() not in existing_names:
            target['contacts_found'] = 0
            target['last_scraped'] = None
            existing_targets.append(target)
            added_count += 1
            print(f"✅ Added: {target['name']} ({target['region']})")
    
    # Save updated targets
    with open(targets_file, 'w') as f:
        json.dump(existing_targets, f, indent=2)
    
    print(f"\n🎯 Added {added_count} new regional targets")
    print(f"📊 Total targets now: {len(existing_targets)}")
    
    # Summary by region
    regions = {}
    for target in existing_targets:
        region = target.get('region', 'US/Global')
        regions[region] = regions.get(region, 0) + 1
    
    print("\n🌍 Targets by region:")
    for region, count in sorted(regions.items()):
        print(f"  • {region}: {count}")

if __name__ == "__main__":
    print("🌍 Adding regional and international startup targets...")
    add_regional_targets()
    print("\n✅ Regional targets added successfully!")
    print("\nThese targets include:")
    print("• Regional startup publications (Europe, Asia, LATAM, etc.)")
    print("• Local accelerators and incubators")
    print("• Angel investor networks")
    print("• Startup ecosystem platforms")
    print("• Tech blogs focused on specific regions")