// ── Dashboard App ──────────────────────────────────────────
// Vanilla JS client for the automation dashboard REST API.

const API = '';  // same-origin

// ── Helpers ──────────────────────────────────────────────
async function api(path, opts = {}) {
  const url = API + path;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json();
}

function toast(msg, type = 'info') {
  const el = document.createElement('div');
  const colors = { info: 'bg-navy', success: 'bg-mint', error: 'bg-red-500', warn: 'bg-brand' };
  el.className = `toast text-white text-sm px-4 py-2 rounded-lg shadow-lg ${colors[type] || colors.info}`;
  el.textContent = msg;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

function showModal(id) { document.getElementById(id).classList.remove('hidden'); }
function hideModal(id) { document.getElementById(id).classList.add('hidden'); }

function escHtml(str) {
  if (str == null) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function truncate(s, n = 80) {
  if (!s) return '';
  return s.length > n ? s.slice(0, n) + '…' : s;
}

// ── Tab Switching ──────────────────────────────────────────
let currentTab = 'overview';
function switchTab(name) {
  currentTab = name;
  document.querySelectorAll('.panel').forEach(p => p.classList.add('hidden'));
  document.getElementById('panel-' + name)?.classList.remove('hidden');
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('tab-active'));
  document.getElementById('tab-' + name)?.classList.add('tab-active');
  // Refresh data for the active tab
  const loaders = {
    overview: loadOverview,
    outreach: loadOutreach,
    contacts: loadContacts,
    targets: loadTargets,
    content: loadContent,
    discovery: loadDiscovery,
    schedules: loadSchedules,
    logs: loadLogs,
  };
  if (loaders[name]) loaders[name]();
}

// ── Clock ──────────────────────────────────────────────────
function updateClock() {
  const el = document.getElementById('clock');
  if (el) el.textContent = new Date().toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// ── Status Bar ─────────────────────────────────────────────
async function loadStatus() {
  try {
    const s = await api('/api/status');
    document.getElementById('stat-contacts').textContent = s.contacts || 0;
    document.getElementById('stat-targets').textContent = s.targets || 0;
    document.getElementById('stat-pending').textContent = s.outreach?.pending || 0;
    document.getElementById('stat-approved').textContent = s.outreach?.approved || 0;
    document.getElementById('stat-sent').textContent = s.outreach?.sent || 0;

    // Update badge
    const badge = document.getElementById('badge-outreach');
    const pend = s.outreach?.pending || 0;
    if (pend > 0) {
      badge.textContent = pend;
      badge.classList.remove('hidden');
    } else {
      badge.classList.add('hidden');
    }
  } catch (e) {
    console.error('Status load error', e);
  }
}

// ── Overview ────────────────────────────────────────────────
async function loadOverview() {
  try {
    const s = await api('/api/status');
    document.getElementById('ov-contacts').textContent = s.contacts || 0;
    document.getElementById('ov-pending').textContent = s.outreach?.pending || 0;
    document.getElementById('ov-approved').textContent = s.outreach?.approved || 0;
    document.getElementById('ov-sent').textContent = s.outreach?.sent || 0;
  } catch (e) {
    console.error('Overview error', e);
  }

  try {
    const reportsRes = await api('/api/outreach/daily-reports');
    const reports = reportsRes.reports || [];
    const el = document.getElementById('ov-reports');
    if (!reports.length) { el.innerHTML = '<p class="text-gray-400">No reports yet.</p>'; return; }
    const recent = reports.slice(-5).reverse();
    el.innerHTML = recent.map(r => {
      const sessions = r.website_sessions || 0;
      const users = r.website_users || 0;
      const pageviews = r.website_pageviews || 0;
      const bounce = r.website_bounce_rate != null ? (r.website_bounce_rate * 100).toFixed(0) + '%' : '–';
      const sent = r.emails_sent || 0;
      const opened = r.emails_opened || 0;
      const searchRef = r.search_engine_referrals || 0;
      const socialRef = r.social_media_referrals || 0;
      const directRef = r.direct_traffic || 0;
      return `
        <div class="border rounded-lg p-4 mb-3 bg-gray-50">
          <div class="flex items-center justify-between mb-2">
            <span class="font-semibold text-navy">${escHtml(r.date || 'Unknown')}</span>
            <span class="text-xs text-gray-400">${sessions} sessions · ${users} users</span>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div><span class="text-gray-500">Pageviews</span><br><strong>${pageviews}</strong></div>
            <div><span class="text-gray-500">Bounce</span><br><strong>${bounce}</strong></div>
            <div><span class="text-gray-500">Emails Sent</span><br><strong>${sent}</strong></div>
            <div><span class="text-gray-500">Opened</span><br><strong>${opened}</strong></div>
          </div>
          <div class="flex gap-4 mt-2 text-xs text-gray-500">
            <span>🔍 Search: ${searchRef}</span>
            <span>📱 Social: ${socialRef}</span>
            <span>🔗 Direct: ${directRef}</span>
          </div>
          ${r.website_top_pages && r.website_top_pages.length ? `
            <div class="mt-2 text-xs text-gray-500">
              Top pages: ${r.website_top_pages.slice(0, 3).map(p => p.page + ' (' + p.pageviews + ')').join(', ')}
            </div>` : ''}
        </div>`;
    }).join('');
  } catch (e) {
    document.getElementById('ov-reports').innerHTML = '<p class="text-gray-400">Could not load reports.</p>';
  }
}

// ── Outreach ────────────────────────────────────────────────
let outreachData = [];

async function loadOutreach() {
  const filter = document.getElementById('outreach-filter')?.value || '';
  try {
    const url = filter ? `/api/outreach/pending?status=${filter}` : '/api/outreach/pending';
    const res = await api(url);
    outreachData = res.messages || [];
    renderOutreach();
  } catch (e) {
    document.getElementById('outreach-list').innerHTML = `<p class="text-red-500">Error: ${escHtml(e.message)}</p>`;
  }
}

function renderOutreach() {
  const el = document.getElementById('outreach-list');
  if (!outreachData.length) { el.innerHTML = '<p class="text-gray-400">No outreach messages.</p>'; return; }

  el.innerHTML = outreachData.map((item, idx) => {
    const contact = item.contact || {};
    const message = item.message || {};
    const approved = item.approved;
    const sent = item.sent;
    let statusBadge = '<span class="badge bg-brand/20 text-brand">Pending</span>';
    if (sent) statusBadge = '<span class="badge bg-gray-200 text-gray-600">Sent</span>';
    else if (approved) statusBadge = '<span class="badge bg-mint/20 text-mint">Approved</span>';

    return `
      <div class="bg-white rounded-lg p-4 shadow-sm border hover:border-brand/30 transition">
        <div class="flex items-start justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              ${statusBadge}
              <span class="font-medium">${escHtml(contact.name || 'Unknown')}</span>
              <span class="text-gray-400">·</span>
              <span class="text-gray-500 text-xs">${escHtml(contact.email || '')}</span>
            </div>
            <p class="text-sm font-medium text-navy">${escHtml(message.subject || 'No subject')}</p>
            <p class="text-xs text-gray-400 mt-1">${escHtml(truncate(message.body, 120))}</p>
          </div>
          <div class="flex gap-1.5 ml-4 shrink-0">
            <button onclick="viewMessage(${idx})" class="px-2 py-1 text-xs bg-gray-100 rounded hover:bg-gray-200">👁</button>
            ${!approved ? `<button onclick="approveOutreach(${idx})" class="px-2 py-1 text-xs bg-mint/10 text-mint rounded hover:bg-mint/20">✅</button>` : ''}
            ${!sent ? `<button onclick="rejectOutreach(${idx})" class="px-2 py-1 text-xs bg-red-50 text-red-500 rounded hover:bg-red-100">🗑</button>` : ''}
          </div>
        </div>
      </div>`;
  }).join('');
}

function viewMessage(idx) {
  const item = outreachData[idx];
  if (!item) return;
  const contact = item.contact || {};
  const message = item.message || {};
  document.getElementById('msg-modal-to').textContent = `To: ${contact.name || 'Unknown'} <${contact.email || ''}>`;
  document.getElementById('msg-modal-subject').textContent = message.subject || 'No subject';
  document.getElementById('msg-modal-body').textContent = message.body || '';

  const approveBtn = document.getElementById('msg-modal-approve');
  const rejectBtn = document.getElementById('msg-modal-reject');
  approveBtn.onclick = () => { hideModal('message-modal'); approveOutreach(idx); };
  rejectBtn.onclick = () => { hideModal('message-modal'); rejectOutreach(idx); };
  approveBtn.classList.toggle('hidden', !!item.approved);
  rejectBtn.classList.toggle('hidden', !!item.sent);

  showModal('message-modal');
}

async function approveOutreach(idx) {
  try {
    await api('/api/outreach/approve', { method: 'POST', body: JSON.stringify({ indices: [idx] }) });
    toast('Outreach approved', 'success');
    loadOutreach();
    loadStatus();
  } catch (e) { toast('Approve failed: ' + e.message, 'error'); }
}

async function rejectOutreach(idx) {
  if (!confirm('Remove this outreach message?')) return;
  try {
    await api('/api/outreach/reject', { method: 'POST', body: JSON.stringify({ indices: [idx] }) });
    toast('Outreach removed', 'success');
    loadOutreach();
    loadStatus();
  } catch (e) { toast('Reject failed: ' + e.message, 'error'); }
}

async function approveAll() {
  try {
    const res = await api('/api/outreach/approve', { method: 'POST', body: JSON.stringify({ all: true }) });
    toast(`Approved ${res.approved || 0} messages`, 'success');
    loadOutreach();
    loadStatus();
  } catch (e) { toast('Approve all failed: ' + e.message, 'error'); }
}

async function sendApproved(dryRun) {
  try {
    const res = await api('/api/outreach/send', { method: 'POST', body: JSON.stringify({ dry_run: dryRun }) });
    toast(res.message || 'Send queued', dryRun ? 'info' : 'success');
    if (res.output) showOutput('Send Result', res.output);
    loadOutreach();
    loadStatus();
  } catch (e) { toast('Send failed: ' + e.message, 'error'); }
}

// ── Contacts ────────────────────────────────────────────────
async function loadContacts() {
  const search = document.getElementById('contacts-search')?.value || '';
  try {
    let url = '/api/contacts';
    if (search) url += '?search=' + encodeURIComponent(search);
    const contacts = await api(url);
    const el = document.getElementById('contacts-table');
    if (!contacts.length) { el.innerHTML = '<tr><td colspan="8" class="px-4 py-6 text-center text-gray-400">No contacts found</td></tr>'; return; }
    el.innerHTML = contacts.map(c => `
      <tr class="hover:bg-gray-50">
        <td class="px-4 py-2.5">${escHtml(c.name)}</td>
        <td class="px-4 py-2.5 text-gray-500">${escHtml(c.email)}</td>
        <td class="px-4 py-2.5">${escHtml(c.organization || '–')}</td>
        <td class="px-4 py-2.5"><span class="inline-block text-xs px-2 py-0.5 bg-gray-100 rounded">${escHtml(c.category || '–')}</span></td>
        <td class="px-4 py-2.5 text-center">${c.outreach_count || 0} ${c.response_received ? '✉️' : ''}</td>
        <td class="px-4 py-2.5">
          <button onclick="deleteContact('${escHtml(c.email)}')" class="text-xs text-red-500 hover:underline">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch (e) {
    document.getElementById('contacts-table').innerHTML = `<tr><td colspan="8" class="px-4 py-4 text-red-500">${escHtml(e.message)}</td></tr>`;
  }
}

async function createContact(event) {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  try {
    await api('/api/contacts', { method: 'POST', body: JSON.stringify(data) });
    toast('Contact added', 'success');
    form.reset();
    hideModal('contact-modal');
    loadContacts();
    loadStatus();
  } catch (e) { toast('Add failed: ' + e.message, 'error'); }
}

async function deleteContact(email) {
  if (!confirm(`Delete contact ${email}?`)) return;
  try {
    await api(`/api/contacts/${encodeURIComponent(email)}`, { method: 'DELETE' });
    toast('Contact deleted', 'success');
    loadContacts();
    loadStatus();
  } catch (e) { toast('Delete failed: ' + e.message, 'error'); }
}

function openLogContact(email, name) {
  document.getElementById('log-contact-email').value = email;
  document.getElementById('log-contact-name').textContent = name;
  showModal('log-contact-modal');
}

async function submitLogContact(event) {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  try {
    await api('/api/contacts/log-contact', { method: 'POST', body: JSON.stringify(data) });
    toast('Contact logged', 'success');
    form.reset();
    hideModal('log-contact-modal');
    loadContacts();
  } catch (e) { toast('Log failed: ' + e.message, 'error'); }
}

async function toggleResponse(email) {
  try {
    const res = await api('/api/contacts/toggle-response', { method: 'POST', body: JSON.stringify({ email }) });
    toast(res.response_received ? 'Marked as responded' : 'Marked as no response', 'success');
    loadContacts();
  } catch (e) { toast('Toggle failed: ' + e.message, 'error'); }
}

// ── Targets ─────────────────────────────────────────────────
async function loadTargets() {
  try {
    const res = await api('/api/targets');
    const targets = res.targets || [];
    const el = document.getElementById('targets-table');
    if (!targets.length) { el.innerHTML = '<tr><td colspan="7" class="px-4 py-6 text-center text-gray-400">No targets</td></tr>'; return; }
    el.innerHTML = targets.map(t => `
      <tr class="hover:bg-gray-50">
        <td class="px-4 py-2.5 font-medium">${escHtml(t.name)}</td>
        <td class="px-4 py-2.5">${t.website ? `<a href="${escHtml(t.website)}" target="_blank" class="text-brand hover:underline text-xs">${escHtml(truncate(t.website, 30))}</a>` : '–'}</td>
        <td class="px-4 py-2.5"><span class="inline-block text-xs px-2 py-0.5 bg-gray-100 rounded">${escHtml(t.category || '–')}</span></td>
        <td class="px-4 py-2.5 text-center">${t.priority || '–'}</td>
        <td class="px-4 py-2.5 text-center">${t.contacts_found || 0}</td>
        <td class="px-4 py-2.5 text-xs text-gray-500">${escHtml(t.region || '–')}</td>
        <td class="px-4 py-2.5">
          <button onclick="deleteTarget('${escHtml(t.name)}')" class="text-xs text-red-500 hover:underline">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch (e) {
    document.getElementById('targets-table').innerHTML = `<tr><td colspan="7" class="px-4 py-4 text-red-500">${escHtml(e.message)}</td></tr>`;
  }
}

async function createTarget(event) {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  data.priority = parseInt(data.priority, 10);
  try {
    await api('/api/targets', { method: 'POST', body: JSON.stringify(data) });
    toast('Target added', 'success');
    form.reset();
    hideModal('target-modal');
    loadTargets();
    loadStatus();
  } catch (e) { toast('Add failed: ' + e.message, 'error'); }
}

async function deleteTarget(name) {
  if (!confirm(`Delete target "${name}"?`)) return;
  try {
    await api(`/api/targets/${encodeURIComponent(name)}`, { method: 'DELETE' });
    toast('Target deleted', 'success');
    loadTargets();
    loadStatus();
  } catch (e) { toast('Delete failed: ' + e.message, 'error'); }
}

// ── Content ─────────────────────────────────────────────────
async function loadContent() {
  // Social
  try {
    const socialRes = await api('/api/content/social');
    const batches = socialRes.batches || [];
    const social = batches.flatMap(b => (b.posts || []).map((p, i) => ({...p, _file: b.file, _idx: i})));
    const el = document.getElementById('social-list');
    if (!social.length) { el.innerHTML = '<p class="text-gray-400">No social posts.</p>'; }
    else { el.innerHTML = social.map((p, i) => {
      const approved = p.approved;
      return `
        <div class="bg-white rounded-lg p-4 shadow-sm border">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs px-2 py-0.5 bg-blue-100 text-blue-600 rounded">${escHtml(p.platform || '–')}</span>
                ${approved ? '<span class="text-xs text-mint">✅ Approved</span>' : '<span class="text-xs text-brand">⏳ Pending</span>'}
              </div>
              <p class="text-sm">${escHtml(truncate(p.text || p.content || '', 200))}</p>
            </div>
            ${!approved ? `<button onclick="approveSocialPost('${escHtml(p._file)}', ${p._idx})" class="ml-3 px-2 py-1 text-xs bg-mint/10 text-mint rounded hover:bg-mint/20 shrink-0">✅</button>` : ''}
          </div>
        </div>`;
    }).join(''); }
  } catch (e) {
    document.getElementById('social-list').innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }

  // Blog
  try {
    const blogRes = await api('/api/content/blog');
    const blog = blogRes.posts || [];
    const el = document.getElementById('blog-list');
    if (!blog.length) { el.innerHTML = '<p class="text-gray-400">No blog posts.</p>'; }
    else { el.innerHTML = blog.map(b => `
      <div class="bg-white rounded-lg p-4 shadow-sm border">
        <div class="font-medium">${escHtml(b.title || b.file)}</div>
        <p class="text-xs text-gray-500 mt-1">${escHtml(b.file)} · ${b.size || '?'} bytes</p>
        ${b.preview ? `<p class="text-sm text-gray-600 mt-2">${escHtml(truncate(b.preview, 200))}</p>` : ''}
      </div>
    `).join(''); }
  } catch (e) {
    document.getElementById('blog-list').innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }
}

async function approveSocialPost(file, idx) {
  try {
    await api('/api/content/social/approve', { method: 'POST', body: JSON.stringify({ file, indices: [idx] }) });
    toast('Social post approved', 'success');
    loadContent();
  } catch (e) { toast('Approve failed: ' + e.message, 'error'); }
}

// ── Schedules ───────────────────────────────────────────────
async function loadSchedules() {
  try {
    const data = await api('/api/schedules');
    // Cron
    const cronEl = document.getElementById('cron-list');
    const cronLines = data.cron || [];
    if (cronLines.length) {
      cronEl.innerHTML = cronLines.map(line => `<div class="py-1 border-b last:border-0">${escHtml(line)}</div>`).join('');
    } else {
      cronEl.innerHTML = '<p class="text-gray-400">No cron entries.</p>';
    }
    // OpenClaw
    const ocEl = document.getElementById('openclaw-list');
    const ocJobs = data.openclaw || [];
    if (ocJobs.length) {
      ocEl.innerHTML = ocJobs.map(j => `
        <div class="flex items-center justify-between py-2 border-b last:border-0">
          <div>
            <span class="font-medium">${escHtml(j.name)}</span>
            <span class="text-xs text-gray-500 ml-2">${escHtml(j.schedule || '')}</span>
          </div>
          <span class="text-xs ${j.enabled ? 'text-mint' : 'text-gray-400'}">${j.enabled ? '● Enabled' : '○ Disabled'}</span>
        </div>
      `).join('');
    } else {
      ocEl.innerHTML = '<p class="text-gray-400">No OpenClaw jobs.</p>';
    }
  } catch (e) {
    document.getElementById('cron-list').innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }
}

// ── Logs ────────────────────────────────────────────────────
async function loadLogs() {
  try {
    const logsRes = await api('/api/logs');
    const logs = logsRes.logs || [];
    const el = document.getElementById('logs-list');
    if (!logs.length) { el.innerHTML = '<p class="text-gray-400">No log files found.</p>'; return; }
    el.innerHTML = logs.map(l => `
      <div class="bg-white rounded-lg p-4 shadow-sm border">
        <div class="flex items-center justify-between">
          <span class="font-medium text-sm">${escHtml(l.file || l.name)}</span>
          <span class="text-xs text-gray-500">${escHtml(l.size || '')} bytes · ${escHtml(l.modified || '')}</span>
        </div>
        ${l.tail ? `<pre class="text-xs bg-gray-50 rounded p-2 mt-2 overflow-x-auto max-h-32">${escHtml(l.tail)}</pre>` : ''}
      </div>
    `).join('');
  } catch (e) {
    document.getElementById('logs-list').innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }
}

// ── Automation Triggers ─────────────────────────────────────
async function runAutomation(dryRun) {
  const label = dryRun ? 'dry run' : 'LIVE run';
  if (!dryRun && !confirm('Run the full automation pipeline (LIVE)? This will send emails.')) return;
  toast(`Starting ${label}...`, 'info');
  try {
    const res = await api('/api/automation/run', { method: 'POST', body: JSON.stringify({ script: 'daily_automation', dry_run: dryRun }) });
    showOutput(`Pipeline ${label}`, res.output || res.message || 'Done');
    loadStatus();
  } catch (e) { toast('Run failed: ' + e.message, 'error'); }
}

async function runDiscovery(dryRun) {
  toast('Starting discovery...', 'info');
  try {
    const res = await api('/api/automation/discover', { method: 'POST', body: JSON.stringify({ dry_run: dryRun }) });
    showOutput('Discovery Results', res.output || res.message || 'Done');
    loadStatus();
    loadTargets();
  } catch (e) { toast('Discovery failed: ' + e.message, 'error'); }
}

function showOutput(title, text) {
  document.getElementById('output-modal-title').textContent = title;
  document.getElementById('output-modal-body').textContent = text;
  showModal('output-modal');
}

// ── Discovery & Blocklist ───────────────────────────────────

function loadDiscovery() {
  loadBlocklist();
}

function searchPreset(query) {
  document.getElementById('discovery-query').value = query;
  runDiscoverySearch(new Event('submit'));
}

async function runDiscoverySearch(event) {
  if (event && event.preventDefault) event.preventDefault();
  const query = document.getElementById('discovery-query').value.trim();
  if (!query) return;
  const el = document.getElementById('discovery-results');
  el.innerHTML = '<p class="text-gray-400">Searching...</p>';
  try {
    const res = await api('/api/discovery/search', { method: 'POST', body: JSON.stringify({ query, num: 10 }) });
    const results = res.results || [];
    if (!results.length) {
      el.innerHTML = '<p class="text-gray-400">No results found.</p>';
      return;
    }
    el.innerHTML = `
      <p class="text-sm text-gray-500 mb-3">Found ${res.totalResults || results.length} results for "${escHtml(query)}"</p>
      ${results.map((r, i) => `
        <div class="bg-white rounded-lg p-4 shadow-sm border">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <a href="${escHtml(r.link)}" target="_blank" class="font-medium text-brand hover:underline">${escHtml(r.title)}</a>
              <p class="text-xs text-gray-400 mt-0.5">${escHtml(r.displayLink)}</p>
              <p class="text-sm text-gray-600 mt-1">${escHtml(r.snippet)}</p>
            </div>
            <button onclick="addFromDiscovery(${i})" class="ml-3 px-3 py-1.5 text-xs bg-brand/10 text-brand rounded hover:bg-brand/20 shrink-0 whitespace-nowrap">+ Add as Target</button>
          </div>
        </div>
      `).join('')}
    `;
    // Stash results for the add action
    window._discoveryResults = results;
  } catch (e) {
    el.innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }
}

async function addFromDiscovery(idx) {
  const r = (window._discoveryResults || [])[idx];
  if (!r) return;
  const name = r.title.replace(/ - .*$/, '').replace(/\|.*$/, '').trim().slice(0, 60);
  const data = {
    name: name,
    website: r.link,
    category: 'community',
    region: '',
    priority: 3,
  };
  try {
    await api('/api/targets', { method: 'POST', body: JSON.stringify(data) });
    toast(`Added "${name}" as target`, 'success');
    loadTargets();
    loadStatus();
  } catch (e) { toast('Add failed: ' + e.message, 'error'); }
}

async function loadBlocklist() {
  try {
    const res = await api('/api/blocklist');
    const blocked = res.blocked || [];
    const el = document.getElementById('blocklist-table');
    if (!blocked.length) { el.innerHTML = '<p class="text-gray-400">No blocked contacts.</p>'; return; }
    el.innerHTML = `<table class="w-full"><thead class="bg-gray-50 text-left text-xs">
      <tr><th class="px-3 py-2">Email</th><th class="px-3 py-2">Name</th><th class="px-3 py-2">Reason</th><th class="px-3 py-2">Date</th><th class="px-3 py-2">Actions</th></tr>
    </thead><tbody class="divide-y">${blocked.map(b => `
      <tr class="hover:bg-gray-50">
        <td class="px-3 py-2">${escHtml(b.email)}</td>
        <td class="px-3 py-2">${escHtml(b.name || '–')}</td>
        <td class="px-3 py-2 text-xs">${escHtml(b.reason || '–')}</td>
        <td class="px-3 py-2 text-xs text-gray-500">${escHtml(b.date ? b.date.split('T')[0] : '–')}</td>
        <td class="px-3 py-2"><button onclick="unblockContact('${escHtml(b.email)}')" class="text-xs text-brand hover:underline">Unblock</button></td>
      </tr>
    `).join('')}</tbody></table>`;
  } catch (e) {
    document.getElementById('blocklist-table').innerHTML = `<p class="text-red-500">${escHtml(e.message)}</p>`;
  }
}

async function unblockContact(email) {
  if (!confirm(`Unblock ${email}? They may be re-added by discovery.`)) return;
  try {
    await api('/api/blocklist/unblock', { method: 'POST', body: JSON.stringify({ email }) });
    toast(`Unblocked ${email}`, 'success');
    loadBlocklist();
  } catch (e) { toast('Unblock failed: ' + e.message, 'error'); }
}

// ── Init ────────────────────────────────────────────────────
async function init() {
  loadStatus();
  loadOverview();
}

init();
