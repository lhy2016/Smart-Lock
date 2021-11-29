from paho.mqtt.client import connack_string
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
from Hub import Hub
from Cloud import Cloud
import time
import sys
import threading

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print(client._client_id, " Connected to Home MQTT Broker")
        # client.subscribe("$SYS/#")
        client.subscribe(userdata["initialTopics"])
    else:
        print(f"Failed to connect, Error: {connack_string(rc)}\n")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(client._client_id, " disconnected from ", userdata["host"])

def on_publish(client, userdata, mid):
    print(client._client_id, " published a message(mid: ", mid ,")")

def hub_on_message(client, userdata, msg):
    print("Hub receive message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    
def cloud_on_message(client, userdata, msg):
    print("Hub Cloud receive message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic.startswith("server/control"):
        hub = Hub.instance()
        if msg.payload != None:
            payloadStr = msg.payload.decode('utf-8')
            temp = payloadStr.split("&")
            device = temp[0]
            action = temp[1]
            hub.publish("hub/control/lock/"+device, action.encode())

def connect_hub():
    try:
        hub = Hub.instance()
        hub.connect(hub._userdata["host"], hub._userdata["port"])
        hub.loop_forever()
    except Exception as e:
        print(e)
        sys.exit(-1)

def connect_cloud():
    cloud = Cloud.instance()
    # will try 100 times in total
    for i in range(100):
        try:
            if cloud.is_connected():
                break
            if i % 5 == 0 and i > 0:
                print(cloud._client_id, " still not connected, will keep trying after ",i*2,"s")
                time.sleep(i*2)
            print(cloud._client_id, " connecting to Server Broker: ", i, " times...")
            cloud.connect(cloud._userdata["host"], cloud._userdata["port"])
            cloud.loop()
        except Exception as e:
            print(e)
            continue

    if cloud.is_connected():
        print(cloud._client_id, " connected successfully!")
        cloud.loop_forever()
    

connect_hanlder = {
    Hub.instance()._client_id: connect_hub,
    Cloud.instance()._client_id: connect_cloud,
}


if __name__ == '__main__':
    hub = Hub.instance()
    cloud = Cloud.instance()
    hub.on_message = hub_on_message
    cloud.on_message = cloud_on_message

    for client in [cloud, hub]:
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish
        connector = connect_hanlder[client._client_id]
        client_thread = threading.Thread(target=connector, args=())
        client_thread.start()




