from flask import Flask, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import psutil
import sys

app = Flask(__name__)
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
    print(request)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=False)