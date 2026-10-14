// Service Worker com Cross-Origin Isolation (COOP / COEP), suporte a PWA / WebAPK e cache
const CACHE_NAME = 'gta5-web-v2';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const r = event.request;
  if (r.cache === 'only-if-cached' && r.mode !== 'same-origin') return;

  event.respondWith(
    fetch(r)
      .then((response) => {
        if (response.status === 0) return response;

        // Injeta os cabeçalhos necessários para habilitar WebAssembly multithreading e SharedArrayBuffer em qualquer host (GitHub Pages, Vercel, etc.)
        const newHeaders = new Headers(response.headers);
        newHeaders.set('Cross-Origin-Embedder-Policy', 'require-corp');
        newHeaders.set('Cross-Origin-Opener-Policy', 'same-origin');
        newHeaders.set('Cross-Origin-Resource-Policy', 'cross-origin');

        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders,
        });
      })
      .catch(() => caches.match(r))
  );
});
