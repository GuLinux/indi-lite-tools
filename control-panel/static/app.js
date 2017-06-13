var send_json = function(data, url, method, on_success, on_failure) {
    jQuery.ajax(url, {
        contentType: 'application/json; charset=utf-8',
        method: method,
        dataType: 'json',
        data: JSON.stringify(data),
        success: on_success,
        error: on_failure
    });
}

var getCoordinates = function(callback) {
    navigator.geolocation.getCurrentPosition(callback);
}

var setUpdateDateTime = function(update) {
    localStorage.setItem("update_datetime", update ? "true" : "false");
}

var sendCoordinates = function(position) {
    send_json({
        "update_datetime": true,
        "timestamp": position.timestamp / 1000.,
        "coords": {
            "accuracy": position.coords.accuracy,
            "altitude": position.coords.altitude,
            "altitudeAccuracy": position.coords.altitudeAccuracy,
            "latitude": position.coords.latitude,
            "longitude": position.coords.longitude,
        }
    }, '/set_coordinates', 'PUT');
}


var newPortURL = function(port) {
     return "http://" + window.location.hostname + ":" + port;
}

var openINDIControlPanel = function() {
    window.open(newPortURL(8624),'_blank');
}

var openShellinabox = function() {
    window.open(newPortURL(4200),'_blank');
}

var shutdown = function() {
    jQuery.ajax('/shutdown', {
        method: 'POST',
        success: function() { $('#shutdown-alert').show() }
    });
}

var fetchTemp = function() {
    jQuery.ajax('/temp_humidity', {
        method: 'GET',
        success: function(e) {
            $('#temp_humidity').show();
            $('#temperature_value').text(e.temperature.toFixed(2));
            $('#humidity_value').text(e.humidity.toFixed(2));
        },
        error: function(e) {
            if(e.status == 404) {
                window.clearInterval(temp_timer);
            }
        }
    });
}

var temp_timer = window.setInterval(fetchTemp, 2000);
