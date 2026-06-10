# Events System Implementation for First City Foundry

## Overview
Created a complete events management system with data-driven architecture, reusable components, and social media sharing capabilities.

## What's Been Created

### 1. **Events Data Structure** (`docs/data/events.json`)
- JSON-based event database for easy management
- Stores complete event information: dates, times, location, speakers, sponsors, schedule
- Social media metadata (OG tags, hashtags, descriptions)
- Easy to add new events without touching code

### 2. **Events Pages**

#### Events Listing Page (`docs/pages/events.html`)
- Main events hub with filtering (All, Upcoming, Past)
- Dynamic event cards loaded from JSON
- Newsletter subscription
- Responsive grid layout
- Easy to manage and add new events

#### StartupGrind PDX Event Page (`docs/events/startup-grind-pdx-relaunch-2026.html`)
- Detailed event page with full information
- Schedule with timeline
- Featured speakers section
- Partner/sponsor showcase
- Capacity notes and attendance information
- Sticky sidebar with event details and RSVP button

### 3. **Social Sharing**
All event pages include OpenGraph and Twitter Card meta tags for:
- **LinkedIn** - Direct share button with event URL
- **Twitter/X** - Custom tweet with event details and hashtags
- **Bluesky** - Alternative social network sharing

### 4. **Components**
- **Event Card Component** (`docs/components/event-card.html`) - Reusable card for listing events
- **Updated Header** - Events link now points to the proper events page

### 5. **Homepage Integration**
- Featured event section on homepage highlighting StartupGrind PDX
- Links to full events page and event details
- Replaces previous hardcoded event card

## Current Event Details

### StartupGrind PDX Relaunch
- **Date:** Thursday, June 11, 2026
- **Time:** 5:30 PM - 8:00 PM
- **Location:** Hyatt Regency Portland, 375 NE Holladay St, Portland, OR 97232
- **Capacity:** 150 seats (300+ signups, first-come-first-served)
- **Speakers:** Greg Lind (StartupGrind), LA Walker (Kurent), Joanna Gough (PDX Hacks)
- **Sponsor:** Nodespace Incubator
- **Partners:** Buildly, PDX Hacks, First City Foundry, Kurent

## Schedule
- 5:30 PM - Doors Open & Arrival
- 5:45 PM - Welcome Session
- 6:00 PM - Fireside Chat with Amber AI
- 7:00 PM - 8:00 PM - Social Hour at Spoke & Fork

## How to Manage Events

### Adding a New Event
1. Edit `website/docs/data/events.json`
2. Add new event object with all required fields
3. Event automatically appears in listings and homepage (if featured: true)

### Creating Event Detail Pages
1. Copy `docs/events/startup-grind-pdx-relaunch-2026.html`
2. Update event details, dates, times, speakers
3. Update the `id` in JSON to match the new page filename
4. Page automatically gets social sharing cards

### Updating Social Share Info
Edit these fields in `events.json` under `socialMeta`:
- title
- description
- image (provide path to hero image)
- hashtags (array of relevant hashtags)

## Files Modified
- `/website/docs/data/events.json` - Created (event data)
- `/website/docs/pages/events.html` - Created (events listing)
- `/website/docs/events/startup-grind-pdx-relaunch-2026.html` - Created (event detail page)
- `/website/docs/components/event-card.html` - Created (reusable component)
- `/website/docs/components/header.html` - Updated (fixed Events link)
- `/website/docs/index.html` - Updated (featured event on homepage)

## To Access
- **Events Hub:** `/pages/events.html`
- **Event Detail:** `/events/startup-grind-pdx-relaunch-2026.html`
- **Homepage Feature:** Front page shows featured event card

## Next Steps (Optional)

### ForgeWeb Admin Integration
To create an admin interface for managing events:
1. Create `website/ForgeWeb/admin/templates/events-manager.html`
2. Add event form with WYSIWYG editor
3. Database integration to auto-save to JSON
4. Image upload for event heroes and speaker photos

### Advanced Features
- Event calendar view (month/week)
- RSVP form integration (Google Forms, Eventbrite API)
- Email reminders for attendees
- Event search and tagging
- Past event archives/gallery
- Attendee testimonials
