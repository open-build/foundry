#!/usr/bin/env python3
"""
Daily Automation Master Script for Buildly Labs Foundry
Runs the complete outreach pipeline: discovery -> outreach -> analytics -> notifications

This script orchestrates all outreach activities in the proper sequence with
comprehensive error handling, logging, and status reporting.

Usage:
    python3 daily_automation.py                    # Full daily run
    python3 daily_automation.py --discovery-only   # Just discovery
    python3 daily_automation.py --outreach-only    # Just outreach 
    python3 daily_automation.py --analytics-only   # Just analytics
    python3 daily_automation.py --dry-run          # Test run without sending
    python3 daily_automation.py --interactive      # Interactive approval mode
"""

import os
import sys
import logging
import argparse
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

def setup_logging() -> logging.Logger:
    """Set up comprehensive logging"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'daily_automation_{timestamp}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('daily_automation')
    logger.info(f"=== Daily Automation Started - {datetime.now().isoformat()} ===")
    logger.info(f"Log file: {log_file}")
    
    return logger

def check_dependencies(logger: logging.Logger) -> bool:
    """Check if all required dependencies are available"""
    try:
        required_files = [
            'scripts/startup_outreach.py',
            'scripts/analytics_reporter.py', 
            'config.py'
        ]
        
        for file_path in required_files:
            if not Path(file_path).exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        # Test imports
        from startup_outreach import StartupOutreachBot
        from analytics_reporter import AnalyticsCollector
        
        logger.info("✅ All dependencies check passed")
        return True
        
    except Exception as e:
        logger.error(f"Dependency check failed: {e}")
        return False

def run_discovery_phase(logger: logging.Logger, dry_run: bool = False) -> bool:
    """Run the discovery phase to find new contacts"""
    try:
        logger.info("🔍 Starting discovery phase...")
        
        from startup_outreach import StartupOutreachBot
        bot = StartupOutreachBot()
        
        # Run discovery
        if dry_run:
            logger.info("DRY RUN: Would run discovery phase")
            return True
        else:
            result = bot.run_discovery_phase()
            logger.info("✅ Discovery phase completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"❌ Discovery phase failed: {e}")
        logger.error(traceback.format_exc())
        return False

def run_outreach_phase(logger: logging.Logger, dry_run: bool = False, interactive: bool = False) -> bool:
    """Run the outreach phase to send emails"""
    try:
        logger.info("📧 Starting outreach phase...")
        
        from startup_outreach import StartupOutreachBot
        bot = StartupOutreachBot()
        
        if dry_run:
            logger.info("DRY RUN: Would run outreach phase")
            # Run dry-run to show what would be sent
            os.system(f"cd {Path.cwd()} && python3 scripts/startup_outreach.py --mode outreach --dry-run --non-interactive")
            return True
        elif interactive:
            logger.info("Running outreach in interactive mode...")
            result = bot.run_outreach_phase(interactive=True)
        else:
            logger.info("Running outreach in auto-send mode...")
            result = bot.run_outreach_phase(interactive=False)
        
        logger.info("✅ Outreach phase completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Outreach phase failed: {e}")
        logger.error(traceback.format_exc())
        return False

def run_analytics_phase(logger: logging.Logger, dry_run: bool = False) -> bool:
    """Run analytics collection and reporting"""
    try:
        logger.info("📊 Starting analytics phase...")
        
        from startup_outreach import StartupOutreachBot
        bot = StartupOutreachBot()
        
        if dry_run:
            logger.info("DRY RUN: Would generate analytics report")
            return True
        else:
            # Only generate analytics data, do not send email here
            # The email will be sent after all phases in main()
            if hasattr(bot, 'generate_analytics_report'):
                bot.generate_analytics_report()
            logger.info("✅ Analytics phase completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"❌ Analytics phase failed: {e}")
        logger.error(traceback.format_exc())
        return False

def send_completion_notification(logger: logging.Logger, results: Dict[str, bool], dry_run: bool = False):
    """Send notification about automation completion"""
    try:
        success_count = sum(results.values())
        total_phases = len(results)
        
        status = "SUCCESS" if success_count == total_phases else "PARTIAL SUCCESS" if success_count > 0 else "FAILED"
        
        message = f"""
Daily Automation {status}
========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Mode: {'DRY RUN' if dry_run else 'LIVE'}

Phase Results:
"""
        
        for phase, success in results.items():
            status_icon = "✅" if success else "❌"
            message += f"{status_icon} {phase}: {'SUCCESS' if success else 'FAILED'}\n"
        
        logger.info(message)
        
        # Send email notification if not dry run and analytics phase succeeded
        if not dry_run and results.get('analytics', False):
            logger.info("📧 Completion notification included in daily analytics report")
        
    except Exception as e:
        logger.error(f"Failed to send completion notification: {e}")

def main():
    """Main automation orchestrator"""
    parser = argparse.ArgumentParser(description='Daily Automation for Buildly Labs Foundry')
    parser.add_argument('--discovery-only', action='store_true', help='Run only discovery phase')
    parser.add_argument('--outreach-only', action='store_true', help='Run only outreach phase')
    parser.add_argument('--analytics-only', action='store_true', help='Run only analytics phase')
    parser.add_argument('--dry-run', action='store_true', help='Test run without sending emails')
    parser.add_argument('--interactive', action='store_true', help='Interactive approval for outreach')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    try:
        # Check dependencies
        if not check_dependencies(logger):
            logger.error("❌ Dependency check failed. Aborting.")
            sys.exit(1)
        
        # Track results
        results = {}
        
        # Run selected phases
        if args.analytics_only:
            results['analytics'] = run_analytics_phase(logger, args.dry_run)
        elif args.discovery_only:
            results['discovery'] = run_discovery_phase(logger, args.dry_run)
        elif args.outreach_only:
            results['outreach'] = run_outreach_phase(logger, args.dry_run, args.interactive)
        else:
            # Full daily run - all phases in sequence
            logger.info("🚀 Starting full daily automation sequence...")
            
            # Phase 1: Discovery
            results['discovery'] = run_discovery_phase(logger, args.dry_run)
            
            # Phase 2: Outreach (only if discovery succeeded or we're in dry-run)
            if results['discovery'] or args.dry_run:
                results['outreach'] = run_outreach_phase(logger, args.dry_run, args.interactive)
            else:
                logger.warning("⚠️ Skipping outreach phase due to discovery failure")
                results['outreach'] = False
            
            # Phase 3: Analytics (always run for reporting)
            results['analytics'] = run_analytics_phase(logger, args.dry_run)
        
        # After all phases, send the daily summary email (if not dry run)
        if not args.dry_run:
            try:
                from startup_outreach import StartupOutreachBot
                bot = StartupOutreachBot()
                bot.send_daily_analytics_report()
                logger.info("✅ Daily summary email sent after all phases")
            except Exception as e:
                logger.error(f"❌ Failed to send daily summary email: {e}")

        # Send completion notification
        send_completion_notification(logger, results, args.dry_run)

        # Final status
        success_count = sum(results.values())
        total_phases = len(results)

        if success_count == total_phases:
            logger.info("🎉 Daily automation completed successfully!")
            sys.exit(0)
        elif success_count > 0:
            logger.warning("⚠️ Daily automation completed with some failures")
            sys.exit(1)
        else:
            logger.error("❌ Daily automation failed completely")
            sys.exit(2)
            
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error in main automation: {e}")
        logger.error(traceback.format_exc())
        sys.exit(3)
    finally:
        logger.info(f"=== Daily Automation Finished - {datetime.now().isoformat()} ===")

if __name__ == "__main__":
    main()