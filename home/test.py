# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import time
import paho.mqtt.client as mqtt



def on_connect(client, userdata, flags, rc):
    print("connected, changing connected to True")
    
def on_disconnect(client, userdata, rc):
    print("disconnecting, changing connected to False")
    

if __name__ == "__main__":
    # creating thread
    cloud = mqtt.Client(client_id="testClient", clean_session=False)
    cloud.on_connect = on_connect
    cloud.on_disconnect = on_disconnect
    for i in range(100):
        try:
            print(i)
            if cloud.is_connected():
                break
            if i % 5 == 0 and i > 0:
                print(cloud._client_id, " still not connected, will keep trying after ",i*2,"s")
                time.sleep(i*2)
            print(cloud._client_id, " connecting to Server Broker: ", i, " times...")
            cloud.connect("54.151.114.117", 1883)
            cloud.loop()
            time.sleep(1)
        except Exception as e:
            print("lian bu shang: ", e)
            continue
    if cloud.is_connected():
        print(cloud._client_id, " connected successfully!")
        cloud.loop_forever()
    
