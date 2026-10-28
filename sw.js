// Service worker de Simulacros UADE: deja la página y el banco de preguntas guardados para usarlos sin conexión.
const VERSION = "simulacros-v3";
const BASE = ["./", "index.html", "banco.json", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Red primero para la página y el banco (así se ven las preguntas nuevas); si no hay red, lo guardado.
async function redPrimero(req) {
  const cache = await caches.open(VERSION);
  try {
    const r = await fetch(req, { cache: "no-store" });
    if (r.ok) cache.put(req.url.includes("banco.json") ? "banco.json" : req, r.clone());
    return r;
  } catch (err) {
    return (await cache.match(req.url.includes("banco.json") ? "banco.json" : req, { ignoreSearch: true }))
        || (await cache.match("index.html"));
  }
}

// Fuentes e íconos: lo guardado primero y se actualiza en segundo plano.
async function guardadoPrimero(req) {
  const cache = await caches.open(VERSION);
  const hit = await cache.match(req);
  const red = fetch(req).then(r => { if (r.ok || r.type === "opaque") cache.put(req, r.clone()); return r; }).catch(() => hit);
  return hit || red;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (req.mode === "navigate" || url.pathname.endsWith("/banco.json") || url.pathname.endsWith("/index.html")) {
    e.respondWith(redPrimero(req));
  } else if (url.origin === location.origin || url.hostname.endsWith("fonts.googleapis.com") || url.hostname.endsWith("fonts.gstatic.com")) {
    e.respondWith(guardadoPrimero(req));
  }
});
