#!/usr/bin/python3
from flask import Flask, render_template, g, request, session, Response
from flask.json import jsonify
from indicontroller import INDIController
from time import sleep
import queue
import logging
import pprint
import threading
import json

app = Flask(__name__)
app.config['bootstrap_version']='3.3.7'
app.config['jquery_version']='3.1.1'

subscriptions = []

def controller():
    if 'controller' not in app.config:
        app.config['controller'] = INDIController()
    return app.config['controller']

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
    return jsonify(INDIController().devices())

@app.route('/device/<devicename>/properties')
def properties(devicename):
    return jsonify(controller().properties(devicename))

@app.route('/device/<devicename>/properties/<property>')
def property(devicename, property):
    return jsonify(controller().property(devicename, property))

@app.route('/device/<devicename>/properties/<property>', methods=['PUT'])
def set_property(devicename, property):
    return jsonify(controller().set_property(devicename, property, request.form['value']))

@app.route('/device/<devicename>/preview/<exposure>')
def preview(devicename, exposure):
    def exp():
        impath = '/'.join([app.static_url_path, controller().preview(devicename, float(exposure), app.static_folder)])
        put_event({'type': 'image', 'url': impath})
    t = threading.Thread(target = exp)
    t.start()
    return ('', 204)

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



app.secret_key = b'\xcc\xfc\xbe6^\x9a\xbf>\xbc\xaa\x9e\xe8\xa6\n7'


if __name__ == '__main__':
    app.run(threaded=True)


# vim: set tabstop=4 shiftwidth=4 expandtab
