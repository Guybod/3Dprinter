import time

import requests
def get_temperature():
    url = "http://192.168.1.103:7125/server/temperature_store?include_monitors=true"

    payload={}
    headers = {
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Accept': '*/*',
       'Host': '192.168.1.103:7125',
       'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    extruder_temperatures = data["result"]["extruder"]["temperatures"]

    print(extruder_temperatures[len(extruder_temperatures)-1])

if __name__ == '__main__':
    while True:
        get_temperature()
        time.sleep(0.5)
