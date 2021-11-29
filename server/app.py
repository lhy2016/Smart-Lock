from flask import Flask, request
from flask.globals import session
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import psutil
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from utilities import row2dict

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

@app.route("/unlock", methods=['POST'])
def unlock():
    mqtt.publish("server/control/lock", "u")
    dataObj = json.loads(request.data)
    user = User.query.filter_by(id=dataObj["user_id"]).all()[0]
    devices = json.loads(user.devices)
    
    hub_name = dataObj["hub_name"]
    device_name = dataObj["device_name"]
    
    deviceStatus = devices[hub_name][device_name]
    deviceStatus["status"] = "off"
    devices[hub_name][device_name] = deviceStatus

    user.devices = json.dumps(devices)
    db.session.commit()

    return json.dumps({"success": True}), 200

@app.route("/lock", methods=['POST'])
def lock():
    mqtt.publish("server/control/lock", "l")
    dataObj = json.loads(request.data)
    user = User.query.filter_by(id=dataObj["user_id"]).all()[0]
    devices = json.loads(user.devices)

    hub_name = dataObj["hub_name"]
    device_name = dataObj["device_name"]
    
    deviceStatus = devices[hub_name][device_name]
    deviceStatus["status"] = "off"
    devices[hub_name][device_name] = deviceStatus

    user.devices = json.dumps(devices)
    db.session.commit()

    return json.dumps({"success": True}), 200


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False, default='')
    last_name = db.Column(db.String(100), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    devices = db.Column(db.PickleType, default=None)

db.create_all()
db.session.commit()

@app.route("/signup", methods=['POST'])
def signup():
    dataObj = json.loads(request.data)
    existing = User.query.filter_by(email=dataObj['email']).all()
    if len(existing) != 0:
        return json.dumps({"error":"Email is already registered"}), 400

    hashed = bcrypt.generate_password_hash(dataObj['password']).decode('utf-8')
    newUser = User(first_name=dataObj['firstName'],last_name=dataObj['lastName'],
                    email=dataObj['email'], password=hashed)
    db.session.add(newUser)
    db.session.commit()
    return json.dumps(row2dict(newUser)), 201

@app.route("/login", methods=['POST'])
def login():
    dataObj = json.loads(request.data)
    user = User.query.filter_by(email=dataObj['email']).all()
    if len(user) != 1:
        return json.dumps({"error": "Can't find user matched with this email"}), 401
    userObj = user[0]
    actual = userObj.password
    print("actual: " + actual)
    hashed = bcrypt.generate_password_hash(dataObj['password']).decode('utf-8')
    print("user hashed: " + hashed)
    if not bcrypt.check_password_hash(actual, dataObj['password']):
        return json.dumps({"error": "Incorrect password"}), 403
    ret = {}
    ret["user_id"] = userObj.id
    ret["first_name"] = userObj.first_name
    ret["email"] = userObj.email
    return json.dumps(ret), 200

@app.route("/device", methods=['POST'])
def add_device():
    dataObj = json.loads(request.data)
    user_id = dataObj["user_id"]
    hub_name = dataObj["hub_name"]
    device_name = dataObj["device_name"]

    user = User.query.filter_by(id=user_id).all()[0]
    print("****************USER.DEVICES")
    devices = {} if user.devices == None else json.loads(user.devices)
    
    devices_under_hub = devices[hub_name] if hub_name in devices else {}
    devices_under_hub[device_name] = {
        "status" : "on"
    }
    devices[hub_name] = devices_under_hub
    print(devices)
    print("****************USER.DEVICES")
    user.devices = json.dumps(devices)
    db.session.commit()
    ret = {"success": True}
    return json.dumps(ret), 201

@app.route("/devices", methods=['GET'])
def get_device():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).all()[0]
    devices = json.dumps({}) if user.devices == None else user.devices
    return devices, 200
    


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=False)
    