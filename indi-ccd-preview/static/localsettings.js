
var LocalSettings = function() {
    this.get = function(key, default_value) {
        var value = localStorage.getItem(key);
        return value == null ? default_value : value;
    };

    this.set = function(key, value) {
        localStorage.setItem(key, value);
    };

    this.getJSON = function(key, default_value) {
        return JSON.parse(this.get(key, default_value));
    };

    this.setJSON = function(key, value) {
        this.set(key, JSON.stringify(value));
    };
};
