#! /usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import urllib.parse as urlparse
from core.config import MQTT_CAMERA_TOPIC, MQTT_SERVO_TOPIC, MQTT_BROKER, MQTT_BROKER_PORT
from typing import Callable

MQTT_BROKER, MQTT_BROKER_PORT = "localhost", 1883

MQTT_CLIENT_TOPICS = [  # topic, QoS
    (MQTT_CAMERA_TOPIC, 0),
    (MQTT_SERVO_TOPIC, 0),
]

def connect_mqtt_broker(client_id: str = "", cb_connect: Callable=None):
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
            if cb_connect is not None:
                cb_connect(client)
        else:
            print(f"Failed to connect, return code {rc}\n")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        # debug
        # print(client.__dict__, userdata)
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        pass

    def on_publish(client, obj, mid):
        print("mid: " + str(mid))
    
    # def on_subscribe(client, obj, mid, granted_qos):
    #     print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(client, obj, level, string):
        print("Log: " + string)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
    client = mqtt.Client(client_id)
    # Connect
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
    url = urlparse.urlparse(url_str)
    client.username_pw_set(url.username, url.password)
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_publish = on_publish
    # client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    # client.on_log = on_log
    client.connect(MQTT_BROKER, MQTT_BROKER_PORT)
    return client