var INDIDevice = function(devicename, properties) {
    this.name = devicename;
    this.properties = properties;

    this.reload = function(callback, devicename) {
        $.ajax(this.__url(['properties']), {success: this.__got_properties.bind(this, callback)});
    }

    this.get = function(property, callback) {
        $.ajax(this.__url(['properties', property]), {success: callback});
    };

    this.set = function(property, value, callback) {
       $.ajax(this.__url(['properties', property]), {method: 'PUT', data: {value: value}, success: callback}); 
    };

    this.__got_properties = function(callback, data) {
        this.properties = data['properties'];
        if(callback)
            callback(this);
    }

    this.__url = function(suburl) {
        if( suburl === undefined)
            suburl = [];
        return ['/device', this.name].concat(suburl).join('/');
    };
};

var INDI = function() {

    this.devices = {};

    this.get_devices = function(callback) {
        $.ajax('/devices', {success: this.__got_devices.bind(this, callback)});
    };


    this.__got_devices = function(callback, data) {
        this.devices = {};
        Object.keys(data).forEach(function(name){
            this.devices[name] = new INDIDevice(name, data[name]);
        }, this);
        if(callback)
            callback(this);
    };


};

