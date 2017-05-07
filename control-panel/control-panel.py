from flask import Flask, render_template, jsonify, request
import json
import os
app = Flask(__name__)

@app.route("/")
def index():
    print(request)
    return render_template('index.html')

@app.route("/set_coordinates", methods=["PUT"])
def set_coordinates():
    data = request.get_json()
    if not data:
        return '', 400
    if data['update_datetime']:
        update_datetime(data['timestamp'])
    update_gps(data['coords'])
    return '', 200


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

if __name__ == "__main__":
    app.run()
