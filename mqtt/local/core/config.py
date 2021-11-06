import os

# MQTT URL
MQTT_URL = os.environ.get('MQTT_URL', '10.0.0.170:1883')

# MQTT broker configuration
MQTT_BROKER = os.environ.get("MQTT_BROKER","10.0.0.170")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT",1883))

# Topic configuration
MQTT_CAMERA_TOPIC = "esp32/camera"
MQTT_SERVO_TOPIC = "esp32/servo"
MQTT_HUB_CAMERA_TOPIC = "hub/camera"
MQTT_HUB_SERVO_TOPIC = "hub/servo"
