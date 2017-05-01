from flask import Flask, jsonify, render_template
from controller import Controller
from sequence_group import SequenceGroup

app = Flask(__name__)

__static_controller_instance = []

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def c():
    if len(__static_controller_instance) == 0:
        __static_controller_instance.append(Controller())
    return __static_controller_instance[0]

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/api/sessions')
def get_sessions():
    return jsonify({'sessions': c().sessions()})



@app.route('/api/sessions/<name>', methods=['POST'])
def create_session(name):
    code = 201 if c().new_session(name) else 409
    return ('', code)

@app.route('/api/sessions/<name>', methods=['DELETE'])
def delete_session(name):
    code = 200 if c().remove_session(name) else 404
    return ('', code)


@app.route('/api/sessions/<name>', methods=['GET'])
def get_session(name):
    session = c().get_session(name)
    if not session:
        return ('', 404)
    return jsonify(session.to_map())

@app.route('/api/sessions/<session>/<sequence_group>', methods=['POST'])
def create_sequence_group(session, sequence_group):
    session = c().get_session(session)
    if not session:
        return ('', 404)
    if sequence_group in [s.name for s in session.sequence_groups]:
        return ('', 409)
    session.sequence_groups.append(SequenceGroup(sequence_group))
    return ('', 201)

if __name__ == "__main__":
    app.run()
