from flask import Flask, jsonify
from controller import Controller
app = Flask(__name__)

__static_controller_instance = []

def c():
    if len(__static_controller_instance) == 0:
        __static_controller_instance.append(Controller())
    return __static_controller_instance[0]

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/sessions')
def get_sessions():
    return jsonify({'sessions': c().sessions()})



@app.route('/sessions/<name>', methods=['POST'])
def create_session(name):
    code = 201 if c().new_session(name) else 409
    return ('', code)

@app.route('/sessions/<name>', methods=['DELETE'])
def delete_session(name):
    code = 200 if c().remove_session(name) else 404
    return ('', code)


@app.route('/sessions/<name>', methods=['GET'])
def get_session(name):
    session = c().get_session(name)
    if not session:
        return ('', 404)
    return jsonify(session.to_map())

if __name__ == "__main__":
    app.run()
