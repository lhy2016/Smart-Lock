#! /usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import urllib.parse as urlparse
from core.config import MQTT_CAMERA_TOPIC, MQTT_SERVO_TOPIC, MQTT_BROKER, MQTT_BROKER_PORT, MQTT_URL
from typing import Callable

MQTT_CLIENT_TOPICS = [  # topic, QoS
    (MQTT_CAMERA_TOPIC, 0),
    (MQTT_SERVO_TOPIC, 0),
]

def connect_mqtt_broker(
    broker_ip=MQTT_BROKER, 
    broker_port=MQTT_BROKER_PORT, 
    mqtt_url: str = MQTT_URL, 
    client_id: str = "", 
    cb_connect: Callable = None, 
    ca_path: str = "", 
    cert_path: str = "", 
    key_path: str = ""
    ):
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
        print("on_message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        pass

    def on_publish(client, obj, mid):
        print("mid: " + str(mid))
        pass
    
    # def on_subscribe(client, obj, mid, granted_qos):
    #     print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(client, obj, level, string):
        print("Log: " + string)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
    
    # Configurate and Connect
    client = mqtt.Client(client_id)
    # For aws iot
    if ca_path and cert_path and key_path:
        import ssl
        client.tls_set(
            ca_path, 
            certfile=cert_path, 
            keyfile=key_path, 
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2, 
            ciphers=None
            )
    
    url_str = mqtt_url
    url = urlparse.urlparse(url_str)
    client.username_pw_set(url.username, url.password)
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_publish = on_publish
    # client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    # client.on_log = on_log
    broker_port=int(broker_port)
    client.connect(broker_ip, broker_port)
    return client
