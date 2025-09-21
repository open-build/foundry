#!/usr/bin/env python3
"""
Local Dashboard Generator for Buildly Labs Foundry
==================================================

Generates a comprehensive HTML dashboard showing:
- Last day/week/month automation metrics
- Real outreach numbers and status
- Environment configuration and missing variables
- Error logs and system health
- Contact database statistics
- Upcoming tasks and recommendations

Usage:
    python3 generate_dashboard.py
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import glob

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv not available, try manual loading
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def load_env_variables() -> Dict[str, Any]:
    """Load and analyze environment variables"""
    env_vars = {}
    required_vars = {
        'BREVO_SMTP_USER': 'Email SMTP username for Brevo',
        'BREVO_SMTP_PASSWORD': 'Email SMTP password for Brevo', 
        'DAILY_NOTIFICATION_EMAIL': 'Primary email for daily reports',
        'DAILY_CC_EMAIL': 'CC email for daily reports',
        'BCC_EMAIL': 'BCC email (optional)',
        'GOOGLE_ANALYTICS_PROPERTY_ID': 'GA4 Property ID for website analytics',
        'GOOGLE_ANALYTICS_API_KEY': 'GA4 API key (optional)',
        'GOOGLE_ANALYTICS_CREDENTIALS_FILE': 'GA4 service account file (optional)',
        'YOUTUBE_CHANNEL_ID': 'YouTube channel ID for analytics',
        'YOUTUBE_API_KEY': 'YouTube Data API key',
        'WEBSITE_URL': 'Main website URL for monitoring'
    }
    
    optional_vars = {
        'BCC_EMAIL': 'Additional BCC for notifications',
        'GOOGLE_ANALYTICS_API_KEY': 'Alternative to service account',
        'GOOGLE_ANALYTICS_CREDENTIALS_FILE': 'Alternative to API key'
    }
    
    configured = {}
    missing = {}
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'KEY' in var:
                display_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            else:
                display_value = value
            configured[var] = {'value': display_value, 'description': description}
        else:
            missing[var] = {'description': description, 'required': var not in optional_vars}
    
    return {
        'configured': configured,
        'missing': missing,
        'total_configured': len(configured),
        'total_missing': len([k for k, v in missing.items() if v['required']])
    }

def analyze_automation_logs() -> Dict[str, Any]:
    """Analyze automation logs for the last day, week, month"""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        return {'error': 'No logs directory found'}
    
    now = datetime.now()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    log_files = list(logs_dir.glob('daily_automation_*.log'))
    log_files.sort(reverse=True)  # Most recent first
    
    periods = {
        'day': {'start': day_ago, 'logs': [], 'success': 0, 'failure': 0, 'errors': []},
        'week': {'start': week_ago, 'logs': [], 'success': 0, 'failure': 0, 'errors': []},
        'month': {'start': month_ago, 'logs': [], 'success': 0, 'failure': 0, 'errors': []}
    }
    
    for log_file in log_files:
        try:
            # Extract timestamp from filename: daily_automation_20250921_092000.log
            timestamp_str = log_file.stem.split('_')[2] + '_' + log_file.stem.split('_')[3]
            log_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            
            # Read log content
            with open(log_file, 'r') as f:
                content = f.read()
            
            # Categorize by period
            for period_name, period_data in periods.items():
                if log_time >= period_data['start']:
                    period_data['logs'].append({
                        'file': log_file.name,
                        'time': log_time.isoformat(),
                        'success': 'completed successfully' in content.lower(),
                        'errors': [line for line in content.split('\n') if 'ERROR' in line or 'FAILED' in line]
                    })
                    
                    if 'completed successfully' in content.lower():
                        period_data['success'] += 1
                    else:
                        period_data['failure'] += 1
                    
                    # Collect errors
                    errors = [line for line in content.split('\n') if 'ERROR' in line or 'FAILED' in line]
                    period_data['errors'].extend(errors)
        
        except Exception as e:
            continue
    
    return periods

def analyze_outreach_data() -> Dict[str, Any]:
    """Analyze outreach performance and database"""
    data_dir = Path('outreach_data')
    if not data_dir.exists():
        return {'error': 'No outreach data directory found'}
    
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    week_ago = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    month_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    
    analysis = {
        'contacts': {'total': 0, 'recent': 0, 'sources': {}},
        'outreach_log': {'total': 0, 'today': 0, 'week': 0, 'month': 0},
        'pending': {'total': 0, 'ready': 0, 'sent': 0},
        'targets': {'total': 0, 'active': 0, 'categories': {}},
        'opt_outs': {'total': 0, 'recent': 0}
    }
    
    # Analyze contacts
    contacts_file = data_dir / 'contacts.json'
    if contacts_file.exists():
        try:
            with open(contacts_file, 'r') as f:
                contacts = json.load(f)
            
            analysis['contacts']['total'] = len(contacts)
            
            for contact in contacts:
                date_discovered = contact.get('date_discovered', '')
                if date_discovered.startswith(today):
                    analysis['contacts']['recent'] += 1
                
                source = contact.get('source', 'Unknown')
                analysis['contacts']['sources'][source] = analysis['contacts']['sources'].get(source, 0) + 1
        
        except Exception as e:
            analysis['contacts']['error'] = str(e)
    
    # Analyze outreach log
    outreach_log_file = data_dir / 'outreach_log.json'
    if outreach_log_file.exists():
        try:
            with open(outreach_log_file, 'r') as f:
                outreach_log = json.load(f)
            
            analysis['outreach_log']['total'] = len(outreach_log)
            
            for entry in outreach_log:
                date = entry.get('date', '')
                if date.startswith(today):
                    analysis['outreach_log']['today'] += 1
                if date >= week_ago:
                    analysis['outreach_log']['week'] += 1
                if date >= month_ago:
                    analysis['outreach_log']['month'] += 1
        
        except Exception as e:
            analysis['outreach_log']['error'] = str(e)
    
    # Analyze pending outreach
    pending_file = data_dir / 'pending_outreach.json'
    if pending_file.exists():
        try:
            with open(pending_file, 'r') as f:
                pending = json.load(f)
            
            analysis['pending']['total'] = len(pending)
            
            for item in pending:
                if item.get('sent', False):
                    analysis['pending']['sent'] += 1
                else:
                    analysis['pending']['ready'] += 1
        
        except Exception as e:
            analysis['pending']['error'] = str(e)
    
    # Analyze targets
    targets_file = data_dir / 'targets.json'
    if targets_file.exists():
        try:
            with open(targets_file, 'r') as f:
                targets = json.load(f)
            
            analysis['targets']['total'] = len(targets)
            
            for target in targets:
                if target.get('active', True):
                    analysis['targets']['active'] += 1
                
                category = target.get('category', 'Unknown')
                analysis['targets']['categories'][category] = analysis['targets']['categories'].get(category, 0) + 1
        
        except Exception as e:
            analysis['targets']['error'] = str(e)
    
    # Analyze opt-outs
    opt_outs_file = data_dir / 'opt_outs.json'
    if opt_outs_file.exists():
        try:
            with open(opt_outs_file, 'r') as f:
                opt_outs = json.load(f)
            
            analysis['opt_outs']['total'] = len(opt_outs)
            
            for opt_out in opt_outs:
                date = opt_out.get('date', '')
                if date >= week_ago:
                    analysis['opt_outs']['recent'] += 1
        
        except Exception as e:
            analysis['opt_outs']['error'] = str(e)
    
    return analysis

def get_system_health() -> Dict[str, Any]:
    """Check system health and file permissions"""
    health = {
        'directories': {},
        'files': {},
        'permissions': {},
        'disk_usage': {}
    }
    
    # Check key directories
    key_dirs = ['outreach_data', 'logs', 'scripts']
    for dir_name in key_dirs:
        dir_path = Path(dir_name)
        health['directories'][dir_name] = {
            'exists': dir_path.exists(),
            'readable': dir_path.is_dir() and os.access(dir_path, os.R_OK),
            'writable': dir_path.is_dir() and os.access(dir_path, os.W_OK)
        }
    
    # Check key files
    key_files = [
        'config.py',
        'daily_automation.py',
        'scripts/startup_outreach.py',
        'scripts/analytics_reporter.py',
        '.env'
    ]
    
    for file_name in key_files:
        file_path = Path(file_name)
        health['files'][file_name] = {
            'exists': file_path.exists(),
            'readable': file_path.is_file() and os.access(file_path, os.R_OK),
            'writable': file_path.is_file() and os.access(file_path, os.W_OK),
            'size': file_path.stat().st_size if file_path.exists() else 0
        }
    
    return health

def get_recommendations() -> List[Dict[str, str]]:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Check environment
    env_data = load_env_variables()
    if env_data['total_missing'] > 0:
        recommendations.append({
            'type': 'warning',
            'title': 'Missing Environment Variables',
            'description': f"{env_data['total_missing']} required environment variables are missing",
            'action': 'Update .env file with missing variables'
        })
    
    # Check outreach data
    outreach_data = analyze_outreach_data()
    if not outreach_data.get('error'):
        if outreach_data['pending']['ready'] > 50:
            recommendations.append({
                'type': 'info',
                'title': 'High Pending Outreach Volume',
                'description': f"{outreach_data['pending']['ready']} messages ready to send",
                'action': 'Run outreach automation or review pending messages'
            })
        
        if outreach_data['contacts']['recent'] == 0:
            recommendations.append({
                'type': 'warning',
                'title': 'No New Contacts Today',
                'description': 'Discovery phase may not be finding new sources',
                'action': 'Check discovery automation and target list'
            })
    
    # Check logs
    log_data = analyze_automation_logs()
    if log_data.get('day', {}).get('failure', 0) > 0:
        recommendations.append({
            'type': 'error',
            'title': 'Recent Automation Failures',
            'description': f"{log_data['day']['failure']} failed automations in the last day",
            'action': 'Review error logs and fix automation issues'
        })
    
    return recommendations

def cleanup_old_reports():
    """Clean up reports and logs older than 30 days"""
    try:
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # Clean up old log files
        logs_dir = Path('logs')
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    logging.info(f"Deleted old log file: {log_file}")
        
        # Clean up old timestamped reports (keep current ones)
        reports_dir = Path('reports')
        if reports_dir.exists():
            # Only delete timestamped archives, not current reports
            for report_file in reports_dir.rglob('*_[0-9]*_[0-9]*.html'):
                if report_file.stat().st_mtime < cutoff_date.timestamp():
                    report_file.unlink()
                    logging.info(f"Deleted old report archive: {report_file}")
            
            for report_file in reports_dir.rglob('*_[0-9]*_[0-9]*.json'):
                if report_file.stat().st_mtime < cutoff_date.timestamp():
                    report_file.unlink()
                    logging.info(f"Deleted old report archive: {report_file}")
        
        logging.info("Cleanup completed: removed archived files older than 30 days")
        
    except Exception as e:
        logging.warning(f"Error during cleanup: {e}")

def generate_html_dashboard() -> str:
    """Generate the complete HTML dashboard"""
    
    # Collect all data
    env_data = load_env_variables()
    log_data = analyze_automation_logs()
    outreach_data = analyze_outreach_data()
    health_data = get_system_health()
    recommendations = get_recommendations()
    
    # Clean up old reports (30 day retention)
    cleanup_old_reports()
    
    # Get recent log files for quick access
    logs_dir = Path('logs')
    recent_logs = []
    if logs_dir.exists():
        log_files = list(logs_dir.glob('*.log'))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        recent_logs = log_files[:10]  # Last 10 log files
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buildly Labs Foundry - Automation Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e1e8ed;
        }}
        
        .card h2 {{
            color: #2d3748;
            margin-bottom: 1rem;
            font-size: 1.4rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            font-weight: 500;
            color: #4a5568;
        }}
        
        .metric-value {{
            font-weight: bold;
            color: #2d3748;
        }}
        
        .status-good {{ color: #38a169; }}
        .status-warning {{ color: #d69e2e; }}
        .status-error {{ color: #e53e3e; }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }}
        
        .recommendation {{
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        
        .recommendation.info {{
            background: #ebf8ff;
            border-color: #3182ce;
        }}
        
        .recommendation.warning {{
            background: #fffaf0;
            border-color: #d69e2e;
        }}
        
        .recommendation.error {{
            background: #fed7d7;
            border-color: #e53e3e;
        }}
        
        .recommendation h4 {{
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .env-var {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        
        .env-var.configured {{
            border-color: #38a169;
            background: #f0fff4;
        }}
        
        .env-var.missing {{
            border-color: #e53e3e;
            background: #fef5e7;
        }}
        
        .env-var-name {{
            font-family: 'Monaco', 'Consolas', monospace;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .env-var-value {{
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85rem;
            color: #666;
        }}
        
        .log-file {{
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            background: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            cursor: pointer;
            transition: background 0.2s;
        }}
        
        .log-file:hover {{
            background: #e2e8f0;
        }}
        
        .log-file-name {{
            font-family: 'Monaco', 'Consolas', monospace;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .log-file-size {{
            font-size: 0.85rem;
            color: #718096;
        }}
        
        .tab-container {{
            margin-top: 2rem;
        }}
        
        .tab-buttons {{
            display: flex;
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 1rem;
        }}
        
        .tab-button {{
            padding: 0.75rem 1.5rem;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 500;
            color: #718096;
            transition: color 0.2s;
        }}
        
        .tab-button.active {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            margin-bottom: -2px;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .error-log {{
            background: #fef5e7;
            border: 1px solid #fed7aa;
            border-radius: 6px;
            padding: 1rem;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85rem;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #718096;
            border-top: 1px solid #e2e8f0;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Buildly Labs Foundry</h1>
        <p>Automation Dashboard - Generated {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
    </div>
    
    <div class="container">
        <!-- Recommendations Section -->
        <div class="card">
            <h2>🎯 Recommendations & Alerts</h2>
            {generate_recommendations_html(recommendations)}
        </div>
        
        <!-- Quick Stats Grid -->
        <div class="grid">
            <!-- Automation Status -->
            <div class="card">
                <h2>📊 Automation Status</h2>
                <div class="metric">
                    <span class="metric-label">Last 24 Hours</span>
                    <span class="metric-value {'status-good' if log_data.get('day', {}).get('success', 0) > 0 and log_data.get('day', {}).get('failure', 0) == 0 else 'status-warning' if log_data.get('day', {}).get('success', 0) > 0 else 'status-error'}">
                        {log_data.get('day', {}).get('success', 0)} success, {log_data.get('day', {}).get('failure', 0)} failures
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Last 7 Days</span>
                    <span class="metric-value">
                        {log_data.get('week', {}).get('success', 0)} success, {log_data.get('week', {}).get('failure', 0)} failures
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Last 30 Days</span>
                    <span class="metric-value">
                        {log_data.get('month', {}).get('success', 0)} success, {log_data.get('month', {}).get('failure', 0)} failures
                    </span>
                </div>
            </div>
            
            <!-- Outreach Stats -->
            <div class="card">
                <h2>📧 Outreach Performance</h2>
                <div class="metric">
                    <span class="metric-label">Total Contacts</span>
                    <span class="metric-value">{outreach_data.get('contacts', {}).get('total', 0):,}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">New Today</span>
                    <span class="metric-value">{outreach_data.get('contacts', {}).get('recent', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Emails Sent (Week)</span>
                    <span class="metric-value">{outreach_data.get('outreach_log', {}).get('week', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Pending Messages</span>
                    <span class="metric-value {'status-warning' if outreach_data.get('pending', {}).get('ready', 0) > 50 else ''}">{outreach_data.get('pending', {}).get('ready', 0)}</span>
                </div>
            </div>
            
            <!-- Configuration Status -->
            <div class="card">
                <h2>⚙️ Configuration Status</h2>
                <div class="metric">
                    <span class="metric-label">Configured Variables</span>
                    <span class="metric-value status-good">{env_data['total_configured']}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Missing Variables</span>
                    <span class="metric-value {'status-error' if env_data['total_missing'] > 0 else 'status-good'}">{env_data['total_missing']}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">System Health</span>
                    <span class="metric-value status-good">Operational</span>
                </div>
            </div>
        </div>
        
        <!-- Detailed Tabs -->
        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab('outreach')">📧 Outreach Details</button>
                <button class="tab-button" onclick="showTab('environment')">⚙️ Environment</button>
                <button class="tab-button" onclick="showTab('logs')">📋 Error Logs</button>
                <button class="tab-button" onclick="showTab('system')">🔧 System Health</button>
            </div>
            
            <!-- Outreach Tab -->
            <div id="outreach" class="tab-content active">
                <div class="grid">
                    <div class="card">
                        <h2>Contact Sources</h2>
                        {generate_sources_html(outreach_data.get('contacts', {}).get('sources', {}))}
                    </div>
                    <div class="card">
                        <h2>Target Categories</h2>
                        {generate_categories_html(outreach_data.get('targets', {}).get('categories', {}))}
                    </div>
                </div>
                
                <div class="card">
                    <h2>Outreach Timeline</h2>
                    <div class="metric">
                        <span class="metric-label">Today</span>
                        <span class="metric-value">{outreach_data.get('outreach_log', {}).get('today', 0)} emails</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">This Week</span>
                        <span class="metric-value">{outreach_data.get('outreach_log', {}).get('week', 0)} emails</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">This Month</span>
                        <span class="metric-value">{outreach_data.get('outreach_log', {}).get('month', 0)} emails</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total Historical</span>
                        <span class="metric-value">{outreach_data.get('outreach_log', {}).get('total', 0)} emails</span>
                    </div>
                </div>
            </div>
            
            <!-- Environment Tab -->
            <div id="environment" class="tab-content">
                <div class="card">
                    <h2>✅ Configured Variables</h2>
                    {generate_env_vars_html(env_data['configured'], True)}
                </div>
                
                {generate_missing_env_html(env_data['missing']) if env_data['missing'] else ''}
            </div>
            
            <!-- Logs Tab -->
            <div id="logs" class="tab-content">
                <div class="card">
                    <h2>Recent Error Logs</h2>
                    {generate_error_logs_html(log_data)}
                </div>
                
                <div class="card">
                    <h2>📋 Recent Log Files</h2>
                    {generate_log_files_html(recent_logs)}
                </div>
            </div>
            
            <!-- System Tab -->
            <div id="system" class="tab-content">
                <div class="grid">
                    <div class="card">
                        <h2>📁 Directories</h2>
                        {generate_health_html(health_data.get('directories', {}), 'directory')}
                    </div>
                    <div class="card">
                        <h2>📄 Key Files</h2>
                        {generate_health_html(health_data.get('files', {}), 'file')}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by Buildly Labs Foundry Dashboard • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Auto-refresh this page to see updated metrics</p>
    </div>
    
    <script>
        function showTab(tabName) {{
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => button.classList.remove('active'));
            
            // Show selected tab and mark button as active
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        function openLogFile(filename) {{
            // In a real implementation, this would show log contents
            alert('Log file: ' + filename + '\\n\\nTo view full contents, check logs/' + filename);
        }}
        
        // Auto-refresh every 5 minutes
        setTimeout(() => {{
            location.reload();
        }}, 300000);
    </script>
</body>
</html>
    """
    
    return html_content

