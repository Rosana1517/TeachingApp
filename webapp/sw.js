const CACHE_VERSION = "v4";
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
  // cache.add() defaults to a normal fetch, which can be satisfied from the
  // browser's HTTP cache — so a precache during install could silently pin
  // stale bytes even after bumping CACHE_VERSION. Force each one to hit the
  // network.
  await Promise.all(
    urls.map((url) =>
      fetch(url, { cache: "reload" })
        .then((res) => cache.put(url, res))
        .catch((err) => console.warn("SW cache miss:", url, err))
    )
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

// Stale-while-revalidate: answer instantly from cache (this is what was
// making every page switch feel sluggish — the old strategy waited for a
// full network round trip before rendering anything, even for content
// that hadn't changed), then quietly refresh the cache in the background
// so the next load picks up whatever changed.
self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(request, { ignoreSearch: true });

      const networkFetch = fetch(request)
        .then((response) => {
          if (response.ok) cache.put(request, response.clone());
          return response;
        })
        .catch(() => null);

      if (cached) {
        event.waitUntil(networkFetch);
        return cached;
      }

      const networkResponse = await networkFetch;
      if (networkResponse) return networkResponse;

      if (request.mode === "navigate") {
        const fallback = await cache.match("index.html");
        if (fallback) return fallback;
      }
      return new Response("Offline and not cached", { status: 503 });
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
