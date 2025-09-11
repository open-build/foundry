#!/usr/bin/env python3
"""
Quick runner script for the startup outreach system
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required = ['rich', 'schedule', 'beautifulsoup4', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)

def setup_config():
    """Set up configuration file if it doesn't exist"""
    config_path = Path('config.py')
    template_path = Path('config_template.py')
    
    if not config_path.exists() and template_path.exists():
        print("Creating config.py from template...")
        import shutil
        shutil.copy(template_path, config_path)
        print("✅ Config file created. Please edit config.py with your settings.")
        return False
    
    return True

def main():
    """Main runner"""
    print("🚀 Startup Outreach System")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Set up config
    if not setup_config():
        print("\n⚠️  Please edit config.py with your email settings before running.")
        return
    
    # Import the bot
    from startup_outreach import StartupOutreachBot
    
    # Show menu
    print("\nSelect mode:")
    print("1. Full run (discover + outreach + interactive review)")
    print("2. Discovery only")
    print("3. Review pending messages")
    print("4. Send all pending (no review)")
    print("5. Generate report")
    print("6. Send daily notification")
    print("7. Custom command line")
    
    choice = input("\nEnter choice (1-7): ").strip()
    
    if choice == '1':
        # Full interactive run
        bot = StartupOutreachBot()
        bot.run_discovery_phase()
        bot.run_outreach_phase(interactive=True)
        bot.generate_analytics_report()
    
    elif choice == '2':
        # Discovery only
        bot = StartupOutreachBot()
        bot.run_discovery_phase()
    
    elif choice == '3':
        # Review pending
        bot = StartupOutreachBot()
        bot.load_pending_outreach()
        if bot.pending_outreach:
            bot.interactive_outreach_session(bot.pending_outreach)
        else:
            print("No pending messages to review")
    
    elif choice == '4':
        # Send all pending
        bot = StartupOutreachBot()
        bot.load_pending_outreach()
        bot.send_all_pending()
    
    elif choice == '5':
        # Generate report
        bot = StartupOutreachBot()
        bot.generate_analytics_report()
    
    elif choice == '6':
        # Send daily notification
        bot = StartupOutreachBot()
        bot.send_daily_notification()
    
    elif choice == '7':
        # Custom command line
        print("\nAvailable commands:")
        print("python startup_outreach.py --mode discover")
        print("python startup_outreach.py --mode outreach")
        print("python startup_outreach.py --mode review")
        print("python startup_outreach.py --mode send")
        print("python startup_outreach.py --mode notify")
        print("python startup_outreach.py --mode report")
        print("python startup_outreach.py --mode full")
        print("python startup_outreach.py --mode full --non-interactive")
        print("python startup_outreach.py --mode outreach --dry-run")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
