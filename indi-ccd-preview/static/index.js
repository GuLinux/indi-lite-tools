var json_request = function(url, data, options) {
    var request_options = {method: 'PUT', data: JSON.stringify(data), contentType: 'application/json' }
    if(options !== undefined) {
        $.extend(request_options, options);
    }
    $.ajax(url, request_options);
};



var indi = new INDI();
var localSettings = new LocalSettings()
var settingsPage = new SettingsPage(localSettings, indi);
var previewPage = new PreviewPage(localSettings, indi);
var histogramPage = new HistogramPage(localSettings, indi);
var miscPage = new MiscPage(localSettings, indi);

var notification = function(level, title, message, options) {
    var notification_id = 'notification-' + new Date().getTime();
    var notification = $('#notification-template').clone().prop('id', notification_id).addClass('alert-' + level).prop('style', '');
    notification.children('.notification-title').text(title);
    notification.children('.notification-text').text(message);
    if(options !== undefined) {
        if('additional_class' in options)
            notification.addClass(options['additional_class']);

        if('timeout' in options && options['timeout'] > 0) {
            window.setTimeout(function() { $('#' + notification_id).alert('close'); }, options['timeout'] * 1000);
        }
        if('on_closed' in options) {
            notification.on('closed.bs.alert', options['on_closed']);
        }
    }
    $('.notifications').append(notification);
};


var tabs = {
    '#ccd-settings': settingsPage,
    '#ccd-image': previewPage,
    '#ccd-histogram': histogramPage,
    '#misc': miscPage
};
var onTabShown = function (hash) {
    if(hash in tabs && tabs[hash].onDisplay !== undefined)
        tabs[hash].onDisplay();
};

$('a[data-toggle="tab"]').on('shown.bs.tab', function(e) { onTabShown(e.target.hash); });


var event_handlers = {
    image: function(event) {
        previewPage.setImage(event['image_url']);
        histogramPage.setImage(event['histogram']);
        histogramPage.setData(event['histogram-data'], event['histogram-bins']);
        $('.image-received-notification').remove();
        notification('success', 'image received', event['image_id'], { timeout: 5, additional_class: 'image-received-notification'});
    },
    notification: function(event) {
        notification(event['level'], event['title'], event['message']);
    }
};

var events_listener = new EventSource('/events');
events_listener.onmessage = function(e) {
    event = JSON.parse(e.data);
    event_handlers[event['type']](event);
};



var current_indi_device = function() {
    var current_devices = indi.device_names();
    if(current_devices.length == 0)
        return null;
    var devicename = localSettings.get(SettingsPage.SETTING_DEVICE, current_devices[0]);
    if(current_devices.indexOf(devicename) == 0)
        devicename = current_devices[0];
    return indi.devices[devicename];
};

var on_server_status = function(status) {
    var text = 'server is idle.';
    if(status['shooting']) {
        var elapsed = Number(status['now'] - status['started']).toFixed(1);
        var remaining = Number(status['exposure'] - elapsed).toFixed(1);
        text = 'server is currently shooting: exposure is ' + Number(status['exposure']).toFixed(1) + 's, elapsed: ' + elapsed + 's, remaining: ' + remaining + 's.';
    }
    $('.server-status-notification').remove();
    notification('info', 'Server Status', text, {timeout: 5, additional_class: 'server-status-notification'});
};

$('#server-status').click(function() { $.ajax('/status', {success: on_server_status}); });
$('.navbar-collapse a').click(function(){
    $(".navbar-collapse").collapse('hide');
});

$('form').submit(function(e){e.preventDefault()});

onTabShown('#ccd-settings');
settingsPage.reload_devices();
