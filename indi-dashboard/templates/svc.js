self.addEventListener('fetch', function(event) {
    console.log('fetch');
    console.log(event);
});

self.addEventListener('install', function(event) {
    console.log('install');
    console.log(event);
});
