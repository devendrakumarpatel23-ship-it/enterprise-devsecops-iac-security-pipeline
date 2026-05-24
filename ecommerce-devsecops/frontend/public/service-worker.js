/* Service Worker for E-Commerce Platform */

const CACHE_NAME = 'ecommerce-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/',
  '/static/js/',
  '/manifest.json',
  '/favicon.svg',
  '/logo192.svg',
  '/logo512.svg'
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Cache installation failed:', error);
      })
  );
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Only cache GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip API requests - always fetch from network
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Clone the response
          const responseClone = response.clone();
          
          // Cache successful responses
          if (response.status === 200) {
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseClone);
            });
          }
          
          return response;
        })
        .catch(error => {
          console.error('Fetch failed:', error);
          // Return a custom offline page
          return caches.match('/index.html');
        })
    );
  } else {
    // Cache-first strategy for static assets
    event.respondWith(
      caches.match(request)
        .then(response => {
          if (response) {
            return response;
          }

          return fetch(request)
            .then(response => {
              // Check if valid response
              if (!response || response.status !== 200 || response.type === 'error') {
                return response;
              }

              // Clone the response
              const responseClone = response.clone();

              // Cache the new response
              caches.open(CACHE_NAME).then(cache => {
                cache.put(request, responseClone);
              });

              return response;
            })
            .catch(error => {
              console.error('Fetch error:', error);
              // Return offline page for navigation requests
              if (request.mode === 'navigate') {
                return caches.match('/index.html');
              }
            });
        })
    );
  }
});

// Handle messages from clients
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Background sync for offline purchases (optional)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-orders') {
    event.waitUntil(
      // Sync orders when connection is restored
      fetch('/api/orders/sync', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          console.log('Orders synced:', data);
        })
        .catch(error => {
          console.error('Sync failed:', error);
          throw error;
        })
    );
  }
});

// Push notifications (optional)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New notification',
    icon: '/logo192.svg',
    badge: '/favicon.svg',
    vibrate: [100, 50, 100],
    actions: [
      { action: 'open', title: 'Open' },
      { action: 'close', title: 'Close' }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('E-Commerce Platform', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then(clientList => {
        for (const client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});