def generate_recommendations_html(recommendations: List[Dict[str, str]]) -> str:
    """Generate HTML for recommendations"""
    if not recommendations:
        return '<div class="recommendation info"><h4>✅ All Systems Operational</h4><p>No immediate actions required.</p></div>'
    
    html = ''
    for rec in recommendations:
        html += f'''
        <div class="recommendation {rec['type']}">
            <h4>{rec['title']}</h4>
            <p><strong>Issue:</strong> {rec['description']}</p>
            <p><strong>Action:</strong> {rec['action']}</p>
        </div>
        '''
    return html

def generate_sources_html(sources: Dict[str, int]) -> str:
    """Generate HTML for contact sources"""
    if not sources:
        return '<p>No contact sources found.</p>'
    
    html = ''
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]:
        html += f'''
        <div class="metric">
            <span class="metric-label">{source}</span>
            <span class="metric-value">{count}</span>
        </div>
        '''
    return html

def generate_categories_html(categories: Dict[str, int]) -> str:
    """Generate HTML for target categories"""
    if not categories:
        return '<p>No target categories found.</p>'
    
    html = ''
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        html += f'''
        <div class="metric">
            <span class="metric-label">{category.title()}</span>
            <span class="metric-value">{count}</span>
        </div>
        '''
    return html

