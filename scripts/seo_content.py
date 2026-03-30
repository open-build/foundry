#!/usr/bin/env python3
"""
SEO & Blog Content Pipeline for First City Foundry
====================================================

Automates:
- Blog post generation + HTML page creation in docs/blog/
- Sitemap.xml updates
- Meta description optimization for every page
- Internal link audit
- Keyword density analysis
"""

import os
import re
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
BLOG_DIR = DOCS_DIR / "blog"
CONTENT_DIR = ROOT_DIR / "content" / "blog"
SITEMAP_PATH = DOCS_DIR / "sitemap.xml"
SITE_URL = os.getenv("WEBSITE_URL", "https://www.firstcityfoundry.com")


# ── Blog publisher ───────────────────────────────────────────

BLOG_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="path-depth" content="1">
    <title>{title} — First City Foundry</title>
    <meta name="description" content="{meta_description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body class="bg-white text-gray-900 font-sans antialiased">
<div id="header-slot"></div>

<main class="pt-24 pb-16">
  <article class="prose prose-lg mx-auto max-w-3xl px-4 sm:px-6">
    <p class="text-sm uppercase tracking-wider text-forest-600 font-semibold mb-2">{date}</p>
    <h1 class="text-3xl sm:text-4xl font-bold mb-8 font-display">{title}</h1>
    {html_content}
  </article>
</main>

