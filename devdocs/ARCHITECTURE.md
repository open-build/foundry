# The Foundry Collective — Architecture & Decisions

> Internal devdoc covering the site redesign, partner model, AI automation, and ForgeWeb integration.

---

## 1. Brand & Site Redesign

**Old brand:** Buildly Labs Foundry (single-partner incubator)
**New brand:** The Foundry Collective — Build. Scale. Escape.

### Colour System
| Token      | Hex       | Usage                          |
|------------|-----------|--------------------------------|
| brand-500  | `#F97316` | Primary CTA, highlights        |
| navy-900   | `#0F1F35` | Hero backgrounds, dark sections|
| mint-500   | `#10B981` | Accent, Kurent / Margin theme  |

### Typography
- **Font family:** Inter (Google Fonts CDN)
- **Stack:** Tailwind CSS via CDN only — no NPM build step

### V·M·I Framework
Every section of the site maps to one of three dimensions:
- **Visibility** — orange — `fa-eye`
- **Margin** — emerald — `fa-chart-line`
- **Independence** — blue — `fa-door-open`

---

## 2. Site Structure

```
docs/                       ← GitHub Pages root
├── index.html              ← Homepage (all sections)
├── register.html           ← Index survey (Google Sheets + BabbleBeaver)
├── podcast.html            ← Legacy podcast guest form
├── success.html            ← Form success page
├── opt-out.html            ← Email opt-out
├── components/
│   ├── header.html         ← Shared nav (loaded via fetch)
│   ├── footer.html         ← Shared footer (loaded via fetch)
│   └── partner-card.html   ← <template> element for partner rendering
├── data/
│   ├── partners.json       ← Partner ecosystem data
│   └── cities.json         ← Global expansion cities
├── pages/
│   ├── podcast.html        ← Podcast hub (new branding)
│   ├── partners.html       ← Partner directory + criteria
│   ├── index-report.html   ← V·M·I Index deep-dive
│   └── about.html          ← Origin story, principles, cities
└── assets/
    ├── css/main.css
    ├── js/
    │   ├── site.js         ← Component loader, partner/city renderers
    │   ├── form.js         ← Registration form (Google Sheets)
    │   ├── opt-out.js
    │   └── podcast-form.js ← Podcast guest form
    └── img/
```

### Path-Depth Convention
Pages in `pages/` set `<meta name="path-depth" content="1">` so that `site.js` prefixes asset paths with `../`. The homepage uses `content="0"`.

---

## 3. Partner Ecosystem Model

### Lifecycle Stages
| Stage    | Partner           | Type         | Responsibility                    |
|----------|-------------------|--------------|-----------------------------------|
| BUILD    | Buildly           | core         | AI-native product development     |
| TRAIN    | Open.Build        | core         | Skills, open-source, CollabHub    |
| CONNECT  | Startup Grind PDX | distribution | Events, community (temporary)     |
| CONNECT  | Prepare4VC        | strategic    | Investor readiness, pitch prep    |
| OPERATE  | Kurent Co         | core         | Operational architecture, SOPs    |

### Acceptance Rules
- **Accept** if: covers unfilled lifecycle stage, equity-free or revenue-share, local + global capacity, aligns with V·M·I
- **Decline** if: duplicates existing partner, requires equity, generic mentorship only, can't commit to city model

### Data Flow
`docs/data/partners.json` → `site.js:loadPartners()` → renders cards with type-coloured badges → links to partner websites

---

## 4. ForgeWeb Integration

### Submodule
```
ForgeWeb/   ← git submodule from Buildly-Marketplace/ForgeWeb
├── admin/
│   ├── file-api.py        ← HTTP server (patched to use docs/)
│   ├── database.py        ← ForgeWebDB class (SQLite)
│   ├── site-config.json   ← Foundry Collective config
│   └── branding-config.json
└── ...
```

### Database
SQLite at `ForgeWeb/admin/forgeweb.db` (gitignored). Tables:
`site_config`, `pages`, `articles`, `navigation`, `branding`, `design_config`, `media`, `settings`, `social_media`

### Import Script
`scripts/import_to_forgeweb.py` populates the DB with all pages, nav items, branding, and settings. Run it after cloning or resetting the DB.

---

## 5. AI Automation

### Outreach Pipeline
1. `scripts/startup_outreach.py` — discovers targets, sends emails via Brevo SMTP
2. `scripts/daily_automation.py` — runs outreach + reporting on a schedule
3. `ai/marketing_prompts.md` — system prompts for LLM-powered outreach personalisation
4. `ai/outreach_templates.md` — email templates with merge variables

### AI-Tools Folder
```
ai-tools/
├── reporting/
│   ├── generate_report.py   ← wraps scripts/generate_dashboard.py
│   └── weekly_summary.py    ← aggregates daily reports
├── automation/
│   └── task_runner.py       ← generic script runner with logging
└── openclaw/
    ├── cron-jobs.json       ← scheduled tasks for OpenClaw
    └── skills.json          ← agent skills for OpenClaw
```

### OpenClaw Integration
OpenClaw v2026.3.1 installed globally. Cron jobs and skills defined in `ai-tools/openclaw/`. Register with:
```bash
openclaw cron import ai-tools/openclaw/cron-jobs.json
openclaw skill import ai-tools/openclaw/skills.json
```

---

## 6. Form Infrastructure

| Form              | Endpoint                          | Handler             |
|-------------------|-----------------------------------|----------------------|
| Index Survey      | Google Apps Script (see form.js)  | `assets/js/form.js`  |
| Podcast Guest     | Same Google Script                | `assets/js/podcast-form.js` |
| BabbleBeaver      | `api.babblebeaver.com/analyze`    | Called from form.js  |

---

## 7. Deployment

- **GitHub Pages** deploys from `docs/` on `main` branch
- **Custom domain:** `www.firstcityfoundry.com` (CNAME file in docs/)
- **No build step** — pure HTML + Tailwind CDN
- ForgeWeb admin runs locally only (not deployed)