def generate_env_vars_html(env_vars: Dict[str, Dict], configured: bool) -> str:
    """Generate HTML for environment variables"""
    if not env_vars:
        return '<p>No variables in this category.</p>'
    
    html = ''
    for var_name, var_data in env_vars.items():
        css_class = 'configured' if configured else 'missing'
        value_display = var_data.get('value', 'NOT SET') if configured else 'MISSING'
        
        html += f'''
        <div class="env-var {css_class}">
            <div>
                <div class="env-var-name">{var_name}</div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.25rem;">{var_data['description']}</div>
            </div>
            <div class="env-var-value">{value_display}</div>
        </div>
        '''
    return html

def generate_missing_env_html(missing_vars: Dict[str, Dict]) -> str:
    """Generate HTML for missing environment variables"""
    required_missing = {k: v for k, v in missing_vars.items() if v['required']}
    optional_missing = {k: v for k, v in missing_vars.items() if not v['required']}
    
    html = ''
    
    if required_missing:
        html += '''
        <div class="card">
            <h2>❌ Missing Required Variables</h2>
        '''
        html += generate_env_vars_html(required_missing, False)
        html += '</div>'
    
    if optional_missing:
        html += '''
        <div class="card">
            <h2>⚠️ Missing Optional Variables</h2>
        '''
        html += generate_env_vars_html(optional_missing, False)
        html += '</div>'
    
    return html

