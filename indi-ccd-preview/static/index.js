var indi = new INDI();
var localSettings = new LocalSettings()
var settingsPage = new SettingsPage(localSettings, indi);
var previewPage = new PreviewPage(localSettings, indi);
var histogramPage = new HistogramPage(localSettings, indi);
var miscPage = new MiscPage(localSettings, indi);

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
        previewPage.setImage(event['image_url']);
        histogramPage.setImage(event['histogram']);
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



var current_indi_device = function() {
    var current_devices = indi.device_names();
    if(current_devices.length == 0)
        return null;
    var devicename = localSettings.get(SettingsPage.SETTING_DEVICE, current_devices[0]);
    if(current_devices.indexOf(devicename) == 0)
        devicename = current_devices[0];
    return indi.devices[devicename];
};

$('.navbar-collapse a').click(function(){
    $(".navbar-collapse").collapse('hide');
});


settingsPage.reload_devices();
