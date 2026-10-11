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
