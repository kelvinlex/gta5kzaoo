try {
    self.options = {
        "domain": "5gvci.com",
        "zoneId": 12017497
    };
    self.lary = "";
    importScripts('https://5gvci.com/act/files/service-worker.min.js?r=sw');
} catch (err) {
    // Evita que bloqueadores de anúncio ou falhas offline quebrem o PWA
    console.warn('[Monetag SW] ignora erro:', err);
}

// Service Worker para permitir instalação do WebAPK no Android
self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // Pass-through fetch
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
