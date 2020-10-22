from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/setServoPosition', methods=['POST'])
def receiveServoPosition():
    data = request.get_json()
    print('data', data)
    print('data2', data['yo'])

    return ''