/* Holy Bible Words service worker: app shell + offline reading. */
const SHELL = 'hbw-shell-v10';
const PAGES = 'hbw-pages-v10';
const DATA = 'hbw-data';            // also filled by "Download for offline" on /app/
const SHELL_URLS = ['/offline/', '/assets/css/app.css?v=10', '/assets/js/app.js?v=10', '/assets/img/logo-64.png',
  '/assets/img/icon-192.png', '/data/books.json', '/data/versions.json', '/data/votd.json', '/manifest.webmanifest'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_URLS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => ![SHELL, PAGES, DATA].includes(k)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function trimPages() {
  const c = await caches.open(PAGES);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - 400; i++) await c.delete(keys[i]);
}

// Build an /api/chapter response from downloaded book files, following the
// version's fallback chain (same rules as resolve_chapter() in lib/bible.php).
async function chapterFromData(ver, book, ch) {
  const vres = await caches.match('/data/versions.json');
  if (!vres) return null;
  const vers = await vres.json();
  if (!vers[ver]) return null;
  const chain = [ver, ...(vers[ver].fallback || [])];
  const texts = {};
  for (const k of chain) {
    const hit = await caches.match(`/data/${k}/${book}.json`);
    if (hit) texts[k] = (await hit.json()).c[ch - 1] || null;
  }
  if (!texts[ver]) return null;
  const rows = [];
  for (let n = 1; n <= texts[ver].length; n++) {
    for (const k of chain) {
      const t = texts[k]?.[n - 1];
      if (t == null) continue;
      if (t === '') {
        const last = rows[rows.length - 1];
        if (last && last[2] === k && last[1] === n - 1) { last[1] = n; break; }
        continue;
      }
      rows.push([n, n, k, t]);
      break;
    }
  }
  return new Response(JSON.stringify({ ver, book, ch: +ch, verses: texts[ver], rows }), { headers: { 'Content-Type': 'application/json' } });
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  // pages: network first, cached copy when offline, else the offline shell
  if (req.mode === 'navigate' || req.headers.get('X-Requested-With') === 'hbw') {
    e.respondWith((async () => {
      try {
        const res = await fetch(req);
        if (res.ok && !url.pathname.startsWith('/search/')) {
          const copy = res.clone();
          caches.open(PAGES).then(c => c.put(url.pathname + url.search, copy)).then(trimPages);
        }
        return res;
      } catch (err) {
        return (await caches.match(url.pathname + url.search)) || (await caches.match('/offline/')) || Response.error();
      }
    })());
    return;
  }

  // chapter API: network, then downloaded data, then cache
  const m = url.pathname.match(/^\/api\/chapter\/(\w+)\/(\w+)\/(\d+)$/);
  if (m) {
    e.respondWith((async () => {
      try {
        const res = await fetch(req);
        if (res.ok) { const copy = res.clone(); caches.open(PAGES).then(c => c.put(req, copy)); }
        return res;
      } catch (err) {
        return (await caches.match(req)) || (await chapterFromData(m[1], m[2], m[3])) || Response.error();
      }
    })());
    return;
  }

  // static assets and data: cache first, refresh in the background
  if (/^\/(assets|data)\//.test(url.pathname) || url.pathname === '/manifest.webmanifest') {
    e.respondWith((async () => {
      const hit = await caches.match(req);
      const net = fetch(req).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(url.pathname.startsWith('/data/') ? DATA : SHELL).then(c => c.put(req, copy)); }
        return res;
      }).catch(() => null);
      return hit || (await net) || Response.error();
    })());
  }
});

// streak reminder (sent by lib/cron-reminders.php)
self.addEventListener('push', e => {
  let m = {};
  try { m = e.data ? e.data.json() : {}; } catch (err) { /* plain text */ }
  e.waitUntil(self.registration.showNotification(m.title || 'Verse of the Day', {
    body: m.body || 'Read today’s verse to keep your streak.',
    icon: '/assets/img/icon-192.png', badge: '/assets/img/icon-192.png',
    tag: m.tag || 'streak', data: { url: m.url || '/verse-of-the-day/' },
  }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = new URL(e.notification.data?.url || '/', location.origin).href;
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    const w = list.find(c => c.url.startsWith(location.origin));
    if (w) { w.navigate(url).catch(() => {}); return w.focus(); }
    return self.clients.openWindow(url);
  }));
});
