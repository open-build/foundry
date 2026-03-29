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
  loadComponent('#header-slot', prefix + 'components/header.html').then(fixNavLinks);
  loadComponent('#footer-slot', prefix + 'components/footer.html').then(fixNavLinks);

  function fixNavLinks() {
    if (depth === '0') return;
    document.querySelectorAll('#header-slot a, #footer-slot a').forEach(a => {
      const href = a.getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('/') && !href.startsWith('../')) {
        a.setAttribute('href', prefix + href);
      }
    });
  }
}

/* ── Partner Rendering ──────────────────────────────────────── */

const TYPE_COLORS = {
  core:         { bg: 'bg-orange-100', text: 'text-orange-700' },
  distribution: { bg: 'bg-blue-100',   text: 'text-blue-700' },
  strategic:    { bg: 'bg-emerald-100', text: 'text-emerald-700' },
  future:       { bg: 'bg-gray-100',   text: 'text-gray-600' }
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
      const colors = TYPE_COLORS[p.type] || TYPE_COLORS.future;
      const logo = p.logo ? (prefix + p.logo) : '';
      const card = document.createElement('div');
      card.className = 'bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-lg hover:border-orange-200 transition-all';
      card.innerHTML = `
        <div class="flex items-start gap-4">
          <img src="${logo}" alt="${p.name}" class="h-12 w-12 rounded-lg object-contain bg-gray-50 p-1"
               onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 40 40%22><rect fill=%22%23f3f4f6%22 width=%2240%22 height=%2240%22 rx=%228%22/><text x=%2220%22 y=%2226%22 text-anchor=%22middle%22 fill=%22%239ca3af%22 font-size=%2216%22>${p.name[0]}</text></svg>'">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-semibold text-gray-900">${p.name}</h3>
              <span class="text-xs font-medium px-2 py-0.5 rounded-full ${colors.bg} ${colors.text}">${p.type}</span>
            </div>
            <p class="text-sm text-orange-600 font-medium mb-2">${p.role}</p>
            <p class="text-sm text-gray-600 leading-relaxed">${p.description}</p>
            ${p.url && p.url !== '#' ? `<a href="${p.url}" target="_blank" rel="noopener" class="inline-block mt-3 text-sm text-blue-600 hover:text-blue-800 font-medium">Learn more &rarr;</a>` : ''}
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
        ? '<span class="inline-block w-2.5 h-2.5 rounded-full bg-green-500 mr-2"></span>'
        : '<span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400 mr-2"></span>';
      const tag = c.status === 'active'
        ? '<span class="text-xs font-medium text-green-700 bg-green-100 px-2 py-0.5 rounded-full">Active</span>'
        : '<span class="text-xs font-medium text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">Planned ' + c.launch + '</span>';
      const el = document.createElement('div');
      el.className = 'flex items-center justify-between bg-white rounded-lg p-4 shadow-sm border border-gray-100';
      el.innerHTML = `<div class="flex items-center">${dot}<span class="font-medium text-gray-900">${c.name}</span><span class="ml-2 text-sm text-gray-500">${c.region}</span></div>${tag}`;
      container.appendChild(el);
    });
  } catch { /* non-critical */ }
}

/* ── Init ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', initComponents);
