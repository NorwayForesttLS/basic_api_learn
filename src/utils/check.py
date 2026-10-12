import json
import requests
import time
from datetime import datetime

url = "https://api.binance.com/api/v3/"

def check_server_time():
    response = requests.get(
        url + "time",
    )
    data = response.json()
    return json.dumps(data,indent=2)

def health_connectivity():
    response = requests.get(
        url + "ping",
    )
    data = response.json()
    if data == {}:
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S.%f")[:-3]
        return json.dumps(f'healthy {timestamp}'
                          ,indent=2)

