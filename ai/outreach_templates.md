# Outreach Templates — The Foundry Collective

Email and message templates for outreach campaigns. Used by `scripts/run_outreach.py` and `scripts/preview_outreach.py`.

---

## Template 1: Cold Intro — Founder

**Subject:** Your ops score might surprise you

**Body:**

Hi {first_name},

I came across {company_name} and noticed you're {personalization_hook}.

We run a free 5-minute survey called the Portland Operations & AI Index that scores companies on three dimensions — Visibility, Margin, and Independence. It's anonymous, benchmarked against other Portland-area companies, and the results are genuinely useful.

No pitch, no strings — just data about how your ops compare.

Take the survey: https://www.firstcityfoundry.com/register.html

Best,
The Foundry Collective team

---

## Template 2: Follow-Up (3 days after Template 1)

**Subject:** Re: Your ops score might surprise you

**Body:**

Hi {first_name},

Quick follow-up — a few founders have told us the V·M·I score clarified exactly where they were losing time.

The survey takes 5 minutes and you'll get a personalised score across Visibility (can you see what's happening?), Margin (how much effort per output?), and Independence (can the business run without you?).

Here's the link: https://www.firstcityfoundry.com/register.html

No pressure — just genuinely useful data.

Best,
The Foundry Collective team

---

## Template 3: Partner Introduction

**Subject:** Foundry Collective — potential partnership

**Body:**

Hi {contact_name},

I'm reaching out from The Foundry Collective — a global equity-free founder network operating in Portland, with expansion planned to Medellín, Nairobi, and Lisbon.

We work as a curated partner ecosystem where each organisation owns a stage of the founder lifecycle (Build → Train → Connect → Operate). We noticed {org_name} does excellent work in {their_domain}, and we currently have a gap in {lifecycle_stage}.

Would you be open to a 20-minute call to explore if there's a fit?

Quick overview: https://www.firstcityfoundry.com/pages/partners.html

Best,
The Foundry Collective team

---

## Template 4: Podcast Guest Invite

**Subject:** The Foundry Podcast — you'd be a great guest

**Body:**

Hi {first_name},

We're launching The Foundry Podcast — conversations with founders about the three things that actually matter: Visibility, Margin, and Independence.

I think {company_name}'s story around {specific_angle} would resonate with our audience. Episodes are 30–45 minutes, remote-friendly, and we handle all editing.

Interested? Apply here: https://www.firstcityfoundry.com/podcast.html

Or just reply and we'll set something up.

Best,
The Foundry Collective team

---

## Template 5: Event Invitation (Local Portland)

**Subject:** {event_name} — {event_date}

**Body:**

Hi {first_name},

The Foundry Collective is hosting {event_name} on {event_date} at {venue}.

This session focuses on {event_topic} — with real examples from Portland founders who've improved their V·M·I scores.

Agenda:
• {agenda_item_1}
• {agenda_item_2}
• Networking & peer benchmarking

RSVP: {rsvp_link}

See you there,
The Foundry Collective team

---

## Template Variables Reference

| Variable | Source | Example |
|---|---|---|
| `{first_name}` | outreach_data CSV | "Sarah" |
| `{company_name}` | outreach_data CSV | "Acme Corp" |
| `{personalization_hook}` | AI-generated from BabbleBeaver | "scaling a dev-tools product with a small team" |
| `{contact_name}` | manual / CRM | "Jordan Lee" |
| `{org_name}` | manual | "TechStars PDX" |
| `{their_domain}` | manual | "early-stage mentorship" |
| `{lifecycle_stage}` | manual | "SCALE" |
| `{specific_angle}` | AI-generated | "bootstrapping to $1M ARR without VC" |
| `{event_name}` | manual | "V·M·I Workshop #3" |
| `{event_date}` | manual | "Thursday, March 20" |
| `{venue}` | manual | "CENTRL Office, Portland" |
| `{event_topic}` | manual | "Automating founder-dependent processes" |
| `{rsvp_link}` | manual | Eventbrite / Luma URL |