<div id="footer-slot"></div>
<script src="../assets/js/site.js"></script>
<script>document.addEventListener('DOMContentLoaded', initComponents);</script>
</body>
</html>
"""


class BlogPublisher:
    """Turn Markdown drafts into HTML pages and update sitemap."""

    def __init__(self):
        BLOG_DIR.mkdir(parents=True, exist_ok=True)
        CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _md_to_html(md: str) -> str:
        """Minimal Markdown → HTML conversion (no external dependency)."""
        lines = md.split("\n")
        html_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            # skip frontmatter
            if stripped == "---":
                continue
            if stripped.startswith("title:") or stripped.startswith("date:") or stripped.startswith("draft:"):
                continue

            if stripped.startswith("### "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h3>{stripped[4:]}</h3>")
            elif stripped.startswith("## "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h2>{stripped[3:]}</h2>")
            elif stripped.startswith("- "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"  <li>{stripped[2:]}</li>")
            elif stripped == "":
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                # bold / italic / links
                processed = stripped
                processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
                processed = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed)
                processed = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" class="text-amber-600 hover:underline">\1</a>', processed)
                html_lines.append(f"<p>{processed}</p>")

        if in_list:
            html_lines.append("</ul>")

        return "\n    ".join(html_lines)

    def publish_draft(self, md_path: Path) -> Optional[Path]:
        """Convert a Markdown draft to an HTML blog page. Returns output path."""
        text = md_path.read_text()

        # extract frontmatter
        title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.MULTILINE)
        date_match = re.search(r'^date:\s*(.+)$', text, re.MULTILINE)
        title = title_match.group(1) if title_match else md_path.stem.replace("-", " ").title()
        date = date_match.group(1).strip() if date_match else datetime.now().strftime("%Y-%m-%d")

        # strip frontmatter block
        body = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL).strip()
        html_content = self._md_to_html(body)

        slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(" ", "-"))[:80]
        filename = f"{slug}.html"
        url = f"{SITE_URL}/blog/{filename}"

        # generate meta description via AI if available
        try:
            from ai_content import AIContentEngine
            meta = AIContentEngine().generate_meta_description(title, body[:500])
        except Exception:
            meta = f"{title} — insights for founders from First City Foundry"

        out_path = BLOG_DIR / filename
        out_path.write_text(BLOG_TEMPLATE.format(
            title=title,
            meta_description=meta[:160],
            url=url,
            date=date,
            html_content=html_content,
        ))

        logger.info(f"Published blog: {out_path}")
        self.update_sitemap(url)
        return out_path

    def publish_all_drafts(self) -> List[Path]:
        """Publish every .md file in content/blog/."""
        published = []
        for md_file in sorted(CONTENT_DIR.glob("*.md")):
            result = self.publish_draft(md_file)
            if result:
                published.append(result)
        return published

    # ── Sitemap management ───────────────────────────────────

    @staticmethod
    def update_sitemap(new_url: str):
        """Add a URL to sitemap.xml if not already present."""
        ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        ET.register_namespace("", ns)

        if SITEMAP_PATH.exists():
            tree = ET.parse(SITEMAP_PATH)
            root = tree.getroot()
        else:
            root = ET.Element(f"{{{ns}}}urlset")
            tree = ET.ElementTree(root)

        # check for duplicates
        existing = {el.text for el in root.iter(f"{{{ns}}}loc")}
        if new_url in existing:
            return

        url_el = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(url_el, f"{{{ns}}}loc").text = new_url
        ET.SubElement(url_el, f"{{{ns}}}lastmod").text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(url_el, f"{{{ns}}}changefreq").text = "monthly"
        ET.SubElement(url_el, f"{{{ns}}}priority").text = "0.7"

        tree.write(SITEMAP_PATH, xml_declaration=True, encoding="UTF-8")
        logger.info(f"Added {new_url} to sitemap.xml")


# ── SEO auditor ──────────────────────────────────────────────

class SEOAuditor:
    """Scan docs/ HTML files for SEO issues."""

    def audit(self) -> List[Dict]:
        """Return a list of issues found across all HTML pages."""
        issues = []

        for html_file in DOCS_DIR.rglob("*.html"):
            rel = html_file.relative_to(DOCS_DIR)
            content = html_file.read_text(errors="ignore")

            # missing title
            if "<title>" not in content:
                issues.append({"file": str(rel), "issue": "Missing <title> tag"})

            # missing meta description
            if 'name="description"' not in content:
                issues.append({"file": str(rel), "issue": "Missing meta description"})

            # title too long
            title_match = re.search(r'<title>(.+?)</title>', content)
            if title_match and len(title_match.group(1)) > 70:
                issues.append({"file": str(rel), "issue": f"Title too long ({len(title_match.group(1))} chars)"})

            # missing alt on images
            imgs_without_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', content)
            if imgs_without_alt:
                issues.append({"file": str(rel), "issue": f"{len(imgs_without_alt)} image(s) missing alt text"})

            # missing h1
            if "<h1" not in content and "index.html" not in str(rel):
                issues.append({"file": str(rel), "issue": "No <h1> tag found"})

        logger.info(f"SEO audit complete: {len(issues)} issues found")
        return issues


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="SEO & Blog Pipeline — First City Foundry")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("publish", help="Publish all Markdown drafts from content/blog/")
    sub.add_parser("audit", help="Run SEO audit on docs/ pages")
    sub.add_parser("sitemap", help="Show current sitemap entries")

    gp = sub.add_parser("generate", help="Generate a blog post via AI, then publish")
    gp.add_argument("--title", required=True)
    gp.add_argument("--outline", default="")

    args = parser.parse_args()

    if args.command == "publish":
        pub = BlogPublisher()
        published = pub.publish_all_drafts()
        print(f"Published {len(published)} posts")
        for p in published:
            print(f"  → {p}")
    elif args.command == "audit":
        issues = SEOAuditor().audit()
        for iss in issues:
            print(f"  [{iss['file']}] {iss['issue']}")
        print(f"\n{len(issues)} total issues")
    elif args.command == "sitemap":
        ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        if SITEMAP_PATH.exists():
            tree = ET.parse(SITEMAP_PATH)
            for loc in tree.getroot().iter(f"{{{ns}}}loc"):
                print(loc.text)
        else:
            print("No sitemap.xml found")
    elif args.command == "generate":
        from ai_content import AIContentEngine
        engine = AIContentEngine()
        engine.generate_blog_draft(args.title, args.outline)
        pub = BlogPublisher()
        published = pub.publish_all_drafts()
        for p in published:
            print(f"Published → {p}")
    else:
        parser.print_help()
