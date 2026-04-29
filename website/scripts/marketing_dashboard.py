#!/usr/bin/env python3
"""
Marketing Analytics Dashboard for First City Foundry
=====================================================

Aggregates data from:
- Outreach pipeline (contacts, emails, responses)
- Social media queue (posts, engagement)
- Blog/SEO pipeline (published posts, SEO issues)
- Google Analytics (if configured)

Outputs an HTML dashboard and optional email summary.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent
OUTREACH_DIR = ROOT_DIR / "outreach_data"
CONTENT_DIR = ROOT_DIR / "content"
REPORTS_DIR = ROOT_DIR / "reports" / "marketing"
DOCS_DIR = ROOT_DIR / "docs"


class MarketingDashboard:
    """Aggregate marketing metrics into a single report."""

    def __init__(self):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def collect_outreach_metrics(self) -> Dict[str, Any]:
        """Metrics from the outreach pipeline."""
        metrics = {"contacts": 0, "emails_sent": 0, "pending": 0, "opt_outs": 0, "targets": 0}

        contacts_file = OUTREACH_DIR / "contacts.json"
        if contacts_file.exists():
            data = json.loads(contacts_file.read_text())
            metrics["contacts"] = len(data)
            metrics["emails_sent"] = sum(1 for c in data if c.get("outreach_count", 0) > 0)

        pending_file = OUTREACH_DIR / "pending_outreach.json"
        if pending_file.exists():
            data = json.loads(pending_file.read_text())
            metrics["pending"] = sum(1 for p in data if not p.get("sent", False))

        opt_outs_file = OUTREACH_DIR / "opt_outs.json"
        if opt_outs_file.exists():
            data = json.loads(opt_outs_file.read_text())
            metrics["opt_outs"] = data.get("total_opt_outs", 0)

        targets_file = OUTREACH_DIR / "targets.json"
        if targets_file.exists():
            data = json.loads(targets_file.read_text())
            metrics["targets"] = len(data)

        return metrics

    def collect_social_metrics(self) -> Dict[str, Any]:
        """Metrics from the social media queue."""
        metrics = {"total_posts": 0, "posted": 0, "pending": 0, "failed": 0}

        queue_file = CONTENT_DIR / "social" / "queue.json"
        if queue_file.exists():
            data = json.loads(queue_file.read_text())
            metrics["total_posts"] = len(data)
            for item in data:
                status = item.get("status", "pending")
                if status == "posted":
                    metrics["posted"] += 1
                elif status == "pending":
                    metrics["pending"] += 1
                elif status == "failed":
                    metrics["failed"] += 1

        # count generated batches
        social_dir = CONTENT_DIR / "social"
        if social_dir.exists():
            metrics["batches_generated"] = len(list(social_dir.glob("batch_*.json")))

        return metrics

    def collect_blog_metrics(self) -> Dict[str, Any]:
        """Metrics from the blog pipeline."""
        metrics = {"drafts": 0, "published": 0}

        blog_content = CONTENT_DIR / "blog"
        if blog_content.exists():
            metrics["drafts"] = len(list(blog_content.glob("*.md")))

        blog_docs = DOCS_DIR / "blog"
        if blog_docs.exists():
            metrics["published"] = len(list(blog_docs.glob("*.html")))

        return metrics

    def collect_seo_metrics(self) -> Dict[str, Any]:
        """Run a quick SEO check."""
        try:
            from seo_content import SEOAuditor
            issues = SEOAuditor().audit()
            return {"total_issues": len(issues), "pages_scanned": len(set(i["file"] for i in issues)) if issues else 0}
        except Exception as e:
            logger.warning(f"SEO audit skipped: {e}")
            return {"total_issues": -1, "pages_scanned": 0}

    def generate_report(self) -> Dict[str, Any]:
        """Collect all metrics into one report dict."""
        report = {
            "generated": datetime.now().isoformat(),
            "outreach": self.collect_outreach_metrics(),
            "social": self.collect_social_metrics(),
            "blog": self.collect_blog_metrics(),
            "seo": self.collect_seo_metrics(),
        }
        return report

    def generate_html(self) -> Path:
        """Generate a pretty HTML dashboard."""
        report = self.generate_report()
        o = report["outreach"]
        s = report["social"]
        b = report["blog"]
        seo = report["seo"]

        html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Marketing Dashboard — First City Foundry</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>body {{ font-family: 'DM Sans', sans-serif; }}</style>
</head>
<body class="bg-stone-50 p-6">
<div class="max-w-5xl mx-auto">
  <h1 class="text-3xl font-bold mb-1">Marketing Dashboard</h1>
  <p class="text-stone-400 text-sm mb-8">Generated {report['generated'][:16]}</p>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
    <div class="bg-white rounded-xl p-5 shadow-sm border border-stone-200">
      <p class="text-xs uppercase tracking-wider text-stone-400 mb-1">Contacts</p>
      <p class="text-3xl font-bold">{o['contacts']}</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-stone-200">
      <p class="text-xs uppercase tracking-wider text-stone-400 mb-1">Emails Sent</p>
      <p class="text-3xl font-bold">{o['emails_sent']}</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-stone-200">
      <p class="text-xs uppercase tracking-wider text-stone-400 mb-1">Social Posts</p>
      <p class="text-3xl font-bold">{s['posted']}</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-stone-200">
      <p class="text-xs uppercase tracking-wider text-stone-400 mb-1">Blog Posts</p>
      <p class="text-3xl font-bold">{b['published']}</p>
    </div>
  </div>

  <div class="grid md:grid-cols-2 gap-6">
    <!-- Outreach -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-stone-200">
      <h2 class="font-semibold text-lg mb-4">📧 Outreach Pipeline</h2>
      <table class="w-full text-sm">
        <tr class="border-b"><td class="py-2 text-stone-500">Contacts discovered</td><td class="py-2 text-right font-medium">{o['contacts']}</td></tr>
        <tr class="border-b"><td class="py-2 text-stone-500">Emails sent</td><td class="py-2 text-right font-medium">{o['emails_sent']}</td></tr>
        <tr class="border-b"><td class="py-2 text-stone-500">Pending queue</td><td class="py-2 text-right font-medium">{o['pending']}</td></tr>
        <tr class="border-b"><td class="py-2 text-stone-500">Opt-outs</td><td class="py-2 text-right font-medium">{o['opt_outs']}</td></tr>
        <tr><td class="py-2 text-stone-500">Target orgs</td><td class="py-2 text-right font-medium">{o['targets']}</td></tr>
      </table>
    </div>

    <!-- Social -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-stone-200">
      <h2 class="font-semibold text-lg mb-4">📱 Social Media</h2>
      <table class="w-full text-sm">
        <tr class="border-b"><td class="py-2 text-stone-500">Total queued</td><td class="py-2 text-right font-medium">{s['total_posts']}</td></tr>
        <tr class="border-b"><td class="py-2 text-stone-500">Posted</td><td class="py-2 text-right font-medium">{s['posted']}</td></tr>
        <tr class="border-b"><td class="py-2 text-stone-500">Pending</td><td class="py-2 text-right font-medium">{s['pending']}</td></tr>
        <tr><td class="py-2 text-stone-500">Failed</td><td class="py-2 text-right font-medium">{s['failed']}</td></tr>
      </table>
    </div>

    <!-- Blog -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-stone-200">
      <h2 class="font-semibold text-lg mb-4">📝 Blog & Content</h2>
      <table class="w-full text-sm">
        <tr class="border-b"><td class="py-2 text-stone-500">Drafts (Markdown)</td><td class="py-2 text-right font-medium">{b['drafts']}</td></tr>
        <tr><td class="py-2 text-stone-500">Published (HTML)</td><td class="py-2 text-right font-medium">{b['published']}</td></tr>
      </table>
    </div>

    <!-- SEO -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-stone-200">
      <h2 class="font-semibold text-lg mb-4">🔍 SEO Health</h2>
      <table class="w-full text-sm">
        <tr class="border-b"><td class="py-2 text-stone-500">Issues found</td><td class="py-2 text-right font-medium">{seo['total_issues'] if seo['total_issues'] >= 0 else 'N/A'}</td></tr>
        <tr><td class="py-2 text-stone-500">Pages with issues</td><td class="py-2 text-right font-medium">{seo['pages_scanned']}</td></tr>
      </table>
    </div>
  </div>

  <p class="text-center text-stone-300 text-xs mt-8">First City Foundry — Marketing Automation Dashboard</p>
</div>
</body></html>"""

        out_path = REPORTS_DIR / f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        out_path.write_text(html)
        logger.info(f"Dashboard → {out_path}")

        # also write a latest.html symlink-like copy
        latest = REPORTS_DIR / "dashboard.html"
        latest.write_text(html)

        return out_path

    def generate_email_summary(self) -> str:
        """Return an HTML snippet suitable for email."""
        report = self.generate_report()
        o, s, b = report["outreach"], report["social"], report["blog"]

        return f"""
<h2 style="font-family:sans-serif">Daily Marketing Summary</h2>
<table style="font-family:sans-serif;font-size:14px;border-collapse:collapse;width:100%">
  <tr><td style="padding:6px;border-bottom:1px solid #eee"><strong>Contacts</strong></td><td style="padding:6px;border-bottom:1px solid #eee">{o['contacts']}</td></tr>
  <tr><td style="padding:6px;border-bottom:1px solid #eee"><strong>Emails sent</strong></td><td style="padding:6px;border-bottom:1px solid #eee">{o['emails_sent']}</td></tr>
  <tr><td style="padding:6px;border-bottom:1px solid #eee"><strong>Social posted</strong></td><td style="padding:6px;border-bottom:1px solid #eee">{s['posted']}</td></tr>
  <tr><td style="padding:6px;border-bottom:1px solid #eee"><strong>Social pending</strong></td><td style="padding:6px;border-bottom:1px solid #eee">{s['pending']}</td></tr>
  <tr><td style="padding:6px"><strong>Blog posts</strong></td><td style="padding:6px">{b['published']}</td></tr>
</table>
"""


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="Marketing Dashboard — First City Foundry")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("report", help="Print JSON report")
    sub.add_parser("html", help="Generate HTML dashboard")
    sub.add_parser("email", help="Print email summary HTML")

    args = parser.parse_args()
    dash = MarketingDashboard()

    if args.command == "report":
        print(json.dumps(dash.generate_report(), indent=2))
    elif args.command == "html":
        path = dash.generate_html()
        print(f"Dashboard written to {path}")
    elif args.command == "email":
        print(dash.generate_email_summary())
    else:
        parser.print_help()
