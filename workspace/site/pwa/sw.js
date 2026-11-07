/* Offline copy of the site. tools/site_build.py writes this file beside the page as sw.js, with BUILD set from the
   page's ax-build stamp, so each build is a new worker with its own cache. Install saves the page, its search index,
   the manifest and the icons; the page asks the waiting worker to take over (message "activate") when the reader
   chooses Refresh. Requests the page sends to version.json and api/ always go to the network. */
var PREFIX = 'step2haki-';
var CACHE = PREFIX + BUILD;
var PAGE = new URL('./', self.registration.scope).href;
var ASSETS = ['manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png'];

function abs(p) { return new URL(p, self.registration.scope).href; }

function stampOf(html) {
  var m = /<meta name="ax-build" content="([^"|]*)/.exec(html);
  return m ? m[1] : '';
}

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    var page = fetch(PAGE, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('page HTTP ' + r.status);
      var type = r.headers.get('content-type') || 'text/html; charset=utf-8';
      return r.text().then(function (html) {
        if (stampOf(html) !== BUILD) throw new Error('page build ' + stampOf(html) + ' is not ' + BUILD);
        return c.put(PAGE, new Response(html, { headers: { 'content-type': type } }));
      });
    });
    var index = fetch(abs('search.json?v=' + encodeURIComponent(BUILD))).then(function (r) {
      if (!r.ok) throw new Error('search.json HTTP ' + r.status);
      return c.put(abs('search.json'), r);
    });
    return Promise.all([page, index, c.addAll(ASSETS.map(function (p) { return new Request(abs(p), { cache: 'no-cache' }); }))]);
  }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf(PREFIX) === 0 && k !== CACHE; })
      .map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('message', function (e) {
  if (e.data && e.data.type === 'activate') self.skipWaiting();
  if (e.data && e.data.type === 'build' && e.ports && e.ports[0]) e.ports[0].postMessage({ build: BUILD });
});

function fromCache(key) {
  return caches.open(CACHE).then(function (c) { return c.match(key); });
}

function cacheFirst(req, key) {
  return fromCache(key).then(function (hit) { return hit || fetch(req); });
}

function networkFirst(req, key) {
  return fetch(req).catch(function () { return fromCache(key).then(function (hit) { if (hit) return hit; throw new Error('offline'); }); });
}

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url), scope = new URL(self.registration.scope);
  if (url.origin !== scope.origin || url.pathname.indexOf(scope.pathname) !== 0) return;
  var rel = url.pathname.slice(scope.pathname.length);
  if (rel === 'version.json' || rel === 'sw.js' || rel.indexOf('api/') === 0) return;
  if (req.mode === 'navigate') {
    if (rel !== '' && rel !== 'index.html') return;
    var asked = url.searchParams.get('v');
    e.respondWith(asked && asked !== BUILD ? networkFirst(req, PAGE) : cacheFirst(req, PAGE));
    return;
  }
  if (rel === 'search.json') {
    var v = url.searchParams.get('v');
    e.respondWith(v && v !== BUILD ? networkFirst(req, abs('search.json')) : cacheFirst(req, abs('search.json')));
    return;
  }
  if (ASSETS.indexOf(rel) >= 0) e.respondWith(cacheFirst(req, abs(rel)));
});
