var SettingsPage = function(localsettings, indi) {
    this.localsettings = localsettings;
    this.indi = indi;
    SettingsPage.SETTING_DEVICE='setting_device';

    this.reload_devices = function() {
        $('#device').empty();
        $('#setting').empty();
        $('#setting-value').val(null);
        this.indi.get_devices(this.__on_devices_reloaded.bind(this));
    };

    this.reload_value = function() {
        var property = $('#setting').val();
        $('#setting-value').val(null);
        current_indi_device().get(property, this.__on_property_value.bind(this))
    };

    this.reload_settings = function() {
        $('#setting').empty();
        $('#setting-value').val(null);
        current_indi_device().reload(this.__on_properties_reloaded.bind(this));
    };

    this.set_value = function() {
        var value = $('#setting-value').val();
        var property = $('#setting').val();
        $('#setting-value').val(null);
        current_indi_device().set(property, value, this.reload_value.bind(this))
    };

    this.__on_property_value = function(property, device) {
        $('#setting-value').val(property['value']);
    };

    this.current_property = function() {
        return $('#setting').val();
    };



    this.__on_properties_reloaded = function(device) {
        $('#setting-value').val(null);
        device.properties.forEach( function(property) {
            var setting = property['property'] + '.' + property['element'];
            $('#setting').append($('<option />').val(setting).text(setting) );
        } );
        device.get(this.current_property(), this.__on_property_value.bind(this));
    };


    this.__on_devices_reloaded = function() {
        $('#setting').empty();
        $('#setting-value').val(null);
        this.indi.device_names().forEach( function(name) {
            $('#device').append($('<option />').val(name).text(name));
        });
        var current_device = current_indi_device(); // TODO
        $('#device').val(current_device.name);
        this.__on_properties_reloaded(current_device);
    };



    $('#refresh-devices').click(this.reload_devices.bind(this));
    $('#refresh-settings').click(this.reload_settings.bind(this));
    $('#reset-value').click(this.reload_value.bind(this));
    $('#set-value').click(this.set_value.bind(this));
    $('#device').change(function() {
        this.localsettings.set(SettingsPage.SETTING_DEVICE, current_indi_device().name);
        this.reload_settings();
    }.bind(this));
    $('#setting').change(this.reload_value.bind(this));
   
};
