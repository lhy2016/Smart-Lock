import paho.mqtt.client as mqtt
from Config import HubClientConfig

class Hub:
    _instance = None

    def __init__(self):
        return

    @staticmethod
    def instance():
        if Hub._instance == None:
            userData = HubClientConfig
            Hub._instance = mqtt.Client(client_id=HubClientConfig["client_id"], clean_session=False, userdata=userData)
        return Hub._instance