def generate_error_logs_html(log_data: Dict[str, Any]) -> str:
    """Generate HTML for recent error logs"""
    errors = []
    
    # Collect errors from all periods
    for period in ['day', 'week', 'month']:
        period_data = log_data.get(period, {})
        period_errors = period_data.get('errors', [])
        if period_errors:
            errors.extend(period_errors[-10:])  # Last 10 errors from each period
    
    if not errors:
        return '<p class="status-good">No recent errors found. ✅</p>'
    
    # Deduplicate and limit errors
    unique_errors = list(set(errors))[-20:]  # Last 20 unique errors
    
    error_text = '\\n'.join(unique_errors)
    return f'<div class="error-log">{error_text}</div>'

def generate_log_files_html(log_files: List[Path]) -> str:
    """Generate HTML for log file listing"""
    if not log_files:
        return '<p>No log files found.</p>'
    
    html = ''
    for log_file in log_files:
        size_kb = log_file.stat().st_size / 1024
        modified = datetime.fromtimestamp(log_file.stat().st_mtime)
        
        html += f'''
        <div class="log-file" onclick="openLogFile('{log_file.name}')">
            <div class="log-file-name">{log_file.name}</div>
            <div class="log-file-size">{size_kb:.1f} KB • Modified {modified.strftime('%Y-%m-%d %H:%M')}</div>
        </div>
        '''
    return html

