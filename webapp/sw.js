const CACHE_VERSION = "v7";
const CACHE_NAME = `teachingapp-${CACHE_VERSION}`;

const APP_SHELL = [
  "index.html",
  "course.html",
  "settings.html",
  "manifest.json",
  "css/style.css",
  "js/app.js",
  "js/progress.js",
  "js/push.js",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "courses.json",
];

async function cacheAll(cache, urls) {
  await Promise.all(
    urls.map((url) =>
      fetch(url, { cache: "reload" })
        .then((res) => {
          // iOS Safari throws "has redirections" if a redirected response is
          // stored in the cache and then served by the SW. Only cache clean,
          // non-redirected 200 responses.
          if (res.ok && !res.redirected) return cache.put(url, res);
        })
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
          if (response.ok && !response.redirected) cache.put(request, response.clone());
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

self.addEventListener("push", (event) => {
  let payload = { title: "TeachingApp 學習提醒", body: "今天還有課程沒學完，點開看看吧！" };
  try {
    if (event.data) payload = { ...payload, ...event.data.json() };
  } catch {
    // ignore malformed payloads, fall back to the default text above
  }
  event.waitUntil(
    self.registration.showNotification(payload.title, {
      body: payload.body,
      icon: "icons/icon-192.png",
      badge: "icons/icon-192.png",
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(
    (async () => {
      const clientsList = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
      const existing = clientsList.find((c) => c.url.includes(self.registration.scope));
      if (existing) {
        existing.focus();
      } else {
        self.clients.openWindow("index.html");
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
