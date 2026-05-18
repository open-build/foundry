/**
 * Foundry Collective — Site Utilities
 * Handles component includes, partner rendering, and city map.
 * No frameworks, no NPM — vanilla JS only.
 */

/* ── Component Loader ───────────────────────────────────────── */

async function loadComponent(selector, url) {
  const el = document.querySelector(selector);
  if (!el) return;
  try {
    const res = await fetch(url);
    if (!res.ok) return;
    el.innerHTML = await res.text();
  } catch { /* component optional */ }
}

function initComponents() {
  const depth = (document.querySelector('meta[name="path-depth"]') || {}).content || '0';
  const prefix = depth === '1' ? '../' : '';
  Promise.all([
    loadComponent('#header-slot', prefix + 'components/header.html'),
    loadComponent('#footer-slot', prefix + 'components/footer.html')
  ]).then(() => {
    fixNavLinks();
    initThemeControls();
  });

  function fixNavLinks() {
    if (depth === '0') return;
    document.querySelectorAll('#header-slot a, #footer-slot a').forEach(a => {
      const href = a.getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('/') && !href.startsWith('../')) {
        a.setAttribute('href', prefix + href);
      }
    });
    document.querySelectorAll('#header-slot img, #footer-slot img').forEach(img => {
      const src = img.getAttribute('src');
      if (src && !src.startsWith('http') && !src.startsWith('/') && !src.startsWith('../')) {
        img.setAttribute('src', prefix + src);
        img.style.display = '';
      }
    });
  }
}

function initThemeControls() {
  const savedTheme = localStorage.getItem('foundry-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  function syncButtons(theme) {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      btn.setAttribute('title', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    });
  }

  syncButtons(savedTheme);
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', () => {
      const nextTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('foundry-theme', nextTheme);
      syncButtons(nextTheme);
    });
  });
}

/* ── Partner Rendering ──────────────────────────────────────── */

const TYPE_COLORS = {
  core: 'Core',
  distribution: 'Distribution',
  strategic: 'Strategic',
  future: 'Future'
};

async function loadPartners(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const depth = (document.querySelector('meta[name="path-depth"]') || {}).content || '0';
  const prefix = depth === '1' ? '../' : '';
  try {
    const res = await fetch(prefix + 'data/partners.json');
    const partners = await res.json();
    container.innerHTML = '';
    partners.forEach(p => {
      const label = TYPE_COLORS[p.type] || TYPE_COLORS.future;
      const logo = p.logo ? (prefix + p.logo) : '';
      const card = document.createElement('div');
      card.className = 'foundry-page-card p-6 transition-all';
      card.innerHTML = `
        <div class="flex items-start gap-5">
          <img src="${logo}" alt="${p.name}" class="h-14 w-14 rounded-foundry object-contain bg-white p-2 ring-1 ring-ink/10"
               onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 56 56%22><rect fill=%22%23FFF1F3%22 width=%2256%22 height=%2256%22 rx=%228%22/><text x=%2228%22 y=%2236%22 text-anchor=%22middle%22 fill=%22%23FF5A6B%22 font-size=%2220%22 font-family=%22Arial%22>${p.name[0]}</text></svg>'">
          <div class="flex-1">
            <div class="flex flex-wrap items-center gap-2 mb-2">
              <h3 class="font-display text-xl font-bold text-ink">${p.name}</h3>
              <span class="foundry-page-badge !px-2 !py-0.5 !text-[0.65rem]">${label}</span>
            </div>
            <p class="text-sm text-coral-500 font-bold mb-2">${p.role}</p>
            <p class="text-sm text-slatebrand leading-relaxed">${p.description}</p>
            ${p.url && p.url !== '#' ? `<a href="${p.url}" target="_blank" rel="noopener" class="foundry-page-link inline-block mt-3 text-sm">Learn more &rarr;</a>` : ''}
          </div>
        </div>`;
      container.appendChild(card);
    });
  } catch { container.innerHTML = '<p class="text-gray-500">Unable to load partners.</p>'; }
}

/* ── City Map ───────────────────────────────────────────────── */

async function loadCities(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const depth = (document.querySelector('meta[name="path-depth"]') || {}).content || '0';
  const prefix = depth === '1' ? '../' : '';
  try {
    const res = await fetch(prefix + 'data/cities.json');
    const cities = await res.json();
    container.innerHTML = '';
    cities.forEach(c => {
      const dot = c.status === 'active'
        ? '<span class="inline-block w-2.5 h-2.5 rounded-full bg-coral-500 mr-2"></span>'
        : '<span class="inline-block w-2.5 h-2.5 rounded-full bg-slatebrand mr-2"></span>';
      const tag = c.status === 'active'
        ? '<span class="foundry-page-badge !px-2 !py-0.5 !text-[0.65rem]">Active</span>'
        : '<span class="foundry-page-badge !px-2 !py-0.5 !text-[0.65rem]">Planned ' + c.launch + '</span>';
      const el = document.createElement('div');
      el.className = 'foundry-page-card flex items-center justify-between p-4';
      el.innerHTML = `<div class="flex items-center">${dot}<span class="font-display font-bold text-ink">${c.name}</span><span class="ml-2 text-sm text-slatebrand">${c.region}</span></div>${tag}`;
      container.appendChild(el);
    });
  } catch { /* non-critical */ }
}

/* ── Init ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', initComponents);
