$('#stop-framing').hide();
var events_listener = new EventSource('/events');
events_listener.onmessage = function(e) {
    event = JSON.parse(e.data);
    if(event['type'] == 'image') {
        $('#ccd-preview').attr('src', event['url']);
        $('.image-container').show();
    }
    if(event['type'] == 'histogram') {
        $('#histogram-image').attr('src', event['url']);
        $('.histogram-container').show();
    }
    if(event['type'] == 'notification') {
        $('.notifications').append(
            '<div class="alert alert-' + event['level'] +
            ' alert-dismissible fade in"><button type="button" class="close" data-dismiss="alert"><span>×</span></button><strong>' +
            event['title'] + '</strong> ' + event['message'] + '</div>');
    }
};


var current_device = function() {
    return $('#device').val();
};

var current_property = function() {
    return $('#setting').val();
};


var select_callback = function(dom_element, transform, data) {
    data.map(transform).forEach(function(element) {
        dom_element.append($('<option />').val(element.value).text(element.text));
    });
};

var refresh_select = function(select_name, url, transform) {
    refresh_element(select_name, url, select_callback.bind(this, select_name, transform));
};

var refresh_element = function(name, url, on_success) {
    $('#' + name).empty();
    $.ajax(url, {success: on_success.bind(this, $('#' + name)) });
};

var refresh_devices = function() {
    $('#setting').empty();
    $('#setting-value').val(null);
    refresh_element('device', '/devices', function(select, data) {
        select_callback(select, function(x) {return {text: x, value: x}; }, data['devices']);
        refresh_settings();
    });
};

var get_properties_url = function() {
    return ['/device', current_device(), 'properties'].join('/');
};

var get_setting_url = function() {
    return ['/device', current_device(), 'properties', current_property()].join('/')
};

var refresh_settings = function() {
    $('#setting-value').val(null);
    refresh_element('setting', get_properties_url(), function(select, data) {
        select_callback(select, function(x) {
            property_element = [x['property'], x['element']].join('.');
            return { text: property_element, value: property_element };
        }, data['properties']);
        refresh_value();
    });
};


var refresh_value = function() {
    refresh_element('setting-value', get_setting_url(), function(txt, d) {
        $('#setting-value').val(d['value']);
    });
};

var set_value = function() {
    value = $('#setting-value').val();
    $('#setting-value').val(null);
    $.ajax(get_setting_url(), {method: 'PUT', data: {value: value}, success: refresh_settings});
};

var preview = function() {
    $.ajax('/device/' + current_device() + '/preview/' + $('#exposure').val());
};

var framing = function() {
    $.ajax('/device/' + current_device() + '/framing/' + $('#exposure').val());
    $('#framing').hide();
    $('#stop-framing').show();
};

var stop_framing = function() {
    $.ajax('/device/' + current_device() + '/framing/stop');
    $('#framing').show();
    $('#stop-framing').hide();
}


var nav = function(name) {
    $('.navlink').removeClass('active');
    $('#nav-' + name).addClass('active');
};

//$('#nav-ccd-settings a').click(nav.bind(this, 'ccd-settings'));
//$('#nav-ccd-image a').click(nav.bind(this, 'ccd-image'));

$('#refresh-devices').click(refresh_devices);
$('#refresh-settings').click(refresh_settings);
$('#reset-value').click(refresh_value);
$('#set-value').click(set_value);
$('#preview').click(preview);
$('#framing').click(framing);
$('#stop-framing').click(stop_framing);

$('#device').change(refresh_settings);
$('#setting').change(refresh_value);

$('#ccd-preview').click(function() {
    $('#ccd-preview').toggleClass('img-responsive');
});
$('#histogram-image').click(function() {
    $('#histogram-image').toggleClass('img-responsive');
});


refresh_devices();
