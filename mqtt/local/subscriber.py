#! /usr/bin/env python3
import paho.mqtt.client as mqtt_client
import os
import urllib.parse as urlparse
from ../core.config import MQTT_CAMERA_TOPIC, MQTT_SERVO_TOPIC #, MQTT_BROKER, MQTT_BROKER_PORT
import json
from ../core.broker import connect_mqtt_broker

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

    #message = json.loads(msg.payload.decode())
    message = str(msg.payload)

    topic = msg.topic
    if topic == MQTT_CAMERA_TOPIC:
        img = message.get("photo",None)
        #msg_camera = message.get("message",'')

        trusted=False
        #TO DO 
        # what to do with image
        if img:
            trusted = True
            # trusted = False
            pass
            
        #TO DO
        #What to do after receiving message from camera esp32
        #if msg_camera:
        #    print(msg_camera)
        if trusted:
            client.publish(MQTT_SERVO_TOPIC, "Trusted person")
        else:
            client.publish(MQTT_SERVO_TOPIC, "Not a trusted person")
            
        print("message from esp32/camera: " + message)

    elif topic == MQTT_SERVO_TOPIC:
        msg_servo = message.get("servo_status",None)

        #TO DO 
        #What to do after receiving message from servo esp32
        if msg_servo:
            # client.publish(MQTT_CAMERA_TOPIC, msg_servo) #redirecting message from servo to camera
            print("servo_status: " + msg_servo)
        else:
            # client.publish(MQTT_CAMERA_TOPIC, "Empty message from ESP32 servo")
            print("message from servo: " + message)
        
def main():
    client = connect_mqtt_broker(cb_connect=subscribe)
    client.loop_forever()

if __name__ == "__main__":
    main()
