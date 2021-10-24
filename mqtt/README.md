Instructions:

`chmod +x installMQTTNano.sh`

`./installMQTTNano.sh`

run the mqtt broker (server)

`mosquitto`
or to run in the background

`mosquitto -d`

to run it at startup, run

`sudo /etc/init.d/mosquitto start`

Then run this to allow communications between PC hub and two ESP32s. It will also print the message received.

`python3 subscriber.py`

there are two topics now:
- esp32/camera
- esp32/servo

Change the following file for publish messages

subscriber.py

Configuration for topics and ip address etc.:

vim ./core/config.py
