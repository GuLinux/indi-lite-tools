
var LocalSettings = function() {
    this.get = function(key, default_value) {
        var value = localStorage.getItem(key);
        return value == null ? default_value : value;
    };

    this.set = function(key, value) {
        localStorage.setItem(key, value);
    };
};
