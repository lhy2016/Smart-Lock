#! /usr/bin/env python3
import paho.mqtt.client as mqtt_client
import os
import urllib.parse as urlparse
from core.config import MQTT_CAMERA_TOPIC, MQTT_SERVO_TOPIC #, MQTT_BROKER, MQTT_BROKER_PORT
import json
from core.broker import connect_mqtt_broker

#MQTT_BROKER, MQTT_BROKER_PORT = "localhost", 1883

MQTT_CLIENT_TOPICS = [  # topic, QoS
    (MQTT_CAMERA_TOPIC, 0),
    (MQTT_SERVO_TOPIC, 0),
]

def subscribe(client: mqtt_client):
    """
    Subscribe client to topic.
    Arguments:
        client {mqtt_client} -- Client process id.
    """

    def on_message(client, userdata, msg):
        try:
            process_message(client,msg)
        except:
            pass

    client.subscribe(MQTT_CLIENT_TOPICS)
    client.on_message = on_message

def process_message(client,msg):
    """
    Process message sent to topic.
    Arguments:
        msg {str} -- Received message.
    """
    # log for debugging
    print(msg.topic + " " + str(msg.payload))
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    message = json.loads(msg.payload.decode())

    topic = msg.topic
    if topic == MQTT_CAMERA_TOPIC:
        img = message.get("photo",None)
        msg = message.get("message",None)
        trusted=False
        #TO DO 
        # what to do with image
        if img:
            print("image: " + img)
            trusted=True

        #TO DO
        #What to do after receiving message from camera esp32
        if msg:
            client.publish(MQTT_SERVO_TOPIC, msg) #redirecting message from camera to servo
        else:
            msg = ''
            if trusted:
                msg = "Trusted person"
            else:
                msg = "Not a trusted person"
            
            client.publish(MQTT_SERVO_TOPIC, "Empty message from ESP32 camera" + ' ' + str(msg))

    elif topic == MQTT_SERVO_TOPIC:
        msg = message.get("servo_status",None)

        #TO DO 
        #What to do after receiving message from servo esp32
        if msg:
            client.publish(MQTT_CAMERA_TOPIC, msg) #redirecting message from servo to camera
        else:
            client.publish(MQTT_CAMERA_TOPIC, "Empty message from ESP32 servo")
        
        
def main():
    client = connect_mqtt_broker(cb_connect=subscribe)
    client.loop_forever()

if __name__ == "__main__":
    main()