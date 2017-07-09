self.addEventListener('fetch', function(event) {
    console.log('fetch');
    console.log(event);
});

self.addEventListener('install', function(event) {
    clients.claim();
    console.log('install finished, claiming clients');
});