def generate_health_html(health_data: Dict[str, Any], item_type: str) -> str:
    """Generate HTML for system health data"""
    if not health_data:
        return f'<p>No {item_type} data available.</p>'
    
    html = ''
    for name, status in health_data.items():
        exists = status.get('exists', False)
        readable = status.get('readable', False)
        writable = status.get('writable', False)
        
        status_icon = '✅' if exists and readable else '❌'
        status_class = 'status-good' if exists and readable else 'status-error'
        
        html += f'''
        <div class="metric">
            <span class="metric-label">{status_icon} {name}</span>
            <span class="metric-value {status_class}">
                {'OK' if exists and readable else 'ERROR'}
            </span>
        </div>
        '''
    return html

def main():
    """Generate and save the dashboard"""
    print("🔄 Generating automation dashboard...")
    
    try:
        # Ensure reports directory exists
        reports_dir = Path('reports/automation')
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        html_content = generate_html_dashboard()
        
        # Archive previous current dashboard if it exists
        current_dashboard = reports_dir / 'dashboard.html'
        if current_dashboard.exists():
            # Create timestamped archive of previous version
            timestamp = datetime.fromtimestamp(current_dashboard.stat().st_mtime).strftime('%Y%m%d_%H%M%S')
            archive_file = reports_dir / f'dashboard_{timestamp}.html'
            current_dashboard.rename(archive_file)
            print(f"📦 Archived previous dashboard: {archive_file.name}")
        
        # Save new current dashboard (no timestamp)
        with open(current_dashboard, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Also save as root-level for backward compatibility
        root_dashboard = Path('automation_dashboard.html')
        with open(root_dashboard, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Current dashboard: {current_dashboard.absolute()}")
        print(f"🔗 Bookmarkable URL: file://{current_dashboard.absolute()}")
        print(f"🌐 Quick access: file://{root_dashboard.absolute()}")
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        raise

if __name__ == "__main__":
    main()