from flask import Flask, render_template, jsonify, request
import json
import os
import argparse
import time

app = Flask(__name__)
app_config = {}
events = []
cached_objects = {}

try:
    import config
    config.setup(app_config)
except:
    pass

@app.route("/")
def index():
    print(request)
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
    if 'temp_humidity' not in cached_objects or time.time() - cached_objects['temp_humidity']['time'] > 2:
        temp_humidity = app_config['temp_humidity'].read()
        temp_humidity['time'] = time.time()
        cached_objects['temp_humidity'] = temp_humidity
    return jsonify(cached_objects['temp_humidity'])

@app.route('/led_text', methods=['PUT'])
def set_led_text():
    if not request.json:
        return 'Bad json request', 400
    if not 'led_display' in app_config:
        return 'led display not configured', 404

    if 'brightness' in request.json:
        app_config['led_display'].set_brightness(int(request.json['brightness']))
    app_config['led_display'].set_text(str(request.json['text']))
    return 'Ok', 200

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
    events.append(event)
    return 'event added', 200

def update_datetime(timestamp):
    # very hacky workaround.. and need sudoer permissions
    date_cmd = 'sudo date -s "@{0}"'.format(timestamp)
    print(date_cmd)
    os.system(date_cmd)

def update_gps(coords):
    # TODO read file path from config?
    with open('/tmp/gps_coords.json', 'w') as outfile:
        json.dump(coords, outfile)
    print(coords)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run server in debug mode (default: off)", action='store_true')
    parser.add_argument('--host', help="Hostname for server listening (default: 127.0.0.1)", default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Port for server listening (default: 5000)", default='5000')
    args = parser.parse_args()
    app.run(threaded=True, host=args.host, port=int(args.port), debug=args.debug)

  
