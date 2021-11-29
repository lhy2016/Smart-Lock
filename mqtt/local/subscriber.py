#! /usr/bin/env python3
import paho.mqtt.client as mqtt_client
import os
import urllib.parse as urlparse
from core.config import MQTT_CAMERA_TOPIC, MQTT_SERVO_TOPIC,MQTT_HUB_CAMERA_TOPIC,MQTT_HUB_SERVO_TOPIC #, MQTT_BROKER, MQTT_BROKER_PORT
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
            # look through dictionary to find corresponding callback
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
    message_payload = json.loads(str(msg.payload.decode()))
    print("Type of payload to json: " , type(message_payload))
    print("actual payload: ",message_payload)
    message = str(msg.payload)

    topic = msg.topic
    if topic == MQTT_CAMERA_TOPIC:
        client.publish(MQTT_HUB_SERVO_TOPIC, "receive camera publish servo")
        
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
