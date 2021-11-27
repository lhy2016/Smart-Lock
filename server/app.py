from flask import Flask, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import psutil
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lhy_2016@localhost:5432/smartlock'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
# app.config['MQTT_USERNAME'] = 'xxx'
# app.config['MQTT_PASSWORD'] = 'xxx'
CORS(app)


mosquitto_services = [p.name() for p in psutil.process_iter() if p.name().startswith("mosquitto")]
if len(mosquitto_services) == 0:
    print("Please start mosquitto first!")
    sys.exit(-1)

mqtt = Mqtt(app)
socketio = SocketIO(app)

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('server: connnected to mosquitto mqtt!')
    mqtt.subscribe('/hub/0001')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.payload)

@app.route("/unlock")
def unlock():
    mqtt.publish("server/control/lock", "u")
    return "<h1>Requesting unlock to hub</h1>"

@app.route("/lock")
def lock():
    mqtt.publish("server/control/lock", "l")
    return "<h1>Requesting lock to hub</h1>"

@app.route("/signup", methods=['POST'])
def signup():
    dataObj = json.loads(request.data)
    hashed = bcrypt.generate_password_hash(dataObj['password']).decode('utf-8')

    existing = User.query.filter_by(email=dataObj['email']).first()
    print("EXISTING")
    print(existing)

    newUser = User(first_name=dataObj['firstName'],last_name=dataObj['lastName'],
                    email=dataObj['email'], password=hashed)
    print(dataObj)
    return json.dumps({"hello":"world"})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, default='')
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    devices = db.Column(db.PickleType, default=None)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=False)