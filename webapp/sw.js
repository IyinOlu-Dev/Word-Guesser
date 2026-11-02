const CACHE = "word-guesser-v";
const SHELL = [
    "./", "./index.html", "./styles.css", "./app.js",
    "./manifest.webmanifest", "./icon-192.png", "./icon-512.png"
];

self.addEventListener("install", (e) => {
    e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)));
    self.skipWaiting();
});

self.addEventListener("activate", (e) => {
    e.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (e) => {
    const req = e.request;
    if (req.method !== "GET") return;
    const url = new URL(req.url);
    if (url.origin !== location.origin) return; // let Google Fonts etc. go to the network

    // Word list: try the network for updates, fall back to the cached copy offline
    if (url.pathname.endsWith("/words.txt")) {
        e.respondWith(
            fetch(req)
                .then((res) => {
                    const copy = res.clone();
                    caches.open(CACHE).then((c) => c.put(req, copy));
                    return res;
                })
                .catch(() => caches.match(req))
        );
        return;
    }

    // App shell: serve from cache, refresh in the background
    e.respondWith(
        caches.match(req).then((cached) => {
            const fresh = fetch(req).then((res) => {
                if (res.ok) caches.open(CACHE).then((c) => c.put(req, res.clone()));
                return res;
            }).catch(() => cached);
            return cached || fresh;
        })
    );
});