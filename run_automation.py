#!/usr/bin/env python3
"""
Daily Automation Launcher
=========================

Simple wrapper to run the daily automation from any location.
Automatically handles path resolution and imports.

Usage:
    python3 daily_automation.py [options]
    
All options are passed through to scripts/daily_automation.py
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(script_dir))

# Change to project root directory
project_root = Path(__file__).parent
os.chdir(project_root)

# Import and run the main automation
try:
    from daily_automation import main
    main()
except ImportError as e:
    print(f"❌ Error importing daily automation: {e}")
    print(f"Make sure scripts/daily_automation.py exists")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running daily automation: {e}")
    sys.exit(1)