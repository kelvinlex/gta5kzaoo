// Service Worker para permitir instalação do WebAPK / PWA e funcionamento offline/cache
const CACHE_NAME = 'gta5-web-v1';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // Pass-through fetch com fallback para cache caso disponível
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
