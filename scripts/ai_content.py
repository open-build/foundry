#!/usr/bin/env python3
"""
AI Content Engine for First City Foundry
=========================================

Uses OpenAI to generate:
- Personalized outreach emails
- Social media posts (LinkedIn, Twitter/X)
- Blog post drafts
- SEO meta descriptions
- Newsletter content

Integrates with the existing StartupOutreachBot pipeline.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# ── Brand context injected into every prompt ────────────────────
BRAND_CONTEXT = """
You are writing for First City Foundry (FCF), a Portland-based startup foundry.

Brand voice:
- Confident but approachable — Pacific Northwest warmth, not Silicon Valley hype
- Direct and founder-focused — speak *to* builders, not *about* them
- Use "we" for FCF, "you" for the reader
- Avoid: "disrupt", "synergy", "leverage", jargon walls
- Favor: clear language, concrete outcomes, short paragraphs

Key facts:
- Portland Metro region HQ, expanding to Medellín, New York, Berlin
- Partners: Buildly, Kurent Co, Open.Build, Startup Grind PDX, Prepare4VC
- VMI Index: Viability-Market-Innovation scoring for startups
- Focus: solo founders and small teams turning ideas into scalable companies
- Website: https://www.firstcityfoundry.com
- Podcast: The Foundry — conversations with founders and operators
"""


class AIContentEngine:
    """Generate marketing content via OpenAI."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.content_dir = Path(__file__).parent.parent / "content"
        self.content_dir.mkdir(exist_ok=True)
        (self.content_dir / "blog").mkdir(exist_ok=True)
        (self.content_dir / "social").mkdir(exist_ok=True)

        if not self.api_key or self.api_key.startswith("sk-..."):
            logger.warning("OPENAI_API_KEY not set — AI content generation disabled")

    # ── low-level chat call ──────────────────────────────────
    def _chat(self, system: str, user: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """Call the OpenAI chat completions API."""
        if not self.api_key or self.api_key.startswith("sk-..."):
            return "[AI content unavailable — set OPENAI_API_KEY in .env]"

        import httpx  # included in requirements

        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()

    # ── Outreach email personalization ───────────────────────
    def personalize_outreach(
        self,
        contact_name: str,
        organization: str,
        category: str,
        focus_areas: List[str],
        template_body: str,
    ) -> Dict[str, str]:
        """Return a personalized subject + body for an outreach email."""

        system = BRAND_CONTEXT + "\nYou specialize in writing short, personalized outreach emails."
        user = f"""Personalize this outreach email for:
Recipient: {contact_name} at {organization}
Category: {category}
Their focus areas: {', '.join(focus_areas)}

--- template ---
{template_body}
--- end ---

Return JSON with keys "subject" and "body". Keep body under 150 words.
Do NOT use markdown in the body — plain text only."""

        raw = self._chat(system, user, max_tokens=600, temperature=0.6)
        try:
            # strip possible ```json fences
            cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"subject": f"First City Foundry × {organization}", "body": raw}

    # ── Social media posts ───────────────────────────────────
    def generate_social_post(
        self,
        platform: str,
        topic: str,
        call_to_action: str = "",
        context: str = "",
    ) -> str:
        """Generate a single social media post for the given platform."""

        length_guide = {
            "twitter": "Under 280 characters. Punchy, conversational. Include 1-2 relevant hashtags.",
            "linkedin": "150-300 words. Professional but warm. End with a question or CTA to drive engagement. Use line breaks for readability.",
        }

        system = BRAND_CONTEXT + f"\nYou write {platform} posts. " + length_guide.get(platform, "")
        user = f"Topic: {topic}"
        if context:
            user += f"\nAdditional context: {context}"
        if call_to_action:
            user += f"\nCall to action: {call_to_action}"

        return self._chat(system, user, max_tokens=500, temperature=0.8)

    def generate_social_batch(
        self,
        topics: List[str],
        platforms: List[str] = None,
    ) -> List[Dict[str, str]]:
        """Generate a batch of posts and save to content/social/."""
        platforms = platforms or ["twitter", "linkedin"]
        posts = []
        for topic in topics:
            for platform in platforms:
                text = self.generate_social_post(platform, topic)
                posts.append({"platform": platform, "topic": topic, "text": text, "generated": datetime.now().isoformat()})

        out_file = self.content_dir / "social" / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(out_file, "w") as f:
            json.dump(posts, f, indent=2)

        logger.info(f"Generated {len(posts)} social posts → {out_file}")
        return posts

    # ── Blog post drafts ─────────────────────────────────────
    def generate_blog_draft(
        self,
        title: str,
        outline: str = "",
        target_words: int = 800,
    ) -> str:
        """Generate a blog post draft in Markdown."""

        system = BRAND_CONTEXT + """
You write blog posts for the First City Foundry website.
Format: Markdown with H2/H3 subheadings, short paragraphs, bullet lists where useful.
Tone: educational and founder-empathetic — teach something, don't just promote.
End with a clear CTA linking to https://www.firstcityfoundry.com/register.html"""

        user = f"Title: {title}\nTarget length: ~{target_words} words"
        if outline:
            user += f"\nOutline:\n{outline}"

        draft = self._chat(system, user, max_tokens=target_words * 2, temperature=0.7)

        slug = title.lower().replace(" ", "-")[:60]
        out_file = self.content_dir / "blog" / f"{datetime.now().strftime('%Y%m%d')}_{slug}.md"
        with open(out_file, "w") as f:
            f.write(f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%d')}\ndraft: true\n---\n\n{draft}")

        logger.info(f"Blog draft → {out_file}")
        return draft

    # ── SEO meta descriptions ────────────────────────────────
    def generate_meta_description(self, page_title: str, page_content_snippet: str) -> str:
        """Generate SEO-optimized meta description (≤160 chars)."""
        system = "You are an SEO specialist. Write a compelling meta description under 160 characters."
        user = f"Page: {page_title}\nContent snippet: {page_content_snippet[:500]}"
        return self._chat(system, user, max_tokens=100, temperature=0.5)

    # ── Newsletter section ───────────────────────────────────
    def generate_newsletter_section(self, updates: List[str], audience: str = "founders") -> str:
        """Generate a newsletter section summarizing recent updates."""
        system = BRAND_CONTEXT + "\nWrite a concise newsletter section in HTML (inline styles OK for email)."
        user = f"Audience: {audience}\nRecent updates:\n" + "\n".join(f"- {u}" for u in updates)
        return self._chat(system, user, max_tokens=800, temperature=0.7)


# ── CLI entry point ──────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="AI Content Engine for First City Foundry")
    sub = parser.add_subparsers(dest="command")

    # social
    sp = sub.add_parser("social", help="Generate social media posts")
    sp.add_argument("--topics", nargs="+", required=True)
    sp.add_argument("--platforms", nargs="+", default=["twitter", "linkedin"])

    # blog
    bp = sub.add_parser("blog", help="Generate a blog draft")
    bp.add_argument("--title", required=True)
    bp.add_argument("--outline", default="")
    bp.add_argument("--words", type=int, default=800)

    # meta
    mp = sub.add_parser("meta", help="Generate meta description")
    mp.add_argument("--page-title", required=True)
    mp.add_argument("--snippet", required=True)

    args = parser.parse_args()
    engine = AIContentEngine()

    if args.command == "social":
        posts = engine.generate_social_batch(args.topics, args.platforms)
        for p in posts:
            print(f"\n[{p['platform'].upper()}] {p['topic']}")
            print(p["text"])
    elif args.command == "blog":
        draft = engine.generate_blog_draft(args.title, args.outline, args.words)
        print(draft)
    elif args.command == "meta":
        desc = engine.generate_meta_description(args.page_title, args.snippet)
        print(desc)
    else:
        parser.print_help()
