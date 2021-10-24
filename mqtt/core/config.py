import os

MQTT_URL = os.environ.get('MQTT_URL', 'mqtt://localhost:1883')

# MQTT broker configuration
MQTT_BROKER = os.environ.get("MQTT_BROKER","localhost")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT",1883))

# Topic configuration
MQTT_CAMERA_TOPIC = "esp32/camera"
MQTT_SERVO_TOPIC = "esp32/servo"
