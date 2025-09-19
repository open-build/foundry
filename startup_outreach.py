#!/usr/bin/env python3
"""
Buildly Labs Foundry Outreach Management Script

Easy-to-use wrapper script for managing the outreach automation system.
This script provides a simple interface to all outreach functionality.

Usage Examples:
    ./startup_outreach.py                          # Interactive menu
    ./startup_outreach.py discover                 # Run discovery only
    ./startup_outreach.py outreach                 # Run outreach only
    ./startup_outreach.py outreach --dry-run       # Test outreach
    ./startup_outreach.py analytics                # Generate analytics
    ./startup_outreach.py daily                    # Full daily automation
    ./startup_outreach.py daily --dry-run          # Test daily automation
    ./startup_outreach.py daily --interactive      # Daily with manual approval
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
MAIN_SCRIPT = SCRIPTS_DIR / 'startup_outreach.py'
DAILY_AUTOMATION = PROJECT_ROOT / 'daily_automation.py'

def run_command(cmd: list, description: str = None) -> int:
    """Run a command and return exit code"""
    if description:
        print(f"🚀 {description}")
    
    try:
        # Change to project directory
        os.chdir(PROJECT_ROOT)
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return 1

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*50)
    print("🏢 Buildly Labs Foundry - Outreach Management")
    print("="*50)
    print("1. 🔍 Discovery - Find new contacts")
    print("2. 📧 Outreach - Send emails (interactive)")
    print("3. 📊 Analytics - Generate reports")
    print("4. 🎯 Full Daily Run (auto-send)")
    print("5. 🧪 Test Daily Run (dry-run)")
    print("6. 📋 Review Pending Messages")
    print("7. 📈 Send Daily Analytics Report")
    print("8. ⚙️  Advanced Options")
    print("9. ❓ Help & Documentation")
    print("0. 🚪 Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("\nSelect option (0-9): ").strip()
            return choice
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)

def handle_menu_choice(choice: str) -> int:
    """Handle menu selection"""
    
    if choice == '1':
        # Discovery
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'discover']
        return run_command(cmd, "Running contact discovery...")
        
    elif choice == '2':
        # Interactive outreach
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'outreach']
        return run_command(cmd, "Running interactive outreach...")
        
    elif choice == '3':
        # Analytics
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'analytics']
        return run_command(cmd, "Generating analytics report...")
        
    elif choice == '4':
        # Full daily run
        cmd = [sys.executable, str(DAILY_AUTOMATION)]
        return run_command(cmd, "Running full daily automation...")
        
    elif choice == '5':
        # Test daily run
        cmd = [sys.executable, str(DAILY_AUTOMATION), '--dry-run']
        return run_command(cmd, "Running test daily automation (dry-run)...")
        
    elif choice == '6':
        # Review pending
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'review']
        return run_command(cmd, "Reviewing pending messages...")
        
    elif choice == '7':
        # Daily analytics report
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'report']
        return run_command(cmd, "Sending daily analytics report...")
        
    elif choice == '8':
        # Advanced options
        show_advanced_menu()
        return 0
        
    elif choice == '9':
        # Help
        show_help()
        return 0
        
    elif choice == '0':
        print("👋 Goodbye!")
        sys.exit(0)
        
    else:
        print("❌ Invalid choice. Please select 0-9.")
        return 1

def show_advanced_menu():
    """Show advanced options menu"""
    print("\n" + "="*50)
    print("⚙️  Advanced Options")
    print("="*50)
    print("1. 🔧 Send all pending (no review)")
    print("2. 🧹 Clean up old logs") 
    print("3. 📝 Show system status")
    print("4. 🛠️  Check configuration")
    print("5. 📊 Full analytics dashboard")
    print("6. 🚫 Process opt-outs")
    print("7. 📤 Custom command line")
    print("0. ⬅️  Back to main menu")
    print("="*50)
    
    choice = input("\nSelect advanced option (0-7): ").strip()
    
    if choice == '1':
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'send', '--auto-send']
        run_command(cmd, "Sending all pending messages...")
    elif choice == '2':
        # Clean up old logs
        logs_dir = PROJECT_ROOT / 'logs'
        if logs_dir.exists():
            import glob
            old_logs = glob.glob(str(logs_dir / '*.log'))
            if len(old_logs) > 10:  # Keep last 10 logs
                old_logs.sort()
                for log in old_logs[:-10]:
                    os.remove(log)
                print(f"🧹 Cleaned up {len(old_logs) - 10} old log files")
            else:
                print("✅ No cleanup needed")
    elif choice == '3':
        show_system_status()
    elif choice == '4':
        check_configuration()
    elif choice == '5':
        cmd = [sys.executable, str(SCRIPTS_DIR / 'analytics_reporter.py')]
        run_command(cmd, "Opening analytics dashboard...")
    elif choice == '6':
        cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'opt-out']
        run_command(cmd, "Processing opt-out requests...")
    elif choice == '7':
        show_custom_commands()
    elif choice == '0':
        return
    else:
        print("❌ Invalid choice")

def show_system_status():
    """Show current system status"""
    print("\n📊 System Status")
    print("="*30)
    
    # Check files
    files_to_check = [
        ('Main Script', MAIN_SCRIPT),
        ('Daily Automation', DAILY_AUTOMATION),
        ('Config File', PROJECT_ROOT / 'config.py'),
        ('Contacts Database', PROJECT_ROOT / 'outreach_data' / 'contacts.json'),
        ('Targets Database', PROJECT_ROOT / 'outreach_data' / 'targets.json')
    ]
    
    for name, path in files_to_check:
        status = "✅" if path.exists() else "❌"
        print(f"{status} {name}: {path}")
    
    # Check data stats
    try:
        import json
        
        contacts_file = PROJECT_ROOT / 'outreach_data' / 'contacts.json'
        targets_file = PROJECT_ROOT / 'outreach_data' / 'targets.json'
        
        if contacts_file.exists():
            with open(contacts_file) as f:
                contacts = json.load(f)
                print(f"📧 Total contacts: {len(contacts)}")
        
        if targets_file.exists():
            with open(targets_file) as f:
                targets = json.load(f)
                print(f"🎯 Total targets: {len(targets)}")
                
    except Exception as e:
        print(f"⚠️  Could not read data files: {e}")

def check_configuration():
    """Check configuration status"""
    print("\n🔧 Configuration Check")
    print("="*30)
    
    config_file = PROJECT_ROOT / 'config.py'
    if not config_file.exists():
        print("❌ config.py not found")
        template_file = PROJECT_ROOT / 'config_template.py'
        if template_file.exists():
            print("📋 config_template.py available - copy to config.py and edit")
        return
    
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        import config
        
        # Check essential config
        required_configs = [
            ('Email Config', hasattr(config, 'EMAIL_CONFIG')),
            ('Brevo Config', hasattr(config, 'BREVO_CONFIG') or 
             (hasattr(config, 'EMAIL_CONFIG') and 'api_key' in getattr(config, 'EMAIL_CONFIG', {}))),
            ('Google Config', hasattr(config, 'GOOGLE_CONFIG')),
            ('Template Config', hasattr(config, 'MESSAGE_TEMPLATES'))
        ]
        
        for name, exists in required_configs:
            status = "✅" if exists else "❌"
            print(f"{status} {name}")
            
    except Exception as e:
        print(f"❌ Error reading config: {e}")

def show_custom_commands():
    """Show available custom commands"""
    print("\n🛠️  Custom Commands")
    print("="*40)
    print("Outreach Commands:")
    print(f"  python3 {MAIN_SCRIPT} --mode discover")
    print(f"  python3 {MAIN_SCRIPT} --mode outreach --dry-run")
    print(f"  python3 {MAIN_SCRIPT} --mode outreach --auto-send")
    print(f"  python3 {MAIN_SCRIPT} --mode review")
    print(f"  python3 {MAIN_SCRIPT} --mode send")
    print(f"  python3 {MAIN_SCRIPT} --mode analytics")
    print()
    print("Automation Commands:")
    print(f"  python3 {DAILY_AUTOMATION}")
    print(f"  python3 {DAILY_AUTOMATION} --dry-run")
    print(f"  python3 {DAILY_AUTOMATION} --interactive")
    print(f"  python3 {DAILY_AUTOMATION} --discovery-only")
    print(f"  python3 {DAILY_AUTOMATION} --outreach-only")
    print(f"  python3 {DAILY_AUTOMATION} --analytics-only")

def show_help():
    """Show help documentation"""
    print("\n❓ Help & Documentation")
    print("="*40)
    print("📖 Quick Start:")
    print("   1. Run './startup_outreach.py' for interactive menu")
    print("   2. Choose option 5 for test run (dry-run)")
    print("   3. Choose option 4 for full daily automation")
    print()
    print("📋 Daily Workflow:")
    print("   • Discovery: Find new startup contacts")
    print("   • Outreach: Send personalized emails")
    print("   • Analytics: Track performance and generate reports")
    print()
    print("🔧 Configuration:")
    print("   • Edit config.py with your email settings")
    print("   • Set up Brevo SMTP for sending emails")
    print("   • Configure Google Apps Script for forms")
    print()
    print("📁 Documentation:")
    print("   • devdocs/OUTREACH_README.md - Detailed setup")
    print("   • devdocs/GOOGLE_APPS_SCRIPT_SETUP.md - Form integration")
    print("   • scripts/README.md - Script documentation")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Buildly Labs Foundry Outreach Management')
    parser.add_argument('command', nargs='?', 
                       choices=['discover', 'outreach', 'analytics', 'daily', 'status'],
                       help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Test run without sending')
    parser.add_argument('--interactive', action='store_true', help='Interactive approval mode')
    parser.add_argument('--auto-send', action='store_true', help='Auto-send without approval')
    
    args = parser.parse_args()
    
    # Check if main script exists
    if not MAIN_SCRIPT.exists():
        print(f"❌ Main script not found: {MAIN_SCRIPT}")
        print("   Make sure you're in the foundry project directory")
        sys.exit(1)
    
    # Handle direct commands
    if args.command:
        if args.command == 'discover':
            cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'discover']
            return run_command(cmd, "Running contact discovery...")
            
        elif args.command == 'outreach':
            cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'outreach']
            if args.dry_run:
                cmd.extend(['--dry-run'])
            if args.auto_send:
                cmd.extend(['--auto-send'])
            return run_command(cmd, "Running outreach...")
            
        elif args.command == 'analytics':
            cmd = [sys.executable, str(MAIN_SCRIPT), '--mode', 'analytics']
            return run_command(cmd, "Generating analytics...")
            
        elif args.command == 'daily':
            cmd = [sys.executable, str(DAILY_AUTOMATION)]
            if args.dry_run:
                cmd.append('--dry-run')
            if args.interactive:
                cmd.append('--interactive')
            return run_command(cmd, "Running daily automation...")
            
        elif args.command == 'status':
            show_system_status()
            return 0
    
    # Interactive menu
    else:
        while True:
            choice = show_menu()
            result = handle_menu_choice(choice)
            
            if result != 0 and choice not in ['8', '9']:  # Don't pause for advanced menu or help
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)