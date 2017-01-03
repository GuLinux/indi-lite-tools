#!/usr/bin/python3
from flask import Flask, render_template, g, request, session, Response
from flask.json import jsonify
from indicontroller import INDIController
from time import sleep
import sys
if sys.version_info[0] == 2:
    import Queue as queue
else:
    import queue
import logging
import pprint
import threading
import json
import argparse
import subprocess
import traceback

app = Flask(__name__)
app.config['bootstrap_version']='3.3.7'
app.config['jquery_version']='3.1.1'
app.config['histogram_bins'] = 256
app.config['histogram_logarithmic'] = True

subscriptions = []

def controller():
    # if 'controller' not in app.config:
    #     app.config['controller'] = INDIController()
    # return app.config['controller']
    return INDIController(app.static_folder + '/images', bins=app.config['histogram_bins'], log_y=app.config['histogram_logarithmic'])

def logger():
    logger = logging.getLogger('indi-preview')
    logger.setLevel(logging.DEBUG)
    return logger

def put_event(evt):
    for s in subscriptions:
        s.put(evt)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def devices():
    return jsonify(controller().devices())

@app.route('/device_names')
def device_names():
    return jsonify({'devices': controller().device_names()})

@app.route('/device/<devicename>/properties')
def properties(devicename):
    return jsonify({'device': devicename, 'properties': controller().properties(devicename)})

@app.route('/device/<devicename>/properties/<property>')
def property(devicename, property):
    return jsonify(controller().property(devicename, property))

@app.route('/device/<devicename>/properties/<property>', methods=['PUT'])
def set_property(devicename, property):
    return jsonify(controller().set_property(devicename, property, request.form['value']))

@app.route('/histogram', methods=['PUT'])
def histogram_settings():
    app.config['histogram_bins'] = int(request.form['bins'])
    app.config['histogram_logarithmic'] = request.form['logarithmic'] == 'true'
    return ('', 204)

def image_path(file):
    return '/'.join([app.static_url_path, 'images', file]) 

def image_event(image) :
    put_event({
        'type': 'image',
        'image_url': image_path( image.imagefile() ),
        'histogram-data': image.hist[0].tolist(),
        'histogram-bins': image.hist[1].tolist(),
        'image_id': image.id
    })

def notification(level, title, message):
    put_event({'type': 'notification', 'level': level, 'title': title, 'message': message})

@app.route('/device/<devicename>/preview/<exposure>')
def preview(devicename, exposure):
    def exp():
        try:
            image_event(controller().preview(devicename, float(exposure) ) )
        except Exception as e:
            traceback.print_exc()
            notification('warning', 'Error', e.args[0])

    t = threading.Thread(target = exp)
    t.start()
    return ('', 204)

@app.route('/device/<devicename>/framing/<exposure>')
def framing(devicename, exposure):
    def exp():
        try:
            while(app.config['framing']):
                image_event( controller().preview(devicename, float(exposure) ) )
        except Exception as e:
            traceback.print_exc()
            notification('warning', 'Error', e.args[0])

    app.config['framing'] = exposure != 'stop'
    if app.config['framing']:
        t = threading.Thread(target = exp)
        t.start()
    return('', 204)

@app.route('/events')
def events():
    def gen():
        q = queue.Queue()
        subscriptions.append(q)
        while(True):
            data = q.get()
            print("sending event...")
            yield("data: {0}\n\n".format(json.dumps(data)))
    return Response(gen(), mimetype="text/event-stream")

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        notification('warning', 'Error', 'unable to shutdown the server')
        return('', 500)
    func()
    return ('', 204)

@app.route('/run_command', methods=['POST'])
def run_command():
    try:
        command = request.form['command']
        result = subprocess.call(command)
        level = 'success' if result == 0 else 'warning'
        return notification(level, 'Run command', 'command "{0}" finished with exit code {1}'.format(command, result))
    except Exception as e:
        traceback.print_exc()
        notification('warning', 'Run command error', e.args[0])
    return ('', 204)



app.secret_key = b'\xcc\xfc\xbe6^\x9a\xbf>\xbc\xaa\x9e\xe8\xa6\n7'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run server in debug mode (default: off)", action='store_true')
    parser.add_argument('--host', help="Hostname for server listening (default: 127.0.0.1)", default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Port for server listening (default: 5000)", default='5000')
    args = parser.parse_args()
    app.run(threaded=True, host=args.host, port=int(args.port), debug=args.debug)


# vim: set tabstop=4 shiftwidth=4 expandtab
