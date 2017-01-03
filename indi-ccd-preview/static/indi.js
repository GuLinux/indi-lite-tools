var INDIDevice = function(devicename, properties) {
    this.name = devicename;
    this.properties = properties;

    this.reload = function(callback, devicename) {
        var url = '/device/' + devicename === undefined ? this.currentDevice() : devicename + '/properties';
        $.ajax(url, {success: this.__got_properties.bind(this, callback)});
    }

    this.__got_properties = function(callback, data) {
        this.properties = data['properties'];
        if(callback)
            callback(this);
    }

};

var INDI = function() {

    this.get_devices = function(callback) {
        $.ajax('/devices', {success: this.__got_devices.bind(this, callback)});
    };

    this.__got_devices = function(callback, data) {
        this.devices = Object.keys(data).map(function(name){
            return new INDIDevice(name, data[name]);
        });
        if(callback)
            callback(this);
    };


};

