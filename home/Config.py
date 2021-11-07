
# Hub client settings
HubClientConfig = {
    "client_id": "HomeHub",
    "host": "localhost",
    "port": 1883,
    "initialTopics": [("devices/info/#", 0)]
}

# Cloud client settings
CloudClientConfig = {
    "client_id": "HubCloud",
    "host": "54.151.114.117", 
    "port": 1883,
    "initialTopics": [("server/control/#", 0)]
}
