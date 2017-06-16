from flask import Flask, render_template, jsonify, request
import json
import os
import argparse
import time
import threading

app = Flask(__name__)
app_config = {}
events = []
cached_objects = {}
temp_humidity_saver = { 'saving': False }

try:
    import config
    config.setup(app_config)
except:
    pass

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/coordinates", methods=["PUT"])
def set_coordinates():
    data = request.get_json()
    if not data:
        return '', 400
    if data['update_datetime']:
        update_datetime(data['timestamp'])
    cached_objects['gps'] = data['coords']
    update_gps(data['coords'])
    return '', 200

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    if 'gps' not in cached_objects:
        return 'No coordinates set', 404
    return jsonify(cached_objects['gps'])

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.system('sudo systemctl poweroff')
    return '', 200

@app.route('/temp_humidity', methods=['GET'])
def temp_humidity():
    if not 'temp_humidity' in app_config:
        return 'temp/humidity reader not configured', 404
    temp_humidity_values = __cache_temp_humidity().copy()
    temp_humidity_values['saving'] = temp_humidity_saver['saving']
    return jsonify(temp_humidity_values)

@app.route('/save_temp_humidity', methods=['PUT'])
def save_temp_humidity():
    if not 'temp_humidity' in app_config:
        return 'temp/humidity reader not configured', 404
    if temp_humidity_saver['saving']:
        return 'save_temp_humidity already active', 400
    temp_humidity_saver['saving'] = True
    temp_humidity_saver['thread'] = threading.Thread(target=__temp_humidity_saver_thread)
    temp_humidity_saver['thread'].start()
    return 'Thread created', 201

@app.route('/save_temp_humidity', methods=['DELETE'])
def stop_save_temp_humidity():
    if not 'temp_humidity' in app_config:
        return 'temp/humidity reader not configured', 404
    if not temp_humidity_saver['saving']:
        return 'save_temp_humidity already stopped', 400
    temp_humidity_saver['saving'] = False
    # temp_humidity_saver['thread'].join()
    return 'Thread removed', 200

@app.route('/led_brightness', methods=['PUT'])
def set_led_brightness():
    if not request.json:
        return 'Bad json request', 400
    if not 'led_display' in app_config:
        return 'led display not configured', 404

    if 'brightness' in request.json:
        app_config['led_display'].driver.set_brightness(int(request.json['brightness']))
    return 'Ok', 200

@app.route('/led/text/<key>', methods=['PUT'])
def add_led_text(key):
    if not request.json:
        return 'Bad json request', 400
    if not 'led_display' in app_config:
        return 'led display not configured', 404
    app_config['led_display'].add_message(key, request.json)
    return 'Message added', 200


@app.route('/led/text/<key>', methods=['DELETE'])
def remove_led_text(key):
    if not 'led_display' in app_config:
        return 'led display not configured', 404
    app_config['led_display'].remove_message(key)
    return 'Message removed', 200


@app.route('/events', methods=['GET'])
def get_events():
    start = int(request.args.get('start', 0))
    return jsonify([e for e in events if e['index'] >= start])

@app.route('/events', methods=['PUT'])
def add_event():
    if not request.json:
        return 'Bad json request', 400
    event = request.json
    event['index'] = len(events)
    event['time'] = time.time()
    events.append(event)
    return 'event added', 200

def update_datetime(timestamp):
    # very hacky workaround.. and need sudoer permissions
    date_cmd = 'sudo date -s "@{0}"'.format(timestamp)
    os.system(date_cmd)

def update_gps(coords):
    # TODO read file path from config?
    with open('/tmp/gps_coords.json', 'w') as outfile:
        json.dump(coords, outfile)


def __cache_temp_humidity():
    if 'temp_humidity' not in cached_objects or time.time() - cached_objects['temp_humidity']['time'] > 2:
        temp_humidity = app_config['temp_humidity'].read()
        temp_humidity['time'] = time.time()
        cached_objects['temp_humidity'] = temp_humidity
    return cached_objects['temp_humidity']


def __temp_humidity_saver_thread():
    outfile = app_config['temp_humidity_save_file']
    interval = app_config['temp_humidity_save_interval']
    if not os.path.isfile(outfile):
        with open(outfile, 'a') as f:
            f.write('time, temperature, humidity\n')
    while temp_humidity_saver['saving']:
        temp = __cache_temp_humidity()
        with open(outfile, 'a') as f:
            f.write('{}, {}, {}\n'.format(temp['time'], temp['temperature'], temp['humidity']))
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run server in debug mode (default: off)", action='store_true')
    parser.add_argument('--host', help="Hostname for server listening (default: 127.0.0.1)", default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Port for server listening (default: 5000)", default='5000')
    args = parser.parse_args()
    app.run(threaded=True, host=args.host, port=int(args.port), debug=args.debug)

  
