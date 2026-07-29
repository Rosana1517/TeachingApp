const CACHE_VERSION = "v1";
const CACHE_NAME = `teachingapp-${CACHE_VERSION}`;

const APP_SHELL = [
  "index.html",
  "course.html",
  "settings.html",
  "manifest.json",
  "css/style.css",
  "js/app.js",
  "js/progress.js",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "courses.json",
];

async function cacheAll(cache, urls) {
  await Promise.all(
    urls.map((url) => cache.add(url).catch((err) => console.warn("SW cache miss:", url, err)))
  );
}

async function precacheLessons(cache) {
  try {
    const res = await fetch("courses.json", { cache: "no-store" });
    const courses = await res.json();
    await cacheAll(cache, courses.map((c) => c.path));
  } catch (err) {
    console.warn("SW: could not precache lessons", err);
  }
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await cacheAll(cache, APP_SHELL);
      await precacheLessons(cache);
      await self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)));
      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      try {
        const networkResponse = await fetch(request);
        cache.put(request, networkResponse.clone());
        return networkResponse;
      } catch {
        const cached = await cache.match(request, { ignoreSearch: true });
        if (cached) return cached;
        if (request.mode === "navigate") {
          const fallback = await cache.match("index.html");
          if (fallback) return fallback;
        }
        throw new Error("Offline and not cached: " + request.url);
      }
    })()
  );
});

self.addEventListener("message", (event) => {
  if (event.data?.type === "REFRESH_CACHE") {
    caches.open(CACHE_NAME).then(async (cache) => {
      await cacheAll(cache, APP_SHELL);
      await precacheLessons(cache);
    });
  }
});
