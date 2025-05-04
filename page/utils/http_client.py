import json
import requests

class HttpClient:
    @staticmethod
    def extruder(url, script):
        payload = json.dumps({
            "script": script
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': '192.168.1.103:7125',
            'Connection': 'keep-alive'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text