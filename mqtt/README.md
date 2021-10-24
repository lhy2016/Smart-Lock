Instructions:
chmod +x installMQTTNano.sh

./installMQTTNano.sh

run the mqtt broker (server)
mosquitto
or to run in the background
mosquitto -d 
to run it at startup, run
sudo /etc/init.d/mosquitto start

Change the following file for publish messages
subscriber.py

Configuration for topics and ip address etc.:
vim ./core/config.py