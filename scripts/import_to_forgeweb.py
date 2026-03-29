#!/usr/bin/env python3
"""
Import Foundry Collective site data into ForgeWeb's SQLite database.

Run from the repo root:
    python scripts/import_to_forgeweb.py

This populates the ForgeWeb admin database with pages, navigation, branding,
and site config so the ForgeWeb admin UI can manage everything.
"""

import sys
import os

# Add ForgeWeb admin to path so we can import the DB class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ForgeWeb', 'admin'))

from database import ForgeWebDB


def main():
    db = ForgeWebDB()

    # ── Site Config ────────────────────────────────────────────
    db.set_site_config('site', {
        'name': 'The Foundry Collective',
        'tagline': 'Build. Scale. Escape.',
        'url': 'https://www.firstcityfoundry.com',
        'description': 'A global network helping founders build AI-native products, scale operations, and create businesses that run without them.',
        'language': 'en',
        'author': 'The Foundry Collective',
    })
    print('  site config')

    # ── Branding (DB column-based table) ───────────────────────
    cursor = db.conn.cursor()
    cursor.execute('DELETE FROM branding')
    cursor.execute('''
        INSERT INTO branding
            (primary_color, secondary_color, accent_color, dark_color, light_color,
             font_family, logo_path, favicon_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        '#F97316',   # primary  — orange
        '#1E3A5F',   # secondary — navy
        '#10B981',   # accent   — emerald/mint
        '#0F1F35',   # dark     — navy-900
        '#F3F4F6',   # light
        'Inter',
        'assets/img/logo.png',
        'assets/img/favicon.png',
    ))
    db.conn.commit()
    print('  branding')

    # ── Design Config ──────────────────────────────────────────
    db.set_design_config(
        system_name='tailwind',
        cdn_urls=['https://cdn.tailwindcss.com?plugins=forms,typography'],
        body_classes='bg-white text-gray-900 font-sans antialiased',
    )
    print('  design config')

    # ── Pages ──────────────────────────────────────────────────
    pages = [
        ('Home',               'index',        'index.html',              '', 'published'),
        ('Register',           'register',     'register.html',           '', 'published'),
        ('Podcast Guest Form', 'podcast-form', 'podcast.html',            '', 'published'),
        ('Success',            'success',      'success.html',            '', 'published'),
        ('Opt Out',            'opt-out',      'opt-out.html',            '', 'published'),
        ('The Foundry Podcast','podcast',      'pages/podcast.html',      '', 'published'),
        ('Partners',           'partners',     'pages/partners.html',     '', 'published'),
        ('The Index',          'index-report', 'pages/index-report.html', '', 'published'),
        ('About',              'about',        'pages/about.html',        '', 'published'),
    ]
    for title, slug, path, template, status in pages:
        db.add_page(title, slug, path, template, status)
    print(f'  {len(pages)} pages')

    # ── Navigation ─────────────────────────────────────────────
    cursor.execute('DELETE FROM navigation')
    db.conn.commit()

    nav_items = [
        ('Home',           '/',                      10, False),
        ('Partners',       '/pages/partners.html',   20, False),
        ('Podcast',        '/pages/podcast.html',    30, False),
        ('The Index',      '/pages/index-report.html', 40, False),
        ('About',          '/pages/about.html',      50, False),
        ('Join the Index', '/register.html',         60, False),
    ]
    for title, url, pos, new_tab in nav_items:
        db.add_navigation_item(title, url, position=pos, open_new_tab=new_tab)
    print(f'  {len(nav_items)} navigation items')

    # ── Social Media ───────────────────────────────────────────
    cursor.execute('DELETE FROM social_media')
    socials = [
        ('linkedin', 'The Foundry Collective', 'https://linkedin.com/company/foundry-collective'),
        ('twitter',  '@foundrycollective',     'https://x.com/foundrycollective'),
        ('youtube',  'The Foundry Podcast',    'https://youtube.com/@foundrycollective'),
        ('github',   'open-build',             'https://github.com/open-build'),
    ]
    for platform, handle, url in socials:
        cursor.execute('''
            INSERT INTO social_media (platform, handle, url, enabled)
            VALUES (?, ?, ?, 1)
        ''', (platform, handle, url))
    db.conn.commit()
    print(f'  {len(socials)} social links')

    # ── Settings ───────────────────────────────────────────────
    db.set_setting('analytics', 'google_analytics_id', '')
    db.set_setting('forms', 'google_script_url',
                   'https://script.google.com/macros/s/AKfycbzaXn82jf98akTlphk00Ao0luuM9lDQF6kN2ZN73lWGdSblLsdKtBjxLSfobnlknSvG/exec')
    db.set_setting('forms', 'babble_beaver_api', 'https://api.babblebeaver.com/analyze')
    print('  settings')

    print('\nDone — ForgeWeb database populated.')
    print(f'DB path: {db.db_path}')


if __name__ == '__main__':
    main()
