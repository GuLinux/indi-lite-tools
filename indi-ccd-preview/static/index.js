var SETTING_EXPOSURE='setting_exposure';
var SETTING_DEVICE='setting_device';
var SETTING_HISTOGRAM_BINS='setting_histogram_bins';
var SETTING_HISTOGRAM_LOG='setting_histogram_log';
var SETTING_RUN_COMMAND='setting_run_command';

var get_setting = function(key, default_value) {
    var value = localStorage.getItem(key);
    return value == null ? default_value : value;
}

var set_image_url = function(basename, url) {
    $('#' + basename + '-image').attr('src', url);
    $('#' + basename + '-container').show();
};

var notification = function(level, title, message, timeout, additional_class) {
    if(additional_class === undefined)
        additional_class = '';
    var notification_id = 'notification-' + new Date().getTime();
    $('.notifications').append(
        '<div id="' + notification_id + '" class="alert alert-' + level + ' ' + additional_class + 
        ' alert-dismissible fade in"><button type="button" class="close" data-dismiss="alert"><span>×</span></button><strong>' +
        title + '</strong> ' + message + '</div>');
    if(timeout > 0) {
        window.setTimeout(function() { $('#' + notification_id).alert('close'); }, timeout * 1000);
    }
};


var event_handlers = {
    image: function(event) {
        set_image_url('ccd-preview', event['image_url']);
        set_image_url('histogram', event['histogram']);
        $('.image-received-notification').remove();
        notification('success', 'image received', event['image_id'], 5, 'image-received-notification');
    },
    notification: function(event) {
        notification(event['level'], event['title'], event['message'], -1);
    }
};

var events_listener = new EventSource('/events');
events_listener.onmessage = function(e) {
    event = JSON.parse(e.data);
    event_handlers[event['type']](event);
};

$('#ccd-preview-image').click(function() {
    $('#ccd-preview-image').toggleClass('img-responsive');
});

$('#histogram-image').click(function() {
    $('#histogram-image').toggleClass('img-responsive');
});



var current_property = function() {
    return $('#setting').val();
};


var indi = new INDI();

var current_indi_device = function() {
    var current_devices = indi.device_names();
    if(current_devices.length == 0)
        return null;
    var devicename = get_setting(SETTING_DEVICE, current_devices);
    if(current_devices.indexOf(devicename) == 0)
        devicename = current_devices[0];
    return indi.devices[devicename];
};

var on_property_value = function(property, device) {
    $('#setting-value').val(property['value']);
};

var on_properties_reloaded = function(device) {
    $('#setting-value').val(null);
    device.properties.forEach( function(property) {
        var setting = property['property'] + '.' + property['element'];
        $('#setting').append($('<option />').val(setting).text(setting) );
    } );
    device.get(current_property(), on_property_value);
};

var on_devices_reloaded = function(indi) {
    $('#setting').empty();
    $('#setting-value').val(null);
    indi.device_names().forEach( function(name) {
        $('#device').append($('<option />').val(name).text(name));
    });
    var current_device = current_indi_device();
    $('#device').val(current_device.name);
    on_properties_reloaded(current_device);
};

var reload_value = function() {
    $('#setting-value').val(null);
    current_indi_device().reload(on_properties_reloaded);
};

var reload_devices = function() {
    $('#device').empty();
    $('#setting').empty();
    $('#setting-value').val(null);
    indi.get_devices(on_devices_reloaded);
};

var reload_settings = function() {
    $('#setting').empty();
    $('#setting-value').val(null);
    reload_value();
};


var set_value = function() {
    value = $('#setting-value').val();
    property = $('#setting').val();
    $('#setting-value').val(null);
    current_indi_device().set(property, value, reload_value)
};

var preview = function() {
    localStorage.setItem(SETTING_EXPOSURE, $('#exposure').val());
    current_indi_device().preview($('#exposure').val());
};

var framing = function() {
    localStorage.setItem(SETTING_EXPOSURE, $('#exposure').val());
    current_indi_device().framing($('#exposure').val());
    $('#framing').hide();
    $('#stop-framing').show();

};

var stop_framing = function() {
    current_indi_device().stop_framing();
    $('#framing').show();
    $('#stop-framing').hide();
}


var update_histogram_settings = function() {
    var bins = parseInt($('#histogram-bins').val());
    var logarithmic = $('#histogram-logarithmic').prop('checked')
    localStorage.setItem(SETTING_HISTOGRAM_BINS, bins);
    localStorage.setItem(SETTING_HISTOGRAM_LOG, logarithmic);
    $.ajax('/histogram', {method: 'PUT', data: {bins: bins, logarithmic: logarithmic} });
};


$('#refresh-devices').click(reload_devices);
$('#refresh-settings').click(reload_settings);
$('#reset-value').click(reload_value);
$('#set-value').click(set_value);
$('#preview').click(preview);
$('#framing').click(framing);
$('#stop-framing').click(stop_framing);
$('#histogram-update-settings').click(update_histogram_settings);

$('#device').change(function() {
    localStorage.setItem(SETTING_DEVICE, current_indi_device().name);
    reload_settings();
});
$('#setting').change(reload_value);

$('.navbar-collapse a').click(function(){
    $(".navbar-collapse").collapse('hide');
});


var run_command = function() {
    var command = $('#run-command').val();
    localStorage.setItem(SETTING_RUN_COMMAND, command);
    $.ajax('/run_command', {method: 'POST', data: {command: command}});
};

$('#exposure').val(get_setting(SETTING_EXPOSURE, 1));
$('#histogram-bins').val(get_setting(SETTING_HISTOGRAM_BINS, 256));
$('#histogram-logarithmic').prop('checked', get_setting(SETTING_HISTOGRAM_LOG, 'true') == 'true');
$('#shutdown-server').click(function() { $.ajax('/shutdown', {success: function(){ notification('danger', 'Shutdown', 'Server is shutting down...'); }}); });
update_histogram_settings();
$('#run-command-btn').click(run_command);

$('#run-command').val(get_setting(SETTING_RUN_COMMAND), '');

$('#stop-framing').hide();
reload_devices();
