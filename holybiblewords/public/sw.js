/* Holy Bible Words service worker: app shell + offline reading. */
const SHELL = 'hbw-shell-v1';
const PAGES = 'hbw-pages-v1';
const DATA = 'hbw-data';            // also filled by "Download for offline" on /app/
const SHELL_URLS = ['/offline/', '/assets/css/app.css?v=1', '/assets/js/app.js?v=1', '/assets/img/logo-64.png',
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

// Build an /api/chapter response from a downloaded book file.
async function chapterFromData(ver, book, ch) {
  const hit = await caches.match(`/data/${ver}/${book}.json`);
  if (!hit) return null;
  const d = await hit.json();
  const verses = d.c[ch - 1];
  if (!verses) return null;
  let fallback = null;
  if (verses.some(v => v === null) && ver !== 'ta') {
    const k = await caches.match(`/data/ta/${book}.json`);
    if (k) fallback = (await k.json()).c[ch - 1];
  }
  return new Response(JSON.stringify({ ver, book, ch: +ch, verses, fallback }), { headers: { 'Content-Type': 'application/json' } });
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
