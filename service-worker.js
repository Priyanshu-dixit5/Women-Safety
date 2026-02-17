self.addEventListener("install", e => {
  e.waitUntil(
    caches.open("safeguard-cache").then(cache => {
      return cache.addAll([
        "/",
        "/index.html",
        "/pg1.html"
      ]);
    })
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
