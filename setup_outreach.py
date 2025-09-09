#!/usr/bin/env python3
"""
Setup script for Startup Outreach Bot
=====================================

This script sets up the outreach system with proper configuration.
"""

import os
import json
from pathlib import Path
import shutil

def setup_outreach_system():
    """Set up the outreach system"""
    print("🚀 Setting up Startup Outreach System...")
    
    # Create data directory
    data_dir = Path("outreach_data")
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Created data directory: {data_dir}")
    
    # Copy config template if config doesn't exist
    if not Path("config.py").exists():
        if Path("config_template.py").exists():
            shutil.copy("config_template.py", "config.py")
            print("✅ Created config.py from template")
            print("⚠️  Please edit config.py with your email settings!")
        else:
            print("❌ config_template.py not found!")
    
    # Update .gitignore
    gitignore_path = Path(".gitignore")
    gitignore_outreach_path = Path(".gitignore_outreach")
    
    if gitignore_outreach_path.exists():
        # Append outreach gitignore to main gitignore
        with open(gitignore_outreach_path, 'r') as f:
            outreach_ignore = f.read()
        
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                current_ignore = f.read()
            
            if "outreach_data/" not in current_ignore:
                with open(gitignore_path, 'a') as f:
                    f.write(f"\n# Outreach System\n{outreach_ignore}")
                print("✅ Updated .gitignore with outreach exclusions")
        else:
            with open(gitignore_path, 'w') as f:
                f.write(outreach_ignore)
            print("✅ Created .gitignore with outreach exclusions")
    
    # Create empty data files
    data_files = [
        "contacts.json",
        "targets.json", 
        "outreach_log.json",
        "analytics.json"
    ]
    
    for filename in data_files:
        filepath = data_dir / filename
        if not filepath.exists():
            with open(filepath, 'w') as f:
                json.dump([], f)
            print(f"✅ Created {filepath}")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("Next steps:")
    print("1. Edit config.py with your email settings")
    print("2. Install dependencies: pip install -r requirements_outreach.txt")
    print("3. Test the system: python startup_outreach.py --dry-run")
    print("4. Run discovery: python startup_outreach.py --mode discover")
    print("5. Start outreach: python startup_outreach.py --mode outreach")
    print("\nFor help: python startup_outreach.py --help")
    print("="*60)

if __name__ == "__main__":
    setup_outreach_system()
