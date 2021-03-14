from flask import Flask, jsonify

from ble import Nespresso
from config import MAC, AUTH_TOKEN

nespresso = Nespresso(MAC, AUTH_TOKEN)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({0: 'Alive'})

@app.route('/status', methods=['GET'])
def ping_coffee():
    resp = jsonify(nespresso.get_status())
    if resp:
        return resp, 200
    else:
        return resp, 500 

@app.route('/brew/<string:brew_type>', methods=['GET'])
def brew(brew_type):
    nespresso.query_brew(brew_type)
    resp = nespresso.status
    if resp[0] == 'Brewing':
        return jsonify(nespresso.status), 200
    else:
        return jsonify(resp[0]), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')