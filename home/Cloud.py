import paho.mqtt.client as mqtt
from Config import CloudClientConfig

class Cloud:
    _instance = None

    def __init__(self):
        return

    @staticmethod
    def instance():
        if Cloud._instance == None:
            userData = CloudClientConfig
            Cloud._instance = mqtt.Client(client_id=CloudClientConfig["client_id"], clean_session=False, userdata=userData)
        return Cloud._instance